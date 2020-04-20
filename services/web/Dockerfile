# setup bsae environment - will only rebuild if Pipfile updated
FROM python:3.6-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN pip install pipenv

WORKDIR /usr/src/app

COPY Pipfile .
RUN pipenv install

# copy project
# TODO: make copy more specific - only copy needed resources
COPY . .
