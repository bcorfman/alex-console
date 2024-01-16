# ALEX (Artificial Life EXperiment)


[![Coverage Status](https://coveralls.io/repos/github/bcorfman/alex/badge.svg?branch=main)](https://coveralls.io/github/bcorfman/alex?branch=main)
![Main branch](https://github.com/bcorfman/alex-console/actions/workflows/build-test.yml/badge.svg)

A game I designed for my Commodore 128 back in the day, but I didn't really have enough experience back then to make it work. 
Now I'm finishing it in Python with some basic terminal graphics, at least for now until I can get the play mechanics where I want them.

<img src="graphics/alex_console.png">

## Prerequisites
* At a command prompt in the project directory, type `make install` to set up the project

## To run the tests
* At a command prompt in the project directory, type `make test`.

## To run the game
* At a command prompt in the project directory, type `make run`.

## Game instructions
* Click anywhere on the map with the mouse to move the player to that location.
* Hit the `q` key to quit the game.
* Yes, it's a prototype.

## Notes for Visual Studio Code users
* I've included some extension recommendations that can make your development easier: [Run On Save](https://marketplace.visualstudio.com/items?itemName=emeraldwalk.RunOnSave) and [Make support and task provider](https://marketplace.visualstudio.com/items?itemName=carlos-algms.make-task-provider).
* These recommendations will pop up when opening the project inside VSCode.
* Installing both extensions will 1) use the code in settings.json to run "make format" on each File:Save, and 2) display available Make targets within the "Makefile Tasks" sidebar pane and allow them to be run with a mouse click.
