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


class TestModel(base_models.BaseModel, table=True):
    id: uuid.UUID = sqlmodel.Field(
        primary_key=True, default_factory=helpers.generate_fixed_uuid, nullable=False
    )
    name: str
    age: int
    city: str = "New York"


class TestModelFilters(base_models.PydanticBaseModel):
    name: str | None = None
    age: int | None = None
    city: str | None = None


class TestModelUpdate(base_models.PydanticBaseModel):
    name: str | None = None
    age: int | None = None
    city: str | None = None


class TestCRUD(base_services.AppCRUD):
    model = TestModel


async def create_entry(
    session: "conftest.AsyncSession", name: str, age: int
) -> TestModel:
    entry = TestModel(name=name, age=age)
    return await db.save(session, entry)


@pytest.mark.anyio
async def test_app_crud_create(session: "conftest.AsyncSession") -> None:
    model_create = TestModel(name="Test Entry", age=25)
    created_entry = await TestCRUD(session).create(model_create)

    assert created_entry.name == model_create.name
    assert created_entry.age == model_create.age
    statement = sqlmodel.select(TestModel).where(TestModel.name == created_entry.name)
    assert (await session.execute(statement)).scalar_one()


@pytest.mark.anyio
async def test_app_crud_read_many(session: "conftest.AsyncSession") -> None:
    entry_1 = await create_entry(session, name="Test Entry 1", age=25)
    entry_2 = await create_entry(session, name="Test Entry 2", age=25)
    entry_3 = await create_entry(session, name="Test Entry 3", age=25)
    entry_4 = await create_entry(session, name="Test Entry 4", age=25)
    filters = TestModelFilters()

    retrieved_entries = await TestCRUD(session).read_many(
        filters, pagination.Pagination()
    )

    assert retrieved_entries == [entry_1, entry_2, entry_3, entry_4]


@pytest.mark.anyio
async def test_app_crud_read_many_pagination(session: "conftest.AsyncSession") -> None:
    await create_entry(session, name="Test Entry 1", age=25)
    entry_2 = await create_entry(session, name="Test Entry 2", age=25)
    entry_3 = await create_entry(session, name="Test Entry 3", age=25)
    await create_entry(session, name="Test Entry 4", age=25)
    filters = TestModelFilters()

    retrieved_entries = await TestCRUD(session).read_many(
        filters, pagination.Pagination(offset=1, limit=2)
    )

    assert retrieved_entries == [entry_2, entry_3]


@pytest.mark.anyio
async def test_app_crud_read_one(session: "conftest.AsyncSession") -> None:
    await create_entry(session, name="Test Entry 1", age=25)
    await create_entry(session, name="Test Entry 2", age=27)
    entry = await create_entry(session, name="Test Entry 2", age=25)
    entry_filters = TestModelFilters(name="Test Entry 2", age=25)

    retrieved_entry = await TestCRUD(session).read_one(entry_filters)

    assert retrieved_entry == entry


@pytest.mark.anyio
async def test_app_crud_update(session: "conftest.AsyncSession") -> None:
    await create_entry(session, name="Test Entry 1", age=25)
    entry = await create_entry(session, name="Test Entry 2", age=25)
    entry_update = TestModelUpdate(name="Updated Entry", age=30)

    updated_entry = await TestCRUD(session).update(entry, entry_update)

    assert updated_entry.name == entry_update.name
    assert updated_entry.age == entry_update.age
    statement = sqlmodel.select(TestModel).where(
        TestModel.name == entry_update.name,
        TestModel.age == entry_update.age,
    )
    assert (await session.execute(statement)).scalar_one()


@pytest.mark.anyio
async def test_app_crud_delete(session: "conftest.AsyncSession") -> None:
    entry = await create_entry(session, name="Test Entry", age=25)

    await TestCRUD(session).delete(entry)

    with pytest.raises(exc.NoResultFound):
        statement = sqlmodel.select(TestModel).where(TestModel.name == entry.name)
        (await session.execute(statement)).scalar_one()


@pytest.mark.anyio
async def test_app_crud_count(
    session: "conftest.AsyncSession",
) -> None:
    await create_entry(session, name="Test Entry 1", age=25)
    await create_entry(session, name="Test Entry 2", age=25)
    await create_entry(session, name="Test Entry 3", age=25)
    entry_filters = TestModelFilters()

    num_users = await TestCRUD(session).count(entry_filters)

    assert num_users == 3


@pytest.mark.anyio
async def test_build_where_statement(
    session: "conftest.AsyncSession",
) -> None:
    name = "Test Entry"
    age = 25
    entry_filters = TestModelFilters(name=name, age=age)

    filters_statement = TestCRUD(session).build_where_statement(
        sqlmodel.select(TestModel), entry_filters
    )

    assert str(filters_statement) == str(
        sqlmodel.select(TestModel)
        .where(TestModel.name == name)
        .where(TestModel.age == age)
    )
