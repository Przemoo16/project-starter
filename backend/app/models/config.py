from app.models import base


class Config(base.BaseModel):
    user_name_max_length: int
    user_password_min_length: int
    user_password_max_length: int
