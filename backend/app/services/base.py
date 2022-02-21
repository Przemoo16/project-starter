import typing

import sqlmodel

if typing.TYPE_CHECKING:
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

    async def _read(
        self, model: typing.Type[Entry], entry: "base.PydanticBaseModel"
    ) -> Entry:
        data = entry.dict(exclude_unset=True)
        read_statement = sqlmodel.select(model)
        for attr, value in data.items():
            read_statement = read_statement.where(getattr(model, attr) == value)
        result = await self.session.execute(read_statement)
        return result.scalar_one()

    async def _update(self, db_entry: Entry, entry: "base.PydanticBaseModel") -> Entry:
        data = entry.dict(exclude_unset=True)
        for key, value in data.items():
            setattr(db_entry, key, value)
        return await self._save(db_entry)

    async def _delete(self, entry: "base.BaseModel") -> None:
        await self.session.delete(entry)
        await self.session.commit()

    async def _save(self, entry: Entry) -> Entry:
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry
