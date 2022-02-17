import uuid

import pytest

from app.utils import converters


def test_change_to_uuid() -> None:
    uuid_str = "0dd53909-fcda-4c72-afcd-1bf4886389f8"

    converted = converters.change_to_uuid(uuid_str, version=4)

    assert converted == uuid.UUID(uuid_str, version=4)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("confirmed_email", "confirmedEmail"),
        ("confirmation_email_key", "confirmationEmailKey"),
        ("reset_password_key", "resetPasswordKey"),
        ("LastUserLogin", "lastUserLogin"),
        ("password", "password"),
    ],
)
def test_to_camel(test_input: str, expected: str) -> None:
    camelized = converters.to_camel(test_input)

    assert camelized == expected
