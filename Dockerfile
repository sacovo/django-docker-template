# pull official base image \
FROM python:3.9-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/app

# create the appropriate directories
RUN mkdir -p /static
RUN mkdir -p /media

RUN useradd -ms /bin/bash app

RUN chown app:app /static /media

ENV HOME=/home/app
ENV APP_HOME=/home/app/web

RUN mkdir $APP_HOME

RUN apt-get update && \
  apt-get install -y \
    netcat gettext libyaml-dev \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/home/app/web/entrypoint.sh"]

# install dependencies

# change to the app user
WORKDIR $APP_HOME

COPY ./requirements.txt $APP_HOME/requirements.txt


RUN pip install --upgrade pip
RUN pip install -r  requirements.txt --no-cache-dir

USER app

# copy project
COPY --chown=app:app . $APP_HOME


RUN python manage.py compilemessages

CMD ["gunicorn", "core.wsgi"]
