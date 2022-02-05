import typing

from app.models import user as user_models

if typing.TYPE_CHECKING:
    from app.tests import conftest


async def create_user(
    session: "conftest.AsyncSession", **kwargs: typing.Any
) -> user_models.User:
    user = user_models.User(**kwargs)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
