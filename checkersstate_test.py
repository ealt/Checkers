import unittest

from checkersstate import CheckersState


class CheckersStateTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tiny_board = [[    0,    2],
                      [-1,   -1   ],
                      [    0,    1],
                      [-2,    1   ]]
        self._tiny_state = CheckersState(tiny_board)
        small_board = [[    0,    0,    0],
                       [-1,    0,    1   ],
                       [   -1,   -1,    0],
                       [ 0,    2,   -1   ],
                       [   -1,   -1,    0],
                       [-2,    0,    1   ]]
        self._small_state = CheckersState(small_board)
        terminal_board_1 = [[    0,    0],
                            [-1,   -1   ],
                            [    0,    0],
                            [-2,    0   ]]
        self._terminal_state_1 = CheckersState(terminal_board_1)
        terminal_board_2 = [[    0,    2],
                            [ 0,    0   ],
                            [    0,    1],
                            [ 0,    1   ]]
        self._terminal_state_2 = CheckersState(terminal_board_2)

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
        self.assertDictEqual(self._tiny_state._moves, expected_moves)

    def test_get_positions(self):
        expected_positions = (set([(0, 1), (2, 1), (3, 1)]),
                              set([(1, 0), (1, 1), (3, 0)]))
        self.assertCountEqual(self._tiny_state._positions, expected_positions)

    def test_is_terminal(self):
        self.assertFalse(self._tiny_state.is_terminal())
        self.assertFalse(self._small_state.is_terminal())
        self.assertTrue(self._terminal_state_1.is_terminal())
        self.assertTrue(self._terminal_state_2.is_terminal())

    def test_actions(self):
        self._tiny_state._active_player = 0
        expected_actions = [((0, 1), (2, 0), (1, 1)),
                            ((2, 1), (0, 0), (1, 1)),
                            ((3, 1), (2, 0), None)]
        self.assertCountEqual(self._tiny_state.actions(), expected_actions)
        self._tiny_state._active_player = 1
        expected_actions = [((1, 0), (2, 0), None),
                            ((1, 1), (2, 0), None),
                            ((3, 0), (2, 0), None)]
        self.assertCountEqual(self._tiny_state.actions(), expected_actions)
        self._small_state._active_player = 0
        expected_actions = [((1, 2), (0, 1), None),
                            ((1, 2), (0, 2), None),
                            ((5, 2), (4, 2), None)]
        self._small_state._active_player = 1
        expected_actions = [((2, 0), (3, 0), None),
                            ((3, 2), (4, 2), None),
                            ((4, 0), (5, 1), None),
                            ((4, 1), (5, 1), None)]


if __name__ == '__main__':
    unittest.main()
