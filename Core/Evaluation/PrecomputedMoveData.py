import numpy as np

class PrecomputedMoveData:
    def __init__(self):
        self.orthogonal_distance = self._compute_orthogonal_distance()
        self.centre_manhattan_distance = self._compute_centre_manhattan_distance()

    @staticmethod
    def _compute_orthogonal_distance():
        orthogonal_distance = np.zeros((64, 64), dtype=int)

        for square_a in range(64):
            coord_a = (square_a // 8, square_a % 8)
            for square_b in range(64):
                coord_b = (square_b // 8, square_b % 8)

                rank_distance = abs(coord_a[0] - coord_b[0])
                file_distance = abs(coord_a[1] - coord_b[1])

                orthogonal_distance[square_a, square_b] = rank_distance + file_distance

        return orthogonal_distance


    @staticmethod
    def _compute_centre_manhattan_distance():
        centre_manhattan_distance = np.zeros(64, dtype=int)

        centre = (3.5, 3.5) # approx

        for square in range(64):
            coord = (square // 8, square % 8)

            centre_manhattan_distance[square] = abs(coord[0] - centre[0]) + abs(coord[1] - centre[1])

        return centre_manhattan_distance