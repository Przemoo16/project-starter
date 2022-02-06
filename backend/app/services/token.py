import datetime
import logging

import fastapi_jwt_auth as jwt_auth
from jose import jwt
from sqlalchemy import exc as sqlalchemy_exceptions

from app.config import general
from app.config import jwt as jwt_config
from app.models import token as token_models
from app.models import user as user_models
from app.services import auth as auth_services
from app.services import base
from app.services import exceptions as resource_exceptions
from app.services import user as user_services

log = logging.getLogger(__name__)

settings = general.get_settings()
jwt_db = jwt_config.get_jwt_db()


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
        if not auth_services.verify_password(password, user_db.password):
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
        remaining_expiration = get_remaining_expiration(decoded_token["exp"])
        # Redis can only accept expiration values greater than 0
        jwt_db.setex(decoded_token["jti"], remaining_expiration or 1, "true")
        log.info("Token has been revoked")


def get_remaining_expiration(exp: int) -> int:
    delta = int(exp - datetime.datetime.utcnow().timestamp())
    return max(0, delta)
