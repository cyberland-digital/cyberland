FROM python:3.6

MAINTAINER James Stone "jstone@jnet-it.com"

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY flaskr .

ENTRYPOINT ["flask"]
ENV FLASK_APP flaskr/__init__.py
ENV FLASK_ENV production

CMD ["run"]

