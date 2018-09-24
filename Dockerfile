FROM python:3.6.3-jessie

RUN apt-get update --fix-missing

WORKDIR /usr/src/app/

ENV DJANGO_SETTINGS_MODULE=busticket.settings.docker
ADD . /usr/src/app/

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000
