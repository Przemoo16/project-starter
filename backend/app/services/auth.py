from fastapi import exceptions, security, status
from fastapi.openapi import models
from fastapi.security import utils
from passlib import context
from starlette import requests as starlette_requests

from app.config import general

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
                raise exceptions.HTTPException(
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
