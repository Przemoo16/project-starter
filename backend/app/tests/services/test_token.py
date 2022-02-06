import datetime
import typing

import fastapi_jwt_auth as jwt_auth
import freezegun
import pytest

from app.services import exceptions
from app.services import token as token_services
from app.tests.helpers import auth
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
        tokens = await token_services.TokenService(session).create_tokens(
            email=user.email, password="plain_password", Authorize=auth_handler
        )

    assert tokens.access_token
    assert tokens.refresh_token
    assert tokens.token_type == "bearer"
    assert auth.is_token_fresh(tokens.access_token)
    assert user.last_login == datetime.datetime(2022, 2, 5, 18, 0, 0)


@pytest.mark.asyncio
async def test_token_service_create_tokens_no_user(
    session: "conftest.AsyncSession",
) -> None:
    email = "test@email.com"
    auth_handler = jwt_auth.AuthJWT()

    with pytest.raises(exceptions.UnauthorizedError) as exc_info:
        await token_services.TokenService(session).create_tokens(
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
        await token_services.TokenService(session).create_tokens(
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
        await token_services.TokenService(session).create_tokens(
            email=user.email, password="plain_password", Authorize=auth_handler
        )
    assert exc_info.value.context == {"email": user.email}


@pytest.mark.asyncio
async def test_token_service_refresh_token(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(
        session,
        email="test@email.com",
        password="hashed_password",
        confirmed_email=True,
    )
    auth_handler = jwt_auth.AuthJWT()

    tokens = token_services.TokenService(session).refresh_token(
        user=user, Authorize=auth_handler
    )

    assert tokens.access_token
    assert tokens.token_type == "bearer"
    assert not auth.is_token_fresh(tokens.access_token)


def test_token_service_revoke_token(session: "conftest.AsyncSession") -> None:
    token = jwt_auth.AuthJWT().create_access_token("dummy_id")

    token_services.TokenService(session).revoke_token(token=token)


@freezegun.freeze_time("2022-02-06 13:30:00")
def test_token_service_revoke_token_already_expired(
    session: "conftest.AsyncSession",
) -> None:
    with freezegun.freeze_time("2021-02-05 13:30:00"):
        token = jwt_auth.AuthJWT().create_access_token("dummy_id")

    token_services.TokenService(session).revoke_token(token=token)


def test_token_service_revoke_token_invalid(session: "conftest.AsyncSession") -> None:
    token = "invalid_token"

    with pytest.raises(exceptions.BadRequestError) as exc_info:
        token_services.TokenService(session).revoke_token(token=token)
    assert exc_info.value.context == {"token": token}


@freezegun.freeze_time("2022-02-06 12:30:00")
def test_get_remaining_expiration() -> None:
    exp = int(datetime.datetime(2022, 2, 6, 13, 0, 0).timestamp())

    remaining_expiration = token_services.get_remaining_expiration(exp)

    assert remaining_expiration == 1800


@freezegun.freeze_time("2022-02-06 12:30:00")
def test_get_remaining_expiration_already_expired() -> None:
    exp = int(datetime.datetime(2022, 2, 6, 12, 0, 0).timestamp())

    remaining_expiration = token_services.get_remaining_expiration(exp)

    assert remaining_expiration == 0
