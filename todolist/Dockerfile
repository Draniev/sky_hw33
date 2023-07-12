FROM python:3.11-slim

WORKDIR /home/todolist

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# CMD ./todolist/manage.py runserver 0.0.0.0:8000
