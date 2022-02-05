import typing
from unittest import mock

import fastapi_jwt_auth as jwt_auth
from fastapi_jwt_auth import exceptions as jwt_exceptions
import pytest

from app.api.deps import user as user_deps
from app.services import exceptions as resource_exceptions
from app.tests.helpers import auth as auth_helpers
from app.tests.helpers import user as user_helpers
from app.utils import converters

if typing.TYPE_CHECKING:
    from app.tests import conftest


@pytest.mark.asyncio
async def test_get_current_user(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(
        session=session, email="test@email.com", password="hashed_password"
    )
    auth_handler = auth_helpers.create_auth_handler(user.id)

    current_user = await user_deps.get_current_user(session, auth_handler)

    assert current_user == user


@pytest.mark.asyncio
async def test_get_current_user_without_jwt(session: "conftest.AsyncSession") -> None:
    auth_handler = jwt_auth.AuthJWT()

    with pytest.raises(jwt_exceptions.MissingTokenError):
        await user_deps.get_current_user(session, auth_handler)


@pytest.mark.asyncio
@mock.patch("fastapi_jwt_auth.AuthJWT.jwt_required")
async def test_get_current_user_empty_jwt_subject(
    session: "conftest.AsyncSession",
) -> None:
    auth_handler = jwt_auth.AuthJWT()

    with pytest.raises(resource_exceptions.UnauthorizedError):
        await user_deps.get_current_user(session, auth_handler)


@pytest.mark.asyncio
async def test_get_current_user_not_found(session: "conftest.AsyncSession") -> None:
    user_id = converters.change_to_uuid("0dd53909-fcda-4c72-afcd-1bf4886389f8")
    auth_handler = auth_helpers.create_auth_handler(user_id)

    with pytest.raises(resource_exceptions.UnauthorizedError):
        await user_deps.get_current_user(session, auth_handler)


@pytest.mark.asyncio
async def test_get_current_active_user(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(
        session=session,
        email="test@email.com",
        password="hashed_password",
        confirmed_email=True,
    )

    current_user = await user_deps.get_current_active_user(user)

    assert current_user == user


@pytest.mark.asyncio
async def test_get_current_active_user_inactive(
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_user(
        session=session, email="test@email.com", password="hashed_password"
    )

    with pytest.raises(resource_exceptions.ForbiddenError) as exc_info:
        await user_deps.get_current_active_user(user)
    assert exc_info.value.context == {"user": user.email}


@pytest.mark.asyncio
async def test_check_user_requests_own_data(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(
        session=session,
        email="test@email.com",
        password="hashed_password",
        confirmed_email=True,
    )

    await user_deps.check_user_requests_own_data(user.id, user)


@pytest.mark.asyncio
async def test_check_user_requests_own_data_foreign_data(
    session: "conftest.AsyncSession",
) -> None:
    user_id = converters.change_to_uuid("0dd53909-fcda-4c72-afcd-1bf4886389f8")
    user = await user_helpers.create_user(
        session=session,
        email="test@email.com",
        password="hashed_password",
        confirmed_email=True,
    )

    with pytest.raises(resource_exceptions.ForbiddenError) as exc_info:
        await user_deps.check_user_requests_own_data(user_id, user)
    assert exc_info.value.context == {"id": user_id}
