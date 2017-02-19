FROM python:3.6-slim

RUN pip3 install Flask

RUN mkdir /opt/code
WORKDIR /opt/code
ADD . /opt/code

ENV HOST_IP=0.0.0.0
ENV FLASK_APP=server.py

CMD flask run --host=$HOST_IP
