import typing

import sqlalchemy
import sqlmodel

from app.models import pagination as pagination_models

if typing.TYPE_CHECKING:
    from sqlmodel.sql import expression

    from app.config import db
    from app.models import base


Entry = typing.TypeVar("Entry", bound="base.BaseModel")


class DBSessionContext:
    def __init__(self, session: "db.AsyncSession"):
        self.session = session


class AppService(DBSessionContext):
    pass


class AppCRUD(DBSessionContext):
    async def _create(
        self, model: typing.Type[Entry], entry: "base.BaseModel"
    ) -> Entry:
        db_entry = model.from_orm(entry)
        return await self._save(db_entry)

    async def _read_many(
        self,
        model: typing.Type[Entry],
        entry: "base.PydanticBaseModel",
        pagination: pagination_models.Pagination = pagination_models.Pagination(),
    ) -> list[Entry]:
        statement = _build_filters_statement(model, entry).offset(pagination.offset)
        if pagination.limit:
            statement = statement.limit(pagination.limit)
        return (await self.session.execute(statement)).scalars().all()

    async def _read_one(
        self, model: typing.Type[Entry], entry: "base.PydanticBaseModel"
    ) -> Entry:
        statement = _build_filters_statement(model, entry)
        return (await self.session.execute(statement)).scalar_one()

    async def _update(self, db_entry: Entry, entry: "base.PydanticBaseModel") -> Entry:
        data = entry.dict(exclude_unset=True)
        for key, value in data.items():
            setattr(db_entry, key, value)
        return await self._save(db_entry)

    async def _delete(self, entry: "base.BaseModel") -> None:
        await self.session.delete(entry)
        await self.session.commit()

    async def _count_all(
        self, model: typing.Type["base.BaseModel"]
    ) -> pagination_models.TotalResults:
        statement = sqlmodel.select([sqlalchemy.func.count()]).select_from(model)
        return (await self.session.execute(statement)).scalar_one()

    async def _save(self, entry: Entry) -> Entry:
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry


def _build_filters_statement(
    model: typing.Type[Entry], filters: "base.PydanticBaseModel"
) -> "expression.SelectOfScalar[Entry]":
    filters_data = filters.dict(exclude_unset=True)
    statement = sqlmodel.select(model)
    for attr, value in filters_data.items():
        statement = statement.where(getattr(model, attr) == value)
    return statement
