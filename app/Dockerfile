FROM python:3.8

ENV PYTHONUNBUFFERED=1

LABEL version = '1'
LABEL master = 'backend-api-example'

RUN mkdir /api
WORKDIR /api



COPY requirements/base.txt .
RUN pip install --upgrade pip
RUN pip install -r base.txt



COPY . .



