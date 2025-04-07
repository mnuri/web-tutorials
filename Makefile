.PHONY: static


base_compose_path = "run-base-services.yml"
backend_docker_compose_path = "run-backend-services.yml"
broker_docker_compose_path = "run-broker-services.yml"
s3_docker_compose_path = "run-s3-service.yml"
nginx_docker_compose_path = "run-nginx-service.yml"

BASE_DC = docker compose
BASE_DC += -f $(base_compose_path)
BASE_DC += -f $(backend_docker_compose_path)
# BASE_DC += -f $(broker_docker_compose_path)
BASE_DC += -f $(s3_docker_compose_path)
BASE_DC += -f $(nginx_docker_compose_path)
PYTHONPATH = ./django


build-no-cache:
	$(BASE_DC) build --no-cache

build:
	$(BASE_DC) build

up:
	$(BASE_DC) up -d

down:
	$(BASE_DC) down --remove-orphans

# Tools

image-build:
	DOCKER_BUILDKIT=1 docker build \
		--platform=linux/amd64 \
		-f Dockerfile \
		-t test-image .

# Development

format: # format your code according to project linter tools
	uv run ruff check
	uv run ruff format
	uv run isort .

ruff:
	uv run ruff check
	uv run ruff format

isort:
	uv run isort --check django

flake8:
	uv run flake8 --inline-quotes '"'

pylint:
	PYTHONPATH=$(PYTHONPATH) uv run pylint --load-plugins pylint_django django

mypy:
	PYTHONPATH=$(PYTHONPATH) uv run mypy --namespace-packages --show-error-codes --check-untyped-defs --ignore-missing-imports --show-traceback django

lint: ruff isort flake8 # pylint mypy

pip-audit:
	uv run pip-audit

test:
	PYTHONPATH=$(PYTHONPATH) uv run pytest -n 2

sync-deps:
	uv sync --frozen --no-cache --no-editable

all: format lint test pip-audit

# CI

ci-lint: sync-deps lint

ci-test: sync-deps test

ci-deps-audit: sync-deps pip-audit

# Pre-commit

pre-commit-install:
	uv tool install pre-commit
	uv run pre-commit install

pre-commit: all
