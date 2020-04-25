from random import choice

class Agent:
    def get_action(self, state):
        raise NotImplementedError


class RandomAgent(Agent):
    def get_action(self, state):
        return choice(state.actions())