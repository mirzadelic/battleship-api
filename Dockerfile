FROM python:3.6.3-jessie

RUN apt-get update --fix-missing

WORKDIR /usr/src/app/

ENV DJANGO_SETTINGS_MODULE=battleship.settings.docker
ADD . /usr/src/app/

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

RUN bash -c "chmod +x ./.docker/run.sh"
CMD ["./.docker/run.sh"]
