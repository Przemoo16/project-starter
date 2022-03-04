import typing
import uuid

from app.models import user as user_models
from app.tests.helpers import db

if typing.TYPE_CHECKING:
    from app.tests import conftest


async def create_user(
    session: "conftest.AsyncSession", **kwargs: typing.Any
) -> user_models.User:
    if "email" not in kwargs:
        kwargs["email"] = f"{uuid.uuid4()}@email.com"
    if "password" not in kwargs:
        kwargs["password"] = "hashed_password"
    if "name" not in kwargs:
        kwargs["name"] = "Test User"
    user = user_models.User(**kwargs)
    return await db.save(session, user)


async def create_active_user(
    session: "conftest.AsyncSession", **kwargs: typing.Any
) -> user_models.User:
    kwargs["confirmed_email"] = True
    return await create_user(session, **kwargs)
