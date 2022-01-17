from datetime import datetime
from unittest import mock
import uuid

import freezegun

from app.models import helpers


@freezegun.freeze_time("2022-01-16 22:00:00")
def test_get_utcnow() -> None:
    utcnow = helpers.get_utcnow()

    assert utcnow == datetime(2022, 1, 16, 22, 0, 0)


def test_generate_fixed_uuid() -> None:
    bad_uuid4_1 = uuid.UUID("0dd53909-fcda-4c72-afcd-1bf4886389f8", version=4)
    bad_uuid4_2 = uuid.UUID("006e20f7-18df-447a-88ae-6fb91298151e", version=4)
    good_uuid4_1 = uuid.UUID("4e08f976-d356-45a8-8fae-9836812c82f0", version=4)
    good_uuid4_2 = uuid.UUID("ce6498fe-ef21-4284-9139-98518a34bfa7", version=4)
    uuid_calls = [bad_uuid4_1, bad_uuid4_2, good_uuid4_1, good_uuid4_2]

    with mock.patch.object(uuid, "uuid4", side_effect=uuid_calls) as mocked_uuid4:
        generated_uuid = helpers.generate_fixed_uuid()

    assert generated_uuid == good_uuid4_1
    assert mocked_uuid4.call_count == 3
