.SILENT: install test lint format

install:
	python -m pip install --upgrade pip
	pip install poetry
	poetry config virtualenvs.in-project true
	poetry config virtualenvs.prefer-active-python true 
	poetry install --no-root

test:
	poetry run pytest --cov-branch --cov-report term --cov-report lcov --cov=game tests/
	rm .coverage*

lint:
	poetry run flake8 --max-line-length=120 --max-complexity=10 

format:
	poetry run yapf --in-place --recursive --style pep8 *.py

run:
	poetry run python main.py
	
all: install lint test