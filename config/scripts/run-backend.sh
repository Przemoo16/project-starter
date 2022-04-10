#!/bin/bash

HOST=0.0.0.0
PORT=8000
MESSAGE="Running backend on $HOST:$PORT"

/scripts/wait-for-it.sh -t 15 $DATABASE_HOST:$DATABASE_PORT

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
