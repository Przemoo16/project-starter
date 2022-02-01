import datetime

from app.models import base


def test_orjson_dumps() -> None:
    data = {
        "id": 123,
        "name": "Przemo",
        "date": datetime.datetime(2023, 2, 1, 16, 0, 0),
    }

    serialized = base.orjson_dumps(data, default=None)

    assert serialized == '{"id":123,"name":"Przemo","date":"2023-02-01T16:00:00Z"}'
