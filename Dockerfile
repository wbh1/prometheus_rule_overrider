FROM python:3.8-alpine
LABEL maintainer="wbhegedus@liberty.edu"

WORKDIR /vetoer
COPY . /vetoer

RUN apk update && \
    apk add --no-cache python3-dev && \
    pip3 install 'pipenv==2018.11.26' && \
    pipenv install --system && \
    pip3 uninstall --yes pipenv && \
    apk del python3-dev


ENTRYPOINT python3 /vetoer/generate.py