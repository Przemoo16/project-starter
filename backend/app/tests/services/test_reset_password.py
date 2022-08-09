import datetime
import typing

import freezegun
import pytest

from app.exceptions.http import reset_password as reset_password_exceptions
from app.models import reset_password as reset_password_models
from app.services import reset_password as reset_password_services
from app.tests.helpers import reset_password as reset_password_helpers
from app.tests.helpers import user as user_helpers
from app.utils import converters

if typing.TYPE_CHECKING:
    from app.tests import conftest


@pytest.mark.anyio
async def test_reset_password_service_create_token(
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_active_user(session)
    token_create = reset_password_models.ResetPasswordTokenCreate(user_id=user.id)

    created_token = await reset_password_services.ResetPasswordService(
        session
    ).create_token(token_create)

    assert created_token.user_id == user.id


@pytest.mark.anyio
@freezegun.freeze_time("2023-07-15 13:00:00")
async def test_reset_password_service_create_token_already_exists(
    session: "conftest.AsyncSession",
) -> None:
    reset_password_service = reset_password_services.ResetPasswordService(session)
    user = await user_helpers.create_active_user(session)
    token = await reset_password_helpers.create_reset_password_token(
        session, user_id=user.id
    )
    token_id = token.id

    token_create = reset_password_models.ResetPasswordTokenCreate(user_id=user.id)

    created_token = await reset_password_service.create_token(token_create)

    assert created_token.user_id == user.id
    token_db = await reset_password_service.get_token(
        reset_password_models.ResetPasswordTokenFilters(id=token_id)
    )
    assert token_db.expire_at == datetime.datetime(2023, 7, 15, 13, 00, 0)


@pytest.mark.anyio
async def test_reset_password_service_get_token(
    session: "conftest.AsyncSession",
) -> None:
    token = await reset_password_helpers.create_reset_password_token(session=session)
    token_filters = reset_password_models.ResetPasswordTokenFilters(id=token.id)

    retrieved_token = await reset_password_services.ResetPasswordService(
        session
    ).get_token(token_filters)

    assert retrieved_token == token


@pytest.mark.anyio
async def test_reset_password_service_get_token_not_found(
    session: "conftest.AsyncSession",
) -> None:
    wrong_id = converters.to_uuid("1dd53909-fcda-4c72-afcd-1bf4886389f8")
    token_filters = reset_password_models.ResetPasswordTokenFilters(id=wrong_id)

    with pytest.raises(
        reset_password_exceptions.ResetPasswordTokenNotFoundError
    ) as exc_info:
        await reset_password_services.ResetPasswordService(session).get_token(
            token_filters
        )
    assert exc_info.value.context == {"id": wrong_id}


@pytest.mark.anyio
async def test_reset_password_service_get_valid_token(
    session: "conftest.AsyncSession",
) -> None:
    token = await reset_password_helpers.create_reset_password_token(session=session)
    token_filters = reset_password_models.ResetPasswordTokenFilters(id=token.id)

    retrieved_token = await reset_password_services.ResetPasswordService(
        session
    ).get_valid_token(token_filters)

    assert retrieved_token == token


@pytest.mark.anyio
@freezegun.freeze_time("2023-07-15 13:00:00")
async def test_reset_password_service_get_valid_token_expired(
    session: "conftest.AsyncSession",
) -> None:
    token = await reset_password_helpers.create_reset_password_token(
        session=session, expire_at=datetime.datetime(2023, 7, 15, 12, 0, 0)
    )
    token_filters = reset_password_models.ResetPasswordTokenFilters(id=token.id)

    with pytest.raises(
        reset_password_exceptions.ResetPasswordTokenExpiredError
    ) as exc_info:
        await reset_password_services.ResetPasswordService(session).get_valid_token(
            token_filters
        )
    assert exc_info.value.context == {"id": token.id}


@pytest.mark.anyio
@freezegun.freeze_time("2023-07-15 13:00:00")
async def test_reset_password_service_force_to_expire(
    session: "conftest.AsyncSession",
) -> None:
    reset_password_service = reset_password_services.ResetPasswordService(session)
    token = await reset_password_helpers.create_reset_password_token(session)
    token_id = token.id

    await reset_password_service.force_to_expire(token)

    token_db = await reset_password_service.get_token(
        reset_password_models.ResetPasswordTokenFilters(id=token_id)
    )
    assert token_db.expire_at == datetime.datetime(2023, 7, 15, 13, 00, 0)


@pytest.mark.anyio
async def test_reset_password_crud_read_latest(
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_user(session)
    await reset_password_helpers.create_reset_password_token(session, user_id=user.id)
    await reset_password_helpers.create_reset_password_token(session, user_id=user.id)
    latest_user_token = await reset_password_helpers.create_reset_password_token(
        session, user_id=user.id
    )
    await reset_password_helpers.create_reset_password_token(session)
    token_filters = reset_password_models.ResetPasswordTokenFilters(user_id=user.id)

    retrieved_latest_token = await reset_password_services.ResetPasswordCRUD(
        session
    ).read_latest(token_filters)

    assert retrieved_latest_token == latest_user_token
