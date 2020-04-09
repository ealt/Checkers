import utils


class CheckersState:

    def __init__(self, board=utils.default_board):
        self._board = board
        self._get_positions()

    def _get_positions(self):
        self._positions = (set(), set())
        for r, row in enumerate(self._board):
            for c, identity in enumerate(row):
                if identity != 0:
                    player = 0 if identity > 0 else 1
                    self._positions[player].add((r, c))

    def visualize(self):
        utils.visualize(self._board)


if __name__ == '__main__':
    cs = CheckersState()
    cs.visualize()