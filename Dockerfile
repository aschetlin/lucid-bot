FROM python:3.9.4-slim-buster

WORKDIR /lucid-bot

RUN apt-get update

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x main.py

CMD ["./main.py"]
