from fastapi import status

from app.exceptions import base


class UnauthorizedError(base.ResourceException):
    def __init__(self, context: base.Context | None = None) -> None:
        status_code = status.HTTP_401_UNAUTHORIZED
        detail = "Not authenticated"
        headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code, detail, context, headers)


class ForbiddenError(base.ResourceException):
    def __init__(self, context: base.Context | None = None) -> None:
        status_code = status.HTTP_403_FORBIDDEN
        detail = "Forbidden access"
        super().__init__(status_code, detail, context)


class NotFoundError(base.ResourceException):
    def __init__(self, context: base.Context | None = None) -> None:
        status_code = status.HTTP_404_NOT_FOUND
        detail = "Resource not found"
        super().__init__(status_code, detail, context)


class ConflictError(base.ResourceException):
    def __init__(self, context: base.Context | None = None) -> None:
        status_code = status.HTTP_409_CONFLICT
        detail = "Resource already exists"
        super().__init__(status_code, detail, context)


class UnprocessableEntityError(base.ResourceException):
    def __init__(self, context: base.Context | None = None) -> None:
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        detail = "Unable to process the request instructions"
        super().__init__(status_code, detail, context)
