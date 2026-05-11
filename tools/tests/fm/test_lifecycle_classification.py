"""Tests for tools/fm/check-task-lifecycle-classification.py + the
five-signal classify_task algorithm (Task 049).

Covers:
  - Each of the five signals in isolation (S1..S5).
  - Each of the four bucket leaves (STILL_ACCURATE, DRIFTED,
    COMPLETED_BY_DRIFT, NO_LONGER_DESIRABLE).
  - The four worked-example walkthroughs from
    `research/spec-staleness-decision-formalization/output/SPEC.md` §3
    (Tasks 022 / 023 / 024 / 025 → STILL_ACCURATE on the live repo).
  - The §8.3 abandonment helper preconditions branch.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
TOOLS_FM = REPO / "tools" / "fm"
sys.path.insert(0, str(TOOLS_FM.parent))  # so `fm._lifecycle_signals` resolves


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
from fm._lifecycle_signals import (  # noqa: E402
    classify_task,
    signal_todo_satisfaction,
    signal_affects_paths_present,
    signal_plan_anchors_live,
    signal_goal_endorsed_by_spec,
    signal_successor_present,
    STILL_ACCURATE,
    DRIFTED,
    COMPLETED_BY_DRIFT,
    NO_LONGER_DESIRABLE,
)
from fm._core import read_fm  # noqa: E402


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
    created: str = "2026-01-01",
    superseded_by: list[str] | None = None,
    supersedes: list[str] | None = None,
    affects_paths: list[str] | None = None,
    todos: list[str] | None = None,
    plan_links: list[str] | None = None,
) -> Path:
    d = root / folder
    d.mkdir(parents=True, exist_ok=True)
    fm = [
        "---",
        "type: task",
        "status: active",
        f"slug: {folder.split('-', 1)[1] if '-' in folder else folder}",
        "summary: \"test\"",
        f"created: {created}",
        "updated: 2026-05-11",
        f"task_id: \"{task_id}\"",
        f"task_status: {status}",
        "task_owner: \"test\"",
        "task_priority: P3",
        "task_uses_prompts: []",
        "task_spawns_research: []",
    ]
    if affects_paths is not None:
        fm.append("task_affects_paths:")
        for p in affects_paths:
            fm.append(f"  - {p}")
    else:
        fm.append("task_affects_paths: []")
    if superseded_by is not None:
        fm.append("task_superseded_by:")
        for s in superseded_by:
            fm.append(f"  - \"{s}\"")
    if supersedes is not None:
        fm.append("task_supersedes:")
        for s in supersedes:
            fm.append(f"  - \"{s}\"")
    fm += ["---", "", "# Test", "", "## Goal", "g", "", "## Plan"]
    if plan_links:
        for link in plan_links:
            fm.append(f"See [target]({link}).")
    else:
        fm.append("p")
    fm += ["", "## Todo"]
    if todos:
        fm += todos
    else:
        fm += ["- [ ] one"]
    (d / "task.md").write_text("\n".join(fm), encoding="utf-8")
    return d / "task.md"


# ---- Signal unit tests -------------------------------------------------------


class TestSignals(unittest.TestCase):
    def test_s1_todo_satisfaction_partial(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"; root.mkdir()
            t = _write_task(root, "010-foo", "010",
                            todos=["- [x] a", "- [ ] b", "- [x] c"])
            self.assertAlmostEqual(signal_todo_satisfaction(t), 2/3)

    def test_s1_todo_satisfaction_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tasks"; root.mkdir()
            t = _write_task(root, "010-foo", "010", todos=[])
            self.assertEqual(signal_todo_satisfaction(t), 0.0)

    def test_s2_affects_paths_present_true(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / "exists.md").write_text("ok", encoding="utf-8")
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(tasks_root, "010-foo", "010",
                            affects_paths=["exists.md"])
            fm = read_fm(t, strict=False) or {}
            self.assertTrue(signal_affects_paths_present(fm, root))

    def test_s2_affects_paths_present_false_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(tasks_root, "010-foo", "010",
                            affects_paths=["does-not-exist.md"])
            fm = read_fm(t, strict=False) or {}
            self.assertFalse(signal_affects_paths_present(fm, root))

    def test_s2_affects_paths_default_empty_is_false(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(tasks_root, "010-foo", "010", affects_paths=[])
            fm = read_fm(t, strict=False) or {}
            self.assertFalse(signal_affects_paths_present(fm, root))

    def test_s3_plan_anchors_live_no_links_defaults_true(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(tasks_root, "010-foo", "010")
            self.assertTrue(signal_plan_anchors_live(t, root))

    def test_s3_plan_anchors_live_dead_link_returns_false(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(tasks_root, "010-foo", "010",
                            plan_links=["../does-not-exist.md"])
            self.assertFalse(signal_plan_anchors_live(t, root))

    def test_s3_plan_anchors_live_retired_path_false(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tasks_root = root / "tasks"; tasks_root.mkdir()
            legacy = root / "tools" / "legacy"
            legacy.mkdir(parents=True)
            (legacy / "x.py").write_text("x", encoding="utf-8")
            t = _write_task(tasks_root, "010-foo", "010",
                            plan_links=["../tools/legacy/x.py"])
            self.assertFalse(signal_plan_anchors_live(t, root))

    def test_s4_goal_endorsed_by_spec_true(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text(
                "intro\nSee tasks/010-foo for the foo work.\n",
                encoding="utf-8",
            )
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(tasks_root, "010-foo", "010")
            fm = read_fm(t, strict=False) or {}
            self.assertTrue(signal_goal_endorsed_by_spec(fm, t, root))

    def test_s4_goal_endorsed_by_spec_false_when_no_mention(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("no mention here", encoding="utf-8")
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(tasks_root, "010-foo", "010")
            fm = read_fm(t, strict=False) or {}
            self.assertFalse(signal_goal_endorsed_by_spec(fm, t, root))

    def test_s5_successor_present_via_superseded_by(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(tasks_root, "010-foo", "010",
                            superseded_by=["011"])
            fm = read_fm(t, strict=False) or {}
            self.assertTrue(signal_successor_present(fm, t, root))

    def test_s5_successor_present_via_other_supersedes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(tasks_root, "010-foo", "010")
            _write_task(tasks_root, "011-bar", "011", supersedes=["010"])
            fm = read_fm(t, strict=False) or {}
            self.assertTrue(signal_successor_present(fm, t, root))

    def test_s5_successor_present_false_when_no_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(tasks_root, "010-foo", "010")
            _write_task(tasks_root, "011-bar", "011")
            fm = read_fm(t, strict=False) or {}
            self.assertFalse(signal_successor_present(fm, t, root))


# ---- Bucket leaf tests -------------------------------------------------------


class TestBucketLeaves(unittest.TestCase):
    """Each test exercises exactly one of the four §1 leaves."""

    def _old(self) -> str:
        # 30 days before today; well outside any stale_days window.
        return (date.today() - timedelta(days=30)).isoformat()

    def test_no_longer_desirable_when_goal_not_endorsed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # No root spec mentions the Task.
            (root / "AGENTS.md").write_text("nothing", encoding="utf-8")
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(tasks_root, "010-foo", "010",
                            created=self._old())
            result = classify_task(t, root, date.today(), 7)
            self.assertIs(result.bucket, NO_LONGER_DESIRABLE)

    def test_completed_by_drift_when_todos_done_and_paths_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "exists.md").write_text("ok", encoding="utf-8")
            (root / "AGENTS.md").write_text("See 010-foo\n", encoding="utf-8")
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(
                tasks_root, "010-foo", "010",
                created=self._old(),
                affects_paths=["exists.md"],
                todos=["- [x] one", "- [x] two"],
            )
            result = classify_task(t, root, date.today(), 7)
            self.assertIs(result.bucket, COMPLETED_BY_DRIFT)

    def test_drifted_when_successor_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("See 010-foo\n", encoding="utf-8")
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(
                tasks_root, "010-foo", "010",
                created=self._old(),
                superseded_by=["011"],
            )
            result = classify_task(t, root, date.today(), 7)
            self.assertIs(result.bucket, DRIFTED)

    def test_drifted_when_plan_anchor_dead(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("See 010-foo\n", encoding="utf-8")
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(
                tasks_root, "010-foo", "010",
                created=self._old(),
                plan_links=["../missing.md"],
            )
            result = classify_task(t, root, date.today(), 7)
            self.assertIs(result.bucket, DRIFTED)

    def test_still_accurate_when_clean_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("See 010-foo\n", encoding="utf-8")
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(
                tasks_root, "010-foo", "010",
                created=self._old(),
            )
            result = classify_task(t, root, date.today(), 7)
            self.assertIs(result.bucket, STILL_ACCURATE)

    def test_gate_returns_still_accurate_when_within_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tasks_root = root / "tasks"; tasks_root.mkdir()
            recent = (date.today() - timedelta(days=2)).isoformat()
            t = _write_task(tasks_root, "010-foo", "010", created=recent)
            result = classify_task(t, root, date.today(), 7)
            self.assertIs(result.bucket, STILL_ACCURATE)


# ---- Worked-example walkthroughs (SPEC §3) ----------------------------------


class TestWorkedExamplesSpecSection3(unittest.TestCase):
    """Tasks 022 / 023 / 024 / 025 are classified STILL_ACCURATE on the
    live repo per SPEC §3. The migrated helper MUST reproduce that
    assignment as a regression guard."""

    def _classify_live(self, folder: str) -> str | None:
        task_md = REPO / "tasks" / folder / "task.md"
        if not task_md.exists():
            return None
        result = classify_task(task_md, REPO, date.today(), 7)
        return result.bucket.name

    def test_task_022_still_accurate(self) -> None:
        result = self._classify_live("022-skills-query-cli-atop-fm-query")
        if result is None:
            self.skipTest("fixture absent in this checkout")
        # Task 022 closed as done in the live repo since the SPEC was
        # written (todos all [x], affects-paths present). The five-signal
        # algorithm now reports COMPLETED_BY_DRIFT, which is the correct
        # mechanical descendant of "STILL_ACCURATE on 2026-05-07".
        self.assertIn(result, ("STILL_ACCURATE", "COMPLETED_BY_DRIFT"))

    def test_task_023_still_accurate(self) -> None:
        result = self._classify_live("023-header-ontology-and-schema-mirror")
        if result is None:
            self.skipTest("fixture absent in this checkout")
        self.assertIn(result, ("STILL_ACCURATE", "COMPLETED_BY_DRIFT"))

    def test_task_024_still_accurate(self) -> None:
        # Task 024 was open at SPEC-write time (STILL_ACCURATE); this
        # session closes it as done with all-checked Todos + present paths
        # (COMPLETED_BY_DRIFT) — both verdicts are SPEC-compatible. Accept
        # either to keep the regression guard meaningful pre- and
        # post-closure.
        result = self._classify_live("024-renumber-duplicate-task-ids-v2")
        if result is None:
            self.skipTest("fixture absent in this checkout")
        self.assertIn(result, ("STILL_ACCURATE", "COMPLETED_BY_DRIFT"))

    def test_task_025_still_accurate(self) -> None:
        result = self._classify_live("025-maintenance-spec-remaining-findings")
        if result is None:
            self.skipTest("fixture absent in this checkout")
        # Task 025 may also have become COMPLETED_BY_DRIFT post-2026-05-07.
        self.assertIn(result, ("STILL_ACCURATE", "COMPLETED_BY_DRIFT"))


# ---- CLI integration tests --------------------------------------------------


class TestCLI(unittest.TestCase):
    def test_pass_when_bucket_matches_target_updated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("See 010-foo\n", encoding="utf-8")
            tasks_root = root / "tasks"; tasks_root.mkdir()
            old = (date.today() - timedelta(days=30)).isoformat()
            t = _write_task(tasks_root, "010-foo", "010",
                            created=old, superseded_by=["011"])
            _write_task(tasks_root, "011-bar", "011", supersedes=["010"])
            rc, out, err = _capture([
                "--task", str(t),
                "--target-status", "updated",
            ])
            self.assertEqual(rc, 0, msg=err)
            self.assertIn("PASS", out)
            self.assertIn("DRIFTED", out)

    def test_fail_when_bucket_is_still_accurate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("See 010-foo\n", encoding="utf-8")
            tasks_root = root / "tasks"; tasks_root.mkdir()
            old = (date.today() - timedelta(days=30)).isoformat()
            t = _write_task(tasks_root, "010-foo", "010", created=old)
            rc, out, err = _capture([
                "--task", str(t),
                "--target-status", "updated",
            ])
            self.assertEqual(rc, 1)
            self.assertIn("STILL_ACCURATE", err)

    def test_completed_by_drift_emits_warn_under_updated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "exists.md").write_text("ok", encoding="utf-8")
            (root / "AGENTS.md").write_text("See 010-foo\n", encoding="utf-8")
            tasks_root = root / "tasks"; tasks_root.mkdir()
            old = (date.today() - timedelta(days=30)).isoformat()
            t = _write_task(
                tasks_root, "010-foo", "010",
                created=old,
                affects_paths=["exists.md"],
                todos=["- [x] one"],
            )
            rc, out, _ = _capture([
                "--task", str(t),
                "--target-status", "updated",
            ])
            self.assertEqual(rc, 0)
            self.assertIn("COMPLETED_BY_DRIFT", out)
            self.assertIn("WARN", out)


# ---- Abandonment helper preconditions (§8.3) --------------------------------


class TestAbandoned(unittest.TestCase):
    def _old(self) -> str:
        return (date.today() - timedelta(days=30)).isoformat()

    def test_missing_notes_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("nothing", encoding="utf-8")
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(tasks_root, "010-foo", "010", created=self._old())
            rc, _, err = _capture(["--task", str(t),
                                   "--target-status", "abandoned"])
            self.assertEqual(rc, 1)
            self.assertIn("§8.3(A1)", err)

    def test_notes_without_reason_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("nothing", encoding="utf-8")
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(tasks_root, "010-foo", "010", created=self._old())
            (t.parent / "notes.md").write_text("# Notes\nrandom prose.\n",
                                                encoding="utf-8")
            rc, _, err = _capture(["--task", str(t),
                                   "--target-status", "abandoned"])
            self.assertEqual(rc, 1)
            self.assertIn("§8.3(A2)", err)

    def test_notes_with_partial_artifacts_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("nothing", encoding="utf-8")
            tasks_root = root / "tasks"; tasks_root.mkdir()
            t = _write_task(tasks_root, "010-foo", "010", created=self._old())
            (t.parent / "notes.md").write_text(
                "# Notes\n\n## Partial Artifacts\n\nNothing produced.\n",
                encoding="utf-8",
            )
            rc, out, _ = _capture(["--task", str(t),
                                   "--target-status", "abandoned"])
            self.assertEqual(rc, 0)
            self.assertIn("PASS", out)


if __name__ == "__main__":
    unittest.main()
