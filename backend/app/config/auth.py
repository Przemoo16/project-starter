import typing

import fastapi_paseto_auth as paseto_auth

from app.config import db, general

paseto_token_db = db.get_paseto_token_db()


@paseto_auth.AuthPASETO.load_config
def get_paseto_token_settings() -> general.Settings:
    return general.get_settings()


def check_if_token_in_denylist(decrypted_token: dict[str, typing.Any]) -> bool:
    jti = decrypted_token["jti"]
    is_revoked = paseto_token_db.get(jti)
    return is_revoked == "true"


paseto_auth.AuthPASETO.token_in_denylist_loader(callback=check_if_token_in_denylist)
