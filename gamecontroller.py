from agent import Agent, HumanCheckersAgent
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


if __name__ == '__main__':
    gc = GameController(CheckersState(),
                        [HumanCheckersAgent(), HumanCheckersAgent()])
    outcome = gc.play_game()
    gc._state.visualize()
    if outcome == (1, -1):
        print('Player 1 wins!')
    elif outcome == (-1, 1):
        print('Player 2 wins!')
    elif outcome == (0, 0):
        print('The game is a draw.')