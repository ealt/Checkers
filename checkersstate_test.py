import unittest

from checkersstate import CheckersState


class CheckersStateTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_constructor(self):
        uneven_board = [[0, 0, 0], [0, 0], [0]]
        with self.assertRaises(ValueError):
            CheckersState(board=uneven_board)
        
        str_board = [['black', 'black'], ['blank', 'blank'], ['red', 'red']]
        with self.assertRaises(ValueError):
            CheckersState(board=str_board)
        
        one_dim_board = [-1, -1, 0, 0, 1, 1]
        with self.assertRaises(AssertionError):
            CheckersState(board=one_dim_board)
        
        three_dim_board = [[[-1, -1], [0, 0]], [[0, 0], [1, 1]]]
        with self.assertRaises(AssertionError):
            CheckersState(board=three_dim_board)
        
        with self.assertRaises(AssertionError):
            CheckersState(active_player=2)

        board = [[    0,    2],
                 [ 0,    0   ],
                 [    0,    0],
                 [-2,    0   ]]
        with self.assertRaises(AssertionError):
            CheckersState(board=board, jump_piece=(0, 0))
        with self.assertRaises(AssertionError):
            CheckersState(board=board, active_player=0, jump_piece=(3, 0))
        with self.assertRaises(AssertionError):
            CheckersState(board=board, active_player=1, jump_piece=(0, 1))

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

    def test_get_pieces(self):
        board = [[    0,    2],
                 [-1,   -1   ],
                 [    0,    1],
                 [-2,    1   ]]
        expected_pieces = (set([(0, 1), (2, 1), (3, 1)]),
                           set([(1, 0), (1, 1), (3, 0)]))
        self.assertCountEqual(CheckersState(board)._pieces,
                              expected_pieces)

    def test_is_terminal(self):
        midgame_board = [[    0,    2],
                         [-1,   -1   ],
                         [    0,    1],
                         [-2,    1   ]]
        self.assertFalse(CheckersState(midgame_board).is_terminal())

        # both player still have pieces
        # active player does have any available actions
        # opponent does not have any available actions
        no_active_action_board = [[    0,    2],
                                  [-1,    0   ],
                                  [   -1,    1],
                                  [-2,    1   ]]
        no_active_action_state = CheckersState(no_active_action_board,
                                               active_player=1)
        self.assertFalse(no_active_action_state.is_terminal())
        self.assertEqual(no_active_action_state.active_player(), 0)

        # both player still have pieces
        # active player just made a jump, but does not have further jumps
        # opponent does have available actions
        postjump_board = [[    2,    2],
                          [-1,    0   ],
                          [    0,    0],
                          [-2,    1   ]]
        postjump_state = CheckersState(board=postjump_board, active_player=0,
                                       jump_piece=(0,0))
        self.assertFalse(postjump_state.is_terminal())
        self.assertEqual(postjump_state.active_player(), 1)
        self.assertIsNone(postjump_state._jump_piece)
        
        # both player still have pieces
        # active player just made a jump, but does not have further jumps
        # opponent does not have any available actions
        # active player does have avalable actions
        postjump_no_opponent_actions_board = [[    2,    2],
                                              [ 0,    0   ],
                                              [   -1,    0],
                                              [-2,    1   ]]
        postjump_no_opponent_actions_state = CheckersState(
                board=postjump_no_opponent_actions_board,
                active_player=0,
                jump_piece=(0,0))
        self.assertFalse(postjump_no_opponent_actions_state.is_terminal())
        self.assertEqual(postjump_no_opponent_actions_state.active_player(), 0)
        self.assertIsNone(postjump_no_opponent_actions_state._jump_piece)

        draw_board = [[    0,    0,    0],
                      [-1,   -1,   -1   ],
                      [   -1,   -1,   -1],
                      [ 1,    1,    1   ],
                      [    1,    1,    1],
                      [ 0,    0,    0   ]]
        self.assertTrue(CheckersState(draw_board).is_terminal())
        
        player_0_win_board = [[    0,    2],
                              [ 0,    0   ],
                              [    0,    1],
                              [ 0,    1   ]]
        self.assertTrue(CheckersState(player_0_win_board).is_terminal())

        player_1_win_board = [[    0,    0],
                              [-1,   -1   ],
                              [    0,    0],
                              [-2,    0   ]]
        self.assertTrue(CheckersState(player_1_win_board).is_terminal())

    def test_outcome(self):
        midgame_board = [[    0,    2],
                         [-1,   -1   ],
                         [    0,    1],
                         [-2,    1   ]]
        expected_midgame_outcome = (0, 0)
        self.assertTupleEqual(CheckersState(midgame_board).outcome(),
                              expected_midgame_outcome)

        draw_board = [[    0,    0,    0],
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
        draw_board = [[    0,    0,    0],
                      [-1,   -1,   -1   ],
                      [   -1,   -1,   -1],
                      [ 1,    1,    1   ],
                      [    1,    1,    1],
                      [ 0,    0,    0   ]]
        expected_draw_actions = []
        self.assertCountEqual(CheckersState(board=draw_board,
                                            active_player=0).actions(),
                              expected_draw_actions)
        self.assertCountEqual(CheckersState(board=draw_board,
                                            active_player=1).actions(),
                              expected_draw_actions)

        tiny_board = [[    0,    2],
                      [-1,   -1   ],
                      [    0,    1],
                      [-2,    1   ]]
        expected_player_0_actions = [((0, 1), (2, 0), (1, 1)),
                                     ((2, 1), (0, 0), (1, 1))]
        self.assertCountEqual(CheckersState(board=tiny_board,
                                            active_player=0).actions(),
                              expected_player_0_actions)
        expected_player_1_actions = [((1, 0), (2, 0), None),
                                     ((1, 1), (2, 0), None),
                                     ((3, 0), (2, 0), None)]
        self.assertCountEqual(CheckersState(board=tiny_board,
                                            active_player=1).actions(),
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
                                            active_player=0).actions(),
                              expected_player_0_actions)
        expected_player_1_actions = [((2, 0), (3, 0), None),
                                     ((3, 2), (4, 2), None),
                                     ((4, 0), (5, 1), None),
                                     ((4, 1), (5, 1), None)]
        self.assertCountEqual(CheckersState(board=small_board,
                                            active_player=1).actions(),
                              expected_player_1_actions)

    def test_jump_actions(self):
        board = [[    0,    0,    0],
                 [ 0,    0,    0   ],
                 [   -1,   -1,    0],
                 [ 0,    2,    0   ],
                 [    0,   -1,    0],
                 [ 0,    0,    0   ]]
        expected_player_0_actions = [((3, 1), (1, 0), (2, 0)),
                                     ((3, 1), (1, 2), (2, 1)),
                                     ((3, 1), (5, 2), (4, 1))]
        self.assertCountEqual(CheckersState(board=board, active_player=0,
                                            jump_piece=(3, 1)).actions(),
                              expected_player_0_actions)
        expected_player_1_actions = [((2, 1), (4, 0), (3, 1))]
        self.assertCountEqual(CheckersState(board=board, active_player=1,
                                            jump_piece=(2, 1)).actions(),
                              expected_player_1_actions)

    def test_result(self):
        initial_board = [[    0,    2],
                         [-1,   -1   ],
                         [    0,    1],
                         [-2,    1   ]]
        invalid_action = ((0, 1), (0, 0), (2, 0))
        with self.assertRaises(AssertionError):
            CheckersState(board=initial_board).result(invalid_action)
        move_action = ((1, 0), (2, 0), None)
        move_result_board = [[    0,    2],
                             [ 0,   -1   ],
                             [   -1,    1],
                             [-2,    1   ]]
        self.assertEqual(CheckersState(board=initial_board, active_player=1,
                                       jump_piece=None).result(move_action),
                         CheckersState(board=move_result_board, active_player=0,
                                       jump_piece=None))
        jump_action = ((0, 1), (2, 0), (1, 1))
        jump_result_board = [[    0,    0],
                             [-1,    0   ],
                             [    2,    1],
                             [-2,    1   ]]
        self.assertEqual(CheckersState(board=initial_board, active_player=0,
                                       jump_piece=None).result(jump_action),
                         CheckersState(board=jump_result_board, active_player=0,
                                       jump_piece=(2,0)))
        promotion_action = ((2, 1), (0, 0), (1, 1))
        promotion_result_board = [[    2,    2],
                                  [-1,    0   ],
                                  [    0,    0],
                                  [-2,    1   ]]
        self.assertEqual(CheckersState(board=initial_board, active_player=0,
                                       jump_piece=None).result(
                                           promotion_action),
                         CheckersState(board=promotion_result_board,
                                       active_player=0, jump_piece=(0, 0)))

    def test_eq(self):
        self.assertTrue(CheckersState() == CheckersState())


if __name__ == '__main__':
    unittest.main()
