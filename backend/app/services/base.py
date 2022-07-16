import typing

import sqlmodel
from sqlmodel.sql import expression

from app.models import base
from app.models import pagination as pagination_models

if typing.TYPE_CHECKING:

    from app.config import db


class DBSessionContext:
    def __init__(self, session: "db.AsyncSession"):
        self.session = session


class AppService(DBSessionContext):
    pass


class AppCRUD(DBSessionContext):  # TODO: Fix typing
    model = base.BaseModel

    async def create(self, entry: base.BaseModel) -> typing.Any:
        db_entry = self.model.from_orm(entry)
        return await self._save(db_entry)

    async def read_many(
        self,
        entry: base.PydanticBaseModel,
        pagination: pagination_models.Pagination = pagination_models.Pagination(),
    ) -> list[typing.Any]:
        statement = self.build_where_statement(
            sqlmodel.select(self.model), entry
        ).offset(pagination.offset)
        if pagination.limit:
            statement = statement.limit(pagination.limit)
        return (await self.session.execute(statement)).scalars().all()

    async def read_one(self, entry: base.PydanticBaseModel) -> typing.Any:
        statement = self.build_where_statement(sqlmodel.select(self.model), entry)
        return (await self.session.execute(statement)).scalar_one()

    async def update(
        self, db_entry: base.BaseModel, entry: base.PydanticBaseModel
    ) -> typing.Any:
        data = entry.dict(exclude_unset=True)
        for key, value in data.items():
            setattr(db_entry, key, value)
        return await self._save(db_entry)

    async def delete(self, entry: base.BaseModel) -> None:
        await self.session.delete(entry)
        await self.session.commit()

    async def count(
        self, entry: base.PydanticBaseModel
    ) -> pagination_models.TotalResults:
        select_statament: expression.SelectOfScalar[typing.Any] = sqlmodel.select(
            [sqlmodel.func.count()]
        ).select_from(self.model)
        where_statement = self.build_where_statement(select_statament, entry)
        return (await self.session.execute(where_statement)).scalar_one()

    async def _save(self, entry: base.BaseModel) -> typing.Any:
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry

    def build_where_statement(
        self,
        statement: expression.SelectOfScalar[typing.Any],
        filters: base.PydanticBaseModel,
    ) -> expression.SelectOfScalar[typing.Any]:
        filters_data = filters.dict(exclude_unset=True)
        for attr, value in filters_data.items():
            statement = statement.where(getattr(self.model, attr) == value)
        return statement
