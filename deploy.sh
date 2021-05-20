#!/bin/sh
echo Pulling latest image
docker pull thealmighty666/chat:latest
echo Stopping existing container
docker stop chat
echo Pruning stopped containers
docker container prune -f
#docker build -t chat .
echo Running lastest
docker run --name chat -e T_USERNAME \
-e T_CHANNEL \
-e T_CLIENT_ID \
-e T_TOKEN \
-e API_OAUTH \
-e API_CLIENT_ID thealmighty666/chat:latest

