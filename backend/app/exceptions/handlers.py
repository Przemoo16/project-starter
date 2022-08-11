import typing

from fastapi import exceptions as fastapi_exceptions
from fastapi import status
from fastapi_paseto_auth import exceptions as paseto_exceptions
from starlette import exceptions as starlette_exceptions

from app.exceptions.http import base
from app.models import exception
from app.utils import responses

if typing.TYPE_CHECKING:
    import fastapi


ValidationErrorDetail = "Invalid data"


def init_handlers(app: "fastapi.FastAPI") -> None:  # pragma: no cover
    @app.exception_handler(starlette_exceptions.HTTPException)
    async def custom_starlette_http_exception_handler(
        request: "fastapi.Request", exc: starlette_exceptions.HTTPException
    ) -> responses.ORJSONResponse:
        return starlette_http_exception_handler(request, exc)

    @app.exception_handler(fastapi_exceptions.RequestValidationError)
    async def custom_request_validation_exception_handler(
        request: "fastapi.Request", exc: fastapi_exceptions.RequestValidationError
    ) -> responses.ORJSONResponse:
        return request_validation_exception_handler(request, exc)

    @app.exception_handler(paseto_exceptions.AuthPASETOException)
    async def custom_authpaseto_exception_handler(
        request: "fastapi.Request", exc: paseto_exceptions.AuthPASETOException
    ) -> responses.ORJSONResponse:
        return authpaseto_exception_handler(request, exc)

    @app.exception_handler(base.HTTPException)
    async def custom_app_http_exception_handler(
        request: "fastapi.Request", exc: base.HTTPException
    ) -> responses.ORJSONResponse:
        return app_http_exception_handler(request, exc)


def starlette_http_exception_handler(
    _: "fastapi.Request", exc: starlette_exceptions.HTTPException
) -> responses.ORJSONResponse:
    return responses.ORJSONResponse(
        status_code=exc.status_code,
        content=_build_content(case=exc.__class__.__name__, detail=exc.detail),
    )


def request_validation_exception_handler(
    _: "fastapi.Request", exc: fastapi_exceptions.RequestValidationError
) -> responses.ORJSONResponse:
    return responses.ORJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_build_content(
            case=exc.__class__.__name__,
            detail=ValidationErrorDetail,
            context=exc.errors(),
        ),
    )


def authpaseto_exception_handler(
    _: "fastapi.Request", exc: paseto_exceptions.AuthPASETOException
) -> responses.ORJSONResponse:
    return responses.ORJSONResponse(
        status_code=exc.status_code,
        content=_build_content(case=exc.__class__.__name__, detail=exc.message),
    )


def app_http_exception_handler(
    _: "fastapi.Request", exc: base.HTTPException
) -> responses.ORJSONResponse:
    return responses.ORJSONResponse(
        status_code=exc.status_code,
        content=_build_content(case=exc.case, detail=exc.detail, context=exc.context),
    )


def _build_content(
    case: str, detail: str, context: exception.ExceptionContext = None
) -> dict[str, typing.Any]:
    return exception.ExceptionContent(case=case, detail=detail, context=context).dict(
        by_alias=True
    )
