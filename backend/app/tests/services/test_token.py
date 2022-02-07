import datetime
import typing
from unittest import mock

import fastapi_jwt_auth as jwt_auth
import freezegun
from jose import jwt
import pytest

from app.config import general
from app.services import exceptions
from app.services import token as token_services
from app.tests.helpers import token as token_helpers
from app.tests.helpers import user as user_helpers

if typing.TYPE_CHECKING:
    from app.tests import conftest

settings = general.get_settings()


@pytest.mark.asyncio
@freezegun.freeze_time("2022-02-05 18:30:00")
async def test_token_service_create_tokens(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(
        session,
        email="test@email.com",
        password="$2b$12$q8JcpltDZkSLOdMuPyt/jORzExLKp9HsKgCoFJQ1IzzITc2/Pg42q",
        confirmed_email=True,
    )

    with freezegun.freeze_time("2022-02-05 18:00:00"):
        tokens = await token_services.TokenService(session).create_tokens(
            email=user.email, password="plain_password"
        )

    assert tokens.access_token
    assert tokens.refresh_token
    assert tokens.token_type == "bearer"
    assert token_helpers.is_token_fresh(tokens.access_token)
    assert user.last_login == datetime.datetime(2022, 2, 5, 18, 0, 0)


@pytest.mark.asyncio
async def test_token_service_create_tokens_no_user(
    session: "conftest.AsyncSession",
) -> None:
    email = "test@email.com"

    with pytest.raises(exceptions.UnauthorizedError) as exc_info:
        await token_services.TokenService(session).create_tokens(
            email=email, password="plain_password"
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
    )

    with pytest.raises(exceptions.UnauthorizedError) as exc_info:
        await token_services.TokenService(session).create_tokens(
            email=user.email, password="invalid_password"
        )
    assert exc_info.value.context == {"email": user.email}


@pytest.mark.asyncio
async def test_token_service_refresh_token(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(
        session, email="test@email.com", password="hashed_password"
    )
    token = jwt_auth.AuthJWT().create_access_token(str(user.id))

    token = await token_services.TokenService(session).refresh_token(token=token)

    assert token.access_token
    assert token.token_type == "bearer"
    assert not token_helpers.is_token_fresh(token.access_token)


@pytest.mark.asyncio
async def test_token_service_refresh_token_invalid(
    session: "conftest.AsyncSession",
) -> None:
    token = "invalid_token"

    with pytest.raises(exceptions.BadRequestError) as exc_info:
        await token_services.TokenService(session).refresh_token(token=token)
    assert exc_info.value.context == {"token": token}


@pytest.mark.asyncio
async def test_token_service_refresh_token_no_user(
    session: "conftest.AsyncSession",
) -> None:
    user_id = "0dd53909-fcda-4c72-afcd-1bf4886389f8"
    token = jwt_auth.AuthJWT().create_access_token(user_id)

    with pytest.raises(exceptions.NotFoundError) as exc_info:
        await token_services.TokenService(session).refresh_token(token=token)
    assert exc_info.value.context == {"token": token}


@mock.patch("app.services.token.jwt_db.setex")
def test_token_service_revoke_token(
    mocked_redis_setex: mock.MagicMock, session: "conftest.AsyncSession"
) -> None:
    token = jwt_auth.AuthJWT().create_access_token("dummy_id")

    token_services.TokenService(session).revoke_token(token=token)

    mocked_redis_setex.assert_called_once()


@mock.patch("app.services.token.jwt_db.setex")
@freezegun.freeze_time("2022-02-06 13:30:00")
def test_token_service_revoke_token_already_expired(
    mocked_redis_setex: mock.MagicMock,
    session: "conftest.AsyncSession",
) -> None:
    with freezegun.freeze_time("2021-02-05 13:30:00"):
        token = jwt_auth.AuthJWT().create_access_token("dummy_id")

    token_services.TokenService(session).revoke_token(token=token)

    mocked_redis_setex.assert_called_once()


def test_token_service_revoke_token_invalid(session: "conftest.AsyncSession") -> None:
    token = "invalid_token"

    with pytest.raises(exceptions.BadRequestError) as exc_info:
        token_services.TokenService(session).revoke_token(token=token)
    assert exc_info.value.context == {"token": token}


@mock.patch("app.services.token.jwt_db.set")
def test_token_service_revoke_token_missing_expiration(
    mocked_redis_set: mock.MagicMock, session: "conftest.AsyncSession"
) -> None:
    jti = "dummy_jti"
    token = jwt.encode(
        claims={"sub": "dummy_subject", "jti": jti},
        key=settings.AUTHJWT_SECRET_KEY,
        algorithm=settings.AUTHJWT_ALGORITHM,
    )

    token_services.TokenService(session).revoke_token(token=token)

    mocked_redis_set.assert_called_with(jti, "true")


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
