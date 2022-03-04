import typing
from unittest import mock

import freezegun
import pytest
from sqlalchemy import exc
import sqlmodel

from app.exceptions.http import user as user_exceptions
from app.models import pagination
from app.models import user as user_models
from app.services import user as user_services
from app.tests.helpers import user as user_helpers
from app.utils import converters

if typing.TYPE_CHECKING:
    from app.tests import conftest


@pytest.mark.asyncio
@mock.patch("app.services.user.user_tasks.send_email_to_confirm_email.delay")
async def test_user_service_create_user(
    mocked_send_email: mock.MagicMock, session: "conftest.AsyncSession"
) -> None:
    password = "plain_password"
    user_create = user_models.UserCreate(
        email=converters.to_pydantic_email("test@email.com"),
        password=password,
        name="Test User",
    )

    created_user = await user_services.UserService(session).create_user(user_create)

    assert created_user.email == user_create.email
    assert created_user.password != password
    assert created_user.name == user_create.name
    mocked_send_email.assert_called_once_with(
        created_user.email, created_user.confirmation_email_key
    )


@pytest.mark.asyncio
@mock.patch("app.services.user.user_tasks.send_email_to_confirm_email.delay")
async def test_user_service_create_user_already_exists(
    mocked_send_email: mock.MagicMock,
    session: "conftest.AsyncSession",
) -> None:
    user_create = user_models.UserCreate(
        email=converters.to_pydantic_email("test@email.com"),
        password="plain_password",
        name="Test User",
    )
    await user_helpers.create_user(session=session, email=user_create.email)

    with pytest.raises(user_exceptions.UserAlreadyExistsError) as exc_info:
        await user_services.UserService(session).create_user(user_create)
    assert exc_info.value.context == {"email": user_create.email}
    mocked_send_email.assert_not_called()


@pytest.mark.asyncio
async def test_user_service_get_users(session: "conftest.AsyncSession") -> None:
    await user_helpers.create_user(session=session)
    user_2 = await user_helpers.create_user(session=session)
    user_3 = await user_helpers.create_user(session=session)
    await user_helpers.create_user(session=session)
    user_filters = user_models.UserFilters()

    retrieved_users = await user_services.UserService(session).get_users(
        user_filters, pagination.Pagination(offset=1, limit=2)
    )

    assert retrieved_users == [user_2, user_3]


@pytest.mark.asyncio
async def test_user_service_get_user(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(session=session, email="test@email.com")
    user_filters = user_models.UserFilters(id=user.id, email=user.email)

    retrieved_user = await user_services.UserService(session).get_user(user_filters)

    assert retrieved_user == user


@pytest.mark.asyncio
async def test_user_service_get_user_not_found(
    session: "conftest.AsyncSession",
) -> None:
    wrong_email = converters.to_pydantic_email("invalid@email.com")
    user = await user_helpers.create_user(session=session, email="test@email.com")
    user_filters = user_models.UserFilters(id=user.id, email=wrong_email)

    with pytest.raises(user_exceptions.UserNotFoundError) as exc_info:
        await user_services.UserService(session).get_user(user_filters)
    assert exc_info.value.context == {"id": user.id, "email": wrong_email}


@pytest.mark.asyncio
async def test_user_service_update_user(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(session=session, name="Test User")
    user_update = user_models.UserUpdate(name="Updated Name", confirmed_email=True)

    updated_user = await user_services.UserService(session).update_user(
        user, user_update
    )

    assert updated_user.name == user_update.name
    assert updated_user.confirmed_email is True
    assert updated_user.password == user.password


@pytest.mark.asyncio
async def test_user_service_update_user_new_password(
    session: "conftest.AsyncSession",
) -> None:
    old_password = "hashed_password"
    user = await user_helpers.create_user(session=session, password=old_password)
    new_plain_password = "plain_password"
    user_update = user_models.UserUpdate(password=new_plain_password)

    updated_user = await user_services.UserService(session).update_user(
        user, user_update
    )

    assert updated_user.password != new_plain_password
    assert updated_user.password != old_password


@pytest.mark.asyncio
async def test_user_service_delete_user(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(session=session)

    await user_services.UserService(session).delete_user(user)


@pytest.mark.asyncio
async def test_user_service_count_users(
    session: "conftest.AsyncSession",
) -> None:
    await user_helpers.create_user(session=session)
    await user_helpers.create_user(session=session)
    await user_helpers.create_user(session=session)
    user_filters = user_models.UserFilters()

    num_users = await user_services.UserService(session).count_users(user_filters)

    assert num_users == 3


@pytest.mark.asyncio
async def test_user_service_confirm_email(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(session=session)

    await user_services.UserService(session).confirm_email(user)

    assert user.confirmed_email is True


@pytest.mark.asyncio
async def test_user_service_confirm_email_already_confirmed(
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_user(session=session, confirmed_email=True)

    with pytest.raises(user_exceptions.ConfirmationEmailError) as exc_info:
        await user_services.UserService(session).confirm_email(user)
    assert exc_info.value.context == {
        "confirmation_email_key": user.confirmation_email_key
    }


@pytest.mark.asyncio
@mock.patch("app.services.user.settings.ACCOUNT_ACTIVATION_DAYS", new=2)
async def test_user_service_confirm_email_time_expired(
    session: "conftest.AsyncSession",
) -> None:

    with freezegun.freeze_time("2023-01-02 10:00:00"):
        user = await user_helpers.create_user(session=session)

    with freezegun.freeze_time("2023-01-05 10:00:00"):
        with pytest.raises(user_exceptions.ConfirmationEmailError) as exc_info:
            await user_services.UserService(session).confirm_email(user)
        assert exc_info.value.context == {
            "confirmation_email_key": user.confirmation_email_key
        }


@pytest.mark.asyncio
@mock.patch("app.services.user.user_tasks.send_email_to_reset_password.delay")
async def test_user_service_request_reset_password(
    mocked_send_email: mock.MagicMock,
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_user(session=session)

    user_services.UserService(session).request_reset_password(user)

    mocked_send_email.assert_called_once_with(user.email, user.reset_password_key)


@pytest.mark.asyncio
async def test_user_service_reset_password(
    session: "conftest.AsyncSession",
) -> None:
    old_password = "hashed_password"
    user = await user_helpers.create_user(session=session, password=old_password)
    old_reset_password_key = user.reset_password_key
    new_plain_password = "plain_password"

    await user_services.UserService(session).reset_password(user, new_plain_password)

    assert user.password != old_password
    assert user.password != new_plain_password
    assert user.reset_password_key != old_reset_password_key


@pytest.mark.asyncio
async def test_user_crud_create(session: "conftest.AsyncSession") -> None:
    user_create = user_models.UserCreate(
        email=converters.to_pydantic_email("test@email.com"),
        password="hashed_password",
        name="Test User",
    )

    created_user = await user_services.UserCRUD(session).create(user_create)

    assert created_user.email == user_create.email
    assert created_user.password == user_create.password
    assert created_user.name == user_create.name
    statement = sqlmodel.select(user_models.User).where(
        user_models.User.id == created_user.id
    )
    assert (await session.execute(statement)).scalar_one()


@pytest.mark.asyncio
async def test_user_crud_read_many(session: "conftest.AsyncSession") -> None:
    await user_helpers.create_user(session=session)
    user_2 = await user_helpers.create_user(session=session)
    user_3 = await user_helpers.create_user(session=session)
    await user_helpers.create_user(session=session)
    user_filters = user_models.UserFilters()

    retrieved_users = await user_services.UserCRUD(session).read_many(
        user_filters, pagination.Pagination(offset=1, limit=2)
    )

    assert retrieved_users == [user_2, user_3]


@pytest.mark.asyncio
async def test_user_crud_read_one(session: "conftest.AsyncSession") -> None:
    await user_helpers.create_user(session=session, email="test@email.com")
    user_2 = await user_helpers.create_user(session=session, email="test2@email.com")
    user_filters = user_models.UserFilters(id=user_2.id, email=user_2.email)

    retrieved_user = await user_services.UserCRUD(session).read_one(user_filters)

    assert retrieved_user == user_2


@pytest.mark.asyncio
async def test_user_crud_update(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(session=session, name="Test User")
    user_update = user_models.UserUpdate(name="Updated Name", confirmed_email=True)

    updated_user = await user_services.UserCRUD(session).update(user, user_update)

    assert updated_user.name == user_update.name
    assert updated_user.confirmed_email is True
    assert updated_user.password == user.password
    statement = sqlmodel.select(
        user_models.User
    ).where(  # pylint: disable=singleton-comparison,
        user_models.User.name == user_update.name,
        user_models.User.confirmed_email == True,  # noqa: E712
    )
    assert (await session.execute(statement)).scalar_one()


@pytest.mark.asyncio
async def test_user_crud_delete(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(session=session)

    await user_services.UserCRUD(session).delete(user)

    with pytest.raises(exc.NoResultFound):
        statement = sqlmodel.select(user_models.User).where(
            user_models.User.id == user.id
        )
        (await session.execute(statement)).scalar_one()


@pytest.mark.asyncio
async def test_user_crud_count(
    session: "conftest.AsyncSession",
) -> None:
    await user_helpers.create_user(session=session)
    await user_helpers.create_user(session=session)
    await user_helpers.create_user(session=session)
    user_filters = user_models.UserFilters()

    num_users = await user_services.UserCRUD(session).count(user_filters)

    assert num_users == 3
