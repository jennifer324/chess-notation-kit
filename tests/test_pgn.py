import unittest

from chessnotation.pgn import parse_movetext


class ParseMovetextTest(unittest.TestCase):
    def test_plain_movetext(self):
        moves = parse_movetext("1. e4 e5 2. Nf3 Nc6")
        self.assertEqual([m.to_square for m in moves], ["e4", "e5", "f3", "c6"])

    def test_black_to_move_first_uses_ellipsis(self):
        moves = parse_movetext("5... Nf6 6. Bg5")
        self.assertEqual([m.to_square for m in moves], ["f6", "g5"])

    def test_move_number_and_move_can_share_no_space(self):
        moves = parse_movetext("1.e4 e5")
        self.assertEqual([m.to_square for m in moves], ["e4", "e5"])

    def test_strips_trailing_result_marker(self):
        for result in ("1-0", "0-1", "1/2-1/2", "*"):
            moves = parse_movetext(f"1. e4 e5 {result}")
            self.assertEqual([m.to_square for m in moves], ["e4", "e5"])

    def test_strips_brace_comments(self):
        moves = parse_movetext("1. e4 {best by test} e5 2. Nf3 Nc6")
        self.assertEqual([m.to_square for m in moves], ["e4", "e5", "f3", "c6"])

    def test_strips_move_annotation_glyphs(self):
        moves = parse_movetext("1. e4! e5?! 2. Qh5?? Nc6")
        self.assertEqual([m.to_square for m in moves], ["e4", "e5", "h5", "c6"])

    def test_strips_numeric_annotation_glyphs(self):
        moves = parse_movetext("1. e4 $1 e5 $2")
        self.assertEqual([m.to_square for m in moves], ["e4", "e5"])

    def test_handles_castling_and_check_tokens(self):
        moves = parse_movetext("7. O-O Nf6+ 8. O-O-O#")
        self.assertEqual(moves[0].castle, "kingside")
        self.assertTrue(moves[1].check)
        self.assertEqual(moves[2].castle, "queenside")
        self.assertTrue(moves[2].checkmate)

    def test_full_game_end_to_end(self):
        movetext = (
            "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 "
            "6. Re1 b5 7. Bb3 O-O 1-0"
        )
        moves = parse_movetext(movetext)
        self.assertEqual(len(moves), 14)
        self.assertEqual(moves[-1].castle, "kingside")

    def test_empty_string_returns_no_moves(self):
        self.assertEqual(parse_movetext(""), [])

    def test_non_string_raises(self):
        with self.assertRaises(ValueError):
            parse_movetext(None)

    def test_parenthesized_variation_raises(self):
        with self.assertRaises(ValueError):
            parse_movetext("1. e4 e5 (1... c5 2. Nf3) 2. Nf3")

    def test_garbage_token_raises(self):
        with self.assertRaises(ValueError):
            parse_movetext("1. e4 not a move")


if __name__ == "__main__":
    unittest.main()
