import typing

import fastapi
from fastapi import exceptions as fastapi_exceptions
from fastapi import responses, status
from fastapi_jwt_auth import exceptions as jwt_exceptions
from starlette import exceptions as starlette_exceptions

from app.exceptions import base


def init_handlers(app: fastapi.FastAPI) -> None:  # pragma: no cover
    @app.exception_handler(starlette_exceptions.HTTPException)
    async def custom_http_exception_handler(
        request: fastapi.Request, exc: starlette_exceptions.HTTPException
    ) -> responses.ORJSONResponse:
        return http_exception_handler(request, exc)

    @app.exception_handler(fastapi_exceptions.RequestValidationError)
    async def custom_request_validation_exception_handler(
        request: fastapi.Request, exc: fastapi_exceptions.RequestValidationError
    ) -> responses.ORJSONResponse:
        return request_validation_exception_handler(request, exc)

    @app.exception_handler(jwt_exceptions.AuthJWTException)
    async def custom_authjwt_exception_handler(
        request: fastapi.Request, exc: jwt_exceptions.AuthJWTException
    ) -> responses.ORJSONResponse:
        return authjwt_exception_handler(request, exc)

    @app.exception_handler(base.ResourceException)
    async def custom_resource_exception_handler(
        request: fastapi.Request, exc: base.ResourceException
    ) -> responses.ORJSONResponse:
        return resource_exception_handler(request, exc)


def http_exception_handler(
    _: fastapi.Request, exc: starlette_exceptions.HTTPException
) -> responses.ORJSONResponse:
    return responses.ORJSONResponse(
        status_code=exc.status_code, content=_build_content(detail=exc.detail)
    )


def request_validation_exception_handler(
    _: fastapi.Request, exc: fastapi_exceptions.RequestValidationError
) -> responses.ORJSONResponse:
    return responses.ORJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_build_content(detail="Invalid data", context=exc.errors()),
    )


def authjwt_exception_handler(
    _: fastapi.Request, exc: jwt_exceptions.AuthJWTException
) -> responses.ORJSONResponse:
    return responses.ORJSONResponse(
        status_code=exc.status_code, content=_build_content(detail=exc.message)
    )


def resource_exception_handler(
    _: fastapi.Request, exc: base.ResourceException
) -> responses.ORJSONResponse:
    return responses.ORJSONResponse(
        status_code=exc.status_code,
        content=_build_content(detail=exc.detail, context=exc.context),
    )


def _build_content(
    detail: str, context: typing.Any | None = None
) -> dict["str", typing.Any]:
    return {"detail": detail, "context": context}
