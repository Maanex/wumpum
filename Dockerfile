FROM arm32v7/python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
COPY config.docker.py config.py

RUN chmod +x /app/*

CMD [ "python3", "index.py"]
