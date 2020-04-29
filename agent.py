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


class GreedyAgent(Agent):
    def __init__(self, score):
        self._score = score
    
    def get_action(self, state):
        return max(state.actions(),
                   key=lambda action: self._score(state.result(action)))


class HumanCheckersAgent(Agent):
    def get_action(self, state):
        self._num_rows = state._board.shape[0]
        state.visualize()
        actions = state.actions()
        print('\n'.join([str(i + 1) + ': ' + self._describe(action)
                         for i, action in enumerate(actions)]))
        selection = int(input('Choose an action from the list above: '))
        assert(0 < selection <= len(actions))
        return actions[selection - 1]
    
    def _describe(self, action):
        old_piece_pos, new_piece_pos, jumped_piece_pos = action
        if jumped_piece_pos:
            return ('Jump from ' + self._get_label(old_piece_pos)
                    + ' to ' + self._get_label(new_piece_pos)
                    + ' over '+ self._get_label(jumped_piece_pos))
        else:
            return ('Move from ' + self._get_label(old_piece_pos)
                    + ' to ' + self._get_label(new_piece_pos))
    
    def _get_label(self, pos):
        row, col = pos
        col *= 2
        if row % 2 == 0:
            col += 1
        row_label = str(self._num_rows - row)
        col_label = chr(65 + col)
        return col_label + row_label
