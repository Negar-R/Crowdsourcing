#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
gunicorn Crowdsourcing.wsgi:application -b 0.0.0.0:80