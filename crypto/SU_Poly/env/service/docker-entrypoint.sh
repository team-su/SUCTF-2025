#!/bin/sh

rm -f /home/sage/docker-entrypoint.sh

socat -v -s TCP4-LISTEN:9999,tcpwrap=script,reuseaddr,fork EXEC:"sage /home/sage/main.sage"