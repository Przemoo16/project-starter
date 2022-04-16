#!/bin/bash

URL=http://frontend:3000
WAIT_TIMEOUT_MS=60000

wait-on $URL -t $WAIT_TIMEOUT_MS && cypress run
