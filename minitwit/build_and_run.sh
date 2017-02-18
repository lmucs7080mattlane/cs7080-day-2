#!/bin/bash

docker build -t minitwit .
docker rm -f minitwit; docker run --name minitwit -t -p 127.0.0.1:5000:5000 -v db:/mnt/db -it minitwit
