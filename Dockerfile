FROM python:3.12.0-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip \
    && pip install setuptools \
    && pip install gunicorn flask \
    && pip install -r requirements.txt \
    && pip install tensorflow

RUN apt-get update && apt-get install -y redis-server

VOLUME /data

EXPOSE 8000

CMD service redis-server start --appendonly yes --dir /data && gunicorn --bind 0.0.0.0:8000 app:app && python3 -m utils.populate_shroom_db
