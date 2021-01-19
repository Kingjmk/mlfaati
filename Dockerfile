FROM python:3.9.1
MAINTAINER Jameel Hamdan
COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r requirements.txt
WORKDIR /usr/src/app
COPY . .
