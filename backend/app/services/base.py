import typing

import sqlmodel

if typing.TYPE_CHECKING:
    from app.db import base

ModelInstance = typing.TypeVar("ModelInstance", bound=sqlmodel.SQLModel)


class DBSessionContext:
    def __init__(self, session: "base.AsyncSession"):
        self.session = session


class AppService(DBSessionContext):
    pass


class AppCRUD(DBSessionContext):
    async def save(self, instance: ModelInstance) -> ModelInstance:
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
