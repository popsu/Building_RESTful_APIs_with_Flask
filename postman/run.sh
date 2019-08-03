#!/bin/bash

# https://stackoverflow.com/questions/43015536/xhost-command-for-docker-gui-apps-eclipse
# Fix by running:
# xhost +"local:docker@"


docker run  \
    --rm \
    -d \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=unix$DISPLAY \
    --device /dev/snd:/dev/snd \
    postman:19.04