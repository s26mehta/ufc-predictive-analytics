FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential curl


RUN pip install Flask

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql.list
RUN apt-get install apt-transport-https -y
RUN apt-get update -y
RUN apt-get --yes install mssql-tools unixodbc-dev -y
RUN apt-get install msodbcsql --assume-yes
RUN sudo pip install pyodbc==3.1.1

ADD api.py /app

RUN pip install uwsgi

ENV HOME /app
WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:8000", "--module", "app:app", "--processes", "1", "--threads", "8"]
