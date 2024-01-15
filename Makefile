SHELL := /bin/bash
.SILENT: install test lint format


install:
	curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash
	source "${HOME}/.rye/env" && rye sync

test:
	rye run pytest --cov-branch --cov-report term --cov=game tests/
	rm .coverage*

lint:
	rye run flake8 --max-line-length=120 --max-complexity=10 

format:
	rye run yapf --in-place --recursive --style pep8 *.py

run:
	rye run alex
	
all: install lint test