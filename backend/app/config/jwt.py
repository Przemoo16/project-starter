import typing

import fastapi_jwt_auth as jwt_auth

from app.config import db, general

settings = general.get_settings()

jwt_db = db.get_jwt_db()


@jwt_auth.AuthJWT.load_config
def get_jwt_settings() -> general.Settings:
    return general.get_settings()


def check_if_token_in_denylist(decrypted_token: dict[str, typing.Any]) -> bool:
    jti = decrypted_token["jti"]
    is_revoked = db.get_jwt_db().get(jti)
    return is_revoked == "true"


jwt_auth.AuthJWT.token_in_denylist_loader(callback=check_if_token_in_denylist)
