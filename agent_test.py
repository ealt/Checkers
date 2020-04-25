import unittest

from agent import Agent
from checkersstate import CheckersState


class CheckersStateTest(unittest.TestCase):

    def test_base_agent(self):
        with self.assertRaises(NotImplementedError):
            Agent().get_action(CheckersState())

if __name__ == '__main__':
    unittest.main()