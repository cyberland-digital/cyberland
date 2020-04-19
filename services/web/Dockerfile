FROM python:3.6-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN pip install pipenv

WORKDIR /usr/src/app

COPY . .

RUN python --version
RUN pipenv install

ENV FLASK_APP flaskr.__init__.py
CMD ["pipenv", "run", "gunicorn", "-w", "4", "-b", ":80","flaskr:create_app()"]