import datetime
import decimal
import typing
import uuid

from humps import main
import orjson
import pydantic


def to_uuid(text: str, version: int = 4) -> uuid.UUID:
    return uuid.UUID(text, version=version)


def to_pydantic_email(text: str) -> pydantic.EmailStr:
    return pydantic.EmailStr(text)


def to_camel(text: str) -> str:
    return main.camelize(text)


def _orjson_default(obj: typing.Any) -> typing.Any:
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError  # pragma: no cover


def orjson_dumps(
    data: typing.Any,
    option: int | None = None,
    default: typing.Callable[[typing.Any], typing.Any] | None = _orjson_default,
) -> bytes:
    # Cannot pass option=None directly to the dumps function
    if option:
        return orjson.dumps(data, option=option, default=default)
    return orjson.dumps(data, default=default)


def to_utc_timestamp(dt: datetime.datetime) -> float:
    """
    Convert datetime object to the UTC timestamp.

    The function returns the proper UTC timestamp from the datetime object.
    To obtain a proper UTC timestamp, the `timestamp()` function cannot be used as
    it treats naive datetime as local time and thus returns "invalid" (as not UTC)
    "POSIX" timestamp:
    https://docs.python.org/3/library/datetime.html#datetime.datetime.timestamp
    """
    return (dt - datetime.datetime(1970, 1, 1)).total_seconds()
