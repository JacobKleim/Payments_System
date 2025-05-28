FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"


RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    curl \
    && apt-get clean


RUN pip install --upgrade pip && \
    pip install pipx && \
    pipx install poetry

WORKDIR /app


COPY pyproject.toml poetry.lock /app/


RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi


COPY app /app
