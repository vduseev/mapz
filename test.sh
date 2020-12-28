#!/bin/bash

# Run all tests
# poetry run pytest --cov . --cov-report html --flake8 --mypy --black

# Test Coverage
poetry run pytest --cov . --cov-report html

# MyPy
poetry run mypy mapz --strict

# Flake8
poetry run pytest --flake8


