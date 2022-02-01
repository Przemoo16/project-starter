from typing import TYPE_CHECKING
from unittest import mock

import freezegun
import pytest
from sqlalchemy import exc
import sqlmodel

from app.models import user as user_model
from app.services import exceptions
from app.services import user as user_service
from app.tests import helpers
from app.utils import converters

if TYPE_CHECKING:
    from app.tests import conftest


@pytest.mark.asyncio
async def test_user_service_create_user(session: "conftest.AsyncSession") -> None:
    password = "plain_password"
    user_create = user_model.UserCreate(email="test@email.com", password=password)

    created_user = await user_service.UserService(session).create_user(user_create)

    assert created_user.email == user_create.email
    assert created_user.password != password


@pytest.mark.asyncio
async def test_user_service_create_user_already_exists(
    session: "conftest.AsyncSession",
) -> None:
    user_create = user_model.UserCreate(
        email="test@email.com", password="plain_password"
    )
    await helpers.create_user(
        session=session, email=user_create.email, password="hashed_password"
    )

    with pytest.raises(exceptions.ConflictError) as exc_info:
        await user_service.UserService(session).create_user(user_create)
    assert exc_info.value.context == {"email": user_create.email}


@pytest.mark.asyncio
async def test_user_service_get_user(session: "conftest.AsyncSession") -> None:
    user = await helpers.create_user(
        session=session, email="test@email.com", password="hashed_password"
    )

    retrieved_user = await user_service.UserService(session).get_user(user.id)

    assert retrieved_user.id == user.id


@pytest.mark.asyncio
async def test_user_service_get_user_not_found(
    session: "conftest.AsyncSession",
) -> None:
    user_id = converters.change_to_uuid("0dd53909-fcda-4c72-afcd-1bf4886389f8")

    with pytest.raises(exceptions.NotFoundError) as exc_info:
        await user_service.UserService(session).get_user(user_id)
    assert exc_info.value.context == {"id": user_id}


@pytest.mark.asyncio
async def test_user_service_update_user(session: "conftest.AsyncSession") -> None:
    user = await helpers.create_user(
        session=session, email="test@email.com", password="hashed_password"
    )
    user_update = user_model.UserUpdate(email="new@email.com")

    updated_user = await user_service.UserService(session).update_user(
        user.id, user_update
    )

    assert updated_user.email == user_update.email
    assert updated_user.password == user.password


@pytest.mark.asyncio
async def test_user_service_update_user_new_password(
    session: "conftest.AsyncSession",
) -> None:
    old_password = "hashed_password"
    user = await helpers.create_user(
        session=session, email="test@email.com", password=old_password
    )
    new_plain_password = "plain_password"
    user_update = user_model.UserUpdate(password=new_plain_password)

    updated_user = await user_service.UserService(session).update_user(
        user.id, user_update
    )

    assert updated_user.password != new_plain_password
    assert updated_user.password != old_password


@pytest.mark.asyncio
async def test_user_service_update_user_not_found(
    session: "conftest.AsyncSession",
) -> None:
    user_id = converters.change_to_uuid("0dd53909-fcda-4c72-afcd-1bf4886389f8")
    user_update = user_model.UserUpdate(email="new@email.com")

    with pytest.raises(exceptions.NotFoundError) as exc_info:
        await user_service.UserService(session).update_user(user_id, user_update)
    assert exc_info.value.context == {"id": user_id}


@pytest.mark.asyncio
async def test_user_service_delete_user(session: "conftest.AsyncSession") -> None:
    user = await helpers.create_user(
        session=session, email="test@email.com", password="hashed_password"
    )

    await user_service.UserService(session).delete_user(user.id)


@pytest.mark.asyncio
async def test_user_service_delete_user_not_found(
    session: "conftest.AsyncSession",
) -> None:
    user_id = converters.change_to_uuid("0dd53909-fcda-4c72-afcd-1bf4886389f8")

    with pytest.raises(exceptions.NotFoundError) as exc_info:
        await user_service.UserService(session).delete_user(user_id)
    assert exc_info.value.context == {"id": user_id}


@pytest.mark.asyncio
async def test_user_service_confirm_email(session: "conftest.AsyncSession") -> None:
    user = await helpers.create_user(
        session=session, email="test@email.com", password="hashed_password"
    )

    confirmed_email = await user_service.UserService(session).confirm_email(
        user.confirmation_email_key
    )

    assert confirmed_email is True
    assert user.confirmed_email is True


@pytest.mark.asyncio
async def test_user_service_confirm_email_not_found(
    session: "conftest.AsyncSession",
) -> None:
    key = converters.change_to_uuid("0dd53909-fcda-4c72-afcd-1bf4886389f8")

    with pytest.raises(exceptions.NotFoundError) as exc_info:
        await user_service.UserService(session).confirm_email(key)
    assert exc_info.value.context == {"key": key}


@pytest.mark.asyncio
async def test_user_service_confirm_email_already_confirmed(
    session: "conftest.AsyncSession",
) -> None:
    user = await helpers.create_user(
        session=session,
        email="test@email.com",
        password="hashed_password",
        confirmed_email=True,
    )

    with pytest.raises(exceptions.NotFoundError) as exc_info:
        await user_service.UserService(session).confirm_email(
            user.confirmation_email_key
        )
    assert exc_info.value.context == {"key": user.confirmation_email_key}


@pytest.mark.asyncio
@mock.patch("app.services.user.settings.ACCOUNT_ACTIVATION_DAYS", new=2)
async def test_user_service_confirm_email_time_expired(
    session: "conftest.AsyncSession",
) -> None:

    with freezegun.freeze_time("2023-01-02 10:00:00"):
        user = await helpers.create_user(
            session=session, email="test@email.com", password="hashed_password"
        )

    with freezegun.freeze_time("2023-01-05 10:00:00"):
        with pytest.raises(exceptions.NotFoundError) as exc_info:
            await user_service.UserService(session).confirm_email(
                user.confirmation_email_key
            )
        assert exc_info.value.context == {"key": user.confirmation_email_key}


@pytest.mark.asyncio
async def test_user_crud_create(session: "conftest.AsyncSession") -> None:
    user_create = user_model.UserCreate(
        email="test@email.com", password="hashed_password"
    )
    read_statement = sqlmodel.select(user_model.User).where(
        user_model.User.email == user_create.email
    )

    created_user = await user_service.UserCRUD(session).create(user_create)

    assert created_user.email == user_create.email
    assert created_user.password == user_create.password
    assert (await session.execute(read_statement)).scalar_one()


@pytest.mark.asyncio
async def test_user_crud_read(session: "conftest.AsyncSession") -> None:
    await helpers.create_user(
        session=session,
        email="test@email.com",
        password="hashed_password",
    )
    user_2 = await helpers.create_user(
        session=session,
        email="test2@email.com",
        password="hashed_password",
        confirmed_email=False,
    )

    retrieved_user = await user_service.UserCRUD(session).read(
        id=user_2.id, email=user_2.email, confirmed_email=False
    )

    assert retrieved_user == user_2


@pytest.mark.asyncio
async def test_user_crud_update(session: "conftest.AsyncSession") -> None:
    user = await helpers.create_user(
        session=session, email="test@email.com", password="hashed_password"
    )
    new_email = "new@email.com"
    read_statement = sqlmodel.select(user_model.User).where(
        user_model.User.email == new_email
    )

    updated_user = await user_service.UserCRUD(session).update(user, email=new_email)

    assert updated_user.email == new_email
    assert updated_user.password == user.password
    db_user = (await session.execute(read_statement)).scalar_one()
    assert db_user.email == new_email


@pytest.mark.asyncio
async def test_user_crud_delete(session: "conftest.AsyncSession") -> None:
    user = await helpers.create_user(
        session=session, email="test@email.com", password="hashed_password"
    )
    read_statement = sqlmodel.select(user_model.User).where(
        user_model.User.email == user.email
    )

    await user_service.UserCRUD(session).delete(user)

    with pytest.raises(exc.NoResultFound):
        (await session.execute(read_statement)).scalar_one()
