import logging

from app.celery import worker
from app.config import general
from app.models import user as user_models
from app.services import email as email_services

log = logging.getLogger(__name__)

settings = general.get_settings()


@worker.app.task
def send_email_to_confirm_email(
    email: user_models.UserEmail, key: user_models.ConfirmationEmailKey
) -> None:
    link = settings.FRONTEND_CONFIRM_EMAIL_URL.format(key=key)
    subject = "Confirm email"
    message_text = f"Click the link to confirm your email: {link}"
    message_html = email_services.load_template(
        template_name="confirm_email.j2", link=link
    )
    message = email_services.build_message(
        message_html=message_html,
        message_text=message_text,
        subject=subject,
        receiver=email,
    )
    email_services.send_email(message, email)
    log.info("Email to confirm email has been sent to %r", email)


@worker.app.task
def send_email_to_reset_password(
    email: user_models.UserEmail, key: user_models.ResetPasswordKey
) -> None:
    link = settings.FRONTEND_RESET_PASSWORD_URL.format(key=key)
    subject = "Reset password"
    message_text = f"Click the link to reset your password: {link}"
    message_html = email_services.load_template(
        template_name="reset_password_email.j2", link=link
    )
    message = email_services.build_message(
        message_html=message_html,
        message_text=message_text,
        subject=subject,
        receiver=email,
    )
    email_services.send_email(message, email)
    log.info("Email to reset password has been sent to %r", email)
