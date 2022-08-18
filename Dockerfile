FROM python:3.9.5-slim

WORKDIR app/
RUN apt-get update && \
      apt-get -y install libpq-dev python3-dev gcc

COPY ginlong_data_processing ginlong_data_processing
COPY requirements.txt requirements.txt 
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR ginlong_data_processing/
RUN adduser initial_load_user
RUN adduser dbt_execution_user