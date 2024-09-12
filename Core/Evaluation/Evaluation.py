import chess
from chess import BISHOP, Piece

from Core.Evaluation.PieceSquareTables import PieceSquareTables, PieceTables
from Core.Evaluation.PrecomputedEvaluationData import PrecomputedEvaluationData


def get_count_of_pieces_of_colour(board: chess.Board, piece: chess.PieceType, colour: chess.Color):
    pieces = board.pieces(piece, colour)
    return len(pieces)


class Evaluation:

    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 320,
        chess.ROOK: 500,
        chess.QUEEN: 900,
    }

    PASSED_PAWN_BONUSES = [0, 120, 80, 50, 30, 15, 15]
    ISOLATED_PAWN_PENALTY = [0, -10, -25, -50, -75, -75, -75, -75, -75]
    KING_PAWN_SHIELD_SCORES = [4, 7, 4, 3, 6, 3]

    # change to find sweet spot
    ENDGAME_MATERIAL_SCORE = PIECE_VALUES[chess.ROOK] * 2 + PIECE_VALUES[chess.BISHOP] + PIECE_VALUES[chess.KNIGHT]

    CHECKMATE_SCORE = 9999999999

    def __init__(self):
        self.board = None
        self.piece_square_tables = PieceSquareTables()

        self.piece_type_mapping = {
            PieceTables.PAWNS_START: chess.PAWN,
            PieceTables.KNIGHTS: chess.KNIGHT,
            PieceTables.BISHOPS: chess.BISHOP,
            PieceTables.ROOKS: chess.ROOK,
            PieceTables.QUEENS: chess.QUEEN,
        }

        self.evaluation_data = PrecomputedEvaluationData

    def get_board(self):
        return self.board

    def evaluate(self, board: chess.Board):
        self.board = board

        white_material_info = MaterialInfo(board, chess.WHITE)
        black_material_info = MaterialInfo(board, chess.BLACK)

        white_material_score = white_material_info.get_material_score()
        black_material_score = black_material_info.get_material_score()

        white_endgame_T = white_material_info.get_endgame_t()
        black_endgame_T = black_material_info.get_endgame_t()

        white_piece_square_score = self.evaluate_piece_square_tables(chess.WHITE, white_endgame_T)
        black_piece_square_score = self.evaluate_piece_square_tables(chess.BLACK, black_endgame_T)

        white_pawn_score = self.evaluate_pawns(chess.WHITE)
        black_pawn_score = self.evaluate_pawns(chess.BLACK)

        # white_pawn_shield_score = self.evaluate_king_pawn_shield(board, chess.WHITE)



        white_score = white_material_score + white_piece_square_score + white_pawn_score
        black_score = black_material_score + black_piece_square_score + black_pawn_score


        return white_score - black_score


    def evaluate_piece_square_tables(self, colour: chess.Color, endgame_T: float):
        board = self.get_board()
        score = 0
        for piece_type in PieceTables:
            if piece_type not in (PieceTables.PAWNS_START, PieceTables.PAWNS_ENDGAME,
                                  PieceTables.KING_START, PieceTables.KING_ENDGAME):
                score += self.evaluate_piece_positions(colour, piece_type)

            # interpolate between early and late game
            elif piece_type in (PieceTables.PAWNS_START, PieceTables.KING_START):
                score += self.evaluate_game_state_piece_positions(colour, piece_type, True) * (1 - endgame_T)
            else:
                score += self.evaluate_game_state_piece_positions(colour, piece_type, False) * endgame_T

        return int(score)

    def evaluate_piece_positions(self, colour: chess.Color, piece_type):
        board = self.get_board()
        colour_table = self.piece_square_tables.get_colour_tables(colour)

        chess_piece = self.piece_type_mapping[piece_type]
        table = colour_table[piece_type]

        positions = board.pieces(chess_piece, colour)

        score = 0
        for square in positions:
            score += table[56 ^ square]

        return score

    def evaluate_game_state_piece_positions(self, colour: chess.Color, piece_type, early_game: bool):
        board = self.get_board()
        colour_table = self.piece_square_tables.get_colour_tables(colour)

        if early_game:
            if piece_type == PieceTables.PAWNS_START:
                table = colour_table[PieceTables.PAWNS_START]
                chess_piece = chess.PAWN
            else:
                table = colour_table[PieceTables.KING_START]
                chess_piece = chess.KING
        else:
            if piece_type == PieceTables.PAWNS_ENDGAME:
                table = colour_table[PieceTables.PAWNS_ENDGAME]
                chess_piece = chess.PAWN
            else:
                table = colour_table[PieceTables.KING_ENDGAME]
                chess_piece = chess.KING

        positions = board.pieces(chess_piece, colour)

        score = 0
        for square in positions:
            score += table[56 ^ square]

        return score


    # mop up eval???


    def evaluate_pawns(self, colour: chess.Color):
        board = self.get_board()

        score = 0
        pawns = board.pieces(chess.PAWN, colour)

        num_isolated_pawns = 0

        for square in pawns:
            if self.is_passed_pawn(square, colour):

                if colour == chess.WHITE:
                    score += self.PASSED_PAWN_BONUSES[7 - chess.square_rank(square)]
                else:
                    score += self.PASSED_PAWN_BONUSES[chess.square_rank(square)]

            if self.is_isolated_pawn(square, colour):
                num_isolated_pawns += 1

        score += self.ISOLATED_PAWN_PENALTY[num_isolated_pawns]
        return score

    def is_isolated_pawn(self, pawn_square: chess.Square, colour: chess.Color):
        board = self.get_board()

        pawn_file = chess.square_file(pawn_square)

        # assume isolated
        is_isolated = True

        # look in neighbouring files for friendly pawns
        for file in [pawn_file - 1, pawn_file + 1]:
            if file < 0 or file > 7:
                continue

            friendly_pawns = board.pieces(chess.PAWN, colour)

            adjacent_pawns = friendly_pawns & chess.SquareSet(chess.BB_FILES[file])

            if adjacent_pawns:
                is_isolated = False
                break

        return is_isolated

    def is_passed_pawn(self, square: chess.Square, colour: chess.Color):
        board = self.get_board()

        enemy_colour = not colour

        pawn_rank, pawn_file = chess.square_rank(square), chess.square_file(square)

        # assume passed
        is_passed = True

        end_rank = 7 if colour == chess.WHITE else 0

        rank_range = range(pawn_rank + 1, end_rank) if colour == chess.WHITE else range(pawn_rank - 1, end_rank, -1)

        min_file = max(0, pawn_file - 1)
        max_file = min(7, pawn_file + 1)

        for rank in rank_range:
            for file in range(min_file, max_file):

                target_square = chess.square(file, rank)

                if board.piece_at(target_square) == chess.Piece(chess.PAWN, enemy_colour):
                    is_passed = False
                    break

            if not is_passed:
                break

        return is_passed

    def evaluate_king_pawn_shield(self, colour: chess.Color, enemy_material_info: "MaterialInfo", enemy_piece_square_score):
        board = self.get_board()

        if enemy_material_info.endgameT >= 1:
            return 0

        penalty = 0
        uncastled_king_penalty = 0
        friendly_pawn = board.pieces(chess.PAWN, colour)

        king_square = board.king(colour)
        king_file = chess.square_file(king_square)
        king_rank = chess.square_rank(king_square)

        if king_file <= 2 or king_file >= 5:
            penalty = self.penalty_for_shield(colour)
        else:
            enemy_development_score = max(
                0, min(
                    1,
                   (enemy_piece_square_score + 10) / 130
                   )
            )
            # adds a penalty of 0-50 depending on how developed enemy is
            uncastled_king_penalty = 50 * enemy_development_score

        open_file_against_king_penalty = 0

        number_enemy_rooks = enemy_material_info.num_friendly_pieces[chess.ROOK]
        number_enemy_queens = enemy_material_info.num_friendly_pieces[chess.QUEEN]
        if number_enemy_rooks > 1 or (
            number_enemy_rooks == 0 and number_enemy_queens > 0
        ):

            # king between file 1-6 only (edge files ignored)
            clamped_king_file = max(1, min(6, king_file))

            for attack_file in (clamped_king_file - 1, clamped_king_file + 1):



    def penalty_for_shield(self, colour: chess.Color):
        board = self.get_board()

        friendly_pawn = board.pieces(chess.PAWN, colour)

        penalty = 0

        shield_squares = self.evaluation_data.get_shield_squares(colour)
        for i, square in enumerate(shield_squares):
            if board.piece_at(square) != friendly_pawn:
                penalty += (
                    self.KING_PAWN_SHIELD_SCORES[
                        min(i, len(self.KING_PAWN_SHIELD_SCORES) - 1)
                    ]
                )

        penalty = penalty ** 2

        return penalty



class MaterialInfo:
    def __init__(self, board: chess.Board, colour: chess.Color):
        self.board = board
        self.colour = colour

        self.piece_names = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]
        self.num_friendly_pieces, self.num_enemy_pawns = self.get_pieces()

        self.material_score = self.get_material_score()

        self.endgameT = self.get_endgame_t()

    def get_pieces(self):

        num_friendly_pieces = {}

        for piece in self.piece_names:
            num_friendly_pieces[piece] = get_count_of_pieces_of_colour(self.board, piece, self.colour)

        num_enemy_pawns = get_count_of_pieces_of_colour(self.board, chess.PAWN, not self.colour)

        return num_friendly_pieces, num_enemy_pawns


    def get_material_score(self):
        score = 0
        for piece in self.piece_names:
            score += self.num_friendly_pieces[piece] * Evaluation.PIECE_VALUES[piece]

        return score

    def get_endgame_t(self):
        ENDGAME_PIECE_WEIGHTS = {
            chess.QUEEN: 45,
            chess.ROOK: 20,
            chess.KNIGHT: 10,
            chess.BISHOP: 11
        }

        STARTING_WEIGHT = (
            2 * ENDGAME_PIECE_WEIGHTS[chess.ROOK] +
            2 * ENDGAME_PIECE_WEIGHTS[chess.BISHOP] +
            2 * ENDGAME_PIECE_WEIGHTS[chess.KNIGHT] +
            1 * ENDGAME_PIECE_WEIGHTS[chess.QUEEN]
        )

        CURRENT_WEIGHT = 0
        for piece in ENDGAME_PIECE_WEIGHTS.keys():
            CURRENT_WEIGHT += self.num_friendly_pieces[piece] * ENDGAME_PIECE_WEIGHTS[piece]

        return 1 - min(1, CURRENT_WEIGHT / STARTING_WEIGHT)

