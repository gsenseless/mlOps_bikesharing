#!/bin/bash
uv pip install pre-commit black flake8 isort
# Install pre-commit hooks
uv run pre-commit install
