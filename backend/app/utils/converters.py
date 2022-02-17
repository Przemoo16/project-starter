import uuid

import humps


def change_to_uuid(text: str, version: int = 4) -> uuid.UUID:
    return uuid.UUID(text, version=version)


def to_camel(text: str) -> str:
    return humps.camelize(text)
