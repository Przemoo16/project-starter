import sentry_sdk
from sentry_sdk.integrations import celery


def init_sentry(dsn: str, dev_mode: bool) -> None:  # pragma: no cover
    if dev_mode:
        return

    sentry_sdk.init(dsn=dsn, integrations=[celery.CeleryIntegration()])
