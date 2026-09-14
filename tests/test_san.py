import unittest

from chessnotation.san import SANMove, format_san, parse_san


class ParseSanPawnMovesTest(unittest.TestCase):
    def test_plain_pawn_push(self):
        move = parse_san("e4")
        self.assertIsNone(move.piece)
        self.assertEqual(move.to_square, "e4")
        self.assertFalse(move.capture)
        self.assertIsNone(move.from_file)
        self.assertIsNone(move.from_rank)

    def test_pawn_capture_carries_source_file(self):
        move = parse_san("exd5")
        self.assertIsNone(move.piece)
        self.assertEqual(move.from_file, "e")
        self.assertTrue(move.capture)
        self.assertEqual(move.to_square, "d5")

    def test_promotion(self):
        move = parse_san("e8=Q")
        self.assertEqual(move.to_square, "e8")
        self.assertEqual(move.promotion, "Q")

    def test_capture_with_promotion_and_check(self):
        move = parse_san("exd8=Q+")
        self.assertEqual(move.from_file, "e")
        self.assertTrue(move.capture)
        self.assertEqual(move.to_square, "d8")
        self.assertEqual(move.promotion, "Q")
        self.assertTrue(move.check)
        self.assertFalse(move.checkmate)


class ParseSanPieceMovesTest(unittest.TestCase):
    def test_plain_piece_move(self):
        move = parse_san("Nf3")
        self.assertEqual(move.piece, "N")
        self.assertEqual(move.to_square, "f3")
        self.assertFalse(move.capture)

    def test_piece_capture(self):
        move = parse_san("Bxe5")
        self.assertEqual(move.piece, "B")
        self.assertTrue(move.capture)
        self.assertEqual(move.to_square, "e5")

    def test_file_disambiguation(self):
        move = parse_san("Nbd2")
        self.assertEqual(move.piece, "N")
        self.assertEqual(move.from_file, "b")
        self.assertIsNone(move.from_rank)
        self.assertEqual(move.to_square, "d2")

    def test_rank_disambiguation(self):
        move = parse_san("N1d2")
        self.assertEqual(move.piece, "N")
        self.assertIsNone(move.from_file)
        self.assertEqual(move.from_rank, "1")

    def test_full_square_disambiguation(self):
        move = parse_san("Qh4e1")
        self.assertEqual(move.piece, "Q")
        self.assertEqual(move.from_file, "h")
        self.assertEqual(move.from_rank, "4")
        self.assertEqual(move.to_square, "e1")

    def test_checkmate_suffix(self):
        move = parse_san("Qxf7#")
        self.assertTrue(move.checkmate)
        self.assertFalse(move.check)


class ParseSanCastlingTest(unittest.TestCase):
    def test_kingside(self):
        move = parse_san("O-O")
        self.assertEqual(move.castle, "kingside")
        self.assertEqual(move.to_square, "")

    def test_queenside(self):
        move = parse_san("O-O-O")
        self.assertEqual(move.castle, "queenside")

    def test_zero_variant_is_normalized(self):
        move = parse_san("0-0")
        self.assertEqual(move.castle, "kingside")

    def test_castle_with_check(self):
        move = parse_san("O-O+")
        self.assertEqual(move.castle, "kingside")
        self.assertTrue(move.check)

    def test_castle_with_checkmate(self):
        move = parse_san("O-O-O#")
        self.assertEqual(move.castle, "queenside")
        self.assertTrue(move.checkmate)


class ParseSanInvalidInputTest(unittest.TestCase):
    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            parse_san("")

    def test_non_string_raises(self):
        with self.assertRaises(ValueError):
            parse_san(None)

    def test_garbage_raises(self):
        with self.assertRaises(ValueError):
            parse_san("not a move")

    def test_bad_square_raises(self):
        with self.assertRaises(ValueError):
            parse_san("Ni9")

    def test_lowercase_piece_letter_raises(self):
        with self.assertRaises(ValueError):
            parse_san("nf3")

    def test_strips_surrounding_whitespace(self):
        move = parse_san("  e4  ")
        self.assertEqual(move.to_square, "e4")


class FormatSanTest(unittest.TestCase):
    def test_round_trips_plain_moves(self):
        for token in ("e4", "Nf3", "Bxe5", "Nbd2+", "exd5", "exd8=Q+", "Qh4e1#"):
            self.assertEqual(format_san(parse_san(token)), token)

    def test_round_trips_castling(self):
        for token in ("O-O", "O-O-O", "O-O+", "O-O-O#"):
            self.assertEqual(format_san(parse_san(token)), token)

    def test_normalizes_zero_castling_notation_on_format(self):
        move = parse_san("0-0")
        self.assertEqual(format_san(move), "O-O")

    def test_raises_on_invalid_destination_square(self):
        move = SANMove(raw="", to_square="z9")
        with self.assertRaises(ValueError):
            format_san(move)

    def test_raises_on_invalid_piece_letter(self):
        move = SANMove(raw="", to_square="e4", piece="X")
        with self.assertRaises(ValueError):
            format_san(move)

    def test_raises_on_invalid_promotion_letter(self):
        move = SANMove(raw="", to_square="e8", promotion="K")
        with self.assertRaises(ValueError):
            format_san(move)


if __name__ == "__main__":
    unittest.main()
