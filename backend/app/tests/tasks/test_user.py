from unittest import mock

from app.tasks import user
from app.utils import converters


@mock.patch("app.services.email.load_template", return_value="<html>Message</html>")
@mock.patch("app.services.email.build_message")
@mock.patch("app.services.email.send_email")
def test_send_email_to_confirm_email(
    mock_send_email: mock.MagicMock,
    mock_build_message: mock.MagicMock,
    _: mock.MagicMock,
) -> None:
    key = converters.to_uuid("1dd53909-fcda-4c72-afcd-1bf4886389f8")
    email_str = "test@email.com"
    email = converters.to_pydantic_email(email_str)
    message = "Message"
    mock_build_message.return_value = message

    task = user.send_email_to_confirm_email.apply(kwargs={"email": email, "key": key})

    assert task.status == "SUCCESS"
    mock_send_email.assert_called_once_with(message, email_str)


@mock.patch("app.services.email.load_template", return_value="<html>Message</html>")
@mock.patch("app.services.email.build_message")
@mock.patch("app.services.email.send_email")
def test_send_email_to_reset_password(
    mock_send_email: mock.MagicMock,
    mock_build_message: mock.MagicMock,
    _: mock.MagicMock,
) -> None:
    token = converters.to_uuid("1dd53909-fcda-4c72-afcd-1bf4886389f8")
    email_str = "test@email.com"
    email = converters.to_pydantic_email(email_str)
    message = "Message"
    mock_build_message.return_value = message

    task = user.send_email_to_reset_password.apply(
        kwargs={"email": email, "token": token}
    )

    assert task.status == "SUCCESS"
    mock_send_email.assert_called_once_with("Message", email_str)
