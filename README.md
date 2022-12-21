
[![Coverage Status](https://coveralls.io/repos/github/bcorfman/alex/badge.svg?branch=main)](https://coveralls.io/github/bcorfman/alex?branch=main)
[![Main branch](https://github.com/bcorfman/alex/actions/workflows/build-test.yml/badge.svg)
[![Open in Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=387066048&machine=standardLinux32gb&devcontainer_path=.devcontainer%2Fdevcontainer.json&location=EastUs)
# ALEX (Artificial Life EXperiment)
A game I designed for my Commodore 128 back in the day, but I didn't really have enough experience back then to make it work. 
Now I'm finishing it in Python with some basic terminal graphics, at least for now until I can get the play mechanics where I want them.

<img src="graphics/alex_console.png">

## Prerequisites
* Install [Python](https://www.python.org) 3.9 or higher
* Install [Poetry](https://python-poetry.org)
* At a command prompt in the project directory, type `poetry install` to set up dependencies

## To run the tests
EITHER
* Click the *Open in GitHub Codespaces* badge above to start Visual Studio Code, click the Testing button in the left-hand pane, and click the Run Tests button to execute the ALEX test suite.

OR
* At a command prompt in the project directory, type `poetry run pytest'.

## To run the game
EITHER
* Start the Visual Studio Code editor in Codespaces, bring up the Terminal window at the bottom, and type `poetry run python main.py`.

OR
* At a command prompt in the project directory, type `poetry run python main.py'.

## Game instructions
* Click anywhere on the map to move the player to that location.
* Hit the "q" key to quit the game.
* Yes, it's a prototype.
