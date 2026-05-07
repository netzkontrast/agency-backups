"""Tests for the Task 019 ST-6 legacy linter shims.

The legacy CLI surface is preserved so tools/check-governance.sh stays
green; behaviour is sourced from fm-validate --type-check.
"""
from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


class TestLintLinkageShim(unittest.TestCase):
    """tools/legacy/lint-linkage.py is a thin shim around fm-validate
    --type-check (Task 019 ST-6)."""

    def test_clean_tree_exits_zero(self) -> None:
        # Running against the live repo tree must exit 0 (the live tree is
        # clean under --type-check at the time of this commit).
        env = {**os.environ, "FM_LEGACY_QUIET": "1"}
        result = subprocess.run(
            [sys.executable, "tools/legacy/lint-linkage.py"],
            cwd=REPO_ROOT, env=env, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0,
                          msg=f"stdout: {result.stdout}\nstderr: {result.stderr}")
        self.assertIn("shim", result.stderr)

    def test_top_shim_works_too(self) -> None:
        env = {**os.environ, "FM_LEGACY_QUIET": "1"}
        result = subprocess.run(
            [sys.executable, "tools/lint-linkage.py"],
            cwd=REPO_ROOT, env=env, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
