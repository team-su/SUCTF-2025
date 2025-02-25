#!/bin/bash
docker build . -t msg_cfgd
docker run -d -p "9999:9999" -h "msg_cfgd" --name="msg_cfgd" msg_cfgd