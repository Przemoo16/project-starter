import typing

import fastapi
from fastapi import responses, status

from app.config import db
from app.exceptions.http import auth as auth_exceptions
from app.exceptions.http import user as user_exceptions
from app.models import auth as auth_models
from app.models import user as user_models
from app.services import auth as auth_services

router = fastapi.APIRouter()


@router.post(
    "/",
    response_model=auth_models.AuthTokens,
    responses={
        **auth_exceptions.InvalidCredentialsError().doc,
        **user_exceptions.InactiveUserError().doc,
    },
)
async def obtain_tokens(
    username: user_models.UserEmail = fastapi.Form(),
    password: user_models.UserPassword = fastapi.Form(),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    return await auth_services.AuthService(session).obtain_tokens(username, password)


@router.post(
    "/refresh",
    response_model=auth_models.AccessToken,
    responses={
        **user_exceptions.InactiveUserError().doc,
        **user_exceptions.UserNotFoundError().doc,
        **auth_exceptions.InvalidTokenError().doc,
        **auth_exceptions.RefreshTokenRequiredError().doc,
        **auth_exceptions.RevokedTokenError().doc,
    },
)
async def refresh_token(
    token: auth_models.AuthToken = fastapi.Body(embed=True),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    return await auth_services.AuthService(session).refresh_token(token)


@router.post(
    "/revoke",
    response_class=responses.Response,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        **auth_exceptions.RevokedTokenError().doc,
        **auth_exceptions.InvalidTokenError().doc,
    },
)
async def revoke_token(
    token: auth_models.AuthToken = fastapi.Body(embed=True),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    await auth_services.AuthService(session).revoke_token(token)
