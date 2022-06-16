#!/usr/bin/env bash

DOMAIN=${DOMAIN:-localhost}
CERTS_PATH=/etc/letsencrypt/live/$DOMAIN
KEY_SIZE=4096
PRIVATE_KEY_PATH=$CERTS_PATH/privkey.pem
FULL_CHAIN_PATH=$CERTS_PATH/fullchain.pem

if [ -e $PRIVATE_KEY_PATH ] && [ -e $FULL_CHAIN_PATH ]; then
    echo SSL certificates already exists
    exit
fi

echo Initializing SSL certificates
mkdir -p $CERTS_PATH
openssl req -x509 -nodes -newkey rsa:$KEY_SIZE -sha256 -days 1 \
    -keyout $PRIVATE_KEY_PATH \
    -out $FULL_CHAIN_PATH \
    -subj /CN=$DOMAIN
echo Initialized SSL certificates in the path $CERTS_PATH
