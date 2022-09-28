FROM python:3.10-slim
MAINTAINER Vladimir Yartsev <proger@vgafk.ru>


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#VOLUME ["/config"]
COPY src/* .
#COPY ./config ./config

CMD python3 main.py