FROM python:3.9.5-slim

WORKDIR app/
RUN apt-get update && \
      apt-get -y install libpq-dev python3-dev gcc

COPY data_management_exercises data_management_exercises
COPY requirements.txt requirements.txt 
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR data_management_exercises/
