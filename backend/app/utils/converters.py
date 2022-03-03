import typing
import uuid

import humps
import orjson
import pydantic


def to_uuid(text: str, version: int = 4) -> uuid.UUID:
    return uuid.UUID(text, version=version)


def to_pydantic_email(text: str) -> pydantic.EmailStr:
    return pydantic.EmailStr(text)


def to_camel(text: str) -> str:
    return humps.camelize(text)


def orjson_dumps(
    data: typing.Any,
    option: int | None = None,
    default: typing.Callable[[typing.Any], typing.Any] | None = None,
) -> bytes:
    # Cannot pass option=None directly to the dumps function
    if option:
        return orjson.dumps(data, option=option, default=default)
    return orjson.dumps(data, default=default)
