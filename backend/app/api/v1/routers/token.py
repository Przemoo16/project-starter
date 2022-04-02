import typing

import fastapi
from fastapi import status

from app.config import db, general
from app.exceptions.http import token as token_exceptions
from app.exceptions.http import user as user_exceptions
from app.models import token as token_models
from app.models import user as user_models
from app.services import token as token_services

settings = general.get_settings()

router = fastapi.APIRouter()


@router.post(
    "/",
    response_model=token_models.Tokens,
    responses={**token_exceptions.InvalidCredentials().doc},
)
async def obtain_tokens(
    username: user_models.UserEmail = fastapi.Form(...),
    password: user_models.UserPassword = fastapi.Form(...),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    return await token_services.TokenService(session).obtain_tokens(username, password)


@router.post(
    "/refresh",
    response_model=token_models.AccessToken,
    responses={
        **user_exceptions.UserNotFoundError().doc,
        **token_exceptions.InvalidTokenError().doc,
        **token_exceptions.RefreshTokenRequiredError().doc,
        **token_exceptions.RevokedTokenError().doc,
    },
)
async def refresh_token(
    token: token_models.Token = fastapi.Body(..., embed=True),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    return await token_services.TokenService(session).refresh_token(token)


@router.post(
    "/revoke",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**token_exceptions.InvalidTokenError().doc},
)
async def revoke_token(
    token: token_models.Token = fastapi.Body(..., embed=True),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    await token_services.TokenService(session).revoke_token(token)
