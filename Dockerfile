FROM python:3.9.13-slim-buster

WORKDIR /app

RUN apt-get update
RUN apt-get install build-essential -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .