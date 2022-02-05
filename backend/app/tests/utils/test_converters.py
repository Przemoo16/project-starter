import uuid

from app.utils import converters


def test_change_to_uuid() -> None:
    uuid_str = "0dd53909-fcda-4c72-afcd-1bf4886389f8"

    converted = converters.change_to_uuid(uuid_str, version=4)

    assert converted == uuid.UUID(uuid_str, version=4)
