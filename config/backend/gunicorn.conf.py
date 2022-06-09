import multiprocessing

MAX_WORKERS = 4
WORKERS_PER_CORE = 1

available_cores = multiprocessing.cpu_count()
web_concurrency = WORKERS_PER_CORE * available_cores

workers = min(web_concurrency, MAX_WORKERS) if MAX_WORKERS else web_concurrency
worker_class = "uvicorn.workers.UvicornWorker"
loglevel = "debug"
