#!/usr/bin/env bash

export DEV_MODE="${DEV_MODE:-off}"
export DNS_SERVER=$(cat /etc/resolv.conf |grep -i '^nameserver'|head -n1|cut -d ' ' -f2)

envsubst '$DEV_MODE $DNS_SERVER' < /var/nginx.conf > /etc/nginx/conf.d/default.conf
