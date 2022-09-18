FROM python:3.10-alpine3.16
LABEL maintainer="ksulldev.space"

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /tmp
COPY ./core /backend

WORKDIR /backend

EXPOSE 8000

# create venv, install requirements, and create new user to avoid using Root
RUN python -m venv /py &&\
    /py/bin/pip install --upgrade pip &&\
    /py/bin/pip install -r /tmp/requirements.txt &&\
    rm -rf /tmp &&\
    adduser --disabled-password --no-create-home django-user

# Add path to $PATH so to check here first
ENV PATH="/py/bin:$PATH"

# Switch users to avoid using Root
USER django-user