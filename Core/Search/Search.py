import copy
import time

import chess

from Core.Evaluation.Evaluation import Evaluation
from Core.Search.Tablebase import get_best_move


class Search:
    def __init__(self, time_limit=None):
        self.eval = Evaluation()
        # self.trans_table = {}

        self.time_limit = time_limit

        # vars to track performance
        self.nodes_searched = 0
        self.table_hits = 0

    def search(self, board, max_depth=3, time_limit=10):
        if len(board.piece_map()) <= 6:
            best_move, evaluation = get_best_move(board.fen())
            if best_move:
                return best_move, evaluation

        self.nodes_searched = 0

        self.trans_table = {}

        self.start_time = time.time()
        self.time_limit = time_limit

        self.best_move_found = None
        self.best_move_evaluation = 0

        maximising_player = board.turn == chess.WHITE



        # iterative deepening
        for depth in range(1, max_depth + 1):
            try:
                best_move, evaluation = self.minimax(
                    board, depth, maximising_player, alpha=float('-inf'), beta=float('inf'),
                )
                self.best_move_found = best_move
                self.best_move_evaluation = evaluation

            except TimeoutError:
                # search terminated as time exceeded
                break

        if self.best_move_found:
            return self.best_move_found, self.best_move_evaluation
        else:
            # haven't found a move, just get any move
            return list(board.legal_moves)[0], 0

        # return self.minimax(board, depth = depth, maximising_player = maximising_player,
        #                     alpha=float('-inf'), beta=float('inf'))

    def _is_base_case(self, depth, board):
        return depth == 0 or board.is_game_over()

    def _handle_base_case(self, depth, board):
        if board.is_checkmate():
            # if white won, return high score, otherwise return negative high score
            return (None, -1 * Evaluation.CHECKMATE_SCORE + depth) if board.turn == chess.WHITE \
                else (None, Evaluation.CHECKMATE_SCORE - depth)

        # if stalemated, score of 0 (dead even)
        elif board.is_stalemate() or board.is_insufficient_material():
            return None, 0

        return None, self.eval.evaluate(board)

    def minimax(self, board, depth, maximising_player, alpha, beta):
        self.nodes_searched += 1

        board_key = board._transposition_key()
        if board_key in self.trans_table:
            entry = self.trans_table[board_key]
            if entry['depth'] >= depth:
                self.table_hits += 1
                return entry['best_move'], entry['evaluation']

        if self._is_base_case(depth, board):
            return self._handle_base_case(depth, board)

        best_move = None

        moves = list(board.legal_moves)
        moves = self.order_moves(board, moves)

        if maximising_player:
            max_eval = float('-inf')

            for move in moves:
                board.push(move)
                _, evaluation = self.minimax(board, depth - 1, False, alpha, beta)
                board.pop()

                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move

                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break

            self.trans_table[board_key] = {
                'depth': depth,
                'best_move': best_move,
                'evaluation': max_eval
            }

            return best_move, max_eval

        else:
            min_eval = float('inf')

            for move in moves:
                board.push(move)
                _, evaluation = self.minimax(board, depth - 1, True, alpha, beta)
                board.pop()

                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move

                beta = min(beta, evaluation)
                if beta <= alpha:
                    break

            self.trans_table[board_key] = {
                'depth': depth,
                'best_move': best_move,
                'evaluation': min_eval
            }

            return best_move, min_eval


    def order_moves(self, board, moves):
        move_scores = []

        for move in moves:
            score = 0

            if board.is_capture(move):
                # MVV - LVA (most valuable victim attacked by least valuable attacker)
                victim_value = self.get_piece_value(
                    board.piece_at(move.to_square) # get piece at target square
                )
                attacker_value = self.get_piece_value(
                    board.piece_at(move.from_square) # piece at original square
                )

                score += 10 * victim_value - attacker_value

            if board.gives_check(move):
                score += 50

            if move.promotion:
                score += 100

            if move == self.best_move_found:
                score += 1000 # prioritise best move found in iterative deepening

            move_scores.append((score, move))

        move_scores.sort(reverse=True, key=lambda x: x[0])
        ordered_moves = [move for score, move in move_scores]

        return ordered_moves

    @staticmethod
    def get_piece_value(piece):
        if piece is None:
            return 0

        values =  {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0, # not possible
        }

        return values.get(piece.piece_type, 0)