FROM python:3.11.0-slim
ENV PYTHONUNBUFFERED=1
# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
ENV PYTHONUNBUFFERED=1
WORKDIR /queue
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN apt-get -y update
RUN apt-get install ffmpeg libsm6 libxext6 -y
COPY . /queue
