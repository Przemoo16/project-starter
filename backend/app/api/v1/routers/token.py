import typing

import fastapi
from fastapi import responses, status

from app.config import db
from app.exceptions.http import token as token_exceptions
from app.exceptions.http import user as user_exceptions
from app.models import token as token_models
from app.models import user as user_models
from app.services import token as token_services

router = fastapi.APIRouter()


@router.post(
    "/",
    response_model=token_models.Tokens,
    responses={
        **token_exceptions.InvalidCredentials().doc,
        **token_exceptions.InactiveUserError().doc,
    },
)
async def obtain_tokens(
    username: user_models.UserEmail = fastapi.Form(),
    password: user_models.UserPassword = fastapi.Form(),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    return await token_services.TokenService(session).obtain_tokens(username, password)


@router.post(
    "/refresh",
    response_model=token_models.AccessToken,
    responses={
        **token_exceptions.InactiveUserError().doc,
        **user_exceptions.UserNotFoundError().doc,
        **token_exceptions.InvalidTokenError().doc,
        **token_exceptions.RefreshTokenRequiredError().doc,
        **token_exceptions.RevokedTokenError().doc,
    },
)
async def refresh_token(
    token: token_models.Token = fastapi.Body(embed=True),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    return await token_services.TokenService(session).refresh_token(token)


@router.post(
    "/revoke",
    response_class=responses.Response,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        **token_exceptions.RevokedTokenError().doc,
        **token_exceptions.InvalidTokenError().doc,
    },
)
async def revoke_token(
    token: token_models.Token = fastapi.Body(embed=True),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    await token_services.TokenService(session).revoke_token(token)
