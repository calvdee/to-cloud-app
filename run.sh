#!/bin/bash

# Start the celery worker with small eventlet pool
python manage.py celery worker -A celery_tocloud.app.main -E --pool=eventlet -c 150