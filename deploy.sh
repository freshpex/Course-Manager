#!/bin/bash

pip install --upgrade pip

pip install -r requirements.txt

pip install Gunicorn

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn --reload helloworld.helloworld.wsgi:application \
    --bind 0.0.0.0:8000