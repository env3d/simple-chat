#!/bin/bash

docker run \
       -e FLASK_APP=app.py \
       -e FLASK_ENV=development \
       -v "$(pwd)/src:/opt/simple-chat/src" \
       -p 5000:5000 \
       --rm -it env3d/simple-chat $@
