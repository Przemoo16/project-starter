import fastapi
from fastapi import exceptions as fastapi_exceptions
from fastapi import status
from fastapi_jwt_auth import exceptions as jwt_exceptions
import orjson
from pydantic import error_wrappers, errors
from starlette import exceptions as starlette_exceptions

from app.exceptions import base, handlers


def test_http_exception_handler() -> None:
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Bad Request"
    exception = starlette_exceptions.HTTPException(status_code, detail)

    response = handlers.http_exception_handler(
        fastapi.Request(scope={"type": "http"}), exception
    )

    assert response.status_code == status_code
    assert orjson.loads(response.body) == {"detail": detail, "context": None}


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
    assert orjson.loads(response.body) == {"detail": detail, "context": None}


def test_resource_exception_handler() -> None:
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found"
    context = {"email": "test@email.com"}
    exception = base.ResourceException(status_code, detail, context)

    response = handlers.resource_exception_handler(
        fastapi.Request(scope={"type": "http"}), exception
    )

    assert response.status_code == status_code
    assert orjson.loads(response.body) == {"detail": detail, "context": context}
