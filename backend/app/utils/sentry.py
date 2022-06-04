import logging

import sentry_sdk
from sentry_sdk import utils
from sentry_sdk.integrations import celery

log = logging.getLogger(__name__)


def init_sentry(dsn: str) -> None:
    try:
        sentry_sdk.init(dsn=dsn, integrations=[celery.CeleryIntegration()])
    except utils.BadDsn as e:
        log.warning("Could not init Sentry: %s", e)
