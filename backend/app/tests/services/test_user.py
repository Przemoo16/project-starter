import datetime
import typing
from unittest import mock

import freezegun
import pytest

from app.exceptions.http import user as user_exceptions
from app.models import pagination
from app.models import user as user_models
from app.services import user as user_services
from app.tests.helpers import reset_password as reset_password_helpers
from app.tests.helpers import user as user_helpers
from app.utils import converters

if typing.TYPE_CHECKING:
    from app.tests import conftest


@pytest.mark.anyio
@mock.patch("app.services.user.user_tasks.send_email_to_confirm_email.delay")
async def test_user_service_create_user(
    mock_send_email: mock.MagicMock, session: "conftest.AsyncSession"
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
    mock_send_email.assert_called_once_with(
        created_user.email, created_user.email_confirmation_token
    )


@pytest.mark.anyio
@mock.patch("app.services.user.user_tasks.send_email_to_confirm_email.delay")
async def test_user_service_create_user_already_exists(
    mock_send_email: mock.MagicMock,
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
    mock_send_email.assert_not_called()


@pytest.mark.anyio
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


@pytest.mark.anyio
async def test_user_service_get_user(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(session=session, email="test@email.com")
    user_filters = user_models.UserFilters(id=user.id, email=user.email)

    retrieved_user = await user_services.UserService(session).get_user(user_filters)

    assert retrieved_user == user


@pytest.mark.anyio
async def test_user_service_get_user_not_found(
    session: "conftest.AsyncSession",
) -> None:
    wrong_email = converters.to_pydantic_email("invalid@email.com")
    user = await user_helpers.create_user(session=session, email="test@email.com")
    user_filters = user_models.UserFilters(id=user.id, email=wrong_email)

    with pytest.raises(user_exceptions.UserNotFoundError) as exc_info:
        await user_services.UserService(session).get_user(user_filters)
    assert exc_info.value.context == {"id": user.id, "email": wrong_email}


@pytest.mark.anyio
async def test_user_service_get_active_user(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_active_user(
        session=session, email="test@email.com"
    )
    user_filters = user_models.UserFilters(id=user.id, email=user.email)

    retrieved_user = await user_services.UserService(session).get_active_user(
        user_filters
    )

    assert retrieved_user == user


@pytest.mark.anyio
async def test_user_service_get_active_user_inactive(
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_user(session=session, email="test@email.com")
    user_filters = user_models.UserFilters(id=user.id, email=user.email)

    with pytest.raises(user_exceptions.InactiveUserError) as exc_info:
        await user_services.UserService(session).get_active_user(user_filters)
    assert exc_info.value.context == {"id": user.id}


@pytest.mark.anyio
async def test_user_service_update_user(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(session=session, name="Test User")
    user_update = user_models.UserUpdate(name="Updated Name", confirmed_email=True)

    updated_user = await user_services.UserService(session).update_user(
        user, user_update
    )

    assert updated_user.name == user_update.name
    assert updated_user.confirmed_email is True
    assert updated_user.password == user.password


@pytest.mark.anyio
async def test_user_service_update_user_password(
    session: "conftest.AsyncSession",
) -> None:
    old_hashed_password = "hashed_password"
    user = await user_helpers.create_user(session=session, password=old_hashed_password)
    new_password = "new_password"
    user_update = user_models.UserUpdate(password=new_password)

    updated_user = await user_services.UserService(session).update_user(
        user, user_update
    )

    assert updated_user.password != old_hashed_password
    assert updated_user.password != new_password


@pytest.mark.anyio
async def test_user_service_delete_user(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(session=session)

    await user_services.UserService(session).delete_user(user)


@pytest.mark.anyio
async def test_user_service_count_users(
    session: "conftest.AsyncSession",
) -> None:
    await user_helpers.create_user(session=session)
    await user_helpers.create_user(session=session)
    await user_helpers.create_user(session=session)
    user_filters = user_models.UserFilters()

    num_users = await user_services.UserService(session).count_users(user_filters)

    assert num_users == 3


@pytest.mark.anyio
async def test_user_service_change_password(
    session: "conftest.AsyncSession",
) -> None:
    old_hashed_password = "$2b$12$q8JcpltDZkSLOdMuPyt/jORzExLKp9HsKgCoFJQ1IzzITc2/Pg42q"
    user = await user_helpers.create_user(session=session, password=old_hashed_password)
    new_password = "new_password"

    await user_services.UserService(session).change_password(
        user, "plain_password", new_password
    )

    assert user.password != old_hashed_password
    assert user.password != new_password


@pytest.mark.anyio
async def test_user_service_change_password_invalid_password(
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_user(
        session=session,
        password="$2b$12$q8JcpltDZkSLOdMuPyt/jORzExLKp9HsKgCoFJQ1IzzITc2/Pg42q",
    )

    with pytest.raises(user_exceptions.InvalidPasswordError):
        await user_services.UserService(session).change_password(
            user, "invalid_password", "new_password"
        )


@pytest.mark.anyio
async def test_user_service_confirm_email(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(session=session)

    await user_services.UserService(session).confirm_email(user)

    assert user.confirmed_email is True


@pytest.mark.anyio
async def test_user_service_confirm_email_already_confirmed(
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_user(session=session, confirmed_email=True)

    with pytest.raises(user_exceptions.EmailAlreadyConfirmedError) as exc_info:
        await user_services.UserService(session).confirm_email(user)
    assert exc_info.value.context == {"id": user.email_confirmation_token}


@pytest.mark.anyio
@mock.patch(
    "app.services.user.settings.EMAIL_CONFIRMATION_TOKEN_EXPIRES",
    new=datetime.timedelta(days=2),
)
async def test_user_service_confirm_email_token_expired(
    session: "conftest.AsyncSession",
) -> None:

    with freezegun.freeze_time("2023-01-02 10:00:00"):
        user = await user_helpers.create_user(session=session)

    with freezegun.freeze_time("2023-01-05 10:00:00"):
        with pytest.raises(
            user_exceptions.EmailConfirmationTokenExpiredError
        ) as exc_info:
            await user_services.UserService(session).confirm_email(user)
        assert exc_info.value.context == {"id": user.email_confirmation_token}


@pytest.mark.anyio
@mock.patch("app.services.reset_password.ResetPasswordService.create_token")
@mock.patch("app.services.user.user_tasks.send_email_to_reset_password.delay")
async def test_user_service_reset_password(
    mock_send_email: mock.MagicMock,
    mock_create_token: mock.AsyncMock,
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_active_user(session=session)
    token = await reset_password_helpers.create_reset_password_token(
        session=session, user_id=user.id
    )
    mock_create_token.return_value = token

    await user_services.UserService(session).reset_password(user)

    mock_send_email.assert_called_once_with(user.email, token.id)


@pytest.mark.anyio
@mock.patch("app.services.reset_password.ResetPasswordService.get_valid_token")
@mock.patch("app.services.reset_password.ResetPasswordService.force_to_expire")
async def test_user_service_set_password(
    mock_force_to_expire: mock.AsyncMock,
    mock_get_valid_token: mock.AsyncMock,
    session: "conftest.AsyncSession",
) -> None:
    current_password = "hashed_password"
    user = await user_helpers.create_active_user(
        session=session, password=current_password
    )
    token = await reset_password_helpers.create_reset_password_token(
        session, user_id=user.id
    )
    mock_get_valid_token.return_value = token
    new_plain_password = "plain_password"

    await user_services.UserService(session).set_password(token.id, new_plain_password)

    assert user.password != current_password
    assert user.password != new_plain_password
    mock_force_to_expire.assert_called_once_with(token)


@pytest.mark.anyio
@mock.patch("app.services.reset_password.ResetPasswordService.get_valid_token")
async def test_user_service_set_password_inactive_user(
    mock_get_valid_token: mock.AsyncMock, session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_user(session=session, password="hashed_password")
    token = await reset_password_helpers.create_reset_password_token(
        session, user_id=user.id
    )
    mock_get_valid_token.return_value = token

    with pytest.raises(user_exceptions.InactiveUserError) as exc_info:
        await user_services.UserService(session).set_password(
            token.id, "plain_password"
        )
    assert exc_info.value.context == {"id": user.id}
