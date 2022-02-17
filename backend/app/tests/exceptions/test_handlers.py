import fastapi
from fastapi import exceptions as fastapi_exceptions
from fastapi import status
from fastapi_jwt_auth import exceptions as jwt_exceptions
import orjson
from pydantic import error_wrappers, errors
from starlette import exceptions as starlette_exceptions

from app.exceptions import handlers
from app.exceptions.http import base


def test_starlette_http_exception_handler() -> None:
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Bad Request"
    exception = starlette_exceptions.HTTPException(status_code, detail)

    response = handlers.starlette_http_exception_handler(
        fastapi.Request(scope={"type": "http"}), exception
    )

    assert response.status_code == status_code
    assert orjson.loads(response.body) == {
        "case": "HTTPException",
        "detail": detail,
        "context": None,
    }


def test_request_validation_exception_handler() -> None:
    exception = fastapi_exceptions.RequestValidationError(
        errors=[
            error_wrappers.ErrorWrapper(exc=errors.IntegerError(), loc="dummy location")
        ]
    )
    deserialized_errors = orjson.loads(orjson.dumps(exception.errors()))

    response = handlers.request_validation_exception_handler(
        fastapi.Request(scope={"type": "http"}), exception
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert orjson.loads(response.body) == {
        "case": "RequestValidationError",
        "detail": "Invalid data",
        "context": deserialized_errors,
    }


def test_authjwt_exception_handler() -> None:
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Missing access token"
    exception = jwt_exceptions.AccessTokenRequired(status_code, message=detail)

    response = handlers.authjwt_exception_handler(
        fastapi.Request(scope={"type": "http"}), exception
    )

    assert response.status_code == status_code
    assert orjson.loads(response.body) == {
        "case": "AccessTokenRequired",
        "detail": detail,
        "context": None,
    }


def test_app_http_exception_handler() -> None:
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"
    context = {"email": "test@email.com"}
    exception = base.HTTPException(
        status_code=status_code, detail=detail, context=context
    )

    response = handlers.app_http_exception_handler(
        fastapi.Request(scope={"type": "http"}), exception
    )

    assert response.status_code == status_code
    assert orjson.loads(response.body) == {
        "case": "HTTPException",
        "detail": detail,
        "context": context,
    }
