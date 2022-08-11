import datetime
import logging

from dateutil import parser
import fastapi_paseto_auth as paseto_auth

from app.config import auth as auth_config
from app.config import db, general
from app.exceptions.app import auth as auth_app_aceptions
from app.exceptions.http import auth as auth_http_exceptions
from app.exceptions.http import user as user_exceptions
from app.models import auth as auth_models
from app.models import user as user_models
from app.services import user as user_services
from app.utils import auth as auth_utils
from app.utils import converters

log = logging.getLogger(__name__)

settings = general.get_settings()
paseto_token_db = db.get_paseto_token_db()


class AuthService:
    def __init__(self, session: db.AsyncSession):
        self.user_service = user_services.UserService(session)

    async def obtain_tokens(
        self, email: user_models.UserEmail, password: user_models.UserPassword
    ) -> auth_models.AuthTokens:
        invalid_credentials_exception = auth_http_exceptions.InvalidCredentialsError()
        user_filters = user_models.UserFilters(email=email)
        try:
            user = await self.user_service.get_active_user(user_filters)
        except user_exceptions.UserNotFoundError as e:
            log.info("User with the email %r not found", email)
            raise invalid_credentials_exception from e
        if not auth_utils.verify_password(password, user.password):
            log.info("Invalid password for user with the email %r", email)
            raise invalid_credentials_exception
        user_update = user_models.UserUpdate(last_login=datetime.datetime.utcnow())
        updated_user = await self.user_service.update_user(user, user_update)
        user_id = str(updated_user.id)
        auth_handler = paseto_auth.AuthPASETO()
        return auth_models.AuthTokens(  # nosec
            access_token=auth_handler.create_access_token(subject=user_id, fresh=True),
            refresh_token=auth_handler.create_refresh_token(subject=user_id),
            token_type="bearer",
        )

    async def refresh_token(
        self, token: auth_models.AuthToken
    ) -> auth_models.AccessToken:
        token_context = {"token": token}
        try:
            payload = auth_utils.decode_token_payload(token)
        except auth_app_aceptions.TokenDecodingError as e:
            raise auth_http_exceptions.InvalidTokenError(context=token_context) from e
        if payload["type"] != "refresh":
            raise auth_http_exceptions.RefreshTokenRequiredError(context=token_context)
        if auth_config.check_if_token_in_denylist(payload):
            raise auth_http_exceptions.RevokedTokenError(context=token_context)
        user_filters = user_models.UserFilters(id=payload["sub"])
        user = await self.user_service.get_active_user(user_filters)
        return auth_models.AccessToken(  # nosec
            access_token=paseto_auth.AuthPASETO().create_access_token(
                str(user.id), fresh=False
            ),
            token_type="bearer",
        )

    async def revoke_token(self, token: auth_models.AuthToken) -> None:
        token_context = {"token": token}
        try:
            payload = auth_utils.decode_token_payload(token)
        except auth_app_aceptions.TokenDecodingError as e:
            raise auth_http_exceptions.InvalidTokenError(context=token_context) from e
        if auth_config.check_if_token_in_denylist(payload):
            raise auth_http_exceptions.RevokedTokenError(context=token_context)
        user_filters = user_models.UserFilters(id=payload["sub"])
        await self.user_service.get_user(user_filters)
        jti = payload["jti"]
        if not (expiration := payload.get("exp")):
            paseto_token_db.set(jti, "true")
            log.warning("Revoked token without expiration")
            return
        remaining_expiration = _get_remaining_expiration(expiration)
        paseto_token_db.setex(jti, remaining_expiration, "true")
        log.info("Token has been revoked")


def _get_remaining_expiration(exp: str) -> int:
    delta = converters.to_utc_timestamp(
        parser.parse(exp, ignoretz=True)
    ) - converters.to_utc_timestamp(datetime.datetime.utcnow())
    # Redis can only accept expiration values greater than 0
    return max(1, int(delta))
