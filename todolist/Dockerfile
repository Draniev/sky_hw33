FROM python:3.11-slim

WORKDIR /home/todolist

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./todolist/requirements.txt ./todolist/requirements.txt
RUN pip install -r ./todolist/requirements.txt
COPY . .

# CMD ./todolist/manage.py runserver 0.0.0.0:8000
