from itertools import product
import copy
import numpy as np
import utils



class CheckersState:

    def __init__(self, board=utils.default_board, active_player=0,
                 jump_piece=None, **kwargs):
        self._board = np.array(board, dtype=np.int32)
        assert(len(self._board.shape) == 2)
        # pylint/issues/3139
        self._num_rows = self._board.shape[0]  # pylint: disable=E1136  
        self._num_cols = self._board.shape[1]  # pylint: disable=E1136
        assert(active_player in (0, 1))
        self._active_player = active_player
        self._get_moves()
        self._get_pieces()
        if jump_piece:
            assert(jump_piece in self._pieces[self._active_player])
        self._jump_piece = jump_piece
        self._get_actions()
        self._get_is_terminal()

    def _get_moves(self):
        self._moves = {}
        for position in product(range(self._num_rows), range(self._num_cols)):
            self._moves[position] = self._get_moves_from_position(position)


    def _get_moves_from_position(self, position):
        r, c = position
        r_max = self._num_rows - 1
        c_max = self._num_cols - 1
        # moves: (upward moves, downward moves)
        # move: (empty space move, jump move)
        moves = ([], [])

        up = r > 0
        down = r < r_max
        left = c > 0
        right = c < c_max

        if r % 2 == 0:
            if up:
                if r > 1 and left:
                    moves[0].append(((r-1, c), (r-2, c-1)))
                else:
                    moves[0].append(((r-1, c), None))
                if right:
                    if r > 1:
                        moves[0].append(((r-1, c+1), (r-2, c+1)))
                    else:
                        moves[0].append(((r-1, c+1), None))
            if down:
                if r < r_max-1 and left:
                    moves[1].append(((r+1, c), (r+2, c-1)))
                else:
                    moves[1].append(((r+1, c), None))
                if right:
                    if r < r_max-1:
                        moves[1].append(((r+1, c+1), (r+2, c+1)))
                    else:
                        moves[1].append(((r+1, c+1), None))
        else:
            if up:
                if left:
                    if r > 1:
                        moves[0].append(((r-1, c-1), (r-2, c-1)))
                    else:
                        moves[0].append(((r-1, c-1), None))
                if r > 1 and right:
                    moves[0].append(((r-1, c), (r-2, c+1)))
                else:
                    moves[0].append(((r-1, c), None))
            if down:
                if left:
                    if r < r_max-1:
                        moves[1].append(((r+1, c-1), (r+2, c-1)))
                    else:
                        moves[1].append(((r+1, c-1), None))
                if r < r_max-1 and right:
                    moves[1].append(((r+1, c), (r+2, c+1)))
                else:
                    moves[1].append(((r+1, c), None))
        return moves

    def _get_pieces(self):
        self._pieces = (set(), set())
        for position in product(range(self._num_rows), range(self._num_cols)):
            identity = self._board[position]
            if identity != 0:
                player = 0 if identity > 0 else 1
                self._pieces[player].add(position)

    def outcome(self):
        if self.is_terminal:
            has_pieces = tuple(map(lambda p: len(p) > 0, self._pieces))
            if has_pieces == (True, False):
                # player 0 wins
                return (1, -1)
            elif has_pieces == (False, True):
                # player 1 wins
                return (-1, 1)
            else:
                # the game is a draw
                return (0, 0)
        else:
            # it is still midgame
            return (0, 0)

    def _get_actions(self):
        self.actions = []
        if self._jump_piece:
            self._get_jump_actions(self._jump_piece)
        else:
            for piece in self._pieces[self._active_player]:
                self._get_jump_actions(piece)
            if len(self.actions) == 0:
                for piece in self._pieces[self._active_player]:
                    self._get_move_actions(piece)

    def _get_jump_actions(self, piece):
        for move, jump in self._get_piece_moves(piece):
            if (self._is_oppoent_piece(move) and jump
                    and self._board[jump] == 0):
                self.actions.append((piece, jump, move))
    
    def _get_move_actions(self, piece):
        for move, _ in self._get_piece_moves(piece):
            if self._board[move] == 0:
                self.actions.append((piece, move, None))

    def _get_piece_moves(self, piece):
        for move in self._moves[piece][self._active_player]:
            yield move
        if abs(self._board[piece]) > 1:
            for move in self._moves[piece][1-self._active_player]:
                yield move

    def _is_oppoent_piece(self, pos):
        if self._active_player == 0:
            return self._board[pos] < 0
        else:
            return self._board[pos] > 0 

    def _get_is_terminal(self):
        self.is_terminal = min(map(len, self._pieces)) == 0
        if not self.is_terminal and len(self.actions) == 0:
            self._active_player = 1 - self._active_player
            self._jump_piece = None
            self._get_actions()
            if len(self.actions) == 0:
                self._active_player = 1 - self._active_player
                self._get_actions()
                if len(self.actions) == 0:
                    self.is_terminal = True
    
    def result(self, action):
        assert action in self.actions
        new_state = copy.deepcopy(self)
        old_piece_pos, new_piece_pos, jumped_piece_pos = action
        new_state._board[old_piece_pos] = 0
        new_state._board[new_piece_pos] = self._get_piece_identity(action)
        new_state._pieces[self._active_player].remove(old_piece_pos)
        new_state._pieces[self._active_player].add(new_piece_pos)
        if jumped_piece_pos:
            new_state._board[jumped_piece_pos] = 0
            new_state._pieces[1 - self._active_player].remove(jumped_piece_pos)
            new_state._jump_piece = new_piece_pos
        else:
            new_state._active_player = 1 - self._active_player
            new_state._jump_piece = None
        new_state._get_actions()
        new_state._get_is_terminal()
        return new_state
    
    def _get_piece_identity(self, action):
        old_piece_pos, new_piece_pos, _ = action
        old_identity = self._board[old_piece_pos]
        if (abs(old_identity) == 1
            and self._promote_piece(old_identity, new_piece_pos)):
            old_identity *= 2
        return old_identity

    def _promote_piece(self, old_identity, new_piece_pos):
        new_piece_row = new_piece_pos[0]
        goal_rows = {1: 0, -1: len(self._board)-1}
        return (old_identity in goal_rows
                and new_piece_row == goal_rows[old_identity])

    def visualize(self):
        utils.visualize(self._board)
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return utils.eq(self.__dict__, other.__dict__)
        else:
            return False    


if __name__ == '__main__':
    cs = CheckersState()
    cs.visualize()
