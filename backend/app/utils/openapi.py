import typing

from fastapi.openapi import utils

if typing.TYPE_CHECKING:
    import fastapi


Schema: typing.TypeAlias = dict[str, typing.Any]


def generate_openapi_schema(app: "fastapi.FastAPI") -> typing.Callable[[], Schema]:
    def generate_schema() -> Schema:  # pragma: no cover
        if app.openapi_schema:
            return app.openapi_schema
        utils.validation_error_response_definition = {
            "title": "HTTPValidationError",
            "type": "object",
            "properties": {
                "detail": {
                    "title": "Context",
                    "type": "string",
                },
                "context": {
                    "title": "Detail",
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/ValidationError"},
                },
            },
        }
        openapi_schema = utils.get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    return generate_schema
