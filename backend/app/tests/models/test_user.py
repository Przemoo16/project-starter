import datetime
import typing

import freezegun
import pytest

from app.models import user as user_models
from app.utils import converters

if typing.TYPE_CHECKING:
    from app.tests import conftest


@pytest.mark.asyncio
@freezegun.freeze_time("2022-01-16 22:00:00")
async def test_user_model(session: "conftest.AsyncSession") -> None:
    email = converters.to_pydantic_email("test@email.com")
    password = "hashed_password"
    user = user_models.User(email=email, password=password)

    session.add(user)
    await session.commit()
    await session.refresh(user)

    assert user.id
    assert user.email == email
    assert user.password == password
    assert user.confirmed_email is False
    assert user.confirmation_email_key
    assert user.reset_password_key
    assert user.created_at == datetime.datetime(2022, 1, 16, 22, 0, 0)
    assert user.updated_at == datetime.datetime(2022, 1, 16, 22, 0, 0)
    assert user.last_login is None
    assert user.is_active is False


@pytest.mark.asyncio
async def test_user_updated_at_field(session: "conftest.AsyncSession") -> None:
    with freezegun.freeze_time("2022-01-16 22:00:00"):
        user = user_models.User(
            email=converters.to_pydantic_email("test@email.com"),
            password="hashed_password",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    with freezegun.freeze_time("2022-01-16 23:00:00"):
        user.email = converters.to_pydantic_email("updated@email.com")
        session.add(user)
        await session.commit()
        await session.refresh(user)

    assert user.updated_at == datetime.datetime(2022, 1, 16, 23, 0, 0)
