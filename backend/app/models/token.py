from app.models import base


class Token(base.BaseModel):
    token: str


class AccessToken(base.BaseModel):
    access_token: str
    token_type: str


class Tokens(AccessToken):
    refresh_token: str
