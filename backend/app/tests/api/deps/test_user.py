import typing

import fastapi
import fastapi_paseto_auth as paseto_auth
import pytest
from fastapi_paseto_auth import exceptions
from starlette import datastructures

from app.api.deps import user as user_deps
from app.exceptions.http import user as user_exceptions
from app.tests.helpers import user as user_helpers
from app.utils import converters

if typing.TYPE_CHECKING:
    from app.tests import conftest


@pytest.mark.anyio
async def test_get_current_user(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(session=session)
    token = paseto_auth.AuthPASETO().create_access_token(str(user.id))
    request = fastapi.Request(
        scope={
            "type": "http",
            "headers": datastructures.Headers({"Authorization": f"Bearer {token}"}).raw,
        }
    )

    current_user = await user_deps.get_current_user(
        session, paseto_auth.AuthPASETO(request)
    )

    assert current_user == user


@pytest.mark.anyio
async def test_get_current_user_without_token(session: "conftest.AsyncSession") -> None:
    request = fastapi.Request(
        scope={
            "type": "http",
            "headers": datastructures.Headers().raw,
        }
    )

    with pytest.raises(exceptions.MissingTokenError):
        await user_deps.get_current_user(session, paseto_auth.AuthPASETO(request))


@pytest.mark.anyio
async def test_get_current_user_empty_token_subject(
    session: "conftest.AsyncSession",
) -> None:
    token = paseto_auth.AuthPASETO().create_access_token("")
    request = fastapi.Request(
        scope={
            "type": "http",
            "headers": datastructures.Headers({"Authorization": f"Bearer {token}"}).raw,
        }
    )

    with pytest.raises(user_exceptions.UserNotFoundError):
        await user_deps.get_current_user(session, paseto_auth.AuthPASETO(request))


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
