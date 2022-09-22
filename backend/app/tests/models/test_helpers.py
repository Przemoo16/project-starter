import datetime
from unittest import mock

import freezegun

from app.models import helpers
from app.utils import converters


@freezegun.freeze_time("2022-01-16 22:00:00")
def test_get_utcnow() -> None:
    utcnow = helpers.get_utcnow()

    assert utcnow == datetime.datetime(2022, 1, 16, 22, 0, 0)


@mock.patch("uuid.uuid4")
def test_get_uuid4(mock_uuid4: mock.MagicMock) -> None:
    test_uuid = converters.to_uuid("1dd53909-fcda-4c72-afcd-1bf4886389f8")
    mock_uuid4.return_value = test_uuid

    uuid4 = helpers.get_uuid4()

    assert uuid4 == test_uuid


def test_orjson_dumps() -> None:
    data = {
        "id": 123,
        "name": "Przemo",
        "date": datetime.datetime(2023, 2, 1, 16, 0, 0),
    }

    serialized = helpers.orjson_dumps(data, default=None)

    assert serialized == '{"id":123,"name":"Przemo","date":"2023-02-01T16:00:00"}'
