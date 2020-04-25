from random import choice

class Agent:
    def get_action(self, state):
        raise NotImplementedError


class PreprogrammedAgent(Agent):
    def __init__(self, actions):
        self._actions = actions[::-1]
    
    def get_action(self, state):
        action = self._actions.pop()
        assert(action in state.actions())
        return action


class RandomAgent(Agent):
    def get_action(self, state):
        return choice(state.actions())