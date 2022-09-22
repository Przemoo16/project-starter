import datetime
import typing
import uuid

from app.utils import converters


def get_utcnow() -> datetime.datetime:
    """
    Return datetime in UTC.

    It allows deferring initialization of the datetime module, thus mock it using
    freezegun.
    """
    return datetime.datetime.utcnow()


def get_uuid4() -> uuid.UUID:
    """
    Generate a random UUID.

    It allows deferring initialization of the uuid module, thus mock it in testing.
    """
    return uuid.uuid4()


def orjson_dumps(
    data: typing.Any, *, default: typing.Callable[[typing.Any], typing.Any] | None
) -> str:
    return converters.orjson_dumps(data, default=default).decode()
