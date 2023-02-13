import typing
import uuid

import pytest
import sqlmodel
from sqlalchemy import exc

from app.models import base as base_models
from app.models import helpers, pagination, sorting
from app.services import base as base_services
from app.tests.helpers import db

if typing.TYPE_CHECKING:
    from app.tests import conftest


class DummyModel(base_models.BaseModel, table=True):
    id: uuid.UUID = sqlmodel.Field(primary_key=True, default_factory=helpers.get_uuid4)
    name: str
    age: int
    city: str = "New York"


class DummyModelFilters(base_models.BaseModel):
    name: str | None = None
    age: int | None = None
    city: str | None = None


class DummyModelUpdate(base_models.BaseModel):
    name: str | None = None
    age: int | None = None
    city: str | None = None


async def create_entry(
    session: "conftest.AsyncSession", name: str, age: int
) -> DummyModel:
    entry = DummyModel(name=name, age=age)
    return await db.save(session, entry)


@pytest.mark.anyio
async def test_app_crud_create(session: "conftest.AsyncSession") -> None:
    model_create = DummyModel(name="Test Entry", age=25)
    created_entry = await base_services.AppCRUD(DummyModel, session).create(
        model_create
    )

    assert created_entry._sa_instance_state.expired  # pylint: disable=protected-access
    statement = sqlmodel.select(DummyModel).where(DummyModel.name == model_create.name)
    assert (await session.execute(statement)).scalar_one()


@pytest.mark.anyio
async def test_app_crud_create_refresh(session: "conftest.AsyncSession") -> None:
    model_create = DummyModel(name="Test Entry", age=25)
    created_entry = await base_services.AppCRUD(DummyModel, session).create(
        model_create, refresh=True
    )

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

    retrieved_entries = await base_services.AppCRUD(DummyModel, session).read_many(
        filters, pagination=pagination.Pagination()
    )

    assert retrieved_entries == [entry_1, entry_2, entry_3, entry_4]


@pytest.mark.anyio
async def test_app_crud_read_many_sort_asc(
    session: "conftest.AsyncSession",
) -> None:
    entry_1 = await create_entry(session, name="Test Entry 1", age=25)
    entry_2 = await create_entry(session, name="Test Entry 2", age=27)
    entry_3 = await create_entry(session, name="Test Entry 3", age=26)
    filters = DummyModelFilters()

    retrieved_entries = await base_services.AppCRUD(DummyModel, session).read_many(
        filters,
        sorting=sorting.Sorting(column=DummyModel.age, way=sorting.SortingWay.ASC),
    )

    assert retrieved_entries == [entry_1, entry_3, entry_2]


@pytest.mark.anyio
async def test_app_crud_read_many_order_by_desc(
    session: "conftest.AsyncSession",
) -> None:
    entry_1 = await create_entry(session, name="Test Entry 1", age=25)
    entry_2 = await create_entry(session, name="Test Entry 2", age=27)
    entry_3 = await create_entry(session, name="Test Entry 3", age=26)
    filters = DummyModelFilters()

    retrieved_entries = await base_services.AppCRUD(DummyModel, session).read_many(
        filters,
        sorting=sorting.Sorting(column=DummyModel.age, way=sorting.SortingWay.DESC),
    )

    assert retrieved_entries == [entry_2, entry_3, entry_1]


@pytest.mark.anyio
async def test_app_crud_read_many_pagination(session: "conftest.AsyncSession") -> None:
    await create_entry(session, name="Test Entry 1", age=25)
    entry_2 = await create_entry(session, name="Test Entry 2", age=25)
    entry_3 = await create_entry(session, name="Test Entry 3", age=25)
    await create_entry(session, name="Test Entry 4", age=25)
    filters = DummyModelFilters()

    retrieved_entries = await base_services.AppCRUD(DummyModel, session).read_many(
        filters, pagination=pagination.Pagination(offset=1, limit=2)
    )

    assert retrieved_entries == [entry_2, entry_3]


@pytest.mark.anyio
async def test_app_crud_read_one(session: "conftest.AsyncSession") -> None:
    await create_entry(session, name="Test Entry 1", age=25)
    await create_entry(session, name="Test Entry 2", age=27)
    entry = await create_entry(session, name="Test Entry 2", age=25)
    entry_filters = DummyModelFilters(name="Test Entry 2", age=25)

    retrieved_entry = await base_services.AppCRUD(DummyModel, session).read_one(
        entry_filters
    )

    assert retrieved_entry == entry


@pytest.mark.anyio
async def test_app_crud_update(session: "conftest.AsyncSession") -> None:
    await create_entry(session, name="Test Entry 1", age=25)
    entry = await create_entry(session, name="Test Entry 2", age=25)
    entry_update = DummyModelUpdate(name="Updated Entry", age=30)

    updated_entry = await base_services.AppCRUD(DummyModel, session).update(
        entry, entry_update
    )

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

    updated_entry = await base_services.AppCRUD(DummyModel, session).update(
        entry, entry_update, refresh=True
    )

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

    await base_services.AppCRUD(DummyModel, session).delete(entry)

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

    num_users = await base_services.AppCRUD(DummyModel, session).count(entry_filters)

    assert num_users == 3
