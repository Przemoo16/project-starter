import logging
import multiprocessing

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MAX_WORKERS = 4
WORKERS_PER_CORE = 1

available_cores = multiprocessing.cpu_count()
web_concurrency = WORKERS_PER_CORE * available_cores

workers = min(web_concurrency, MAX_WORKERS) if MAX_WORKERS else web_concurrency
worker_class = "uvicorn.workers.UvicornWorker"
loglevel = "debug"

parameters = {
    "workers": workers,
    "worker_class": worker_class,
    "loglevel": loglevel,
}
log.info("Gunicorn parameters: %r", parameters)
