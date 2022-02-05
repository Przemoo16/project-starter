from app.models import base


class Tokens(base.BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
