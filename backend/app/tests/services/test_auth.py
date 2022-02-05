import datetime
import typing

import fastapi_jwt_auth as jwt_auth
import freezegun
import pytest

from app.services import auth, exceptions
from app.tests.helpers import auth as auth_helpers
from app.tests.helpers import user as user_helpers

if typing.TYPE_CHECKING:
    from app.tests import conftest


@pytest.mark.asyncio
@freezegun.freeze_time("2022-02-05 18:30:00")
async def test_token_service_create_tokens(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(
        session,
        email="test@email.com",
        password="$2b$12$q8JcpltDZkSLOdMuPyt/jORzExLKp9HsKgCoFJQ1IzzITc2/Pg42q",
        confirmed_email=True,
    )
    auth_handler = jwt_auth.AuthJWT()

    with freezegun.freeze_time("2022-02-05 18:00:00"):
        tokens = await auth.TokenService(session).create_tokens(
            email=user.email, password="plain_password", Authorize=auth_handler
        )

    assert tokens.access_token
    assert tokens.refresh_token
    assert tokens.token_type == "bearer"
    assert auth_helpers.is_token_fresh(tokens.access_token)
    assert user.last_login == datetime.datetime(2022, 2, 5, 18, 0, 0)


@pytest.mark.asyncio
async def test_token_service_create_tokens_no_user(
    session: "conftest.AsyncSession",
) -> None:
    email = "test@email.com"
    auth_handler = jwt_auth.AuthJWT()

    with pytest.raises(exceptions.UnauthorizedError) as exc_info:
        await auth.TokenService(session).create_tokens(
            email=email, password="plain_password", Authorize=auth_handler
        )
    assert exc_info.value.context == {"email": email}


@pytest.mark.asyncio
async def test_token_service_create_tokens_invalid_password(
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_user(
        session,
        email="test@email.com",
        password="$2b$12$q8JcpltDZkSLOdMuPyt/jORzExLKp9HsKgCoFJQ1IzzITc2/Pg42q",
        confirmed_email=True,
    )
    auth_handler = jwt_auth.AuthJWT()

    with pytest.raises(exceptions.UnauthorizedError) as exc_info:
        await auth.TokenService(session).create_tokens(
            email=user.email, password="invalid_password", Authorize=auth_handler
        )
    assert exc_info.value.context == {"email": user.email}


@pytest.mark.asyncio
async def test_token_service_create_tokens_inactive_user(
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_user(
        session,
        email="test@email.com",
        password="$2b$12$q8JcpltDZkSLOdMuPyt/jORzExLKp9HsKgCoFJQ1IzzITc2/Pg42q",
    )
    auth_handler = jwt_auth.AuthJWT()

    with pytest.raises(exceptions.UnauthorizedError) as exc_info:
        await auth.TokenService(session).create_tokens(
            email=user.email, password="plain_password", Authorize=auth_handler
        )
    assert exc_info.value.context == {"email": user.email}
