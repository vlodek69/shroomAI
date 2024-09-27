FROM python:3.12.0-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app/

# RUN apt-get update && apt-get install -y redis-tools

RUN pip install --upgrade pip \
    && pip install setuptools \
    && pip install gunicorn flask \
    && pip install -r requirements.txt \
    && pip install tensorflow

RUN apt-get update && apt-get install -y redis-server

EXPOSE 8000

# Populate the database
#RUN python3 -m utils.populate_shroom_db

CMD service redis-server start && python3 -m utils.populate_shroom_db && gunicorn --bind 0.0.0.0:8000 app:app
