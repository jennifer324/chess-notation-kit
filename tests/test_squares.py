import unittest

from chessnotation.squares import (
    coords_to_square,
    distance,
    is_valid_square,
    same_diagonal,
    same_file,
    same_rank,
    square_color,
    square_to_coords,
)


class IsValidSquareTest(unittest.TestCase):
    def test_accepts_every_square_on_the_board(self):
        for file_letter in "abcdefgh":
            for rank_digit in "12345678":
                self.assertTrue(is_valid_square(file_letter + rank_digit))

    def test_rejects_bad_file_or_rank(self):
        self.assertFalse(is_valid_square("i4"))
        self.assertFalse(is_valid_square("a9"))
        self.assertFalse(is_valid_square("a0"))

    def test_rejects_wrong_length(self):
        self.assertFalse(is_valid_square("e"))
        self.assertFalse(is_valid_square("e44"))
        self.assertFalse(is_valid_square(""))

    def test_rejects_wrong_case(self):
        self.assertFalse(is_valid_square("E4"))

    def test_rejects_non_string(self):
        self.assertFalse(is_valid_square(None))
        self.assertFalse(is_valid_square(("e", 4)))


class SquareToCoordsTest(unittest.TestCase):
    def test_corners(self):
        self.assertEqual(square_to_coords("a1"), (0, 0))
        self.assertEqual(square_to_coords("h8"), (7, 7))

    def test_middle(self):
        self.assertEqual(square_to_coords("e4"), (4, 3))

    def test_raises_on_invalid_square(self):
        with self.assertRaises(ValueError):
            square_to_coords("z9")


class CoordsToSquareTest(unittest.TestCase):
    def test_round_trips_with_square_to_coords(self):
        for file_letter in "abcdefgh":
            for rank_digit in "12345678":
                square = file_letter + rank_digit
                self.assertEqual(coords_to_square(*square_to_coords(square)), square)

    def test_raises_on_out_of_range_coordinates(self):
        with self.assertRaises(ValueError):
            coords_to_square(8, 0)
        with self.assertRaises(ValueError):
            coords_to_square(0, -1)


class SquareColorTest(unittest.TestCase):
    def test_a1_is_dark(self):
        self.assertEqual(square_color("a1"), "dark")

    def test_h1_is_light(self):
        self.assertEqual(square_color("h1"), "light")

    def test_e4_is_light(self):
        self.assertEqual(square_color("e4"), "light")

    def test_d4_is_dark(self):
        self.assertEqual(square_color("d4"), "dark")


class SameLineTest(unittest.TestCase):
    def test_same_file(self):
        self.assertTrue(same_file("e2", "e4"))
        self.assertFalse(same_file("e2", "d2"))

    def test_same_rank(self):
        self.assertTrue(same_rank("a4", "h4"))
        self.assertFalse(same_rank("a4", "a5"))

    def test_same_diagonal(self):
        self.assertTrue(same_diagonal("a1", "h8"))
        self.assertTrue(same_diagonal("c1", "a3"))
        self.assertFalse(same_diagonal("a1", "b3"))

    def test_a_square_is_on_its_own_diagonal(self):
        self.assertTrue(same_diagonal("e4", "e4"))


class DistanceTest(unittest.TestCase):
    def test_same_square_is_zero(self):
        self.assertEqual(distance("e4", "e4"), 0)

    def test_adjacent_square_is_one(self):
        self.assertEqual(distance("e4", "e5"), 1)
        self.assertEqual(distance("e4", "f5"), 1)

    def test_uses_chebyshev_not_manhattan(self):
        # a1 -> h8 is 7 diagonal king steps, not 14.
        self.assertEqual(distance("a1", "h8"), 7)
        # a straight-line move still measures by the longer axis.
        self.assertEqual(distance("a1", "a8"), 7)
        self.assertEqual(distance("a1", "d5"), 4)


if __name__ == "__main__":
    unittest.main()
