import functools
from typing import Any

import fastapi_jwt_auth as jwt_auth
import redis

from app.config import general

settings = general.get_settings()


@jwt_auth.AuthJWT.load_config
def get_jwt_settings() -> general.Settings:
    return general.get_settings()


@functools.lru_cache()
def get_jwt_db() -> redis.Redis:  # type: ignore
    return redis.Redis.from_url(settings.AUTHJWT_DATABASE_URL, decode_responses=True)


@jwt_auth.AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token: dict[str, Any]) -> bool:
    jti = decrypted_token["jti"]
    is_revoked = get_jwt_db().get(jti)
    return is_revoked == "true"
