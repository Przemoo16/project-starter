from fastapi import status

from app.exceptions.http import base
from app.models import exception


def test_base_exception_doc() -> None:
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User is not authorized"
    context = {"email": "test@email.com"}
    headers = {"WWW-Authenticate": "Bearer"}
    http_exception = base.HTTPException(
        status_code=status_code, detail=detail, context=context, headers=headers
    )

    doc = http_exception.doc

    assert doc == {
        status_code: {
            "model": exception.ExceptionContent,
            "description": detail,
            "headers": headers,
            "content": {
                "application/json": {
                    "example": {
                        "case": "HTTPException",
                        "detail": detail,
                        "context": context,
                    },
                }
            },
        }
    }
