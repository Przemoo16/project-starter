import typing

import fastapi
import fastapi_jwt_auth as jwt_auth
from starlette import datastructures

from app.models import user as user_model

if typing.TYPE_CHECKING:
    from app.tests import conftest


async def create_user(
    session: "conftest.AsyncSession", **kwargs: typing.Any
) -> user_model.User:
    user = user_model.User(**kwargs)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


def create_auth_handler(subject: typing.Any) -> jwt_auth.AuthJWT:
    token = jwt_auth.AuthJWT().create_access_token(str(subject))
    request = fastapi.Request(
        scope={
            "type": "http",
            "headers": datastructures.Headers({"Authorization": f"Bearer {token}"}).raw,
        }
    )
    return jwt_auth.AuthJWT(request)
