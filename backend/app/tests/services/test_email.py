import smtplib
from unittest import mock

import jinja2
import pytest

from app.exceptions.app import email as email_exceptions
from app.services import email as email_services

TEMPLATE_HTML = """
<!DOCTYPE html>
<html>
    <head></head>
    <body>
        <h1>Hello {{ name }}</h1>
        <p>
            <a href="{{ link }}">Click here to confirm your email</a>
        </p>
    </body>
</html>
"""

MESSAGE_HTML = """
<!DOCTYPE html>
<html>
    <head></head>
    <body>
        <h1>Hello John</h1>
        <p>
            <a href="https://example.com">Click here to confirm your email</a>
        </p>
    </body>
</html>
"""

BUILT_MESSAGE = """
Content-Type: multipart/alternative; boundary="===============0000000000000000123=="
MIME-Version: 1.0
Subject: Dummy subject
From: test@email.com
To: receiver@email.com

--===============0000000000000000123==
Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit

Hello
--===============0000000000000000123==
Content-Type: text/html; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit

<html>Hello</html>
--===============0000000000000000123==--
"""


@mock.patch(
    "app.utils.jinja.env.get_template", return_value=jinja2.Template(TEMPLATE_HTML)
)
def test_load_template(_: mock.MagicMock) -> None:
    message_html = email_services.load_template(
        "dummy_template.j2", name="John", link="https://example.com"
    )

    assert message_html.strip() == MESSAGE_HTML.strip()


@mock.patch("random.randrange", return_value=123)
def test_build_message(_: mock.MagicMock) -> None:
    message = email_services.build_message(
        message_html="<html>Hello</html>",
        message_text="Hello",
        subject="Dummy subject",
        receiver="receiver@email.com",
    )

    assert message.strip() == BUILT_MESSAGE.strip()


@mock.patch("app.services.email.settings.DEV_MODE", new=False)
@mock.patch("smtplib.SMTP.connect", return_value=(220, b"dummy response"))
@mock.patch("smtplib.SMTP.login", return_value=(235, b"dummy response"))
@mock.patch("smtplib.SMTP.sendmail")
@mock.patch("app.services.email.settings.EMAIL_SENDER_EMAIL", new="test@email.com")
def test_send_email(mock_sendmail: mock.MagicMock, *_: mock.MagicMock) -> None:
    receiver = "receiver@email.com"

    email_services.send_email(BUILT_MESSAGE, receiver)

    mock_sendmail.assert_called_once_with("test@email.com", receiver, BUILT_MESSAGE)


@mock.patch("app.services.email.settings.DEV_MODE", new=False)
@mock.patch("smtplib.SMTP.connect", return_value=(220, b"dummy response"))
@mock.patch("smtplib.SMTP.login", return_value=(235, b"dummy response"))
@mock.patch("smtplib.SMTP.sendmail", side_effect=smtplib.SMTPException)
def test_send_email_error(*_: mock.MagicMock) -> None:
    with pytest.raises(email_exceptions.SendingEmailError):
        email_services.send_email(BUILT_MESSAGE, "receiver@email.com")
