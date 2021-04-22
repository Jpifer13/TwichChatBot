#!/bin/sh
docker pull thealmighty666/chat:latest
docker stop chat
docker container prune -f
#docker build -t chat .
docker run -e T_USERNAME \
-e T_CHANNEL \
-e T_CLIENT_ID \
-e T_TOKEN \
-e API_OAUTH \
-e API_CLIENT_ID thealmighty666/chat:latest

