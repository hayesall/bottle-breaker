.PHONY: lint style build test

## Run linting and check code formatting
lint:
	ruff .
	isort --check .
	black --check .

## Style code for consistency
style:
	isort .
	black .

## Build dependencies
build:
	pip-compile --allow-unsafe --resolver=backtracking --generate-hashes --output-file=requirements.txt pyproject.toml
	pip-compile --allow-unsafe --resolver=backtracking --generate-hashes --extra=dev --output-file=requirements-dev.txt pyproject.toml

## Run unit tests
test:
	pytest --cov=bottle_breaker .
