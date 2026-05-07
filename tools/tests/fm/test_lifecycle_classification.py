"""Tests for tools/fm/check-task-lifecycle-classification.py (Task 033 ST-4).

Covers each of the four §4.7 conditions in isolation plus the §8.3
abandonment-helper branch.
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
        "check_task_lifecycle_classification",
        TOOLS_FM / "check-task-lifecycle-classification.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_task_lifecycle_classification"] = module
    spec.loader.exec_module(module)
    return module


cl = _load_module()


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = cl.main(argv)
    return rc, out.getvalue(), err.getvalue()


def _write_task(
    root: Path,
    folder: str,
    task_id: str,
    *,
    status: str = "open",
    superseded_by: list[str] | None = None,
    supersedes: list[str] | None = None,
    todos: list[str] | None = None,
) -> Path:
    d = root / folder
    d.mkdir(parents=True, exist_ok=True)
    fm = [
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
        fm.append("task_superseded_by:")
        for s in superseded_by:
            fm.append(f"  - \"{s}\"")
    if supersedes is not None:
        fm.append("task_supersedes:")
        for s in supersedes:
            fm.append(f"  - \"{s}\"")
    fm += ["---", "", "# Test", "", "## Goal", "g", "", "## Plan", "p", "", "## Todo"]
    if todos:
        fm += todos
    else:
        fm += ["- [ ] one"]
    (d / "task.md").write_text("\n".join(fm), encoding="utf-8")
    return d / "task.md"


class TestUpdatedConditions(unittest.TestCase):
    def test_missing_attestation_flags_fail(self) -> None:
        """§4.7(1) and §4.7(2) ERR when CLI flags absent."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"; root.mkdir()
            t = _write_task(root, "010-foo", "010")
            rc, _, err = _capture(["--task", str(t), "--target-status", "updated"])
            self.assertEqual(rc, 1)
            self.assertIn("§4.7(1)", err)
            self.assertIn("§4.7(2)", err)

    def test_no_successor_fails_condition_3(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"; root.mkdir()
            t = _write_task(root, "010-foo", "010")
            rc, _, err = _capture([
                "--task", str(t),
                "--target-status", "updated",
                "--goal-still-desirable", "--plan-drifted",
            ])
            self.assertEqual(rc, 1)
            self.assertIn("§4.7(3)", err)

    def test_unresolved_successor_ref_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"; root.mkdir()
            t = _write_task(root, "010-foo", "010", superseded_by=["999"])
            rc, _, err = _capture([
                "--task", str(t),
                "--target-status", "updated",
                "--goal-still-desirable", "--plan-drifted",
            ])
            self.assertEqual(rc, 1)
            self.assertIn("does not resolve", err)

    def test_reciprocity_broken_fails_condition_4(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"; root.mkdir()
            pred = _write_task(root, "010-foo", "010", superseded_by=["011"])
            _write_task(root, "011-bar", "011")  # successor missing task_supersedes
            rc, _, err = _capture([
                "--task", str(pred),
                "--target-status", "updated",
                "--goal-still-desirable", "--plan-drifted",
            ])
            self.assertEqual(rc, 1)
            self.assertIn("§4.7(4)", err)

    def test_full_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"; root.mkdir()
            pred = _write_task(root, "010-foo", "010", superseded_by=["011"])
            _write_task(root, "011-bar", "011", supersedes=["010"])
            rc, out, err = _capture([
                "--task", str(pred),
                "--target-status", "updated",
                "--goal-still-desirable", "--plan-drifted",
            ])
            self.assertEqual(rc, 0, msg=err)
            self.assertIn("PASS", out)

    def test_all_todos_checked_emits_warn(self) -> None:
        """Heuristic WARN when every todo is already `[x]` (suggests `done`)."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"; root.mkdir()
            pred = _write_task(
                root, "010-foo", "010",
                superseded_by=["011"],
                todos=["- [x] one", "- [x] two"],
            )
            _write_task(root, "011-bar", "011", supersedes=["010"])
            rc, out, err = _capture([
                "--task", str(pred),
                "--target-status", "updated",
                "--goal-still-desirable", "--plan-drifted",
            ])
            self.assertEqual(rc, 0)
            self.assertIn("heuristic", out)


class TestAbandoned(unittest.TestCase):
    def test_missing_notes_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"; root.mkdir()
            t = _write_task(root, "010-foo", "010")
            rc, _, err = _capture(["--task", str(t), "--target-status", "abandoned"])
            self.assertEqual(rc, 1)
            self.assertIn("§8.3(A1)", err)

    def test_notes_without_reason_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"; root.mkdir()
            t = _write_task(root, "010-foo", "010")
            (t.parent / "notes.md").write_text("# Notes\n\nrandom prose.\n", encoding="utf-8")
            rc, _, err = _capture(["--task", str(t), "--target-status", "abandoned"])
            self.assertEqual(rc, 1)
            self.assertIn("§8.3(A2)", err)

    def test_notes_with_partial_artifacts_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"; root.mkdir()
            t = _write_task(root, "010-foo", "010")
            (t.parent / "notes.md").write_text(
                "# Notes\n\n## Partial Artifacts\n\nNothing produced.\n",
                encoding="utf-8",
            )
            rc, out, _ = _capture(["--task", str(t), "--target-status", "abandoned"])
            self.assertEqual(rc, 0)
            self.assertIn("PASS", out)


if __name__ == "__main__":
    unittest.main()
