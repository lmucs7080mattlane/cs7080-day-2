#!/bin/bash

docker pull mongo:3.2
docker rm -f mongo
docker run --name mongo -v mongo:/data/db -d mongo

docker build -t flask_hello_world .
docker rm -f flask_hello_world
docker run --name flask_hello_world -t -p 0.0.0.0:5000:5000 --link mongo -it flask_hello_world
