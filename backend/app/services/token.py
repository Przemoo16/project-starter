import datetime
import logging
import typing

import fastapi_jwt_auth as jwt_auth
from jose import jwt
from sqlalchemy import exc

from app.config import db, general
from app.exceptions import resource
from app.models import token as token_models
from app.services import auth, base
from app.services import user as user_services

log = logging.getLogger(__name__)

settings = general.get_settings()
jwt_db = db.get_jwt_db()


class TokenService(base.AppService):
    async def create_tokens(self, email: str, password: str) -> token_models.Tokens:
        user_crud_service = user_services.UserCRUD(self.session)
        unauthorized_exception = resource.UnauthorizedError({"email": email})
        try:
            user_db = await user_crud_service.read(email=email)
        except exc.NoResultFound as e:
            log.info("User with the email %r not found", email)
            raise unauthorized_exception from e
        if not auth.verify_password(password, user_db.password):
            log.info("Invalid password for user with the email %r", email)
            raise unauthorized_exception
        updated_user = await user_crud_service.update(
            user_db, last_login=datetime.datetime.utcnow()
        )
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
        try:
            decoded_token = decode_token(token)
        except jwt.JWTError as e:
            log.info("Invalid token: %r", token)
            raise resource.UnprocessableEntityError({"token": token}) from e
        if decoded_token["type"] != "refresh":
            log.info("Token %r is not a refresh token", token)
            raise resource.UnprocessableEntityError({"token": token})
        if check_if_token_in_denylist(decoded_token):
            log.info("Token %r is revoked", token)
            raise resource.UnprocessableEntityError({"token": token})
        user_id = decoded_token["sub"]
        try:
            user = await user_services.UserCRUD(self.session).read(id=user_id)
        except exc.NoResultFound as e:
            log.info("User with the ID %r not found", user_id)
            raise resource.NotFoundError({"token": token}) from e
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
            log.info("Invalid token: %r", token)
            raise resource.UnprocessableEntityError({"token": token}) from e
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
