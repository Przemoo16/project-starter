import datetime
import uuid


def get_utcnow() -> datetime.datetime:
    """
    Return datetime in UTC.

    It allows deferring initialization of the datetime module, thus mock it using
    freezegun.
    """
    return datetime.datetime.utcnow()


def generate_fixed_uuid() -> uuid.UUID:
    """
    Make sure that uuid does not start with a leading 0.

    TODO: Remove it when https://github.com/tiangolo/sqlmodel/issues/25 will be solved.
    """
    val = uuid.uuid4()
    while val.hex[0] == "0":
        val = uuid.uuid4()
    return val
