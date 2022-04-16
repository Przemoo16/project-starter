#!/bin/bash

WAIT_TIMEOUT_SECONDS=15
HOST=0.0.0.0
PORT=8000
MESSAGE="Running backend on $HOST:$PORT"

/scripts/wait-for-it.sh -t $WAIT_TIMEOUT_SECONDS $DATABASE_HOST:$DATABASE_PORT

alembic upgrade head
status=$?
if [ $status -ne 0 ]; then
    echo "Failed to migrate: $status"
    exit $status
fi

if [[ "$DEV_MODE" == "on" ]]; then
    echo "$MESSAGE with reloading"
    RELOAD=--reload
else
    echo "$MESSAGE without reloading"
    RELOAD=""
fi

uvicorn app.main:app --host ${HOST} --port ${PORT} ${RELOAD}
