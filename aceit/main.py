"""CLI entry point for AceIt."""

import argparse
import sys

from aceit.parser import parse_args, parse_file
from aceit.overlay import Overlay


def main():
    parser = argparse.ArgumentParser(
        prog="aceit",
        description="Interview teleprompter — bullet points near your camera",
    )
    parser.add_argument("file", nargs="?", help="Text file with one bullet point per line")
    parser.add_argument(
        "--bullets", "-b", nargs="+", help="Bullet points as inline arguments"
    )

    args = parser.parse_args()

    if args.file:
        bullets = parse_file(args.file)
    elif args.bullets:
        bullets = parse_args(args.bullets)
    else:
        parser.print_help()
        sys.exit(1)

    if not bullets:
        print("No bullet points found.", file=sys.stderr)
        sys.exit(1)

    overlay = Overlay(bullets)
    overlay.run()


if __name__ == "__main__":
    main()
