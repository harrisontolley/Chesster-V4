import copy

from Core.Search.Tablebase import get_best_move


class Search:
    def __init__(self):
        # self.eval = Evaluation()
        # self.trans_table = TranspositionTable()

    def search(self, board, depth=3):
        if len(board.piece_map()) <= 7:
            best_move = get_best_move(board.fen())
            if best_move: return best_move



    def minimax(self, board, depth, alpha, beta, maximising_player):
        if depth == 0:
            return 5
            # return self.eval(board)


        if maximising_player:
            max_eval = float('-inf')

            for move in board.legal_moves:
                new_board = board.copy(stack=5)

                board.push(move)

                score = self.minimax(new_board, depth - 1, alpha, beta, False)


