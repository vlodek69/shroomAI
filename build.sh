#!/usr/bin/env bash
# exit on error
set -o errexit

apt-get update
apt-get install redis-server
redis-server --port 6380

pip install -r wsl-requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
