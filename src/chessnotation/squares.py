"""Square-coordinate math for the standard 8x8 board.

A square is the two-character string a chess player writes ("e4"). Internally
we index files and ranks 0-7 (a=0, rank 1=0) because that maps directly onto
list/array indexing if a caller wants to build a board on top of this.
"""

FILES = "abcdefgh"
RANKS = "12345678"


def is_valid_square(square: str) -> bool:
    return (
        isinstance(square, str)
        and len(square) == 2
        and square[0] in FILES
        and square[1] in RANKS
    )


def square_to_coords(square: str) -> tuple[int, int]:
    """Return (file_index, rank_index), both 0-7, for a square like "e4"."""
    if not is_valid_square(square):
        raise ValueError(f"not a valid square: {square!r}")
    return FILES.index(square[0]), RANKS.index(square[1])


def coords_to_square(file_index: int, rank_index: int) -> str:
    if not (0 <= file_index <= 7 and 0 <= rank_index <= 7):
        raise ValueError(f"coordinates out of range: {(file_index, rank_index)!r}")
    return FILES[file_index] + RANKS[rank_index]


def square_color(square: str) -> str:
    """"light" or "dark", matching how the square looks on a physical board."""
    file_index, rank_index = square_to_coords(square)
    return "light" if (file_index + rank_index) % 2 == 1 else "dark"


def same_file(a: str, b: str) -> bool:
    return square_to_coords(a)[0] == square_to_coords(b)[0]


def same_rank(a: str, b: str) -> bool:
    return square_to_coords(a)[1] == square_to_coords(b)[1]


def same_diagonal(a: str, b: str) -> bool:
    fa, ra = square_to_coords(a)
    fb, rb = square_to_coords(b)
    return abs(fa - fb) == abs(ra - rb)


def distance(a: str, b: str) -> int:
    """Chebyshev distance: how many king moves it takes to go from a to b."""
    fa, ra = square_to_coords(a)
    fb, rb = square_to_coords(b)
    return max(abs(fa - fb), abs(ra - rb))
