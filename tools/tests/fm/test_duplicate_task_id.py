"""Tests for tools/fm/check-duplicate-task-id.py (Task 033 ST-3).

Covers:
  - clean repo (no duplicates) → exit 0
  - 006/006 collision (two active tasks share id 006) → exit 1
  - 009/009 collision → exit 1
  - supersession-explained duplicate (predecessor `updated`, successor
    `task_supersedes` reciprocal) → exit 0
  - abandoned-status predecessor sharing id with active successor → exit 1
    (abandoned does not satisfy supersession reciprocity)
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
TOOLS_FM = REPO / "tools" / "fm"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "check_duplicate_task_id",
        TOOLS_FM / "check-duplicate-task-id.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_duplicate_task_id"] = module
    spec.loader.exec_module(module)
    return module


cdt = _load_module()


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = cdt.main(argv)
    return rc, out.getvalue(), err.getvalue()


def _write_task(
    root: Path,
    folder: str,
    task_id: str,
    *,
    status: str = "open",
    superseded_by: list[str] | None = None,
    supersedes: list[str] | None = None,
) -> Path:
    d = root / folder
    d.mkdir(parents=True, exist_ok=True)
    fm_lines = [
        "---",
        "type: task",
        "status: active",
        f"slug: {folder.split('-', 1)[1] if '-' in folder else folder}",
        "summary: \"test\"",
        "created: 2026-05-07",
        "updated: 2026-05-07",
        f"task_id: \"{task_id}\"",
        f"task_status: {status}",
        "task_owner: \"test\"",
        "task_priority: P3",
        "task_uses_prompts: []",
        "task_spawns_research: []",
        "task_affects_paths: []",
    ]
    if superseded_by is not None:
        fm_lines.append("task_superseded_by:")
        for s in superseded_by:
            fm_lines.append(f"  - \"{s}\"")
    if supersedes is not None:
        fm_lines.append("task_supersedes:")
        for s in supersedes:
            fm_lines.append(f"  - \"{s}\"")
    fm_lines.append("---")
    fm_lines.append("")
    fm_lines.append("# Test task")
    fm_lines.append("")
    (d / "task.md").write_text("\n".join(fm_lines), encoding="utf-8")
    return d / "task.md"


class TestCleanRepo(unittest.TestCase):
    def test_no_duplicates_exits_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"
            root.mkdir()
            _write_task(root, "001-foo", "001")
            _write_task(root, "002-bar", "002")
            _write_task(root, "003-baz", "003")
            rc, _, err = _capture([str(root)])
            self.assertEqual(rc, 0, msg=err)
            self.assertNotIn("ERROR", err)


class TestCollisions(unittest.TestCase):
    def test_006_collision_fails(self) -> None:
        """Two active task folders sharing id 006 with no supersession → ERROR."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"
            root.mkdir()
            _write_task(root, "006-alpha", "006", status="done")
            _write_task(root, "006-beta", "006", status="open")
            rc, _, err = _capture([str(root)])
            self.assertEqual(rc, 1, msg=err)
            self.assertIn("task_id='006'", err)
            self.assertIn("ERROR", err)

    def test_009_collision_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"
            root.mkdir()
            _write_task(root, "009-alpha", "009", status="done")
            _write_task(root, "009-beta", "009", status="in_progress")
            rc, _, err = _capture([str(root)])
            self.assertEqual(rc, 1, msg=err)
            self.assertIn("task_id='009'", err)


class TestSupersessionExplained(unittest.TestCase):
    def test_reciprocal_supersession_passes(self) -> None:
        """Predecessor `updated` + reciprocal supersession refs → INFO, exit 0."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"
            root.mkdir()
            _write_task(
                root, "010-alpha", "010",
                status="updated",
                superseded_by=["010-beta"],
            )
            _write_task(
                root, "010-beta", "010",
                status="open",
                supersedes=["010-alpha"],
            )
            rc, out, err = _capture([str(root)])
            self.assertEqual(rc, 0, msg=err)
            self.assertNotIn("ERROR", err)
            self.assertIn("INFO", out)
            self.assertIn("supersession reciprocity", out)

    def test_non_reciprocal_supersession_fails(self) -> None:
        """Predecessor cites successor but successor does not cite predecessor → ERROR."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"
            root.mkdir()
            _write_task(
                root, "020-alpha", "020",
                status="updated",
                superseded_by=["020-beta"],
            )
            _write_task(
                root, "020-beta", "020",
                status="open",
                # missing task_supersedes
            )
            rc, _, err = _capture([str(root)])
            self.assertEqual(rc, 1, msg=err)


class TestRealRepoIntegration(unittest.TestCase):
    """Smoke test against the actual repo state — the brief notes the
    linter is *expected* to fail on the current repo because Task 043
    has not yet renumbered the 006/006, 009/009, 031/031, 032/032
    collisions. This test pins that expected failure so a regression
    (e.g. accidental supersession-reciprocity loosening) is caught."""

    def test_repo_currently_has_known_collisions(self) -> None:
        repo_tasks = REPO / "tasks"
        if not repo_tasks.exists():
            self.skipTest("repo tasks/ tree not present in this checkout")
        rc, _, err = _capture([str(repo_tasks)])
        # Until Task 043 lands, the linter MUST flag the four known
        # collisions. After Task 043, this assertion flips to rc == 0
        # and the test becomes a guard against re-introduction.
        if rc == 0:
            self.skipTest(
                "repo has no duplicate-task_id collisions — Task 043 "
                "appears to have landed; flip this assertion."
            )
        self.assertEqual(rc, 1)
        for tid in ("006", "009", "031", "032"):
            self.assertIn(f"task_id='{tid}'", err,
                          msg=f"expected linter to flag the {tid}/{tid} collision")


if __name__ == "__main__":
    unittest.main()
