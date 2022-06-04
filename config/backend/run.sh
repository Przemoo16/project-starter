#!/bin/bash

WAIT_TIMEOUT_SECONDS=15
HOST=0.0.0.0
PORT=8000
APP_MODULE=app.main:app

/scripts/wait-for-it.sh -t $WAIT_TIMEOUT_SECONDS $DATABASE_HOST:$DATABASE_PORT

alembic upgrade head
status=$?
if [ $status -ne 0 ]; then
    echo "Failed to migrate: $status"
    exit $status
fi

if [[ "$DEV_MODE" == "on" ]]; then
    echo "Running backend in development mode using uvicorn"
    uvicorn ${APP_MODULE} --host ${HOST} --port ${PORT} --reload
else
    echo "Running backend in production mode using gunicorn"
    gunicorn ${APP_MODULE} -c /scripts/gunicorn.conf.py --bind "${HOST}:${PORT}"
fi
