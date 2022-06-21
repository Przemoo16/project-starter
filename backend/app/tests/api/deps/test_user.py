import typing
from unittest import mock

import fastapi_jwt_auth as jwt_auth
from fastapi_jwt_auth import exceptions
import pytest

from app.api.deps import user as user_deps
from app.exceptions.http import user as user_exceptions
from app.tests.helpers import auth as auth_helpers
from app.tests.helpers import user as user_helpers
from app.utils import converters

if typing.TYPE_CHECKING:
    from app.tests import conftest


@pytest.mark.anyio
async def test_get_current_user(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(session=session)
    auth_handler = auth_helpers.create_auth_handler(user.id)

    current_user = await user_deps.get_current_user(session, auth_handler)

    assert current_user == user


@pytest.mark.anyio
async def test_get_current_user_without_jwt(session: "conftest.AsyncSession") -> None:
    auth_handler = jwt_auth.AuthJWT()

    with pytest.raises(exceptions.MissingTokenError):
        await user_deps.get_current_user(session, auth_handler)


@pytest.mark.anyio
@mock.patch("fastapi_jwt_auth.AuthJWT.jwt_required")
async def test_get_current_user_empty_jwt_subject(
    session: "conftest.AsyncSession",
) -> None:
    auth_handler = jwt_auth.AuthJWT()

    with pytest.raises(user_exceptions.UserNotFoundError):
        await user_deps.get_current_user(session, auth_handler)


@pytest.mark.anyio
async def test_get_current_active_user(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_active_user(session=session)

    current_user = await user_deps.get_current_active_user(user)

    assert current_user == user


@pytest.mark.anyio
async def test_get_current_active_user_inactive(
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_user(session=session)

    with pytest.raises(user_exceptions.InactiveUserError) as exc_info:
        await user_deps.get_current_active_user(user)
    assert exc_info.value.context == {"id": user.id}


@pytest.mark.anyio
async def test_check_user_requests_own_data(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_active_user(session=session)

    await user_deps.check_user_requests_own_data(user.id, user)


@pytest.mark.anyio
async def test_check_user_requests_own_data_foreign_data(
    session: "conftest.AsyncSession",
) -> None:
    user_id = converters.to_uuid("1dd53909-fcda-4c72-afcd-1bf4886389f8")
    user = await user_helpers.create_active_user(session=session)

    with pytest.raises(user_exceptions.UserForbiddenError) as exc_info:
        await user_deps.check_user_requests_own_data(user_id, user)
    assert exc_info.value.context == {"id": user_id}
