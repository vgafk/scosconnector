FROM python:3.10-slim

#WORKDIR /pinger

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN apt update && apt install -y iputils-ping
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#VOLUME ["/config"]
COPY src/* .
#COPY ./config ./config

CMD python3 main.py

EXPOSE 5000