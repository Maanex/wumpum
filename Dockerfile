FROM python:3.8.3

WORKDIR /app

COPY requirements.txt requirements.txt
#RUN pip install --upgrade pip
RUN pip install discord.py
RUN pip install prometheus-client

COPY . .
COPY config.docker.py config.py

RUN chmod +x /app/*

CMD [ "python3", "index.py"]
