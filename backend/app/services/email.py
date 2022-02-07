from email.mime import multipart, text
import logging
import smtplib
import ssl
import typing

from app.config import general, jinja
from app.exceptions import email as email_exceptions

log = logging.getLogger(__name__)

settings = general.get_settings()


def load_template(template_name: str, **kwargs: typing.Any) -> str:
    template = jinja.env.get_template(template_name)
    return template.render(**kwargs)


def build_message(
    message_html: str, message_text: str, subject: str, receiver: str
) -> str:
    message = multipart.MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = settings.EMAIL_SENDER_EMAIL
    message["To"] = receiver
    message.attach(text.MIMEText(message_text, "plain"))
    message.attach(text.MIMEText(message_html, "html"))
    return message.as_string()


def send_email(message: str, receiver: str) -> None:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        settings.SMTP_HOST, settings.SMTP_PORT, context=context
    ) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        try:
            response = server.sendmail(settings.EMAIL_SENDER_EMAIL, receiver, message)
        except smtplib.SMTPException as e:
            log.exception("Exception occurred when sending an email")
            raise email_exceptions.SendingEmailError() from e
        log.debug("Email response: %r", response)
