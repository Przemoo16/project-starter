#!/usr/bin/env bash

/scripts/init-config.sh
/scripts/init-certs.sh
/scripts/nginx-template-subst.sh

while :; do
    sleep 6h;
    nginx -s reload;
done & exec nginx -g 'daemon off;'
