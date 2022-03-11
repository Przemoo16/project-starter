import datetime
from unittest import mock

import freezegun

from app.models import helpers
from app.utils import converters


@freezegun.freeze_time("2022-01-16 22:00:00")
def test_get_utcnow() -> None:
    utcnow = helpers.get_utcnow()

    assert utcnow == datetime.datetime(2022, 1, 16, 22, 0, 0)


def test_generate_fixed_uuid() -> None:
    bad_uuid4_1 = converters.to_uuid("0dd53909-fcda-4c72-afcd-1bf4886389f8")
    bad_uuid4_2 = converters.to_uuid("006e20f7-18df-447a-88ae-6fb91298151e")
    good_uuid4_1 = converters.to_uuid("4e08f976-d356-45a8-8fae-9836812c82f0")
    good_uuid4_2 = converters.to_uuid("ce6498fe-ef21-4284-9139-98518a34bfa7")
    uuid_calls = [bad_uuid4_1, bad_uuid4_2, good_uuid4_1, good_uuid4_2]

    with mock.patch("uuid.uuid4", side_effect=uuid_calls) as mock_uuid4:
        generated_uuid = helpers.generate_fixed_uuid()

    assert generated_uuid == good_uuid4_1
    assert mock_uuid4.call_count == 3


def test_orjson_dumps() -> None:
    data = {
        "id": 123,
        "name": "Przemo",
        "date": datetime.datetime(2023, 2, 1, 16, 0, 0),
    }

    serialized = helpers.orjson_dumps(data, default=None)

    assert serialized == '{"id":123,"name":"Przemo","date":"2023-02-01T16:00:00"}'
