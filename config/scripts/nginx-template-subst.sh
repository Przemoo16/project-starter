#!/usr/bin/env bash

export DOMAIN="${DOMAIN:-localhost}"
export DNS_SERVER=$(cat /etc/resolv.conf |grep -i '^nameserver'|head -n1|cut -d ' ' -f2)

envsubst '$DOMAIN $DNS_SERVER' < /var/nginx.conf > /etc/nginx/conf.d/default.conf
