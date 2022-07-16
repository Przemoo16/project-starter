import datetime
import typing
from unittest import mock

import fastapi_jwt_auth as jwt_auth
import freezegun
from jose import jwt
import pytest

from app.config import general
from app.exceptions.http import token as token_exceptions
from app.exceptions.http import user as user_exceptions
from app.models import user as user_models
from app.services import token as token_services
from app.tests.helpers import token as token_helpers
from app.tests.helpers import user as user_helpers
from app.utils import converters

if typing.TYPE_CHECKING:
    from app.tests import conftest

settings = general.get_settings()


@pytest.mark.anyio
@freezegun.freeze_time("2022-02-05 18:30:00")
@mock.patch("app.services.user.UserService.get_active_user")
@mock.patch("app.services.user.UserService.update_user")
async def test_token_service_obtain_tokens(
    mock_update_user: mock.AsyncMock,
    mock_get_active_user: mock.AsyncMock,
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_active_user(
        session,
        email="test@email.com",
        password="$2b$12$q8JcpltDZkSLOdMuPyt/jORzExLKp9HsKgCoFJQ1IzzITc2/Pg42q",
    )
    mock_get_active_user.return_value = user

    with freezegun.freeze_time("2022-02-05 18:00:00"):
        tokens = await token_services.TokenService(session).obtain_tokens(
            email=user.email, password="plain_password"
        )

    assert tokens.access_token
    assert tokens.refresh_token
    assert tokens.token_type == "bearer"
    assert token_helpers.is_token_fresh(tokens.access_token)
    mock_update_user.assert_called_once_with(
        user, user_models.UserUpdate(last_login=datetime.datetime(2022, 2, 5, 18, 0, 0))
    )


@pytest.mark.anyio
@mock.patch(
    "app.services.user.UserService.get_active_user",
    side_effect=user_exceptions.UserNotFoundError,
)
async def test_token_service_obtain_tokens_user_not_found(
    _: mock.AsyncMock, session: "conftest.AsyncSession"
) -> None:
    email = converters.to_pydantic_email("test@email.com")

    with pytest.raises(token_exceptions.InvalidCredentialsError):
        await token_services.TokenService(session).obtain_tokens(
            email=email, password="plain_password"
        )


@pytest.mark.anyio
@mock.patch("app.services.user.UserService.get_active_user")
async def test_token_service_obtain_tokens_invalid_password(
    mock_get_active_user: mock.AsyncMock, session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_active_user(
        session,
        email="test@email.com",
        password="$2b$12$q8JcpltDZkSLOdMuPyt/jORzExLKp9HsKgCoFJQ1IzzITc2/Pg42q",
    )
    mock_get_active_user.return_value = user

    with pytest.raises(token_exceptions.InvalidCredentialsError):
        await token_services.TokenService(session).obtain_tokens(
            email=user.email, password="invalid_password"
        )


@pytest.mark.anyio
@mock.patch("app.services.user.UserService.get_active_user")
async def test_token_service_refresh_token(
    mock_get_active_user: mock.AsyncMock, session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_active_user(session)
    mock_get_active_user.return_value = user
    refresh_token = jwt_auth.AuthJWT().create_refresh_token(str(user.id))

    token = await token_services.TokenService(session).refresh_token(
        token=refresh_token
    )

    assert token.access_token
    assert token.token_type == "bearer"
    assert not token_helpers.is_token_fresh(token.access_token)


@pytest.mark.anyio
async def test_token_service_refresh_token_invalid(
    session: "conftest.AsyncSession",
) -> None:
    token = "invalid_token"

    with pytest.raises(token_exceptions.InvalidTokenError) as exc_info:
        await token_services.TokenService(session).refresh_token(token=token)
    assert exc_info.value.context == {"token": token}


@pytest.mark.anyio
async def test_token_service_refresh_no_refresh_type(
    session: "conftest.AsyncSession",
) -> None:
    user_id = "1dd53909-fcda-4c72-afcd-1bf4886389f8"
    token = jwt_auth.AuthJWT().create_access_token(user_id)

    with pytest.raises(token_exceptions.RefreshTokenRequiredError) as exc_info:
        await token_services.TokenService(session).refresh_token(token=token)
    assert exc_info.value.context == {"token": token}


@pytest.mark.anyio
@mock.patch("app.services.token.jwt_db.get", return_value="true")
async def test_token_service_refresh_revoked_token(
    _: mock.MagicMock, session: "conftest.AsyncSession"
) -> None:
    user_id = "1dd53909-fcda-4c72-afcd-1bf4886389f8"
    token = jwt_auth.AuthJWT().create_refresh_token(user_id)

    with pytest.raises(token_exceptions.RevokedTokenError) as exc_info:
        await token_services.TokenService(session).refresh_token(token=token)
    assert exc_info.value.context == {"token": token}


@pytest.mark.anyio
@mock.patch("app.services.user.UserService.get_user")
@mock.patch("app.services.token.jwt_db.setex")
async def test_token_service_revoke_access_token(
    mock_redis_setex: mock.MagicMock,
    _: mock.AsyncMock,
    session: "conftest.AsyncSession",
) -> None:
    user_id = "1dd53909-fcda-4c72-afcd-1bf4886389f8"
    token = jwt_auth.AuthJWT().create_access_token(user_id)

    await token_services.TokenService(session).revoke_token(token=token)

    mock_redis_setex.assert_called_once()


@pytest.mark.anyio
@mock.patch("app.services.user.UserService.get_user")
@mock.patch("app.services.token.jwt_db.setex")
async def test_token_service_revoke_refresh_token(
    mock_redis_setex: mock.MagicMock,
    _: mock.AsyncMock,
    session: "conftest.AsyncSession",
) -> None:
    user_id = "1dd53909-fcda-4c72-afcd-1bf4886389f8"
    token = jwt_auth.AuthJWT().create_refresh_token(user_id)

    await token_services.TokenService(session).revoke_token(token=token)

    mock_redis_setex.assert_called_once()


@pytest.mark.anyio
async def test_token_service_revoke_token_invalid(
    session: "conftest.AsyncSession",
) -> None:
    token = "invalid_token"

    with pytest.raises(token_exceptions.InvalidTokenError) as exc_info:
        await token_services.TokenService(session).revoke_token(token=token)
    assert exc_info.value.context == {"token": token}


@pytest.mark.anyio
@freezegun.freeze_time("2022-02-06 13:30:00")
async def test_token_service_revoke_token_already_expired(
    session: "conftest.AsyncSession",
) -> None:
    user_id = "1dd53909-fcda-4c72-afcd-1bf4886389f8"
    with freezegun.freeze_time("2021-02-05 13:30:00"):
        token = jwt_auth.AuthJWT().create_access_token(user_id)

    with pytest.raises(token_exceptions.InvalidTokenError) as exc_info:
        await token_services.TokenService(session).revoke_token(token=token)
    assert exc_info.value.context == {"token": token}


@pytest.mark.anyio
@mock.patch("app.services.token.jwt_db.get", return_value="true")
async def test_token_service_revoke_already_revoked_token(
    _: mock.MagicMock, session: "conftest.AsyncSession"
) -> None:
    user_id = "1dd53909-fcda-4c72-afcd-1bf4886389f8"
    token = jwt_auth.AuthJWT().create_access_token(user_id)

    with pytest.raises(token_exceptions.RevokedTokenError) as exc_info:
        await token_services.TokenService(session).revoke_token(token=token)
    assert exc_info.value.context == {"token": token}


@pytest.mark.anyio
@mock.patch("app.services.user.UserService.get_user")
@mock.patch("app.services.token.jwt_db.set")
async def test_token_service_revoke_token_missing_expiration(
    mock_redis_set: mock.MagicMock, _: mock.AsyncMock, session: "conftest.AsyncSession"
) -> None:
    jti = "dummy_jti"
    user_id = "1dd53909-fcda-4c72-afcd-1bf4886389f8"
    token = jwt.encode(
        claims={"sub": user_id, "jti": jti},
        key=settings.AUTHJWT_SECRET_KEY,
        algorithm=settings.AUTHJWT_ALGORITHM,
    )

    await token_services.TokenService(session).revoke_token(token=token)

    mock_redis_set.assert_called_with(jti, "true")


@freezegun.freeze_time("2022-02-06 12:30:00")
def test_get_remaining_expiration() -> None:
    exp = int(converters.to_utc_timestamp(datetime.datetime(2022, 2, 6, 13, 0, 0)))

    remaining_expiration = (
        token_services._get_remaining_expiration(  # pylint: disable=protected-access
            exp
        )
    )

    assert remaining_expiration == 1800


@freezegun.freeze_time("2022-02-06 12:30:00")
def test_get_remaining_expiration_already_expired() -> None:
    exp = int(converters.to_utc_timestamp(datetime.datetime(2022, 2, 6, 12, 0, 0)))

    remaining_expiration = (
        token_services._get_remaining_expiration(  # pylint: disable=protected-access
            exp
        )
    )

    assert remaining_expiration == 1
