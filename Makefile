.SILENT: install test lint format

install:
	/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	brew install rye
	rye sync

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