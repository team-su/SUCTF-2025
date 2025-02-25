#!/bin/bash

rm -f /docker-entrypoint.sh

exec  /var/www/html/bin/cake server -H 0.0.0.0 -p 80 