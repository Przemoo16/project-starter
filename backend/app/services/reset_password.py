import datetime
import typing

from sqlalchemy import exc
import sqlmodel

from app.exceptions.http import reset_password as reset_password_exceptions
from app.models import reset_password as reset_password_models
from app.services import base

if typing.TYPE_CHECKING:
    from app.config import db


class ResetPasswordService:
    def __init__(self, session: "db.AsyncSession"):
        self.crud = ResetPasswordCRUD(session)

    async def create_token(
        self, token: reset_password_models.ResetPasswordTokenCreate
    ) -> reset_password_models.ResetPasswordToken:
        if latest_token := await self.crud.read_latest(
            reset_password_models.ResetPasswordTokenFilters(user_id=token.user_id)
        ):
            await self.force_to_expire(latest_token)
        return await self.crud.create(token)

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
        await self.crud.update(
            token,
            reset_password_models.ResetPasswordTokenUpdate(
                expire_at=datetime.datetime.utcnow()
            ),
        )


class ResetPasswordCRUD(base.AppCRUD):
    model = reset_password_models.ResetPasswordToken

    async def read_latest(
        self, filters: reset_password_models.ResetPasswordTokenFilters
    ) -> reset_password_models.ResetPasswordToken | None:
        where_statement = self.build_where_statement(
            sqlmodel.select(self.model), filters
        )
        order_by_statement = where_statement.order_by(
            sqlmodel.col(self.model.expire_at).desc()  # pylint: disable=no-member
        )
        return (await self.session.execute(order_by_statement)).scalar()
