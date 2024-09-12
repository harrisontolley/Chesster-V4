import chess

class PrecomputedEvaluationData:
    def __init__(self):
        self.pawn_shield_squares_white = [[] for _ in range(64)]
        self.pawn_shield_squares_black = [[] for _ in range(64)]
        self._initialize_pawn_shields()

    def _initialize_pawn_shields(self):
        for square_index in range(64):
            self._create_pawn_shield_square(square_index)

    def _create_pawn_shield_square(self, square_index):
        shield_indices_white = []
        shield_indices_black = []
        file = chess.square_file(square_index)
        rank = chess.square_rank(square_index)

        # Adjust file indices to ensure they stay within bounds when computing neighbors
        file = max(min(file, 6), 1)

        for file_offset in range(-1, 2):
            self._add_if_valid(chess.square(file + file_offset, rank + 1), shield_indices_white)
            self._add_if_valid(chess.square(file + file_offset, rank - 1), shield_indices_black)

        for file_offset in range(-1, 2):
            self._add_if_valid(chess.square(file + file_offset, rank + 2), shield_indices_white)
            self._add_if_valid(chess.square(file + file_offset, rank - 2), shield_indices_black)

        self.pawn_shield_squares_white[square_index] = shield_indices_white
        self.pawn_shield_squares_black[square_index] = shield_indices_black

    @staticmethod
    def _add_if_valid(square, list_):
        if 0 <= chess.square_rank(square) < 8:
            list_.append(square)

    def get_shield_squares(self, colour: chess.Color):
        if colour == chess.WHITE:
            return self.pawn_shield_squares_white
        else:
            return self.pawn_shield_squares_black