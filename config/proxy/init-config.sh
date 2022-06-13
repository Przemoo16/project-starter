#!/usr/bin/env bash

LETSENCRYPT_PATH=/etc/letsencrypt
NGINX_OPTIONS_PATH=$LETSENCRYPT_PATH/options-ssl-nginx.conf
DHPARAMS_PATH=$LETSENCRYPT_PATH/ssl-dhparams.pem

if [ -d $NGINX_OPTIONS_PATH ] && [ -d $DHPARAMS_PATH ]; then
    echo SSL NGINX config already exists
    exit
fi

echo Initializing SSL NGINX config

mkdir -p $LETSENCRYPT_PATH

curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > $NGINX_OPTIONS_PATH
curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > $DHPARAMS_PATH

echo Initialized SSL NGINX config in the path $LETSENCRYPT_PATH
