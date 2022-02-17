import typing

import fastapi
from fastapi import exceptions as fastapi_exceptions
from fastapi import responses, status
from fastapi_jwt_auth import exceptions as jwt_exceptions
from starlette import exceptions as starlette_exceptions

from app.exceptions.http import base
from app.models import exception
from app.utils import openapi


def init_handlers(app: fastapi.FastAPI) -> None:  # pragma: no cover
    @app.exception_handler(starlette_exceptions.HTTPException)
    async def custom_starlette_http_exception_handler(
        request: fastapi.Request, exc: starlette_exceptions.HTTPException
    ) -> responses.ORJSONResponse:
        return starlette_http_exception_handler(request, exc)

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

    @app.exception_handler(base.HTTPException)
    async def custom_app_http_exception_handler(
        request: fastapi.Request, exc: base.HTTPException
    ) -> responses.ORJSONResponse:
        return app_http_exception_handler(request, exc)


def starlette_http_exception_handler(
    _: fastapi.Request, exc: starlette_exceptions.HTTPException
) -> responses.ORJSONResponse:
    return responses.ORJSONResponse(
        status_code=exc.status_code,
        content=_build_content(case=exc.__class__.__name__, detail=exc.detail),
    )


def request_validation_exception_handler(
    _: fastapi.Request, exc: fastapi_exceptions.RequestValidationError
) -> responses.ORJSONResponse:
    return responses.ORJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_build_content(
            case=exc.__class__.__name__,
            detail=openapi.ValidationErrorDetail,
            context=exc.errors(),
        ),
    )


def authjwt_exception_handler(
    _: fastapi.Request, exc: jwt_exceptions.AuthJWTException
) -> responses.ORJSONResponse:
    return responses.ORJSONResponse(
        status_code=exc.status_code,
        content=_build_content(case=exc.__class__.__name__, detail=exc.message),
    )


def app_http_exception_handler(
    _: fastapi.Request, exc: base.HTTPException
) -> responses.ORJSONResponse:
    return responses.ORJSONResponse(
        status_code=exc.status_code,
        content=_build_content(case=exc.case, detail=exc.detail, context=exc.context),
    )


def _build_content(
    case: str, detail: str, context: exception.ExceptionContext = None
) -> dict[str, typing.Any]:
    return exception.ExceptionContent(case=case, detail=detail, context=context).dict()
