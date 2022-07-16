import datetime
import logging
import typing

import fastapi_jwt_auth as jwt_auth
from jose import jwt

from app.config import db, general
from app.config import jwt as jwt_config
from app.exceptions.http import token as token_exceptions
from app.exceptions.http import user as user_exceptions
from app.models import token as token_models
from app.models import user as user_models
from app.services import base
from app.services import user as user_services
from app.utils import auth, converters

log = logging.getLogger(__name__)

settings = general.get_settings()
jwt_db = db.get_jwt_db()


class TokenService(base.AppService):
    def __init__(self, session: db.AsyncSession):
        super().__init__(session)
        self.user_service = user_services.UserService(self.session)

    async def obtain_tokens(
        self, email: user_models.UserEmail, password: user_models.UserPassword
    ) -> token_models.Tokens:
        invalid_credentials_exception = token_exceptions.InvalidCredentials()
        user_filters = user_models.UserFilters(email=email)
        try:
            user = await self.user_service.get_user(user_filters)
        except user_exceptions.UserNotFoundError as e:
            log.info("User with the email %r not found", email)
            raise invalid_credentials_exception from e
        if not auth.verify_password(password, user.password):
            log.info("Invalid password for user with the email %r", email)
            raise invalid_credentials_exception
        if not self.user_service.is_active(user):
            raise token_exceptions.InactiveUserError(context={"id": user.id})
        user_update = user_models.UserUpdate(last_login=datetime.datetime.utcnow())
        updated_user = await self.user_service.update_user(user, user_update)
        user_id = str(updated_user.id)
        auth_handler = jwt_auth.AuthJWT()
        return token_models.Tokens(  # nosec
            access_token=auth_handler.create_access_token(subject=user_id, fresh=True),
            refresh_token=auth_handler.create_refresh_token(subject=user_id),
            token_type="bearer",
        )

    async def refresh_token(
        self, token: token_models.Token
    ) -> token_models.AccessToken:
        token_context = {"token": token}
        try:
            decoded_token = decode_token(token)
        except jwt.JWTError as e:
            raise token_exceptions.InvalidTokenError(context=token_context) from e
        if decoded_token["type"] != "refresh":
            raise token_exceptions.RefreshTokenRequiredError(context=token_context)
        if jwt_config.check_if_token_in_denylist(decoded_token):
            raise token_exceptions.RevokedTokenError(context=token_context)
        user_filters = user_models.UserFilters(id=decoded_token["sub"])
        user = await self.user_service.get_user(user_filters)
        if not self.user_service.is_active(user):
            raise token_exceptions.InactiveUserError(context={"id": user.id})
        return token_models.AccessToken(  # nosec
            access_token=jwt_auth.AuthJWT().create_access_token(
                str(user.id), fresh=False
            ),
            token_type="bearer",
        )

    async def revoke_token(self, token: token_models.Token) -> None:
        token_context = {"token": token}
        try:
            decoded_token = decode_token(token)
        except jwt.JWTError as e:
            raise token_exceptions.InvalidTokenError(context=token_context) from e
        if jwt_config.check_if_token_in_denylist(decoded_token):
            raise token_exceptions.RevokedTokenError(context=token_context)
        user_filters = user_models.UserFilters(id=decoded_token["sub"])
        await self.user_service.get_user(user_filters)
        jti = decoded_token["jti"]
        if not (expiration := decoded_token.get("exp")):
            jwt_db.set(jti, "true")
            log.warning("Revoked token without expiration")
            return
        remaining_expiration = _get_remaining_expiration(expiration)
        jwt_db.setex(jti, remaining_expiration, "true")
        log.info("Token has been revoked")


def decode_token(
    token: token_models.Token, options: dict[str, typing.Any] | None = None
) -> dict[str, typing.Any]:
    return dict(
        jwt.decode(
            token,
            settings.AUTHJWT_SECRET_KEY,
            settings.AUTHJWT_DECODE_ALGORITHMS,
            options=options,
        )
    )


def _get_remaining_expiration(exp: int) -> int:
    delta = int(exp - converters.to_utc_timestamp(datetime.datetime.utcnow()))
    # Redis can only accept expiration values greater than 0
    return max(1, delta)
