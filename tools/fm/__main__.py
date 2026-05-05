"""Entry point so `python3 -m tools.fm <subcommand>` works."""
from __future__ import annotations

import sys

from .fm import main

if __name__ == "__main__":
    sys.exit(main())
