from itertools import product
import numpy as np
import utils



class CheckersState:

    def __init__(self, board=utils.default_board):
        self._board = np.array(board, dtype=np.int32)
        self._get_positions()

    def _get_positions(self):
        self._positions = (set(), set())
        num_rows, num_cols = self._board.shape
        for position in product(range(num_rows), range(num_cols)):
            identity = self._board[position]
            if identity != 0:
                player = 0 if identity > 0 else 1
                self._positions[player].add(position)

    def visualize(self):
        utils.visualize(self._board)


if __name__ == '__main__':
    cs = CheckersState()
    cs.visualize()