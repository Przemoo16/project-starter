import typing

from app.models import base

AuthToken: typing.TypeAlias = str


class AccessToken(base.BaseModel):
    access_token: AuthToken
    token_type: str


class AuthTokens(AccessToken):
    refresh_token: AuthToken
