import typing
import uuid

import humps
import orjson
import pydantic

DEFAULT_ORJSON_OPTION = orjson.OPT_NAIVE_UTC | orjson.OPT_UTC_Z


def to_uuid(text: str, version: int = 4) -> uuid.UUID:
    return uuid.UUID(text, version=version)


def to_pydantic_email(text: str) -> pydantic.EmailStr:
    return pydantic.EmailStr(text)


def to_camel(text: str) -> str:
    return humps.camelize(text)


def orjson_dumps(
    data: typing.Any,
    option: int | None = DEFAULT_ORJSON_OPTION,
    default: typing.Callable[[typing.Any], typing.Any] | None = None,
) -> bytes:
    return orjson.dumps(data, option=option, default=default)
