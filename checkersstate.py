import utils


class CheckersState:

    def __init__(self, board=utils.default_board):
        self._board = board

    def visualize(self):
        utils.visualize(self._board)


if __name__ == '__main__':
    cs = CheckersState()
    cs.visualize()