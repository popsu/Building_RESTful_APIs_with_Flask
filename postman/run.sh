#!/bin/bash

# https://stackoverflow.com/questions/43015536/xhost-command-for-docker-gui-apps-eclipse
# Fix by running:
# xhost +"local:docker@"

# https://stackoverflow.com/questions/31324981/how-to-access-host-port-from-docker-container
# Use --net="host" to have container's localhost point to host


docker run  \
    --rm \
    -d \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=unix$DISPLAY \
    --device /dev/snd:/dev/snd \
    --net="host" \
    postman:19.04