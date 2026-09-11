"""Thin CLI over the chessnotation library. All the logic lives in
squares.py and san.py; this module only wires argv to those functions and
prints the result as JSON.
"""

import argparse
import json
import sys
from dataclasses import asdict

from .san import parse_san
from .squares import distance, is_valid_square, same_diagonal, same_file, same_rank, square_color


def _cmd_square(args: argparse.Namespace) -> int:
    if not is_valid_square(args.square):
        print(f"error: not a valid square: {args.square!r}", file=sys.stderr)
        return 1
    print(json.dumps({"square": args.square, "color": square_color(args.square)}))
    return 0


def _cmd_compare(args: argparse.Namespace) -> int:
    for square in (args.a, args.b):
        if not is_valid_square(square):
            print(f"error: not a valid square: {square!r}", file=sys.stderr)
            return 1
    print(
        json.dumps(
            {
                "a": args.a,
                "b": args.b,
                "same_file": same_file(args.a, args.b),
                "same_rank": same_rank(args.a, args.b),
                "same_diagonal": same_diagonal(args.a, args.b),
                "king_moves": distance(args.a, args.b),
            }
        )
    )
    return 0


def _cmd_san(args: argparse.Namespace) -> int:
    try:
        move = parse_san(args.token)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(asdict(move)))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="chessnotation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    square = subparsers.add_parser("square", help="describe a single square")
    square.add_argument("square", help='e.g. "e4"')
    square.set_defaults(func=_cmd_square)

    compare = subparsers.add_parser("compare", help="compare two squares")
    compare.add_argument("a")
    compare.add_argument("b")
    compare.set_defaults(func=_cmd_compare)

    san = subparsers.add_parser("san", help="parse a SAN move token")
    san.add_argument("token", help='e.g. "Nbd2+" or "exd5=Q"')
    san.set_defaults(func=_cmd_san)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
