import contextlib
import io
import json
import unittest

from chessnotation.cli import main


def _run(argv):
    """Run the CLI and return (exit_code, parsed_stdout_json, stderr_text)."""
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = main(argv)
    out = stdout.getvalue()
    return code, (json.loads(out) if out.strip() else None), stderr.getvalue()


class SquareCommandTest(unittest.TestCase):
    def test_prints_square_and_color(self):
        code, payload, _ = _run(["square", "e4"])
        self.assertEqual(code, 0)
        self.assertEqual(payload, {"square": "e4", "color": "light"})

    def test_invalid_square_errors(self):
        code, payload, err = _run(["square", "z9"])
        self.assertEqual(code, 1)
        self.assertIsNone(payload)
        self.assertIn("z9", err)


class CompareCommandTest(unittest.TestCase):
    def test_prints_comparison(self):
        code, payload, _ = _run(["compare", "e1", "e8"])
        self.assertEqual(code, 0)
        self.assertEqual(
            payload,
            {
                "a": "e1",
                "b": "e8",
                "same_file": True,
                "same_rank": False,
                "same_diagonal": False,
                "king_moves": 7,
            },
        )

    def test_invalid_square_errors(self):
        code, payload, err = _run(["compare", "z9", "e4"])
        self.assertEqual(code, 1)
        self.assertIsNone(payload)
        self.assertIn("z9", err)


class SanCommandTest(unittest.TestCase):
    def test_prints_parsed_move(self):
        code, payload, _ = _run(["san", "Nbd2+"])
        self.assertEqual(code, 0)
        self.assertEqual(payload["piece"], "N")
        self.assertEqual(payload["from_file"], "b")
        self.assertEqual(payload["to_square"], "d2")
        self.assertTrue(payload["check"])

    def test_invalid_token_errors(self):
        code, payload, err = _run(["san", "not a move"])
        self.assertEqual(code, 1)
        self.assertIsNone(payload)
        self.assertTrue(err.startswith("error:"))


class PgnCommandTest(unittest.TestCase):
    def test_prints_move_list(self):
        code, payload, _ = _run(["pgn", "1. e4 e5 2. Nf3 Nc6"])
        self.assertEqual(code, 0)
        self.assertEqual([move["to_square"] for move in payload], ["e4", "e5", "f3", "c6"])

    def test_unsupported_variation_errors(self):
        code, payload, err = _run(["pgn", "1. e4 e5 (1... c5) 2. Nf3"])
        self.assertEqual(code, 1)
        self.assertIsNone(payload)
        self.assertTrue(err.startswith("error:"))


if __name__ == "__main__":
    unittest.main()
