#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

readonly cmd="$*"

###########################
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser \
       --noinput \
       --username $DJANGO_SUPERUSER_USERNAME \
       --email $DJANGO_SUPERUSER_EMAIL
###########################

exec $cmd
