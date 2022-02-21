import typing

from fastapi import status
import fastapi_jwt_auth as jwt_auth
import pytest

from app.tests.helpers import user as user_helpers

if typing.TYPE_CHECKING:
    from app.tests import conftest

API_URL = "/api/v1"


@pytest.mark.asyncio
async def test_create_user(async_client: "conftest.TestClient") -> None:
    email = "test@example.com"
    request_data = {"email": email, "password": "plain_password"}

    response = await async_client.post(
        f"{API_URL}/users", json=request_data, follow_redirects=True
    )
    user = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert user == {"id": user["id"], "email": email, "isActive": False}


@pytest.mark.asyncio
async def test_get_user(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_active_user(session=session)
    user_id = str(user.id)
    token = jwt_auth.AuthJWT().create_access_token(user_id)
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.get(f"{API_URL}/users/{user_id}", headers=headers)
    retrieved_user = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert retrieved_user == {"id": user_id, "email": user.email, "isActive": True}


@pytest.mark.asyncio
async def test_get_user_stranger_request(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    owner = await user_helpers.create_active_user(
        session=session, email="test@example.com"
    )
    stranger = await user_helpers.create_active_user(
        session=session, email="test2@email.com"
    )
    token = jwt_auth.AuthJWT().create_access_token(str(stranger.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.get(f"{API_URL}/users/{owner.id}", headers=headers)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_update_user(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_active_user(
        session=session, email="test@example.com"
    )
    updated_email = "updated@email.com"
    request_data = {"email": updated_email}
    user_id = str(user.id)
    token = jwt_auth.AuthJWT().create_access_token(user_id)
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.patch(
        f"{API_URL}/users/{user_id}", json=request_data, headers=headers
    )
    retrieved_user = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert retrieved_user == {"id": user_id, "email": updated_email, "isActive": True}


@pytest.mark.asyncio
async def test_update_user_stranger_request(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    owner = await user_helpers.create_active_user(
        session=session, email="test@example.com"
    )
    stranger = await user_helpers.create_active_user(
        session=session, email="test2@email.com"
    )
    request_data = {"email": "updated@email.com"}
    token = jwt_auth.AuthJWT().create_access_token(str(stranger.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.patch(
        f"{API_URL}/users/{owner.id}", json=request_data, headers=headers
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_delete_user(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_active_user(session=session)
    token = jwt_auth.AuthJWT().create_access_token(str(user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.delete(f"{API_URL}/users/{user.id}", headers=headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_user_stranger_request(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    owner = await user_helpers.create_active_user(
        session=session, email="test@example.com"
    )
    stranger = await user_helpers.create_active_user(
        session=session, email="test2@email.com"
    )
    token = jwt_auth.AuthJWT().create_access_token(str(stranger.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.delete(f"{API_URL}/users/{owner.id}", headers=headers)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_confirm_email(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_user(session=session)
    request_data = {"key": str(user.confirmation_email_key)}

    response = await async_client.post(
        f"{API_URL}/users/email-confirmation", json=request_data
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_request_reset_password(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_active_user(session=session)
    request_data = {"email": user.email}

    response = await async_client.post(
        f"{API_URL}/users/password/reset-request", json=request_data
    )
    message = response.json()

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert message == {
        "message": "If provided valid email, the email to reset password has been sent"
    }


@pytest.mark.asyncio
async def test_reset_password(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_active_user(session=session)
    request_data = {"key": str(user.reset_password_key), "password": "plain_password"}

    response = await async_client.post(
        f"{API_URL}/users/password/reset", json=request_data
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
