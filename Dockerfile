FROM python:3.9.4-slim-buster

WORKDIR /lucid-bot

RUN apt-get update # update container packages

RUN pip install --upgrade pip # update pip

COPY . . # copy project to /lucid-bot

RUN pip install -r requirements.txt # install dependancies

RUN chmod +x main.py # make main.py executable

CMD ./main.py # run bot
