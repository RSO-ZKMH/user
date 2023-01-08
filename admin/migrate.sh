#!/bin/bash 

SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"admin@gmail.com"}
SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-"admin"}
cd /app/

/opt/venv/bin/python manage.py migrate --noinput
DJANGO_SUPERUSER_PASSWORD=Password1 /opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --username $SUPERUSER_USERNAME --noinput || true