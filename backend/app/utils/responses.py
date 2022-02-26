import typing

from fastapi import responses as fastapi_responses

from app.utils import converters


class ORJSONResponse(fastapi_responses.JSONResponse):
    media_type = "application/json"

    @staticmethod
    def render(content: typing.Any) -> bytes:
        return converters.orjson_dumps(content)
