import datetime
import logging

from fastapi import exceptions as fastapi_exceptions
from fastapi import security, status
from fastapi.openapi import models
from fastapi.security import utils
import fastapi_jwt_auth as jwt_auth
from passlib import context
from sqlalchemy import exc as sqlalchemy_exceptions
from starlette import requests as starlette_requests

from app.config import general
from app.models import auth as auth_model
from app.services import base
from app.services import exceptions as resource_exceptions
from app.services import user as user_service

log = logging.getLogger(__name__)

settings = general.get_settings()


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


pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class TokenService(base.AppService):
    async def create_tokens(
        self, email: str, password: str, Authorize: jwt_auth.AuthJWT
    ) -> auth_model.Tokens:
        user_crud_service = user_service.UserCRUD(self.session)
        unauthorized_exception = resource_exceptions.UnauthorizedError({"email": email})
        try:
            user_db = await user_crud_service.read(email=email)
        except sqlalchemy_exceptions.NoResultFound as e:
            log.info("User with the email %r not found", email)
            raise unauthorized_exception from e
        if not verify_password(password, user_db.password):
            log.info("Invalid password for user with the email %r", email)
            raise unauthorized_exception
        if not user_db.is_active:
            log.info("User with the email %r is inactive", email)
            raise unauthorized_exception
        updated_user = await user_crud_service.update(
            user_db, last_login=datetime.datetime.utcnow()
        )
        user_id = str(updated_user.id)
        return auth_model.Tokens(  # nosec
            access_token=Authorize.create_access_token(subject=user_id, fresh=True),
            refresh_token=Authorize.create_refresh_token(subject=user_id),
            token_type="bearer",
        )
