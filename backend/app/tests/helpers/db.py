import typing

if typing.TYPE_CHECKING:
    from app.models import base
    from app.tests import conftest

Entry = typing.TypeVar("Entry", bound="base.BaseModel")


async def save(session: "conftest.AsyncSession", entry: Entry) -> Entry:
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry
