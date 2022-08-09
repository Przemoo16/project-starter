import typing
from unittest import mock

from fastapi import status
import fastapi_jwt_auth as jwt_auth
import pytest

from app.exceptions.http import user as user_exceptions
from app.tests.helpers import response as response_helpers
from app.tests.helpers import user as user_helpers

if typing.TYPE_CHECKING:
    from app.tests import conftest

API_URL = "/api/v1"


@pytest.mark.anyio
@mock.patch("app.services.user.UserService.create_user")
async def test_create_user(
    mock_create_user: mock.AsyncMock,
    async_client: "conftest.TestClient",
    session: "conftest.AsyncSession",
) -> None:
    email = "test@email.com"
    name = "Test User"
    user = await user_helpers.create_active_user(
        session=session, email=email, name=name
    )
    mock_create_user.return_value = user
    request_data = {"email": email, "password": "plain_password", "name": name}

    response = await async_client.post(
        f"{API_URL}/users", json=request_data, follow_redirects=True
    )
    retrieved_user = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert retrieved_user == response_helpers.format_response(
        {
            "id": str(user.id),
            "email": email,
            "name": name,
        }
    )


@pytest.mark.anyio
async def test_get_me(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_active_user(session=session)
    token = jwt_auth.AuthJWT().create_access_token(str(user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.get(f"{API_URL}/users/me", headers=headers)
    retrieved_user = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert retrieved_user == response_helpers.format_response(
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        }
    )


@pytest.mark.anyio
async def test_get_me_inactive_user(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_user(session=session)
    token = jwt_auth.AuthJWT().create_access_token(str(user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.get(f"{API_URL}/users/me", headers=headers)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
@mock.patch("app.services.user.UserService.update_user")
async def test_update_me(
    mock_update_user: mock.AsyncMock,
    async_client: "conftest.TestClient",
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_active_user(session=session, name="Test User")
    mock_update_user.return_value = user
    request_data = {"name": "Updated Name"}
    token = jwt_auth.AuthJWT().create_access_token(str(user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.patch(
        f"{API_URL}/users/me", json=request_data, headers=headers
    )
    retrieved_user = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert retrieved_user == response_helpers.format_response(
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        }
    )


@pytest.mark.anyio
async def test_update_me_inactive_user(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_user(session=session)
    request_data = {"name": "Updated Name"}
    token = jwt_auth.AuthJWT().create_access_token(str(user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.patch(
        f"{API_URL}/users/me", json=request_data, headers=headers
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
@mock.patch("app.services.user.UserService.delete_user", return_value=None)
async def test_delete_me(
    _: mock.AsyncMock,
    async_client: "conftest.TestClient",
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_active_user(session=session)
    token = jwt_auth.AuthJWT().create_access_token(str(user.id), fresh=True)
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.delete(f"{API_URL}/users/me", headers=headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content


@pytest.mark.anyio
async def test_delete_me_inactive_user(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_user(session=session)
    token = jwt_auth.AuthJWT().create_access_token(str(user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.delete(f"{API_URL}/users/me", headers=headers)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_delete_me_no_fresh_token(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_active_user(session=session)
    token = jwt_auth.AuthJWT().create_access_token(str(user.id), fresh=False)
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.delete(f"{API_URL}/users/me", headers=headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
@mock.patch("app.services.user.UserService.change_password", return_value=None)
async def test_change_my_password(
    _: mock.AsyncMock,
    async_client: "conftest.TestClient",
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_active_user(
        session=session,
        password=(
            "$argon2id$v=19$m=65536,t=3,p=4$AoDw3nvPea/VGiNkzPn/Pw$grh02g7mdXN47S8kSt2P"
            "Vmv52AAt7wisY63TPS80qMo"
        ),
    )
    request_data = {"currentPassword": "plain_password", "newPassword": "new_password"}
    token = jwt_auth.AuthJWT().create_access_token(str(user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.post(
        f"{API_URL}/users/me/password", json=request_data, headers=headers
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content


@pytest.mark.anyio
async def test_change_my_password_inactive_user(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_user(
        session=session,
        password=(
            "$argon2id$v=19$m=65536,t=3,p=4$AoDw3nvPea/VGiNkzPn/Pw$grh02g7mdXN47S8kSt2P"
            "Vmv52AAt7wisY63TPS80qMo"
        ),
    )
    request_data = {"currentPassword": "plain_password", "newPassword": "new_password"}
    token = jwt_auth.AuthJWT().create_access_token(str(user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.post(
        f"{API_URL}/users/me/password", json=request_data, headers=headers
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
@mock.patch("app.services.user.UserService.get_user")
async def test_get_user(
    mock_get_user: mock.AsyncMock,
    async_client: "conftest.TestClient",
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_active_user(session=session)
    mock_get_user.return_value = user
    token = jwt_auth.AuthJWT().create_access_token(str(user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.get(f"{API_URL}/users/{user.id}", headers=headers)
    retrieved_user = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert retrieved_user == response_helpers.format_response(
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        }
    )


@pytest.mark.anyio
async def test_get_user_inactive_user(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_user(session=session)
    token = jwt_auth.AuthJWT().create_access_token(str(user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.get(f"{API_URL}/users/{user.id}", headers=headers)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
@mock.patch("app.services.user.UserService.get_user")
@mock.patch("app.services.user.UserService.confirm_email", return_value=None)
async def test_confirm_email(
    _: mock.AsyncMock,
    mock_get_user: mock.AsyncMock,
    async_client: "conftest.TestClient",
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_user(session=session)
    mock_get_user.return_value = user
    request_data = {"token": str(user.email_confirmation_token)}

    response = await async_client.post(
        f"{API_URL}/users/email-confirmation", json=request_data
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content


@pytest.mark.anyio
@mock.patch("app.services.user.UserService.get_active_user")
@mock.patch("app.services.user.UserService.reset_password", return_value=None)
async def test_reset_password(
    _: mock.AsyncMock,
    mock_get_active_user: mock.AsyncMock,
    async_client: "conftest.TestClient",
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_active_user(session=session)
    mock_get_active_user.return_value = user
    request_data = {"email": user.email}

    response = await async_client.post(
        f"{API_URL}/users/password/reset", json=request_data
    )
    message = response.json()

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert message == response_helpers.format_response(
        {
            "message": (
                "If provided valid email, the email to reset password has been sent"
            )
        }
    )


@pytest.mark.anyio
@mock.patch(
    "app.services.user.UserService.get_active_user",
    side_effect=user_exceptions.UserNotFoundError,
)
@mock.patch("app.services.user.UserService.reset_password", return_value=None)
async def test_reset_password_user_not_found(  # pylint: disable=unused-argument
    mock_reset_password: mock.AsyncMock,
    mock_get_active_user: mock.AsyncMock,
    async_client: "conftest.TestClient",
) -> None:
    request_data = {"email": "test@email.com"}

    response = await async_client.post(
        f"{API_URL}/users/password/reset", json=request_data
    )
    message = response.json()

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert message == response_helpers.format_response(
        {
            "message": (
                "If provided valid email, the email to reset password has been sent"
            )
        }
    )


@pytest.mark.anyio
@mock.patch(
    "app.services.user.UserService.get_active_user",
    side_effect=user_exceptions.InactiveUserError,
)
@mock.patch("app.services.user.UserService.reset_password", return_value=None)
async def test_reset_password_inactive_user(  # pylint: disable=unused-argument
    mock_reset_password: mock.AsyncMock,
    mock_get_active_user: mock.AsyncMock,
    async_client: "conftest.TestClient",
) -> None:
    request_data = {"email": "test@email.com"}

    response = await async_client.post(
        f"{API_URL}/users/password/reset", json=request_data
    )
    message = response.json()

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert message == response_helpers.format_response(
        {
            "message": (
                "If provided valid email, the email to reset password has been sent"
            )
        }
    )


@pytest.mark.anyio
@mock.patch("app.services.user.UserService.set_password", return_value=None)
async def test_set_password(
    _: mock.AsyncMock,
    async_client: "conftest.TestClient",
) -> None:
    token = "1dd53909-fcda-4c72-afcd-1bf4886389f8"

    request_data = {
        "token": token,
        "password": "plain_password",
    }

    response = await async_client.post(
        f"{API_URL}/users/password/set", json=request_data
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content
