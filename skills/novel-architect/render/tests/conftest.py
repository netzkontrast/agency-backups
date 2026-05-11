"""Make the render package importable for tests."""

from __future__ import annotations

import sys
from pathlib import Path

# Add the render/ dir (containing render_intent.py, io_helpers.py) to sys.path
# so tests can `import render_intent` and `import io_helpers` directly.
RENDER_DIR = Path(__file__).resolve().parent.parent
if str(RENDER_DIR) not in sys.path:
    sys.path.insert(0, str(RENDER_DIR))
