# Checkers
This project implements a checkers environment suitable for use by computer agents or human player (with an appropriate UI).

## Checkers overview
If you are completely unfamiliar with checkers, you can read the following [wikipeidia article](https://en.wikipedia.org/wiki/Draughts) for an introduction.

Notable choices made for this implementation include:
* the default starting state is
  * an 8x8 board
  * the two players have 3 rows of ordinary pieces (12 total) on opposite ends of the board
* when an ordinary piece reaches the opposite end (row) of the board, it is promoted to a king and can move in any direction
* if at the start of their turn the active player is capable of making a jump move, they are required to make a jump move
* after an initial jump, the piece that performed a jump must continue making jump moves as long as they are available
* if a player does not have any available actions, their turn is passed
* if neither player has any available actions, the game ends in a draw

## Getting started
The environment can be installed cloning this project:
```
$ git clone https://github.com/ealt/Checkers.git
```
The code was developed using **Python 3.5.4**, to ensure it works for your system you can run the suite of unit tests:
```
$ python checkerstate_test.py
```