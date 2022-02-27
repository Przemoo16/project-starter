from fastapi import status

from app.exceptions.http import base


class InactiveUserError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "User is inactive"
        status_code = status.HTTP_403_FORBIDDEN
        super().__init__(status_code, detail, context)


class InvalidTokenError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "Invalid token"
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        super().__init__(status_code, detail, context)


class RefreshTokenRequiredError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "Refresh token required"
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        super().__init__(status_code, detail, context)


class RevokedTokenError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "Token has been revoked"
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        super().__init__(status_code, detail, context)
