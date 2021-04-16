# This script builds the dockerfile then runs the image and passes the proper environment variables
docker build -t chat .
docker run -e T_USERNAME \
-e T_CHANNEL \
-e T_CLIENT_ID \
-e T_TOKEN \
-e API_OATH \
-e API_CLIENT_ID chat
