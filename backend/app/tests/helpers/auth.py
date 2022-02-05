import typing

import fastapi
import fastapi_jwt_auth as jwt_auth
import jwt
from starlette import datastructures

from app.config import general

settings = general.get_settings()


def create_auth_handler(subject: typing.Any) -> jwt_auth.AuthJWT:
    token = jwt_auth.AuthJWT().create_access_token(str(subject))
    request = fastapi.Request(
        scope={
            "type": "http",
            "headers": datastructures.Headers({"Authorization": f"Bearer {token}"}).raw,
        }
    )
    return jwt_auth.AuthJWT(request)


def is_token_fresh(token: str) -> bool:
    decoded_token = jwt.decode(
        jwt=token,
        key=settings.AUTHJWT_SECRET_KEY,
        algorithms=list(settings.AUTHJWT_DECODE_ALGORITHMS),
        options={"verify_exp": False},
    )
    return decoded_token["fresh"]
