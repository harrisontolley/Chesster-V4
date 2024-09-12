import enum

import chess

class PieceTables(enum.Enum):
    PAWNS_START = 0
    PAWNS_ENDGAME = 1
    KNIGHTS = 2
    BISHOPS = 3
    ROOKS = 4
    QUEENS = 5
    KING_START = 6
    KING_ENDGAME = 7

class PieceSquareTables:
    PAWNS_START = [
        0, 0, 0, 0, 0, 0, 0, 0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5, 5, 10, 25, 25, 10, 5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, -5, -10, 0, 0, -10, -5, 5,
        5, 10, 10, -20, -20, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0
    ]

    PAWNS_ENDGAME = [
        0, 0, 0, 0, 0, 0, 0, 0,
        80, 80, 80, 80, 80, 80, 80, 80,
        50, 50, 50, 50, 50, 50, 50, 50,
        30, 30, 30, 30, 30, 30, 30, 30,
        20, 20, 20, 20, 20, 20, 20, 20,
        10, 10, 10, 10, 10, 10, 10, 10,
        10, 10, 10, 10, 10, 10, 10, 10,
        0, 0, 0, 0, 0, 0, 0, 0
    ]

    KNIGHTS = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
    ]

    BISHOPS = [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -20, -10, -10, -10, -10, -10, -10, -20
    ]

    ROOKS = [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, 10, 10, 10, 10, 5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        0, 0, 0, 5, 5, 0, 0, 0
    ]

    QUEENS = [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -5, 0, 5, 5, 5, 5, 0, -5,
        0, 0, 5, 5, 5, 5, 0, -5,
        -10, 5, 5, 5, 5, 5, 0, -10,
        -10, 0, 5, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20
    ]

    KING_START = [
        -80, -70, -70, -70, -70, -70, -70, -80,
        -60, -60, -60, -60, -60, -60, -60, -60,
        -40, -50, -50, -60, -60, -50, -50, -40,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        20, 20, -5, -5, -5, -5, 20, 20,
        20, 30, 10, 0, 0, 10, 30, 20
    ]

    KING_ENDGAME = [
        -50, -30, -30, -30, -30, -30, -30, -50,
        -30, -10, 0, 10, 10, 0, -10, -30,
        -30, -5, 20, 30, 30, 20, -5, -30,
        -30, -10, 35, 45, 45, 35, -10, -30,
        -30, -15, 30, 40, 40, 30, -15, -30,
        -30, -20, 20, 25, 25, 20, -20, -30,
        -30, -25, 0, 0, 0, 0, -25, -30,
        -50, -30, -30, -30, -30, -30, -30, -50
    ]

    def __init__(self):

        self.white_tables = {
            PieceTables.PAWNS_START: self.PAWNS_START,
            PieceTables.PAWNS_ENDGAME: self.PAWNS_ENDGAME,
            PieceTables.KNIGHTS: self.KNIGHTS,
            PieceTables.BISHOPS: self.BISHOPS,
            PieceTables.ROOKS: self.ROOKS,
            PieceTables.QUEENS: self.QUEENS,
            PieceTables.KING_START: self.KING_START,
            PieceTables.KING_ENDGAME: self.KING_ENDGAME
        }

        self.black_tables = {}

        for piece, table in self.white_tables.items():
            self.black_tables[piece] = self.mirror_table(table)


    # as tables are based on white perspective, need to mirror for blacks
    @staticmethod
    def mirror_table(table):
        mirrored_table = [0] * 64

        for idx in range(64):
            file = chess.square_file(idx)
            rank = chess.square_rank(idx)

            rank = 7 - rank

            new_idx = chess.square(file, rank)
            mirrored_table[new_idx] = table[idx]

        return mirrored_table

    def print_mirrored_table_test(self, table):
        table = self.mirror_table(table)

        # print 8 lines at a time
        for i in range(0, len(table), 8):
            print(table[i:i+8])

    def get_colour_tables(self, colour: chess.Color):
        if colour == chess.WHITE:
            return self.white_tables
        else:
            return self.black_tables

    # def get_value_for_piece(self, piece: chess.Piece, ):
