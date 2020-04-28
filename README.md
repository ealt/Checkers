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
$ python gamecontroller_test.py
```

## Playing a game
gamecontroller.py defines the `GameController` glass.
To coordinate a game between a pair of agents, create an instance of `GameController` passing in the arguments:
* `state`: accepts an instance of a game state (described in the Checkers State section below) as the initial state of the game
* `agents`: appects a pair of two agent instances as opposing players in the game
After creating a `GameController` instance, call the method `play_game()` to simulate a game to completion. The controller will solicit actions from each agent when it is their turn and use those actions to evolve tha game state until a terminal state is reached. At that point, the method will return the final game state outcome.

By default, simply running gameconroller.py from the command line:
```
$ python gamecontroller.py
```
will start a standard game of checkers between two human players who select from available actions presented to them in the command line for each state.

## Checkers State

# Creating a game state
checkersstate.py defines the `CheckersState` class.
To simulate play, start by creating an initial `CheckersState` game state. With no arguments, the default starting state described in the overview is created. The following optional arguments can be used to create different states:
* `board`: accepts a rectangular numeric list or array
  * passing an rxc array creates an rx2c board 
  * rows in the array correspond to rows of the board
  * columns are represented in a compressed format, removing inacessible spaces
  * the values in the array (coerced to integers) denote the occupancy of each space on the board
    * zeros are empty spaces
    * positive numbers are pieces belonging to player 0
    * negative numbers are pieces belonging to player 1
    * pieces with an absolute value of 1 are ordinary pieces (must advance forward)
    * pieces with absolute values greater than 1 are king pieces (can move in any direction)
* `active_player`: can be 0 (default) or 1 to denote whose turn it is
* `jump_piece`: can be None (default) or the board position tuple for a piece that just completed a jump
For example:
```
my_state = CheckersState(board=[[    2,    0],  # 5x2 array creates a 5x4 board
                                [-1,    0   ],  # an ordinary piece belonging to player 1 at position (1, 0)
                                [   -1,    0],  # row 2, the space at position (2, 1) is empty
                                [-2,    1   ],  # player 1 king, player 0 ordinary piece
                                [    1,    0]], # even rows shift right, odd rows shift left
                         active_player=1,       # it is player 1's turn
                         jump_piece=(2, 0))     # the piece at (2, 0) just made a jump, in this state
                                                #   player 1 must use this piece to make the jump to (4, 1)
```

# Interacting with a game state
Game controllers and agents can observe and act in a state as follows:
* `my_state.active_player()`: returns the identity of the active player in the state (0 or 1)
* `my_state.actions()`: returns the list of actions available to the active player. Each action has 3 elements:
  * the position of the piece that would move
  * the new position of the piece after the move
  * the position of an opponent's piece that is jumped (or None)
* `my_state.outcome(action)`: returns the state resulting the active player taking the action `action`
* `my_state.is_terminal()`: returns a boolean indicating whether the state is a terminal game state
* `my_state.outcome()`: returns a tuple with the payoffs for player 0 and 1 respectively. the values can be:
  * `0`: if the game has not ended, or it has ended in a draw
  * `1`: the player won the game
  * `-1`: the player lost the game
* `my_state.visualize()`: prints a human readable depiction of the board to stdout