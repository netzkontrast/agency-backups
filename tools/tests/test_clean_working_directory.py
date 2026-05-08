"""Tests for tools/check-clean-working-directory.py (PRE_COMMIT.md PC.1.1).

Covers Acceptance Criteria from
prompts/tooling-clean-working-directory-linter/brief.md:
  - clean tree (pass)
  - scratchpad outside an exempt directory (ERROR)
  - scratchpad inside `/tools/` (pass — exempt)
  - scratchpad inside `/decisions/` (pass — FOLDERS.md §8 exempt)
  - allowlisted scratchpad (pass)
  - session.log preserved (pass)
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
        "check_clean_working_directory",
        TOOLS / "check-clean-working-directory.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_clean_working_directory"] = module
    spec.loader.exec_module(module)
    return module


ccwd = _load_module()


def _capture(argv: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    """Invoke main() with patched REPO_ROOT to point at a temp tree."""
    out, err = io.StringIO(), io.StringIO()
    saved_root = ccwd.REPO_ROOT
    saved_allow = ccwd._ALLOWLIST_FILE
    if cwd is not None:
        ccwd.REPO_ROOT = cwd
        ccwd._ALLOWLIST_FILE = cwd / "tools" / ".script-allowlist"
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = ccwd.main(argv)
    finally:
        ccwd.REPO_ROOT = saved_root
        ccwd._ALLOWLIST_FILE = saved_allow
    return rc, out.getvalue(), err.getvalue()


class CleanWorkingDirectoryTests(unittest.TestCase):

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        # Mirror the relevant exempt dirs so the test is isolated.
        for d in ("tools", "tests", "decisions", "skills", "templates",
                  "maintenance", "Agency-System", ".githooks", ".agent_cache"):
            (self.root / d).mkdir()

    def _write(self, rel: str, content: str = "") -> Path:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return p

    def test_clean_tree_passes(self) -> None:
        self._write("README.md", "# stub")
        self._write("tasks/000-x/task.md", "# stub")
        rc, _, err = _capture([str(self.root)], cwd=self.root)
        self.assertEqual(rc, 0, msg=err)
        self.assertEqual(err.strip(), "")

    def test_scratchpad_outside_exempt_dir_errors(self) -> None:
        self._write("tasks/000-x/scratch.py", "print(1)")
        rc, _, err = _capture([str(self.root)], cwd=self.root)
        self.assertEqual(rc, 1)
        self.assertIn("PC.1.1:script-scratchpad", err)
        self.assertIn("tasks/000-x/scratch.py", err)

    def test_scratchpad_in_tools_passes(self) -> None:
        self._write("tools/scratch.py", "x")
        rc, _, err = _capture([str(self.root)], cwd=self.root)
        self.assertEqual(rc, 0, msg=err)

    def test_scratchpad_in_decisions_passes(self) -> None:
        # FOLDERS.md §8 exemption — `/decisions/` is governed by adr/cli.py,
        # not by PC.1.1.
        self._write("decisions/0001-stray.py", "x")
        rc, _, err = _capture([str(self.root)], cwd=self.root)
        self.assertEqual(rc, 0, msg=err)

    def test_scratchpad_in_tests_passes(self) -> None:
        self._write("tests/fm/test_x.py", "x")
        rc, _, err = _capture([str(self.root)], cwd=self.root)
        self.assertEqual(rc, 0, msg=err)

    def test_session_log_preserved(self) -> None:
        # RESEARCH.md §4.5 — session.log is mandatory and must not trigger.
        self._write("research/x/workspace/session.log", "trace")
        rc, _, err = _capture([str(self.root)], cwd=self.root)
        self.assertEqual(rc, 0, msg=err)

    def test_arbitrary_log_outside_exempt_dir_errors(self) -> None:
        self._write("research/x/workspace/trace.log", "noise")
        rc, _, err = _capture([str(self.root)], cwd=self.root)
        self.assertEqual(rc, 1)
        self.assertIn("trace.log", err)

    def test_allowlist_silences_match(self) -> None:
        self._write("tasks/041-extract-subtask-prompts/scripts/extract.py", "x")
        # Mirror the production allowlist line.
        self._write(
            "tools/.script-allowlist",
            "tasks/041-extract-subtask-prompts/scripts/*.py\n",
        )
        rc, _, err = _capture([str(self.root)], cwd=self.root)
        self.assertEqual(rc, 0, msg=err)

    def test_allowlist_does_not_silence_unrelated(self) -> None:
        self._write("tasks/041-extract-subtask-prompts/scripts/extract.py", "x")
        self._write("tasks/099-other/scratch.py", "x")
        self._write(
            "tools/.script-allowlist",
            "tasks/041-extract-subtask-prompts/scripts/*.py\n",
        )
        rc, _, err = _capture([str(self.root)], cwd=self.root)
        self.assertEqual(rc, 1)
        self.assertIn("tasks/099-other/scratch.py", err)
        self.assertNotIn("041-extract", err)

    def test_diagnostic_format_matches_pc11(self) -> None:
        self._write("foo/bar.sh", "echo")
        rc, _, err = _capture([str(self.root)], cwd=self.root)
        self.assertEqual(rc, 1)
        # Format: <relpath>::ERROR:PC.1.1:script-scratchpad
        self.assertRegex(
            err,
            r"^foo/bar\.sh::ERROR:PC\.1\.1:script-scratchpad\s*$",
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
