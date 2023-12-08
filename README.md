# ALEX (Artificial Life EXperiment)


[![Coverage Status](https://coveralls.io/repos/github/bcorfman/alex/badge.svg?branch=main)](https://coveralls.io/github/bcorfman/alex?branch=main)
![Main branch](https://github.com/bcorfman/alex/actions/workflows/build-test.yml/badge.svg)
[![Open in Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=387066048&machine=standardLinux32gb&devcontainer_path=.devcontainer%2Fdevcontainer.json&location=EastUs)

A game I designed for my Commodore 128 back in the day, but I didn't really have enough experience back then to make it work. 
Now I'm finishing it in Python with some basic terminal graphics, at least for now until I can get the play mechanics where I want them.

<img src="graphics/alex_console.png">

## Prerequisites
* Click on the *Open with GitHub Codespaces* badge above to launch the project in a browser or on your desktop inside Visual Studio Code.

OR

* Install [Python](https://www.python.org) 3.9 or higher
* At a command prompt in the project directory, type `make install` to set up the project

## To run the tests
* In Visual Studio Code, click the Testing button in the left-hand pane, and click the Run Tests button to execute the ALEX test suite.

OR
* At a command prompt in the project directory, type `make test`.

## To run the game
* In Visual Studio Code, bring up the Terminal window at the bottom, and type `make run`.

OR
* At a command prompt in the project directory, type `make run`.

## Game instructions
* Click anywhere on the map with the mouse to move the player to that location.
* Hit the `q` key to quit the game.
* Yes, it's a prototype.
