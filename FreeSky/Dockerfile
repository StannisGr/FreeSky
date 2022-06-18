FROM python:3.10-slim

RUN mkdir -p /app/

WORKDIR /app/

COPY requirements.txt /app/

RUN apt-get update
RUN apt-get -y install libpq-dev gcc
RUN	pip install --no-cache-dir -r requirements.txt

COPY . /app/