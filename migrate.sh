#!/bin/bash
python manage.py migrate --noinput 2>&1 | tee migrate.log