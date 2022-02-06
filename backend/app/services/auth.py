import datetime
import logging

from fastapi import exceptions as fastapi_exceptions
from fastapi import security, status
from fastapi.openapi import models
from fastapi.security import utils
import fastapi_jwt_auth as jwt_auth
from jose import jwt
from sqlalchemy import exc as sqlalchemy_exceptions
from starlette import requests as starlette_requests

from app.config import general
from app.config import jwt as jwt_config
from app.models import token as token_models
from app.models import user as user_models
from app.services import base
from app.services import exceptions as resource_exceptions
from app.services import user as user_services
from app.utils import security as security_utils

log = logging.getLogger(__name__)

settings = general.get_settings()

jwt_db = jwt_config.get_jwt_db()


class OAuth2PasswordBearer(security.OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        refreshUrl: str | None = None,
        scheme_name: str | None = None,
        scopes: dict[str, str] | None = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = models.OAuthFlows(
            password={"tokenUrl": tokenUrl, "refreshUrl": refreshUrl, "scopes": scopes}
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            auto_error=auto_error,
        )

    async def __call__(
        self, request: starlette_requests.Request
    ) -> str | None:  # pragma: no cover
        authorization: str = request.headers.get("Authorization")
        scheme, param = utils.get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise fastapi_exceptions.HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return None
        return param


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_VERSION}/token",
    refreshUrl=f"{settings.API_VERSION}/token/refresh",
)


class TokenService(base.AppService):
    async def create_tokens(
        self, email: str, password: str, Authorize: jwt_auth.AuthJWT
    ) -> token_models.Tokens:
        user_crud_service = user_services.UserCRUD(self.session)
        unauthorized_exception = resource_exceptions.UnauthorizedError({"email": email})
        try:
            user_db = await user_crud_service.read(email=email)
        except sqlalchemy_exceptions.NoResultFound as e:
            log.info("User with the email %r not found", email)
            raise unauthorized_exception from e
        if not security_utils.verify_password(password, user_db.password):
            log.info("Invalid password for user with the email %r", email)
            raise unauthorized_exception
        if not user_db.is_active:
            log.info("User with the email %r is inactive", email)
            raise unauthorized_exception
        updated_user = await user_crud_service.update(
            user_db, last_login=datetime.datetime.utcnow()
        )
        user_id = str(updated_user.id)
        return token_models.Tokens(  # nosec
            access_token=Authorize.create_access_token(subject=user_id, fresh=True),
            refresh_token=Authorize.create_refresh_token(subject=user_id),
            token_type="bearer",
        )

    @staticmethod
    def refresh_token(
        user: user_models.User, Authorize: jwt_auth.AuthJWT
    ) -> token_models.AccessToken:
        return token_models.AccessToken(  # nosec
            access_token=Authorize.create_access_token(str(user.id), fresh=False),
            token_type="bearer",
        )

    @staticmethod
    def revoke_token(token: str) -> None:
        try:
            decoded_token = jwt.decode(
                token,
                settings.AUTHJWT_SECRET_KEY,
                settings.AUTHJWT_DECODE_ALGORITHMS,
                options={"verify_exp": False},
            )
        except jwt.JWTError as e:
            log.info("Invalid token")
            raise resource_exceptions.BadRequestError({"token": token}) from e
        remaining_expiration = security_utils.get_remaining_expiration(
            decoded_token["exp"]
        )
        # Redis can only accept expiration values greater than 0
        jwt_db.setex(decoded_token["jti"], remaining_expiration or 1, "true")
        log.info("Token has been revoked")
