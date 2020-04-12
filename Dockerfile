FROM python:3.6.9

WORKDIR /cyberland/

ADD ./cyberland /
RUN ls /cyberland
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]
