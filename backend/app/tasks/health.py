import logging

import celery

log = logging.getLogger(__name__)


@celery.shared_task
def check_health() -> None:
    log.debug("Celery health task executed")
