from fastapi import status

from app.exceptions.http import base


class ResetPasswordTokenNotFound(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "Reset password token not found"
        status_code = status.HTTP_404_NOT_FOUND
        super().__init__(status_code, detail, context)


class ResetPasswordTokenExpired(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "Reset password token expired"
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        super().__init__(status_code, detail, context)
