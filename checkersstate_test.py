import unittest

from checkersstate import CheckersState


class CheckersStateTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_get_moves(self):
        board = [[    0,    2],
                 [-1,   -1   ],
                 [    0,    1],
                 [-2,    1   ]]
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
        self.assertDictEqual(CheckersState(board)._moves, expected_moves)

    def test_get_positions(self):
        board = [[    0,    2],
                 [-1,   -1   ],
                 [    0,    1],
                 [-2,    1   ]]
        expected_positions = (set([(0, 1), (2, 1), (3, 1)]),
                              set([(1, 0), (1, 1), (3, 0)]))
        self.assertCountEqual(CheckersState(board)._positions,
                              expected_positions)

    def test_is_terminal(self):
        midgame_board = [[    0,    2],
                         [-1,   -1   ],
                         [    0,    1],
                         [-2,    1   ]]
        self.assertFalse(CheckersState(midgame_board).is_terminal)

        draw_board = [[   0,    0,     0],
                      [-1,   -1,   -1   ],
                      [   -1,   -1,   -1],
                      [ 1,    1,    1   ],
                      [    1,    1,    1],
                      [ 0,    0,    0   ]]
        self.assertTrue(CheckersState(draw_board).is_terminal)
        
        player_0_win_board = [[    0,    2],
                              [ 0,    0   ],
                              [    0,    1],
                              [ 0,    1   ]]
        self.assertTrue(CheckersState(player_0_win_board).is_terminal)

        player_1_win_board = [[    0,    0],
                              [-1,   -1   ],
                              [    0,    0],
                              [-2,    0   ]]
        self.assertTrue(CheckersState(player_1_win_board).is_terminal)

    def test_outcome(self):
        midgame_board = [[    0,    2],
                         [-1,   -1   ],
                         [    0,    1],
                         [-2,    1   ]]
        expected_midgame_outcome = (0, 0)
        self.assertTupleEqual(CheckersState(midgame_board).outcome(),
                              expected_midgame_outcome)

        draw_board = [[   0,    0,     0],
                      [-1,   -1,   -1   ],
                      [   -1,   -1,   -1],
                      [ 1,    1,    1   ],
                      [    1,    1,    1],
                      [ 0,    0,    0   ]]
        expected_draw_outcome = (0, 0)
        self.assertTupleEqual(CheckersState(draw_board).outcome(),
                              expected_draw_outcome)

        player_0_win_board = [[    0,    2],
                              [ 0,    0   ],
                              [    0,    1],
                              [ 0,    1   ]]
        expected_player_0_win_outcome = (1, -1)
        self.assertTupleEqual(CheckersState(player_0_win_board).outcome(),
                              expected_player_0_win_outcome)

        player_1_win_board = [[    0,    0],
                              [-1,   -1   ],
                              [    0,    0],
                              [-2,    0   ]]
        expected_player_1_win_outcome = (-1, 1)
        self.assertTupleEqual(CheckersState(player_1_win_board).outcome(),
                              expected_player_1_win_outcome)

    def test_actions(self):
        draw_board = [[   0,    0,     0],
                      [-1,   -1,   -1   ],
                      [   -1,   -1,   -1],
                      [ 1,    1,    1   ],
                      [    1,    1,    1],
                      [ 0,    0,    0   ]]
        expected_draw_actions = []
        self.assertCountEqual(CheckersState(board=draw_board,
                                            active_player=0).actions,
                              expected_draw_actions)
        self.assertCountEqual(CheckersState(board=draw_board,
                                            active_player=1).actions,
                              expected_draw_actions)

        tiny_board = [[    0,    2],
                      [-1,   -1   ],
                      [    0,    1],
                      [-2,    1   ]]
        expected_player_0_actions = [((0, 1), (2, 0), (1, 1)),
                                     ((2, 1), (0, 0), (1, 1)),
                                     ((3, 1), (2, 0), None)]
        self.assertCountEqual(CheckersState(board=tiny_board,
                                            active_player=0).actions,
                              expected_player_0_actions)
        expected_player_1_actions = [((1, 0), (2, 0), None),
                                     ((1, 1), (2, 0), None),
                                     ((3, 0), (2, 0), None)]
        self.assertCountEqual(CheckersState(board=tiny_board,
                                            active_player=1).actions,
                              expected_player_1_actions)

        small_board = [[    0,    0,    0],
                       [-1,    0,    1   ],
                       [   -1,   -1,    0],
                       [ 0,    2,   -1   ],
                       [   -1,   -1,    0],
                       [-2,    0,    1   ]]
        expected_player_0_actions = [((1, 2), (0, 1), None),
                                     ((1, 2), (0, 2), None),
                                     ((5, 2), (4, 2), None)]
        self.assertCountEqual(CheckersState(board=small_board,
                                            active_player=0).actions,
                              expected_player_0_actions)
        expected_player_1_actions = [((2, 0), (3, 0), None),
                                     ((3, 2), (4, 2), None),
                                     ((4, 0), (5, 1), None),
                                     ((4, 1), (5, 1), None)]
        self.assertCountEqual(CheckersState(board=small_board,
                                            active_player=1).actions,
                              expected_player_1_actions)


if __name__ == '__main__':
    unittest.main()
