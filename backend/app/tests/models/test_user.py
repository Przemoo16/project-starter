from datetime import datetime
from typing import TYPE_CHECKING

import freezegun
import pytest

from app import models

if TYPE_CHECKING:
    from sqlalchemy.ext import asyncio


@freezegun.freeze_time("2022-01-16 22:00:00")
@pytest.mark.asyncio
async def test_user_model(session: "asyncio.AsyncSession") -> None:
    email = "test@email.com"
    password = "test_password"
    user = models.User(email=email, password=password)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    assert user.id
    assert user.email == email
    assert user.password == password
    assert user.confirmed_email is False
    assert user.confirmation_email_key
    assert user.reset_password_key
    assert user.created_at == datetime(2022, 1, 16, 22, 0, 0)
    assert user.updated_at == datetime(2022, 1, 16, 22, 0, 0)
    assert user.last_login is None
    assert user.is_active is True
    assert user.is_superuser is False


@pytest.mark.asyncio
async def test_user_updated_at_field(session: "asyncio.AsyncSession") -> None:
    with freezegun.freeze_time("2022-01-16 22:00:00"):
        user = models.User(email="test@email.com", password="test_password")
        session.add(user)
        await session.commit()
        await session.refresh(user)

    with freezegun.freeze_time("2022-01-16 23:00:00"):
        user.email = "updated@email.com"
        session.add(user)
        await session.commit()
        await session.refresh(user)

    assert user.updated_at == datetime(2022, 1, 16, 23, 0, 0)
