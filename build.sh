#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install setuptools
pip install gunicorn flask
pip install -r requirements.txt
pip install tensorflow

python3 -m utils.populate_shroom_db
