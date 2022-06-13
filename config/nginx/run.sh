#!/usr/bin/env bash

/scripts/nginx-template-subst.sh

nginx -g 'daemon off;'
