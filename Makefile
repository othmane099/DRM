PYTHON=./.venv/bin/python

PHONY = help install install-dev format lint type-check secure migrations migrate

help:
	@echo "---------------HELP-----------------"
	@echo "To install the project type -> make install"
	@echo "To install the project for development type -> make install-dev"
	@echo "To format code type -> make format"
	@echo "To check linter type -> make lint"
	@echo "To run type checker -> make type-check"
	@echo "To run all security related commands -> make secure"
	@echo "To create database migrations -> make migrations"
	@echo "To run database migrations -> make migrate"
	@echo "------------------------------------"

install:
	uv pip install .

install-dev:
	uv pip install --group dev

format:
	${PYTHON} -m isort src --force-single-line-imports
	${PYTHON} -m autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place src --exclude=__init__.py
	${PYTHON} -m black src --config pyproject.toml
	${PYTHON} -m isort src

lint:
	${PYTHON} -m flake8 --max-complexity 5 --max-cognitive-complexity=3 --max-line-length=88 --ignore=E402 src
	${PYTHON} -m black src --check --diff --config pyproject.toml
	${PYTHON} -m isort src --check --diff

type-check:
	${PYTHON} -m mypy --check-untyped-defs src

secure:
	${PYTHON} -m bandit -r src --config pyproject.toml

run:
	${PYTHON} -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

migrations:
	alembic -c alembic.ini revision --autogenerate

migrate:
	alembic -c alembic.ini upgrade head