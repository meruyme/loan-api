FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENV TZ="America/Recife"

WORKDIR /code
RUN python3 -m venv /code/venv

COPY ./requirements.txt /code/
RUN pip3 install -r requirements.txt