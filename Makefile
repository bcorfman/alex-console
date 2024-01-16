SHELL := env PYTHON_VERSION=$(PYTHON_VERSION) /bin/bash
.SILENT: install test lint format
PYTHON_VERSION ?= 3.12

install:
	curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash
	$(HOME)/.rye/shims/rye pin $(PYTHON_VERSION)
	$(HOME)/.rye/shims/rye sync

test:
	$(HOME)/.rye/shims/rye run pytest --cov-branch --cov-report term --cov=game tests/
	rm .coverage*

lint:
	$(HOME)/.rye/shims/rye run flake8 --max-line-length=120 --max-complexity=10 

format:
	$(HOME)/.rye/shims/rye run yapf --in-place --recursive main.py ./tests ./game

run:
	$(HOME)/.rye/shims/rye run alex
	
all: install lint test