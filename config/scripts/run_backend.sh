#!/bin/bash

HOST=0.0.0.0
PORT=80

if [[ "$DEV_MODE" == "on" ]]; then
    echo "Running backend with reloading"
    RELOAD=--reload
else
    echo "Running backend without reloading"
    RELOAD=""
fi

uvicorn app.main:app --host ${HOST} --port ${PORT} ${RELOAD}
