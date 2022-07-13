import typing

from fastapi import status
import fastapi_jwt_auth as jwt_auth
import pytest

from app.tests.helpers import response as response_helpers
from app.tests.helpers import user as user_helpers

if typing.TYPE_CHECKING:
    from app.tests import conftest

API_URL = "/api/v1"


@pytest.mark.anyio
async def test_create_user(async_client: "conftest.TestClient") -> None:
    email = "test@email.com"
    name = "Test User"
    request_data = {"email": email, "password": "plain_password", "name": name}

    response = await async_client.post(
        f"{API_URL}/users", json=request_data, follow_redirects=True
    )
    retrieved_user = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert retrieved_user == response_helpers.format_response(
        {
            "id": retrieved_user["id"],
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
async def test_update_me(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_active_user(session=session, name="Test User")
    new_name = "Updated Name"
    request_data = {"name": new_name}
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
            "name": new_name,
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
async def test_delete_me(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
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
async def test_change_my_password(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_active_user(
        session=session,
        password="$2b$12$q8JcpltDZkSLOdMuPyt/jORzExLKp9HsKgCoFJQ1IzzITc2/Pg42q",
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
        password="$2b$12$q8JcpltDZkSLOdMuPyt/jORzExLKp9HsKgCoFJQ1IzzITc2/Pg42q",
    )
    request_data = {"currentPassword": "plain_password", "newPassword": "new_password"}
    token = jwt_auth.AuthJWT().create_access_token(str(user.id))
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.post(
        f"{API_URL}/users/me/password", json=request_data, headers=headers
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_get_user(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_active_user(session=session)
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
async def test_confirm_email(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_user(session=session)
    request_data = {"key": str(user.confirmation_email_key)}

    response = await async_client.post(
        f"{API_URL}/users/email-confirmation", json=request_data
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content


@pytest.mark.anyio
async def test_reset_password(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_user(session=session)
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
async def test_reset_password_user_not_found(
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
async def test_set_password(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_user(session=session)
    request_data = {"key": str(user.reset_password_key), "password": "plain_password"}

    response = await async_client.post(
        f"{API_URL}/users/password/set", json=request_data
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content
