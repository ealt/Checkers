import unittest

from agent import PreprogrammedAgent
from checkersstate import CheckersState
from gamecontroller import GameController


class CheckersStateTest(unittest.TestCase):

    def test_constuctor(self):
        valid_state = CheckersState()
        invalid_state = 'not_a_state'
        valid_agents = [PreprogrammedAgent([]) for _ in range(2)]
        invalid_agents = ['not_an_agent' for _ in range(2)]
        _ = GameController(valid_state, valid_agents)

        with self.assertRaises(AssertionError):
            GameController(invalid_state, valid_agents)
        
        with self.assertRaises(AssertionError):
            GameController(valid_state, invalid_agents)

    def test_play_game(self):
        state = CheckersState(board=[[   -1,   -1],
                                     [ 0,    0   ],
                                     [    1,    1]])
        agents = [
            PreprogrammedAgent([
                ((2, 0), (1, 0), None),    # move 1
                ((2, 1), (1, 1), None),    # move 4
                ((1, 0), (0, 0), None),    # move 9
                ((0, 0), (1, 1), None)     # move 11

            ]),
            PreprogrammedAgent([
                ((0, 1), (1, 1), None),    # move 2
                ((1, 1), (2, 0), None),    # move 3
                ((2, 0), (0, 1), (1, 1)),  # move 5
                ((0, 1), (1, 1), None),    # move 6
                ((1, 1), (2, 1), None),    # move 7
                ((0, 0), (1, 1), None),    # move 8
                ((1, 1), (2, 0), None),    # move 10
                ((2, 0), (0, 1), (1, 1))   # move 12
            ])
        ]
        expected_outcome = (-1, 1)
        self.assertTupleEqual(GameController(state, agents).play_game(),
                              expected_outcome)


if __name__ == '__main__':
    unittest.main()
