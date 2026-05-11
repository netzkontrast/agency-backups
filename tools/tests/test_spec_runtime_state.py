"""Tests for tools/check-spec-runtime-state.py (Task 055).

Three fixtures cover the falsifiable acceptance set:
  1. Clean spec (no banned heading) → exit 0, no diagnostics.
  2. Spec with one banned heading → WARN diagnostic emitted.
  3. Spec with banned heading whose body is empty → still flagged.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOLS = REPO / "tools"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "check_spec_runtime_state",
        TOOLS / "check-spec-runtime-state.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_spec_runtime_state"] = module
    spec.loader.exec_module(module)
    return module


csrs = _load_module()


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = csrs.main(argv)
    return rc, out.getvalue(), err.getvalue()


class TestSpecRuntimeStateLinter(unittest.TestCase):
    def test_clean_spec_no_findings(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "AGENTS.md").write_text(
                "# AGENTS\n\n## Theoretical Foundations\nbody\n",
                encoding="utf-8",
            )
            rc, _, err = _capture(["--root", str(base)])
            self.assertEqual(rc, 0, msg=err)
            self.assertNotIn("R.19", err)

    def test_banned_heading_emits_warn(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "AGENTS.md").write_text(
                "# AGENTS\n\n## LOOP_LOG\nrecord 1\nrecord 2\n",
                encoding="utf-8",
            )
            rc, _, err = _capture(["--root", str(base)])
            # WARN tier — exit 0 by default.
            self.assertEqual(rc, 0)
            self.assertIn("R.19", err)
            self.assertIn("LOOP_LOG", err)
            self.assertIn("WARN", err)

    def test_banned_heading_empty_body_still_flagged(self):
        """An empty `## STATE` heading with no body MUST still flag."""
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "AGENTS.md").write_text(
                "# AGENTS\n\n## STATE\n",
                encoding="utf-8",
            )
            rc, _, err = _capture(["--root", str(base)])
            self.assertEqual(rc, 0)
            self.assertIn("R.19", err)
            self.assertIn("STATE", err)

    def test_strict_mode_promotes_to_error(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "AGENTS.md").write_text(
                "# AGENTS\n\n## SESSION_LOG\nrecord\n",
                encoding="utf-8",
            )
            rc, _, err = _capture(["--root", str(base), "--strict"])
            self.assertEqual(rc, 1)
            self.assertIn("ERROR", err)
            self.assertIn("R.19", err)

    def test_fenced_heading_ignored(self):
        """A `## LOOP_LOG` line inside a fenced block is not a real heading."""
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "AGENTS.md").write_text(
                "# AGENTS\n\n```markdown\n## LOOP_LOG\n```\n\n## Real Heading\n",
                encoding="utf-8",
            )
            rc, _, err = _capture(["--root", str(base)])
            self.assertEqual(rc, 0)
            self.assertNotIn("R.19", err)

    def test_current_state_does_not_match(self):
        """The closed vocabulary MUST be exact-token (case-insensitive,
        trailing-punct stripped) — not a substring search. `## Current State`
        contains the substring 'state' but is not in the vocabulary."""
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "AGENTS.md").write_text(
                "# AGENTS\n\n## Current State\nbody\n",
                encoding="utf-8",
            )
            rc, _, err = _capture(["--root", str(base)])
            self.assertEqual(rc, 0)
            self.assertNotIn("R.19", err)


if __name__ == "__main__":
    unittest.main()
