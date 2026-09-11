"""Structural parsing of Standard Algebraic Notation move tokens.

This deliberately stops short of legality checking. Working out which of
two knights can actually reach a square needs a board; that belongs in a
separate move-generation layer built on top of this one. What lives here is
the part that's pure text: pull a SAN token apart into its pieces, or put
those pieces back together, without ever needing to know the game state.
"""

import re
from dataclasses import dataclass

from .squares import is_valid_square

_PIECE_LETTERS = "KQRBN"
_PROMOTION_LETTERS = "QRBN"

_MOVE_RE = re.compile(
    r"^(?P<piece>[KQRBN])?"
    r"(?P<from_file>[a-h])?(?P<from_rank>[1-8])?"
    r"(?P<capture>x)?"
    r"(?P<to>[a-h][1-8])"
    r"(?:=(?P<promotion>[QRBN]))?"
    r"(?P<check>[+#])?$"
)


@dataclass(frozen=True)
class SANMove:
    raw: str
    to_square: str
    piece: str | None = None  # None means pawn
    from_file: str | None = None
    from_rank: str | None = None
    capture: bool = False
    promotion: str | None = None
    check: bool = False
    checkmate: bool = False
    castle: str | None = None  # "kingside", "queenside", or None


def parse_san(token: str) -> SANMove:
    """Parse one SAN move token, e.g. "Nbd2+", "exd5=Q", "O-O".

    Raises ValueError if the token isn't a well-formed SAN move. Move
    numbers, result markers ("1-0"), and annotations ("!?") are not part of
    a move token and should be stripped by the caller before calling this.
    """
    if not isinstance(token, str) or not token:
        raise ValueError("SAN token must be a non-empty string")

    stripped = token.strip()
    castle = _parse_castle(stripped)
    if castle is not None:
        side, check, checkmate = castle
        return SANMove(
            raw=token,
            to_square="",
            castle=side,
            check=check,
            checkmate=checkmate,
        )

    match = _MOVE_RE.match(stripped)
    if match is None:
        raise ValueError(f"not a valid SAN move: {token!r}")

    to_square = match.group("to")
    if not is_valid_square(to_square):
        raise ValueError(f"not a valid SAN move: {token!r}")

    check_mark = match.group("check")
    return SANMove(
        raw=token,
        to_square=to_square,
        piece=match.group("piece"),
        from_file=match.group("from_file"),
        from_rank=match.group("from_rank"),
        capture=match.group("capture") == "x",
        promotion=match.group("promotion"),
        check=check_mark == "+",
        checkmate=check_mark == "#",
    )


def format_san(move: SANMove) -> str:
    """Render a SANMove back into a SAN token. Inverse of parse_san."""
    suffix = "#" if move.checkmate else "+" if move.check else ""

    if move.castle == "kingside":
        return "O-O" + suffix
    if move.castle == "queenside":
        return "O-O-O" + suffix

    if not is_valid_square(move.to_square):
        raise ValueError(f"not a valid destination square: {move.to_square!r}")
    if move.piece is not None and move.piece not in _PIECE_LETTERS:
        raise ValueError(f"not a valid piece letter: {move.piece!r}")
    if move.promotion is not None and move.promotion not in _PROMOTION_LETTERS:
        raise ValueError(f"not a valid promotion piece: {move.promotion!r}")

    piece = move.piece or ""
    origin = (move.from_file or "") + (move.from_rank or "")
    capture = "x" if move.capture else ""
    promotion = f"={move.promotion}" if move.promotion else ""
    return f"{piece}{origin}{capture}{move.to_square}{promotion}{suffix}"


def _parse_castle(token: str) -> tuple[str, bool, bool] | None:
    body = token.rstrip("+#")
    suffix = token[len(body):]
    check = suffix == "+"
    checkmate = suffix == "#"

    normalized = body.replace("0", "O")
    if normalized == "O-O":
        return "kingside", check, checkmate
    if normalized == "O-O-O":
        return "queenside", check, checkmate
    return None
