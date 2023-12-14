FROM python:3.11.5-slim-bullseye
ENV PIP_DISABLE_PIP_VERSION_CHECK true
ENV PYTHONDONTWRITEBYTECODE true
ENV PYTHONUNBUFFERED true
WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .