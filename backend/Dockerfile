FROM python:3.10.9-slim-buster

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

COPY requirements/ /tmp/requirements

RUN pip install -U pip && \
    pip install --no-cache-dir -r /tmp/requirements/dev.txt

COPY . /app
ENV PATH "$PATH:/app/scripts"

RUN useradd -m -d /app -s /bin/bash app \
    && chown -R app:app /app/* && chmod +x /app/scripts/* \
    && chmod +x /app/entrypoint.sh

WORKDIR /app
USER app

ENTRYPOINT ["/app/entrypoint.sh"]
