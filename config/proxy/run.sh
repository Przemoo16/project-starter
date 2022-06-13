#!/usr/bin/env bash

/var/scripts/init-config.sh
/var/scripts/init-certs.sh
/var/scripts/nginx-template-subst.sh

while :; do
    sleep 6h;
    nginx -s reload;
done & exec nginx -g 'daemon off;'
