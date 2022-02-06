import typing

import fastapi
import fastapi_jwt_auth as jwt_auth
from starlette import datastructures


def create_auth_handler(subject: typing.Any) -> jwt_auth.AuthJWT:
    token = jwt_auth.AuthJWT().create_access_token(str(subject))
    request = fastapi.Request(
        scope={
            "type": "http",
            "headers": datastructures.Headers({"Authorization": f"Bearer {token}"}).raw,
        }
    )
    return jwt_auth.AuthJWT(request)
