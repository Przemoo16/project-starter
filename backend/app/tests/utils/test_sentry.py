from unittest import mock

from sentry_sdk import utils

from app.utils import sentry


@mock.patch("sentry_sdk.init")
def test_init_sentry(_: mock.MagicMock) -> None:
    sentry.init_sentry("Dummy DSN")


@mock.patch("sentry_sdk.init", side_effect=utils.BadDsn)
def test_init_sentry_bad_dsn(_: mock.MagicMock) -> None:
    sentry.init_sentry("Dummy DSN")
