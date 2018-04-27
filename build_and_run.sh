#!/bin/bash

docker build -t flask_hello_world .
docker rm -f flask_hello_world; docker run --name flask_hello_world -t -p 0.0.0.0:5000:5000 -it flask_hello_world
