from agent import Agent
from checkersstate import State, CheckersState

class GameController:
    def __init__(self, state, agents):
        assert(isinstance(state, State))
        self._state = state
        for agent in agents:
            assert(isinstance(agent, Agent))
        self._agents = agents
    
    def play_game(self):
        while not self._state.is_terminal():
            active_idx = self._state.active_player()
            action = self._agents[active_idx].get_action(self._state)
            self._state = self._state.result(action)
        return self._state.outcome()