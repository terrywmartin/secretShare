# syntax=docker/dockerfile:1
FROM python:3.10-slim



##COPY ./entrypoint.sh /entrypoint.sh
COPY ./requirements.txt /.


RUN apt-get update && \
    apt-get install -y  build-essential python3-dev python3-setuptools make gcc \
    && python3 -m pip install -r requirements.txt \
    && apt-get remove -y --purge make gcc build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . .

#RUN chmod +x entrypoint.sh

#CMD [ "./entrypoint.sh/" ]