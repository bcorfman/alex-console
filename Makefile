SHELL := env PYTHON_VERSION=$(PYTHON_VERSION) /bin/bash
.SILENT: install test lint format
PYTHON_VERSION ?= 3.12

install:
	curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash
	$(HOME)/.rye/shims/rye pin $(PYTHON_VERSION)
	$(HOME)/.rye/shims/rye sync --no-lock

test:
	$(HOME)/.rye/shims/rye run pytest tests/

lint:
	$(HOME)/.rye/shims/rye run pylint ./game 

format:
	$(HOME)/.rye/shims/rye run yapf --in-place --recursive main.py ./tests ./game

run:
	$(HOME)/.rye/shims/rye run alex
	
all: install lint test