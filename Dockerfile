FROM python:3.9.4-slim-buster

RUN apt-get update # update container packages

RUN pip install --upgrade pip # update pip

COPY . /lucid-bot 

RUN cd /lucid-bot && pip install -r requirements.txt # install dependancies

RUN cd /lucid-bot && chmod +x main.py # make main.py executable

CMD cd /lucid-bot && ./main.py # run bot
