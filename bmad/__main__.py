from __future__ import annotations

import sys

from .cli import main


def _strip_slash_commands(argv: list[str]) -> list[str]:
    # Allow: python -m bmad /start ...
    if len(argv) >= 2 and argv[1].startswith("/"):
        argv = argv[:]
        argv[1] = argv[1][1:]
    return argv


if __name__ == "__main__":
    sys.exit(main(_strip_slash_commands(sys.argv)))
