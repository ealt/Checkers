import unittest

from agent import Agent, PreprogrammedAgent, RandomAgent
from checkersstate import State, CheckersState


class DummyState(State):
    def __init__(self, active_player=None, state_subtree={}, score=None,
                 **kwargs):
        self._active_player = active_player
        self._state_subtree = state_subtree
        self.score = score

    def active_player(self):
        return self._active_player

    def actions(self):
        return self._state_subtree.keys()

    def result(self, action):
        return DummyState(**self._state_subtree[action])

    def is_terminal(self):
        return len(self._state_subtree) == 0

    def outcome(self):
        return self.score


class CheckersStateTest(unittest.TestCase):

    def test_base_agent(self):
        with self.assertRaises(NotImplementedError):
            Agent().get_action(CheckersState())

    def test_preprogrammed_agent(self):
        available_actions = [1, 2, 3]
        state_subtree = {action: {} for action in available_actions}
        state = DummyState(state_subtree=state_subtree)
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