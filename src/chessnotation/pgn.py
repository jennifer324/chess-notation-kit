"""Parsing PGN movetext into a sequence of SAN moves.

PGN movetext interleaves move numbers, halfmove SAN tokens, brace comments,
and a trailing result marker in one string, e.g.:

    1. e4 e5 2. Nf3 {developing} Nc6 3. Bb5 a6 1-0

This module strips everything that isn't a move token and hands the rest to
san.parse_san one token at a time.
"""

import re

from .san import SANMove, parse_san

_RESULT_TOKENS = frozenset({"1-0", "0-1", "1/2-1/2", "*"})
_COMMENT_RE = re.compile(r"\{[^}]*\}")
_LEADING_MOVE_NUMBER_RE = re.compile(r"^\d+\.+")
_TRAILING_ANNOTATION_RE = re.compile(r"[!?]+$")


def parse_movetext(movetext: str) -> list[SANMove]:
    """Parse a PGN movetext string into an ordered list of SANMove.

    Handles move numbers ("12." or "12..."), brace comments, Numeric
    Annotation Glyphs ("$1"), move annotation suffixes ("!", "?!", "!!",
    ...), and a trailing game result marker ("1-0", "0-1", "1/2-1/2", "*").

    Parenthesized variations (RAV) aren't supported yet: a "(" or ")" in
    the input raises ValueError rather than silently dropping the
    sub-line's moves.
    """
    if not isinstance(movetext, str):
        raise ValueError("movetext must be a string")

    text = _COMMENT_RE.sub(" ", movetext)
    if "(" in text or ")" in text:
        raise ValueError("parenthesized variations are not supported yet")

    moves = []
    for raw_token in text.split():
        if raw_token in _RESULT_TOKENS or raw_token.startswith("$"):
            continue
        token = _LEADING_MOVE_NUMBER_RE.sub("", raw_token)
        if not token:
            continue
        token = _TRAILING_ANNOTATION_RE.sub("", token)
        moves.append(parse_san(token))
    return moves
