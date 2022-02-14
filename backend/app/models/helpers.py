import datetime
import typing
import uuid

import humps
import orjson


def get_utcnow() -> datetime.datetime:
    """
    Return datetime in UTC.

    It allows deferring initialization of the datetime module, thus mock it using
    freezegun.
    """
    return datetime.datetime.utcnow()


def generate_fixed_uuid() -> uuid.UUID:
    """
    Make sure that uuid does not start with a leading 0.

    TODO: Remove it when https://github.com/tiangolo/sqlmodel/issues/25 will be solved.
    """
    val = uuid.uuid4()
    while val.hex[0] == "0":
        val = uuid.uuid4()
    return val


def to_camel(text: str) -> str:
    return humps.camelize(text)


def orjson_dumps(
    data: typing.Any, *, default: typing.Callable[[typing.Any], typing.Any] | None
) -> str:
    return orjson.dumps(
        data, default=default, option=orjson.OPT_NAIVE_UTC | orjson.OPT_UTC_Z
    ).decode()
