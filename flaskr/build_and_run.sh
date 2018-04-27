#!/bin/bash

docker build -t flaskr .
docker rm -f flaskr; docker run --name flaskr -t -p 0.0.0.0:5000:5000 -v flaskdb:/mnt/db -it flaskr
