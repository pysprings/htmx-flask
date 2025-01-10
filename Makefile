.PHONY: help install test fmt lint clean run start default

# Default target
default: help

# Variables with sane defaults
PYTHON ?= python
PYTEST_ARGS ?= -v
FLASK_ENV ?= development
FLASK_APP ?= run.py

## Install project dependencies
install:
	poetry install

## Run the test suite
test:
	poetry run pytest $(PYTEST_ARGS)

## Format code using black
fmt:
	poetry run black app tests

## Run all linters
lint: lint/flake8 lint/mypy

## Run flake8 linter
lint/flake8:
	poetry run flake8 app tests

## Run mypy type checker
lint/mypy:
	poetry run mypy app tests

## Clean up temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

## Run the Flask development server
start:
	poetry run flask --app $(FLASK_APP) run

## Run security audit
audit:
	poetry run safety scan
	poetry run bandit -r app

## This help screen
help:
	@printf "Available targets:\n\n"
	@awk '/^[a-zA-Z\-_0-9%:\\]+/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = $$1; \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			gsub("\\\\", "", helpCommand); \
			gsub(":+$$", "", helpCommand); \
			printf "  \x1b[32;01m%-35s\x1b[0m %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort -u
	@printf "\n"
