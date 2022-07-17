import logging
import typing

import celery

from app.config import general
from app.services import email as email_services
from app.utils.translation import gettext_lazy as _

if typing.TYPE_CHECKING:
    from app.models import reset_password, user


log = logging.getLogger(__name__)

settings = general.get_settings()


@celery.shared_task
def send_email_to_confirm_email(
    email: "user.UserEmail", token: "user.UserEmailConfirmationToken"
) -> None:
    link = settings.CONFIRM_EMAIL_URL.format(token=token)
    subject = _("Confirm email")
    message_text = _("Click the link to confirm your email: %(link)s") % {"link": link}
    message_html = email_services.load_template(
        template_name="confirm_email.html.jinja", link=link
    )
    message = email_services.build_message(
        message_html=message_html,
        message_text=message_text,
        subject=subject,
        receiver=email,
    )
    email_services.send_email(message, email)
    log.info("Email to confirm email has been sent to %r", email)


@celery.shared_task
def send_email_to_reset_password(
    email: "user.UserEmail", token: "reset_password.ResetPasswordToken"
) -> None:
    link = settings.RESET_PASSWORD_URL.format(token=token)
    subject = _("Reset password")
    message_text = _("Click the link to reset your password: %(link)s") % {"link": link}
    message_html = email_services.load_template(
        template_name="reset_password_email.html.jinja", link=link
    )
    message = email_services.build_message(
        message_html=message_html,
        message_text=message_text,
        subject=subject,
        receiver=email,
    )
    email_services.send_email(message, email)
    log.info("Email to reset password has been sent to %r", email)
