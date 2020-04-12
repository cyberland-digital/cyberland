FROM python:3.6.9

WORKDIR /cyberland

APP ./cyberland

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]
