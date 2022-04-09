#!/bin/bash

HOST=0.0.0.0
PORT=8000
MESSAGE="Running backend on $HOST:$PORT"

if [[ "$DEV_MODE" == "on" ]]; then
    echo "$MESSAGE with reloading"
    RELOAD=--reload
else
    echo "$MESSAGE without reloading"
    RELOAD=""
fi

uvicorn app.main:app --host ${HOST} --port ${PORT} ${RELOAD}
