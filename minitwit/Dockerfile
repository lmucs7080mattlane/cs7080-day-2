FROM python:3.6-slim

ENV DATABASE_DIR=/mnt/db
RUN mkdir -p $DATABASE_DIR

RUN mkdir /opt/code
WORKDIR /opt/code
ADD . /opt/code

RUN pip install --editable .

ENV FLASK_APP=minitwit
ENV HOST_IP=0.0.0.0

# If the database directory is empty, initialise it via flask initdb.
# Either way, then run the flask webserver
CMD ./run_flask.sh
