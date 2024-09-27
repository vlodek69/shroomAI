FROM python:3.12.0-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install Redis (required if you want to use redis-cli for debugging)
RUN apt-get update && apt-get install -y redis-tools

# Upgrade pip, install setuptools, gunicorn, and flask
RUN pip install --upgrade pip \
    && pip install setuptools \
    && pip install gunicorn flask

# Install requirements from requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install TensorFlow (if not included in requirements.txt)
RUN pip install tensorflow

# Copy the rest of the app code
COPY . /app/

# Populate the database
#RUN python3 -m utils.populate_shroom_db

# Command to run the app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
