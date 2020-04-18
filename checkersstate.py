from itertools import product
import numpy as np
import utils



class CheckersState:

    def __init__(self, board=utils.default_board, active_player=0,
                 jump_piece=None, **kwargs):
        self._board = np.array(board, dtype=np.int32)
        assert(len(self._board.shape) == 2)
        assert(active_player in (0, 1))
        self._active_player = active_player
        self._get_moves()
        self._get_positions()
        if jump_piece:
            assert(jump_piece in self._positions[self._active_player])
        self._jump_piece = jump_piece
        self._get_actions()
        self._get_is_terminal()

    def _get_moves(self):
        self._moves = {}
        num_rows, num_cols = self._board.shape
        for position in product(range(num_rows), range(num_cols)):
            self._moves[position] = self._get_moves_from_position(position)


    def _get_moves_from_position(self, position):
        r, c = position
        r_max, c_max = (n-1 for n in self._board.shape)
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

    def _get_positions(self):
        self._positions = (set(), set())
        num_rows, num_cols = self._board.shape
        for position in product(range(num_rows), range(num_cols)):
            identity = self._board[position]
            if identity != 0:
                player = 0 if identity > 0 else 1
                self._positions[player].add(position)

    def outcome(self):
        if self.is_terminal:
            has_pieces = tuple(map(lambda p: len(p) > 0, self._positions))
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
            self._get_jump_actions()
        else:
            self._get_all_actions()

    def _get_jump_actions(self):
        for move, jump in self._get_piece_moves(self._jump_piece):
            if (self._is_oppoent_piece(move) and jump
                    and self._board[jump] == 0):
                self.actions.append((self._jump_piece, jump, move))

    def _get_all_actions(self):
        for position in self._positions[self._active_player]:
            for move, jump in self._get_piece_moves(position):
                if self._board[move] == 0:
                    self.actions.append((position, move, None))
                elif (self._is_oppoent_piece(move) and jump
                        and self._board[jump] == 0):
                    self.actions.append((position, jump, move))

    def _get_piece_moves(self, position):
        for move in self._moves[position][self._active_player]:
            yield move
        if abs(self._board[position]) > 1:
            for move in self._moves[position][1-self._active_player]:
                yield move

    def _is_oppoent_piece(self, pos):
        if self._active_player == 0:
            return self._board[pos] < 0
        else:
            return self._board[pos] > 0 

    def _get_is_terminal(self):
        self.is_terminal = min(map(len, self._positions)) == 0
        if len(self.actions) == 0:
            self._active_player = 1 - self._active_player
            self._get_actions()
            if len(self.actions) == 0:
                self._active_player = 1 - self._active_player
                self.is_terminal = True
        

    def visualize(self):
        utils.visualize(self._board)


if __name__ == '__main__':
    cs = CheckersState()
    cs.visualize()
