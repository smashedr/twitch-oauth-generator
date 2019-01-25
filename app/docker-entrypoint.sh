#!/usr/bin/env bash

set -ex

python manage.py collectstatic --noinput

exec "$@"
