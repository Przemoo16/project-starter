#!/usr/bin/env bash

/var/scripts/nginx-template-subst.sh

nginx -g 'daemon off;'
