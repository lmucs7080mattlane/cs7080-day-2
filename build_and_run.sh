#!/bin/bash

docker build -t flask_hello_world .
docker rm -f flask_hello_world; docker run --name flask_hello_world -t -p 127.0.0.1:5000:5000 -it flask_hello_world
