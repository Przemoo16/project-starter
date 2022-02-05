import typing

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
