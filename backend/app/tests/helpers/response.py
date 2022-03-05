import typing

import orjson

from app.utils import converters


def format_response(response: typing.Any) -> typing.Any:
    return orjson.loads(converters.orjson_dumps(response))
