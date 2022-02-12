from app.models import base


class Message(base.BaseModel):
    message: str
