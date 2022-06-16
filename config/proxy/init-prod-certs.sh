#!/usr/bin/env bash

KEY_SIZE=4096
DOMAIN='$DOMAIN' # Use DOMAIN env from the container and not from the host
EMAIL='contact@$DOMAIN'
CERTBOT_CONTAINER=$(docker ps -aqf name=certbot)
PROXY_CONTAINER=$(docker ps -aqf name=proxy)
WEBROOT_PATH=/var/www/certbot

echo Deleting existing certificates
docker exec $CERTBOT_CONTAINER sh -c " \
    rm -rf /etc/letsencrypt/live/$DOMAIN && \
    rm -rf /etc/letsencrypt/archive/$DOMAIN && \
    rm -rf /etc/letsencrypt/renewal/$DOMAIN.conf"
echo Deleted existing certificates

echo Creating new production certificates
docker exec $CERTBOT_CONTAINER sh -c " \
    certbot certonly --webroot -w $WEBROOT_PATH \
        --email $EMAIL \
        --domains $DOMAIN \
        --domains www.$DOMAIN \
        --rsa-key-size $KEY_SIZE \
        --agree-tos \
        --non-interactive \
        --force-renewal"
echo Created production certificates

echo Reloading proxy
docker exec $PROXY_CONTAINER nginx -s reload
echo Reloaded proxy
