import datetime
import logging
import typing

import fastapi_jwt_auth as jwt_auth
from jose import jwt

from app.config import db, general
from app.exceptions.http import token as token_exceptions
from app.exceptions.http import user as user_exceptions
from app.models import token as token_models
from app.models import user as user_models
from app.services import auth, base
from app.services import user as user_services

log = logging.getLogger(__name__)

settings = general.get_settings()
jwt_db = db.get_jwt_db()


class TokenService(base.AppService):
    async def obtain_tokens(self, email: str, password: str) -> token_models.Tokens:
        user_service = user_services.UserService(self.session)
        unauthorized_exception = user_exceptions.UnauthorizedUserError()
        user_read = user_models.UserRead(email=email)
        try:
            user_db = await user_service.get_user(user_read)
        except user_exceptions.UserNotFoundError as e:
            log.info("User with the email %r not found", email)
            raise unauthorized_exception from e
        if not auth.verify_password(password, user_db.password):
            log.info("Invalid password for user with the email %r", email)
            raise unauthorized_exception
        user_update = user_models.UserUpdate(last_login=datetime.datetime.utcnow())
        updated_user = await user_service.update_user(user_db.id, user_update)
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
        if check_if_token_in_denylist(decoded_token):
            raise token_exceptions.RevokedTokenError(context=token_context)
        user_id = decoded_token["sub"]
        user_read = user_models.UserRead(id=user_id)
        user = await user_services.UserService(self.session).get_user(user_read)
        return token_models.AccessToken(  # nosec
            access_token=jwt_auth.AuthJWT().create_access_token(
                str(user.id), fresh=False
            ),
            token_type="bearer",
        )

    @staticmethod
    def revoke_token(token: token_models.Token) -> None:
        try:
            decoded_token = decode_token(token)
        except jwt.JWTError as e:
            raise token_exceptions.InvalidTokenError(context={"token": token}) from e
        jti = decoded_token["jti"]
        if not (expiration := decoded_token.get("exp")):
            jwt_db.set(jti, "true")
            log.info("Token without expiration has been revoked")
            return
        remaining_expiration = _get_remaining_expiration(expiration)
        # Redis can only accept expiration values greater than 0
        jwt_db.setex(jti, remaining_expiration or 1, "true")
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


def check_if_token_in_denylist(decrypted_token: dict[str, typing.Any]) -> bool:
    """
    Check if the token has been revoked.

    The method is also used internally by the fastapi_jwt_auth library and registered
    as a callback using the AuthJWT.token_in_denylist_loader method.
    """
    jti = decrypted_token["jti"]
    is_revoked = db.get_jwt_db().get(jti)
    return is_revoked == "true"


def _get_remaining_expiration(exp: int) -> int:
    delta = int(exp - datetime.datetime.utcnow().timestamp())
    return max(0, delta)
