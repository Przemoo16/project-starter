import fastapi_jwt_auth as jwt_auth

from app.config import general
from app.services import token  # TODO: Find better way than importing it from services

settings = general.get_settings()


@jwt_auth.AuthJWT.load_config
def get_jwt_settings() -> general.Settings:
    return general.get_settings()


jwt_auth.AuthJWT.token_in_denylist_loader(callback=token.check_if_token_in_denylist)
