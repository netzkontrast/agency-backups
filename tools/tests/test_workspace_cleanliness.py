"""Tests for tools/check-workspace-cleanliness.py — Task 035 ST-2.

Coverage per the brief at
prompts/tooling-workspace-cleanliness-linter/brief.md §Acceptance Criteria:

  * clean workspace — exit 0.
  * straggler .py — exit 1, WARN diagnostic with R.4.4 code.
  * straggler .sh — exit 1.
  * .cleanignore exempt — exit 0.
  * session.log allowed — exit 0.
  * missing-workspace edge case — exit 0.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOLS = REPO / "tools"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "check_workspace_cleanliness",
        TOOLS / "check-workspace-cleanliness.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_workspace_cleanliness"] = module
    spec.loader.exec_module(module)
    return module


cwc = _load_module()


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = cwc.main(argv)
    return rc, out.getvalue(), err.getvalue()


@contextlib.contextmanager
def _fake_repo():
    """Build a synthetic repo with a research/<slug>/workspace tree.

    The linter resolves paths against ``REPO_ROOT``; we monkey-patch that
    constant so the temp tree is treated as the repository root.
    """
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        ws = root / "research" / "demo" / "workspace"
        ws.mkdir(parents=True)
        original_root = cwc.REPO_ROOT
        cwc.REPO_ROOT = root
        cwd = os.getcwd()
        os.chdir(root)
        try:
            yield root, ws
        finally:
            cwc.REPO_ROOT = original_root
            os.chdir(cwd)


class CleanWorkspace(unittest.TestCase):
    def test_clean_workspace_exits_zero(self) -> None:
        with _fake_repo() as (_root, ws):
            (ws / "session.log").write_text("ok\n")
            (ws / "notes.md").write_text("notes\n")
            rc, _, err = _capture([str(ws)])
            self.assertEqual(rc, 0, err)
            self.assertEqual(err, "")

    def test_straggler_py_emits_warn(self) -> None:
        with _fake_repo() as (_root, ws):
            (ws / "scratch.py").write_text("print('x')\n")
            rc, _, err = _capture([str(ws)])
            self.assertEqual(rc, 1, err)
            self.assertIn("WARN:R.4.4:execution-script-not-cleaned", err)
            self.assertIn("research/demo/workspace/scratch.py", err)

    def test_straggler_sh_emits_warn(self) -> None:
        with _fake_repo() as (_root, ws):
            (ws / "run.sh").write_text("echo x\n")
            rc, _, err = _capture([str(ws)])
            self.assertEqual(rc, 1, err)
            self.assertIn("research/demo/workspace/run.sh", err)

    def test_cleanignore_exempts_path(self) -> None:
        with _fake_repo() as (_root, ws):
            (ws / "scratch.py").write_text("print('x')\n")
            (ws / ".cleanignore").write_text("scratch.py\n")
            rc, _, err = _capture([str(ws)])
            self.assertEqual(rc, 0, err)

    def test_cleanignore_glob_exempts_subdir(self) -> None:
        with _fake_repo() as (_root, ws):
            sub = ws / "examples"
            sub.mkdir()
            (sub / "demo.py").write_text("x\n")
            (ws / ".cleanignore").write_text("examples/*.py\n")
            rc, _, err = _capture([str(ws)])
            self.assertEqual(rc, 0, err)

    def test_session_log_always_allowed(self) -> None:
        with _fake_repo() as (_root, ws):
            (ws / "session.log").write_text("trace\n")
            rc, _, err = _capture([str(ws)])
            self.assertEqual(rc, 0, err)

    def test_other_log_flagged(self) -> None:
        with _fake_repo() as (_root, ws):
            (ws / "stderr.log").write_text("noise\n")
            rc, _, err = _capture([str(ws)])
            self.assertEqual(rc, 1, err)
            self.assertIn("stderr.log", err)

    def test_missing_workspace_is_silent(self) -> None:
        """Pointing the linter at a non-research/ tree returns 0."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "src").mkdir()
            (root / "src" / "tool.py").write_text("x\n")
            rc, _, err = _capture([str(root)])
            self.assertEqual(rc, 0, err)

    def test_non_existent_path_is_silent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ghost = Path(td) / "does-not-exist"
            rc, _, _ = _capture([str(ghost)])
            self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
