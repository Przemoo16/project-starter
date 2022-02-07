from app.celery import worker
from app.models import user as user_models


@worker.app.task
def send_email_to_confirm_email(
    email: user_models.UserEmail, key: user_models.ConfirmationEmailKey
) -> None:
    pass


@worker.app.task
def send_email_to_reset_password(
    email: user_models.UserEmail, key: user_models.ResetPasswordKey
) -> None:
    pass
