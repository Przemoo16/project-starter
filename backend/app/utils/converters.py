import uuid


def change_to_uuid(text: str, version: int = 4) -> uuid.UUID:
    return uuid.UUID(text, version=version)
