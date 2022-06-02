import logging

import sentry_sdk
from sentry_sdk import utils
from sentry_sdk.integrations import celery

log = logging.getLogger(__name__)


def init_sentry(dsn: str, dev_mode: bool) -> None:  # pragma: no cover
    if dev_mode:
        return
    try:
        sentry_sdk.init(dsn=dsn, integrations=[celery.CeleryIntegration()])
    except utils.BadDsn:
        log.exception("Could not init Sentry")
