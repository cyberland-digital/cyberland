FROM python:3.6

MAINTAINER James Stone "jstone@jnet-it.com"

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY flaskr .

ENTRYPOINT ["flask"]
ENV FLASK_APP flaskr

CMD ["run"]

