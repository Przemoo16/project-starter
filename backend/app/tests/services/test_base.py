import typing
import uuid

import pytest
from sqlalchemy import exc
import sqlmodel

from app.models import base as base_models
from app.models import helpers, pagination
from app.services import base as base_services
from app.tests.helpers import db

if typing.TYPE_CHECKING:
    from app.tests import conftest


class DummyModel(base_models.BaseModel, table=True):
    id: uuid.UUID = sqlmodel.Field(
        primary_key=True, default_factory=helpers.generate_fixed_uuid, nullable=False
    )
    name: str
    age: int
    city: str = "New York"


class DummyModelFilters(base_models.PydanticBaseModel):
    name: str | None = None
    age: int | None = None
    city: str | None = None


class DummyModelUpdate(base_models.PydanticBaseModel):
    name: str | None = None
    age: int | None = None
    city: str | None = None


class DummyCRUD(base_services.AppCRUD):
    model: type[DummyModel] = DummyModel


async def create_entry(
    session: "conftest.AsyncSession", name: str, age: int
) -> DummyModel:
    entry = DummyModel(name=name, age=age)
    return await db.save(session, entry)


@pytest.mark.anyio
async def test_app_crud_create(session: "conftest.AsyncSession") -> None:
    model_create = DummyModel(name="Test Entry", age=25)
    created_entry = await DummyCRUD(session).create(model_create)

    assert created_entry._sa_instance_state.expired  # pylint: disable=protected-access
    statement = sqlmodel.select(DummyModel).where(DummyModel.name == model_create.name)
    assert (await session.execute(statement)).scalar_one()


@pytest.mark.anyio
async def test_app_crud_create_refresh(session: "conftest.AsyncSession") -> None:
    model_create = DummyModel(name="Test Entry", age=25)
    created_entry = await DummyCRUD(session).create(model_create, refresh=True)

    assert (
        not created_entry._sa_instance_state.expired  # pylint: disable=protected-access
    )
    assert created_entry.name == model_create.name
    assert created_entry.age == model_create.age
    statement = sqlmodel.select(DummyModel).where(DummyModel.name == created_entry.name)
    assert (await session.execute(statement)).scalar_one()


@pytest.mark.anyio
async def test_app_crud_read_many(session: "conftest.AsyncSession") -> None:
    entry_1 = await create_entry(session, name="Test Entry 1", age=25)
    entry_2 = await create_entry(session, name="Test Entry 2", age=25)
    entry_3 = await create_entry(session, name="Test Entry 3", age=25)
    entry_4 = await create_entry(session, name="Test Entry 4", age=25)
    filters = DummyModelFilters()

    retrieved_entries = await DummyCRUD(session).read_many(
        filters, pagination.Pagination()
    )

    assert retrieved_entries == [entry_1, entry_2, entry_3, entry_4]


@pytest.mark.anyio
async def test_app_crud_read_many_pagination(session: "conftest.AsyncSession") -> None:
    await create_entry(session, name="Test Entry 1", age=25)
    entry_2 = await create_entry(session, name="Test Entry 2", age=25)
    entry_3 = await create_entry(session, name="Test Entry 3", age=25)
    await create_entry(session, name="Test Entry 4", age=25)
    filters = DummyModelFilters()

    retrieved_entries = await DummyCRUD(session).read_many(
        filters, pagination.Pagination(offset=1, limit=2)
    )

    assert retrieved_entries == [entry_2, entry_3]


@pytest.mark.anyio
async def test_app_crud_read_one(session: "conftest.AsyncSession") -> None:
    await create_entry(session, name="Test Entry 1", age=25)
    await create_entry(session, name="Test Entry 2", age=27)
    entry = await create_entry(session, name="Test Entry 2", age=25)
    entry_filters = DummyModelFilters(name="Test Entry 2", age=25)

    retrieved_entry = await DummyCRUD(session).read_one(entry_filters)

    assert retrieved_entry == entry


@pytest.mark.anyio
async def test_app_crud_update(session: "conftest.AsyncSession") -> None:
    await create_entry(session, name="Test Entry 1", age=25)
    entry = await create_entry(session, name="Test Entry 2", age=25)
    entry_update = DummyModelUpdate(name="Updated Entry", age=30)

    updated_entry = await DummyCRUD(session).update(entry, entry_update)

    assert updated_entry._sa_instance_state.expired  # pylint: disable=protected-access
    statement = sqlmodel.select(DummyModel).where(
        DummyModel.name == entry_update.name,
        DummyModel.age == entry_update.age,
    )
    assert (await session.execute(statement)).scalar_one()


@pytest.mark.anyio
async def test_app_crud_update_refresh(session: "conftest.AsyncSession") -> None:
    await create_entry(session, name="Test Entry 1", age=25)
    entry = await create_entry(session, name="Test Entry 2", age=25)
    entry_update = DummyModelUpdate(name="Updated Entry", age=30)

    updated_entry = await DummyCRUD(session).update(entry, entry_update, refresh=True)

    assert (
        not updated_entry._sa_instance_state.expired  # pylint: disable=protected-access
    )
    assert updated_entry.name == entry_update.name
    assert updated_entry.age == entry_update.age
    statement = sqlmodel.select(DummyModel).where(
        DummyModel.name == entry_update.name,
        DummyModel.age == entry_update.age,
    )
    assert (await session.execute(statement)).scalar_one()


@pytest.mark.anyio
async def test_app_crud_delete(session: "conftest.AsyncSession") -> None:
    entry = await create_entry(session, name="Test Entry", age=25)

    await DummyCRUD(session).delete(entry)

    with pytest.raises(exc.NoResultFound):
        statement = sqlmodel.select(DummyModel).where(DummyModel.name == entry.name)
        (await session.execute(statement)).scalar_one()


@pytest.mark.anyio
async def test_app_crud_count(
    session: "conftest.AsyncSession",
) -> None:
    await create_entry(session, name="Test Entry 1", age=25)
    await create_entry(session, name="Test Entry 2", age=25)
    await create_entry(session, name="Test Entry 3", age=25)
    entry_filters = DummyModelFilters()

    num_users = await DummyCRUD(session).count(entry_filters)

    assert num_users == 3


@pytest.mark.anyio
async def test_build_where_statement(
    session: "conftest.AsyncSession",
) -> None:
    name = "Test Entry"
    age = 25
    entry_filters = DummyModelFilters(name=name, age=age)

    filters_statement = DummyCRUD(session).build_where_statement(
        sqlmodel.select(DummyModel), entry_filters
    )

    assert str(filters_statement) == str(
        sqlmodel.select(DummyModel)
        .where(DummyModel.name == name)
        .where(DummyModel.age == age)
    )
