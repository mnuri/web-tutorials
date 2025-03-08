FROM python:3.13-slim

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE 1 \
    CRYPTOGRAPHY_DONT_BUILD_RUST 1

RUN apt-get update \
    && apt-get install -y libmagic1 gcc build-essential nodejs curl ca-certificates --no-install-recommends \
    && pip install --upgrade --no-cache-dir pip wheel setuptools poetry

WORKDIR /app

# install uv package manager
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

# will be cached if no changes in this files
COPY uv.lock .
COPY pyproject.toml .

COPY /scripts/start.sh /start.sh
COPY /scripts/wait-for-it.sh /wait-for-it.sh

RUN chmod +x /start.sh \
    && chmod +x /wait-for-it.sh \
    && uv sync --frozen --no-cache --no-editable \
    && useradd -m backend \
    && chown -R backend:backend /app \
    && mkdir /static \
    && chown -R backend:backend /static

COPY backend .

# Establish the runtime user (with no password and no sudo)
USER backend
