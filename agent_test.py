import unittest

from agent import Agent, BFSAgent, GreedyAgent, PreprogrammedAgent, RandomAgent
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


class AgentTest(unittest.TestCase):

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

    def test_greedy_agent(self):
        agent = GreedyAgent(score=lambda state: state.score)
        state = DummyState(state_subtree={1: {'score': 2},
                                          2: {'score': 3},
                                          3: {'score': 1}})
        self.assertEqual(agent.get_action(state), 2)

    def test_random_agent(self):
        state = CheckersState()
        self.assertIn(RandomAgent().get_action(state), state.actions())

    def test_bfs_agent(self):
        # state tree based on: https://www.endtoend.ai/assets/mooc/aind/13/3_player_tree.png
        # active player does not cycle with each action
        state_tree = {
            'active_player': 0,
            'score': (7, 7, 1),
            'state_subtree': {
                'a': {
                    'active_player': 2,
                    'score': (1, 2, 6),
                    'state_subtree': {
                        'a': {
                            'active_player': 2,
                            'score': (1, 2, 6),
                            'state_subtree': {
                                'a': {'score': (1, 2, 6)},
                                'b': {'score': (4, 2, 3)}
                            }
                        },
                        'b': {
                            'active_player': 1,
                            'score': (7, 4, 1),
                            'state_subtree': {
                                'a': {'score': (6, 1, 2)},
                                'b': {'score': (7, 4, 1)}
                            }
                        }
                    }
                },
                'b': {
                    'active_player': 0,
                    'score': (7, 7, 1),
                    'state_subtree': {
                        'a': {
                            'active_player': 2,
                            'score': (1, 5, 2),
                            'state_subtree': {
                                'a': {'score': (5, 1, 1)},
                                'b': {'score': (1, 5, 2)}
                            }
                        },
                        'b': {
                            'active_player': 0,
                            'score': (7, 7, 1),
                            'state_subtree': {
                                'a': {'score': (7, 7, 1)},
                                'b': {'score': (5, 4, 5)}
                            }
                        }
                    }
                }
            }
        }
        score = lambda state: state.score

        state = DummyState(**state_tree)
        agent = BFSAgent(score=score, max_depth=3)
        self.assertEqual(agent.get_action(state), 'b')

        state = state.result('a')
        agent = BFSAgent(score=score, max_depth=3)
        self.assertEqual(agent.get_action(state), 'a')


if __name__ == '__main__':
    unittest.main()