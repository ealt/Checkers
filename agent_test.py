import unittest

from agent import Agent, PreprogrammedAgent, RandomAgent
from checkersstate import State, CheckersState


class DummyState(State):
    def __init__(self, available_actions):
        self._available_actions = available_actions

    def active_player(self):
        pass

    def actions(self):
        return self._available_actions

    def result(self, action):
        pass

    def is_terminal(self):
        pass

    def outcome(self):
        pass

class CheckersStateTest(unittest.TestCase):

    def test_base_agent(self):
        with self.assertRaises(NotImplementedError):
            Agent().get_action(CheckersState())

    def test_preprogrammed_agent(self):
        available_actions = [1, 2, 3]
        state = DummyState(available_actions)
        preprogrammed_actions = [2, 1, 1, 3, 2, 3]
        agent = PreprogrammedAgent(preprogrammed_actions)
        for expected_action in preprogrammed_actions:
            self.assertEqual(agent.get_action(state), expected_action)
        
        invalid_action = 4
        with self.assertRaises(AssertionError):
            PreprogrammedAgent([invalid_action]).get_action(state)

    def test_random_agent(self):
        state = CheckersState()
        self.assertIn(RandomAgent().get_action(state), state.actions())


if __name__ == '__main__':
    unittest.main()