#!/usr/bin/env bash
# exit on error
set -o errexit

sudo apt-get update
sudo apt-get install redis-server
redis-server --port 6380

pip install -r wsl-requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
