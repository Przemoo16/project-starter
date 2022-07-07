from app.config import general
from app.models import config, user
from app.services import base

settings = general.get_settings()


class ConfigService(base.AppService):
    @staticmethod
    def get_config() -> config.Config:
        return config.Config(
            user_name_min_length=user.USER_NAME_MIN_LENGTH,
            user_name_max_length=user.USER_NAME_MAX_LENGTH,
            user_password_min_length=settings.USER_PASSWORD_MIN_LENGTH,
            user_password_max_length=settings.USER_PASSWORD_MAX_LENGTH,
        )
