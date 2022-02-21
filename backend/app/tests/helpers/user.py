import typing

from app.models import user as user_models

if typing.TYPE_CHECKING:
    from app.tests import conftest


async def create_user(
    session: "conftest.AsyncSession", **kwargs: typing.Any
) -> user_models.User:
    if "email" not in kwargs:
        kwargs["email"] = "test@example.com"
    if "password" not in kwargs:
        kwargs["password"] = "hashed_password"
    user = user_models.User(**kwargs)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def create_active_user(
    session: "conftest.AsyncSession", **kwargs: typing.Any
) -> user_models.User:
    kwargs["confirmed_email"] = True
    return await create_user(session, **kwargs)
