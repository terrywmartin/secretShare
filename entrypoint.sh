#!/bin/bash

RUN_PORT="8000"

# wait 5 seconds so the database server is fully online and ready to take requests
sleep 5
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input --clear
#python3 manage.py runserver

gunicorn passwordShare.wsgi:application --bind "0.0.0.0:${RUN_PORT}"