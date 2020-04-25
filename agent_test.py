import unittest

from agent import Agent, RandomAgent
from checkersstate import CheckersState


class CheckersStateTest(unittest.TestCase):

    def test_base_agent(self):
        with self.assertRaises(NotImplementedError):
            Agent().get_action(CheckersState())

    def test_random_agent(self):
        state = CheckersState()
        self.assertIn(RandomAgent().get_action(state), state.actions())


if __name__ == '__main__':
    unittest.main()