import logging
import smtplib
import socket
import ssl
import typing
from email.mime import multipart, text

from app.config import general
from app.utils import jinja, translation

log = logging.getLogger(__name__)

settings = general.get_settings()


def load_template(template_name: str, **kwargs: typing.Any) -> str:
    template = jinja.env.get_template(template_name)
    return template.render(**kwargs)


def build_message(
    message_html: str,
    message_text: str | translation.LazyString,
    subject: str | translation.LazyString,
    receiver: str,
) -> str:
    message = multipart.MIMEMultipart("alternative")
    message["Subject"] = str(subject)
    message["From"] = settings.EMAIL_SENDER
    message["To"] = receiver
    message.attach(text.MIMEText(str(message_text), "plain"))
    message.attach(text.MIMEText(message_html, "html"))
    return message.as_string()


def send_email(message: str, receiver: str) -> None:
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(
            settings.SMTP_HOST, settings.SMTP_PORT, context=context
        ) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            response = server.sendmail(settings.EMAIL_SENDER, receiver, message)
            log.debug("Email response: %r", response)
    except (smtplib.SMTPException, socket.gaierror) as e:
        log.warning("Error occurred when sending an email: %s", e)
