import enum
import json
import typing

from fastapi import exceptions, security, status
from fastapi.openapi import models
from fastapi.security import utils
from passlib import context
import pyseto
from starlette import requests as starlette_requests

from app.config import general
from app.exceptions.app import auth as auth_exceptions

settings = general.get_settings()


class OAuth2PasswordBearer(security.OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        refreshUrl: str,
        scheme_name: str | None = None,
        scopes: dict[str, str] | None = None,
        auto_error: bool = True,
    ):
        flows = models.OAuthFlows(
            password=models.OAuthFlowPassword(
                tokenUrl=tokenUrl, refreshUrl=refreshUrl, scopes=scopes or {}
            )
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
                raise exceptions.HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return None
        return param


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_URL}/{settings.TOKEN_URL}",
    refreshUrl=f"{settings.API_URL}/{settings.REFRESH_TOKEN_URL}",
)

pwd_context = context.CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class TokenPurpose(enum.Enum):
    LOCAL = "local"
    PUBLIC = "public"


def decode_token(
    token: str, version: int = 4, purpose: TokenPurpose = TokenPurpose.LOCAL
) -> pyseto.Token:
    decoding_key = pyseto.Key.new(
        version=version, purpose=purpose.value, key=settings.AUTHPASETO_SECRET_KEY
    )
    try:
        return pyseto.decode(keys=decoding_key, token=token, deserializer=json)
    except (pyseto.VerifyError, pyseto.DecryptError, pyseto.SignError, ValueError) as e:
        raise auth_exceptions.TokenDecodingError from e


def decode_token_payload(
    token: str, version: int = 4, purpose: TokenPurpose = TokenPurpose.LOCAL
) -> dict[str, typing.Any]:
    payload = decode_token(token, version, purpose).payload
    # Improve typing by ensuring that payload is always a dictionary
    assert isinstance(payload, dict)  # nosec
    return payload


def is_token_fresh(
    token: str, version: int = 4, purpose: TokenPurpose = TokenPurpose.LOCAL
) -> bool:
    payload = decode_token_payload(token, version, purpose)
    return payload["fresh"]
