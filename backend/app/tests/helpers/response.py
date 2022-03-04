import decimal
import typing

import orjson

from app.utils import converters


def _orjson_default(obj: typing.Any) -> typing.Any:
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


def format_response(response: typing.Any) -> typing.Any:
    return orjson.loads(converters.orjson_dumps(response, default=_orjson_default))
