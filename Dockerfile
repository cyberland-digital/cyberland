FROM python:3.6

RUN pip install pipenv

WORKDIR /usr/src/app

COPY . .

RUN python --version
RUN pipenv install

ENV FLASK_APP flaskr.__init__.py
CMD ["pipenv", "run", "gunicorn", "-w", "4", "-b", ":443","--certfile", "/certs/fullchain.pem", "--keyfile", "/certs/privkey.pem", "flaskr:create_app()"]