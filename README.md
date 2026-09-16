# chessnotation

Small toolkit for the text side of chess: square coordinates and Standard
Algebraic Notation (SAN) move tokens like `Nbd2+` or `exd5=Q`. Every public
function is pure — same input, same output, no board or global state — so
the whole thing is easy to unit test and easy to embed in something bigger
(a PGN reader, a puzzle generator, whatever).

This is not a chess engine. It doesn't know the rules of chess and it can't
tell you whether a move is legal. What it does is turn notation into
structured data and back, which is the annoying, error-prone part you'd
otherwise end up hand-rolling with regexes scattered across a codebase.

## Install

No dependencies, standard library only. For now, clone it and add `src/` to
your path, or install it locally in editable mode:

```
pip install -e .
```

## Library usage

```python
from chessnotation import parse_san, format_san, parse_movetext, square_to_coords, square_color

move = parse_san("Nbd2+")
move.piece        # "N"
move.from_file    # "b"
move.to_square    # "d2"
move.check        # True

format_san(move)  # "Nbd2+" — round-trips back to the original token

square_to_coords("e4")   # (4, 3), zero-indexed (file, rank)
square_color("e4")       # "light"
```

Castling and promotions parse the same way:

```python
parse_san("O-O-O").castle       # "queenside"
parse_san("e8=Q+").promotion    # "Q"
```

`parse_san` raises `ValueError` on malformed input rather than guessing.

A full game's movetext parses to a list of `SANMove`, in order:

```python
parse_movetext("1. e4 e5 2. Nf3 Nc6 3. Bb5 a6")
# [SANMove(to_square="e4", ...), SANMove(to_square="e5", ...), ...]
```

`parse_movetext` strips move numbers, brace comments, `$` NAGs, and `!`/`?`
annotation suffixes, and drops a trailing result marker (`1-0`, `0-1`,
`1/2-1/2`, `*`). Parenthesized variations aren't supported yet and raise
`ValueError`.

## CLI

The library ships a thin CLI for quick lookups from a terminal:

```
$ python -m chessnotation.cli square e4
{"square": "e4", "color": "light"}

$ python -m chessnotation.cli san "exd5=Q+"
{"raw": "exd5=Q+", "to_square": "d5", "piece": null, "from_file": "e", ...}

$ python -m chessnotation.cli compare e1 e8
{"a": "e1", "b": "e8", "same_file": true, "same_rank": false, ...}

$ python -m chessnotation.cli pgn "1. e4 e5 2. Nf3 Nc6"
[{"raw": "e4", "to_square": "e4", ...}, {"raw": "e5", ...}, ...]
```

If installed via `pip install -e .`, the `chessnotation` command is also
available directly.

## Status

Early. SAN parsing covers standard moves, captures, disambiguation,
promotion, castling, and check/mate suffixes. PGN movetext parses down to
a list of moves, but parenthesized variations aren't handled yet. En
passant is only representable the same way any other pawn capture is
(this layer doesn't know board state, so it can't distinguish them — that
needs the move-generation layer this is meant to sit under).
