import unittest

from checkersstate import CheckersState


class CheckersStateTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        test_board = [[0, 2], [-1, -1], [0, 1], [-1, 1]]
        self._cs = CheckersState(test_board)

    def test_get_moves(self):
        expected_moves = {
            (0, 0): ([],
                     [((1, 0), None), ((1, 1), (2, 1))]),
            (0, 1): ([],
                     [((1, 1), (2, 0))]),
            (1, 0): ([((0, 0), None)],
                     [((2, 0), (3, 1))]),
            (1, 1): ([((0, 0), None), ((0, 1), None)],
                     [((2, 0), (3, 0)), ((2, 1), None)]),
            (2, 0): ([((1, 0), None), ((1, 1), (0, 1))],
                     [((3, 0), None), ((3, 1), None)]),
            (2, 1): ([((1, 1), (0, 0))],
                     [((3, 1), None)]),
            (3, 0): ([((2, 0), (1, 1))],
                     []),
            (3, 1): ([((2, 0), (1, 0)), ((2, 1), None)],
                     [])
        }
        self.assertDictEqual(self._cs._moves, expected_moves)

    def test_get_positions(self):
        expected_positions = (set([(0, 1), (2, 1), (3, 1)]),
                              set([(1, 0), (1, 1), (3, 0)]))
        self.assertCountEqual(self._cs._positions, expected_positions)


if __name__ == '__main__':
    unittest.main()
