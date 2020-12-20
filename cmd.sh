#!/bin/sh
python manage.py makemigrations
python manage.py migrate
gunicorn Crowdsourcing.wsgi -b 0.0.0.0:8000 --log-level=debug