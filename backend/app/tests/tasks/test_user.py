from unittest import mock

from app.tasks import user
from app.utils import converters


@mock.patch("app.services.email.load_template", return_value="<html>Message</html>")
@mock.patch("app.services.email.send_email")
def test_send_email_to_confirm_email(
    mocked_send_email: mock.MagicMock, _: mock.MagicMock
) -> None:
    key = converters.to_uuid("1dd53909-fcda-4c72-afcd-1bf4886389f8")
    email = "test@email.com"

    task = user.send_email_to_confirm_email.apply(args=(email, key))

    assert task.status == "SUCCESS"
    mocked_send_email.assert_called_once()


@mock.patch("app.services.email.load_template", return_value="<html>Message</html>")
@mock.patch("app.services.email.send_email")
def test_send_email_to_reset_password(
    mocked_send_email: mock.MagicMock, _: mock.MagicMock
) -> None:
    key = converters.to_uuid("1dd53909-fcda-4c72-afcd-1bf4886389f8")
    email = "test@email.com"

    task = user.send_email_to_reset_password.apply(args=(email, key))

    assert task.status == "SUCCESS"
    mocked_send_email.assert_called_once()
