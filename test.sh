#!/bin/bash
poetry run pytest --cov . --cov-report html --flake8 --mypy --black
