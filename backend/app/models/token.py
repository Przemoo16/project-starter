import typing

from app.models import base

Token: typing.TypeAlias = str


class AccessToken(base.BaseModel):
    access_token: Token
    token_type: str


class Tokens(AccessToken):
    refresh_token: Token
