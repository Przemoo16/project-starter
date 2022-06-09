#!/usr/bin/env bash

CERTS_PATH=./config/proxy/ssl
KEY_SIZE=4096

openssl req -x509 -nodes -newkey rsa:$KEY_SIZE -sha256 -days 1 \
    -keyout "$CERTS_PATH/privkey.pem" \
    -out "$CERTS_PATH/fullchain.pem" \
    -subj "/CN=localhost" \
