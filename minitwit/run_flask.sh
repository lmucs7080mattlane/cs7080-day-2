#!/bin/bash

# If the database directory is empty, initialise it via flask initdb.
[ ! "$(ls -A $DATABASE_DIR)" ] && flask initdb

# Either way, then run the flask webserver
flask run --host=$HOST_IP
