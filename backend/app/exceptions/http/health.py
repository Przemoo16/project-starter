from fastapi import status

from app.exceptions.http import base


class HealthError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "Health error"
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        super().__init__(status_code, detail, context)
