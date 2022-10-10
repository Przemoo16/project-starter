import datetime
import typing

from sqlalchemy import exc

from app.exceptions.http import reset_password as reset_password_exceptions
from app.models import reset_password as reset_password_models
from app.models import sorting as sorting_models
from app.services import base

if typing.TYPE_CHECKING:
    from app.config import db


class ResetPasswordService:
    def __init__(self, session: "db.AsyncSession"):
        self.crud = base.AppCRUD(reset_password_models.ResetPasswordToken, session)

    async def create_token(
        self, token: reset_password_models.ResetPasswordTokenCreate
    ) -> reset_password_models.ResetPasswordToken:
        sorting = sorting_models.Sorting(
            column=reset_password_models.ResetPasswordToken.expire_at,
            way=sorting_models.SortingWay.DESC,
        )
        sorted_tokens = await self.crud.read_many(
            reset_password_models.ResetPasswordTokenFilters(user_id=token.user_id),
            sorting=sorting,
        )
        if sorted_tokens:
            await self.force_to_expire(sorted_tokens[0])
        return await self.crud.create(token, refresh=True)

    async def get_token(
        self, filters: reset_password_models.ResetPasswordTokenFilters
    ) -> reset_password_models.ResetPasswordToken:
        try:
            return await self.crud.read_one(filters)
        except exc.NoResultFound as e:
            filters_data = filters.dict(exclude_unset=True)
            raise reset_password_exceptions.ResetPasswordTokenNotFoundError(
                context=filters_data
            ) from e

    async def get_valid_token(
        self, filters: reset_password_models.ResetPasswordTokenFilters
    ) -> reset_password_models.ResetPasswordToken:
        token = await self.get_token(filters)
        if token.is_expired:
            raise reset_password_exceptions.ResetPasswordTokenExpiredError(
                context={"id": token.id}
            )
        return token

    async def force_to_expire(
        self, token: reset_password_models.ResetPasswordToken
    ) -> None:
        if token.is_expired:
            return
        await self.crud.update(
            token,
            reset_password_models.ResetPasswordTokenUpdate(
                expire_at=datetime.datetime.utcnow()
            ),
        )
