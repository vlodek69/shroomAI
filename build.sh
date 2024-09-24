#!/usr/bin/env bash
# exit on error
set -o errexit

redis-server --port 6380

pip install -r wsl-requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
