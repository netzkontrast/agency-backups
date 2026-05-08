"""Tests for tools/maintenance/staleness-audit.py.

Coverage matrix (per Task 039 ST-3 brief):

    Required by ST-3 brief:
      - Each of the four §3.4 buckets exercised at least once.
      - The age-gate (`MAINT_STALE_DAYS`) skips young tasks.
      - Missing-field defaults match SPEC §2.
      - Worked examples Tasks 022/023/024/025 from SPEC §3 reproduce
        STILL_ACCURATE bucket assignment.

The fixtures use `tempfile.TemporaryDirectory` to mint a synthetic repo
root with a minimal `tasks/<NNN>-<slug>/task.md` corpus plus a stand-in
root spec, so the linter exercises the real `_audit_one` path without
mutating the live repo.
"""
from __future__ import annotations

import contextlib
import datetime as dt
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
TOOLS = REPO / "tools"
LIVE_TASKS = REPO / "tasks"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "staleness_audit",
        TOOLS / "maintenance" / "staleness-audit.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["staleness_audit"] = module
    spec.loader.exec_module(module)
    return module


sa = _load_module()


# ---- Fixture helpers ------------------------------------------------------


def _write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def _build_task_md(
    *,
    task_id: str,
    slug: str,
    created: str = "2026-01-01",
    updated: str = "2026-01-01",
    status: str = "open",
    affects_paths: list[str] | None = None,
    superseded_by: list[str] | None = None,
    todo_lines: list[str] | None = None,
    plan_links: list[str] | None = None,
    extra_frontmatter: str = "",
) -> str:
    """Render a minimal but well-formed task.md body."""
    affects_block = ""
    if affects_paths:
        affects_block = "task_affects_paths:\n" + "".join(
            f"  - {p}\n" for p in affects_paths
        )
    elif affects_paths is None:
        affects_block = "task_affects_paths: []\n"
    else:
        affects_block = "task_affects_paths: []\n"

    superseded_block = ""
    if superseded_by:
        superseded_block = "task_superseded_by:\n" + "".join(
            f"  - \"{s}\"\n" for s in superseded_by
        )
    else:
        superseded_block = "task_superseded_by: []\n"

    todo = "\n".join(todo_lines or ["- [ ] 1. placeholder"])
    plan = "\n".join(plan_links or ["1. placeholder step (no link)"])

    return (
        "---\n"
        "type: task\n"
        "status: active\n"
        f"slug: {slug}\n"
        "summary: \"fixture\"\n"
        f"created: {created}\n"
        f"updated: {updated}\n"
        f"task_id: \"{task_id}\"\n"
        f"task_status: {status}\n"
        "task_owner: \"unassigned\"\n"
        "task_priority: P2\n"
        "task_uses_prompts: []\n"
        "task_spawns_research: []\n"
        "task_spawns_prompts: []\n"
        "task_blocked_by: []\n"
        f"{superseded_block}"
        "task_supersedes: []\n"
        f"{affects_block}"
        f"{extra_frontmatter}"
        "---\n"
        "\n"
        f"# Task {task_id} — {slug}\n"
        "\n"
        "## Goal\n"
        "\n"
        "fixture goal.\n"
        "\n"
        "## Plan\n"
        "\n"
        f"{plan}\n"
        "\n"
        "## Todo\n"
        "\n"
        f"{todo}\n"
    )


def _seed_repo(
    tmp: Path,
    *,
    spec_mentions: list[str] | None = None,
    spec_name: str = "TASK.md",
) -> Path:
    """Build a stand-in repo root with AGENTS.md plus the named root spec.

    `spec_mentions` is a list of substrings the named root spec MUST contain,
    used to drive the S4 (`goal_endorsed`) signal. AGENTS.md is required
    for `_core.repo_root_from_cwd` discovery.
    """
    (tmp / "AGENTS.md").write_text("# Agents (fixture)\n", encoding="utf-8")
    body = "# Spec (fixture)\n\n"
    for mention in spec_mentions or []:
        body += f"- references {mention}\n"
    (tmp / spec_name).write_text(body, encoding="utf-8")
    (tmp / "tasks").mkdir(exist_ok=True)
    return tmp


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = sa.main(argv)
    return rc, out.getvalue(), err.getvalue()


# ---- Tests ---------------------------------------------------------------


class TestConfigResolution(unittest.TestCase):
    def test_default_when_unset(self) -> None:
        self.assertEqual(sa.resolve_stale_days(None, env={}), sa.DEFAULT_STALE_DAYS)

    def test_env_override(self) -> None:
        self.assertEqual(sa.resolve_stale_days(None, env={"MAINT_STALE_DAYS": "14"}), 14)

    def test_cli_override_wins(self) -> None:
        self.assertEqual(
            sa.resolve_stale_days(3, env={"MAINT_STALE_DAYS": "999"}), 3
        )

    def test_negative_rejected(self) -> None:
        with self.assertRaises(ValueError):
            sa.resolve_stale_days(0, env={})

    def test_non_integer_env_rejected(self) -> None:
        with self.assertRaises(ValueError):
            sa.resolve_stale_days(None, env={"MAINT_STALE_DAYS": "abc"})

    def test_overlong_rejected(self) -> None:
        with self.assertRaises(ValueError):
            sa.resolve_stale_days(None, env={"MAINT_STALE_DAYS": "9999"})


class TestAgeGate(unittest.TestCase):
    def test_young_task_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            _seed_repo(tmp)
            tdir = tmp / "tasks" / "100-young"
            _write(
                tdir / "task.md",
                _build_task_md(
                    task_id="100",
                    slug="young",
                    created="2026-05-05",
                    updated="2026-05-05",
                ),
            )
            results = sa.audit_tasks(
                repo_root=tmp,
                today=dt.date(2026, 5, 8),
                stale_days=7,
            )
            self.assertEqual(len(results), 1)
            rec, sig = results[0]
            self.assertTrue(rec.skipped)
            self.assertIsNone(sig)
            self.assertEqual(rec.bucket, sa.BUCKET_STILL_ACCURATE)

    def test_old_task_is_audited(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            _seed_repo(tmp)
            tdir = tmp / "tasks" / "100-old"
            _write(
                tdir / "task.md",
                _build_task_md(
                    task_id="100",
                    slug="old",
                    created="2026-04-01",
                    updated="2026-04-01",
                ),
            )
            results = sa.audit_tasks(
                repo_root=tmp,
                today=dt.date(2026, 5, 8),
                stale_days=7,
            )
            self.assertEqual(len(results), 1)
            rec, sig = results[0]
            self.assertFalse(rec.skipped)
            self.assertIsNotNone(sig)


class TestStillAccurate(unittest.TestCase):
    """Bucket 1 — the steady-state outcome."""

    def test_endorsed_partial_todo_no_successor_anchors_live(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            _seed_repo(tmp, spec_mentions=["my-feature"], spec_name="MAINTENANCE.md")
            (tmp / "tools").mkdir(exist_ok=True)
            (tmp / "tools" / "my-feature.py").write_text("x", encoding="utf-8")
            tdir = tmp / "tasks" / "100-my-feature"
            _write(
                tdir / "task.md",
                _build_task_md(
                    task_id="100",
                    slug="my-feature",
                    created="2026-04-01",
                    affects_paths=["tools/my-feature.py"],
                ),
            )
            results = sa.audit_tasks(
                repo_root=tmp,
                today=dt.date(2026, 5, 8),
                stale_days=7,
            )
            rec, sig = results[0]
            self.assertEqual(rec.bucket, sa.BUCKET_STILL_ACCURATE)
            self.assertTrue(sig.goal_endorsed)
            self.assertFalse(sig.successor_present)
            self.assertTrue(sig.plan_anchors_live)
            self.assertLess(sig.todo_satisfaction, 1.0)


class TestDrifted(unittest.TestCase):
    """Bucket 2 — DRIFTED via successor_present OR plan-anchor retired."""

    def test_drifted_via_superseded_by(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            _seed_repo(tmp, spec_mentions=["legacy-thing"], spec_name="TASK.md")
            (tmp / "tools").mkdir(exist_ok=True)
            (tmp / "tools" / "legacy-thing.py").write_text("x", encoding="utf-8")
            tdir = tmp / "tasks" / "100-legacy-thing"
            _write(
                tdir / "task.md",
                _build_task_md(
                    task_id="100",
                    slug="legacy-thing",
                    created="2026-04-01",
                    affects_paths=["tools/legacy-thing.py"],
                    superseded_by=["200"],
                ),
            )
            results = sa.audit_tasks(
                repo_root=tmp,
                today=dt.date(2026, 5, 8),
                stale_days=7,
            )
            rec, sig = results[0]
            self.assertEqual(rec.bucket, sa.BUCKET_DRIFTED)
            self.assertTrue(sig.successor_present)
            self.assertTrue(sig.goal_endorsed)

    def test_drifted_via_retired_plan_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            _seed_repo(tmp, spec_mentions=["renumber"], spec_name="MAINTENANCE.md")
            (tmp / "tools" / "legacy").mkdir(parents=True, exist_ok=True)
            (tmp / "tools" / "legacy" / "old.py").write_text("x", encoding="utf-8")
            (tmp / "tools" / "renumber.py").write_text("x", encoding="utf-8")
            tdir = tmp / "tasks" / "100-renumber"
            _write(
                tdir / "task.md",
                _build_task_md(
                    task_id="100",
                    slug="renumber",
                    created="2026-04-01",
                    affects_paths=["tools/renumber.py"],
                    plan_links=[
                        "1. invoke [legacy](../../tools/legacy/old.py)",
                    ],
                ),
            )
            results = sa.audit_tasks(
                repo_root=tmp,
                today=dt.date(2026, 5, 8),
                stale_days=7,
            )
            rec, sig = results[0]
            self.assertEqual(rec.bucket, sa.BUCKET_DRIFTED)
            self.assertFalse(sig.plan_anchors_live)


class TestCompletedByDrift(unittest.TestCase):
    """Bucket 3 — every Todo checked AND every affects-path on disk."""

    def test_completed_by_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            _seed_repo(tmp, spec_mentions=["finished"], spec_name="TASK.md")
            (tmp / "artefact.md").write_text("x", encoding="utf-8")
            tdir = tmp / "tasks" / "100-finished"
            _write(
                tdir / "task.md",
                _build_task_md(
                    task_id="100",
                    slug="finished",
                    created="2026-04-01",
                    affects_paths=["artefact.md"],
                    todo_lines=["- [x] 1. ship it", "- [x] 2. test it"],
                ),
            )
            results = sa.audit_tasks(
                repo_root=tmp,
                today=dt.date(2026, 5, 8),
                stale_days=7,
            )
            rec, sig = results[0]
            self.assertEqual(rec.bucket, sa.BUCKET_COMPLETED_BY_DRIFT)
            self.assertGreaterEqual(sig.todo_satisfaction, 1.0)
            self.assertTrue(sig.affects_paths_present)


class TestNoLongerDesirable(unittest.TestCase):
    """Bucket 4 — Goal not endorsed by any current root spec."""

    def test_goal_not_endorsed_anywhere(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            # Seed the repo WITHOUT mentioning the slug or affects-paths in
            # any root spec, and create blank root specs so S4 finds nothing.
            (tmp / "AGENTS.md").write_text("# A\n", encoding="utf-8")
            for s in sa.ROOT_SPECS:
                if s == "AGENTS.md":
                    continue
                (tmp / s).write_text(f"# {s}\n", encoding="utf-8")
            (tmp / "tasks").mkdir(exist_ok=True)
            (tmp / "deleted-feature.py").write_text("x", encoding="utf-8")
            tdir = tmp / "tasks" / "100-deleted-feature"
            _write(
                tdir / "task.md",
                _build_task_md(
                    task_id="100",
                    slug="deleted-feature",
                    created="2026-04-01",
                    affects_paths=["deleted-feature.py"],
                ),
            )
            results = sa.audit_tasks(
                repo_root=tmp,
                today=dt.date(2026, 5, 8),
                stale_days=7,
            )
            rec, sig = results[0]
            self.assertEqual(rec.bucket, sa.BUCKET_NO_LONGER_DESIRABLE)
            self.assertFalse(sig.goal_endorsed)


class TestMissingFieldDefaults(unittest.TestCase):
    """SPEC §2 'Defaults under ambiguity' regression coverage."""

    def test_no_todo_section_defaults_to_zero(self) -> None:
        body = "## Goal\n\nfixture\n\n## Plan\n\n1. step\n"
        self.assertEqual(sa.signal_todo_satisfaction(body), 0.0)

    def test_empty_affects_paths_defaults_false(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            self.assertFalse(sa.signal_affects_paths_present([], tmp))

    def test_no_plan_section_defaults_live(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            (tmp / "tasks" / "100-x").mkdir(parents=True)
            live, retired = sa._check_plan_links("# no plan\n", tmp / "tasks" / "100-x", tmp)
            self.assertTrue(live)
            self.assertEqual(retired, [])

    def test_goal_endorsed_default_false(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            self.assertFalse(sa.signal_goal_endorsed("100", "no-such-thing", [], tmp))

    def test_successor_default_false(self) -> None:
        present, evidence = sa.signal_successor_present(
            "100", {"task_superseded_by": []}, []
        )
        self.assertFalse(present)
        self.assertEqual(evidence, [])


class TestClosedTasksExcluded(unittest.TestCase):
    """Only `task_status` ∈ {open, in_progress} participate in the audit."""

    def test_done_task_skipped_from_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            _seed_repo(tmp)
            tdir = tmp / "tasks" / "100-done"
            _write(
                tdir / "task.md",
                _build_task_md(
                    task_id="100",
                    slug="done",
                    created="2026-04-01",
                    status="done",
                ),
            )
            results = sa.audit_tasks(
                repo_root=tmp,
                today=dt.date(2026, 5, 8),
                stale_days=7,
            )
            self.assertEqual(results, [])


# ---- §3 worked examples — Tasks 022 / 023 / 024 / 025 against the live repo ---


class TestSpecWorkedExamples(unittest.TestCase):
    """SPEC §3 worked examples — Tasks 022/023/024/025 must classify
    STILL_ACCURATE against the live `tasks/` corpus when the audit clock
    matches the SPEC's evaluation context (2026-05-08 with stale_days=1
    forces all four into the audit window — gate-equivalent to SPEC §3
    'evaluated as if the gate fires')."""

    @classmethod
    def setUpClass(cls) -> None:
        if not LIVE_TASKS.is_dir():
            raise unittest.SkipTest("live tasks/ tree absent; cannot run §3 walkthroughs")
        cls.results = {
            rec.task_id: (rec, sig)
            for rec, sig in sa.audit_tasks(
                repo_root=REPO,
                today=dt.date(2026, 5, 8),
                stale_days=1,
            )
        }

    def _assert_bucket(self, task_id: str, expected: str) -> None:
        self.assertIn(
            task_id,
            self.results,
            msg=f"Task {task_id} not in active corpus — fixture drift?",
        )
        rec, _sig = self.results[task_id]
        self.assertEqual(
            rec.bucket,
            expected,
            msg=(
                f"Task {task_id}: SPEC §3 expects {expected}, got {rec.bucket}; "
                f"evidence={rec.evidence}"
            ),
        )

    def test_task_022_still_accurate(self) -> None:
        self._assert_bucket("022", sa.BUCKET_STILL_ACCURATE)

    def test_task_023_still_accurate(self) -> None:
        self._assert_bucket("023", sa.BUCKET_STILL_ACCURATE)

    def test_task_024_still_accurate(self) -> None:
        self._assert_bucket("024", sa.BUCKET_STILL_ACCURATE)

    def test_task_025_still_accurate(self) -> None:
        self._assert_bucket("025", sa.BUCKET_STILL_ACCURATE)


# ---- CLI integration tests -----------------------------------------------


class TestCliFormats(unittest.TestCase):
    def test_diagnostic_format_emits_path_double_colon_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            _seed_repo(tmp, spec_mentions=["my-feature"], spec_name="MAINTENANCE.md")
            (tmp / "tools").mkdir(exist_ok=True)
            (tmp / "tools" / "my-feature.py").write_text("x", encoding="utf-8")
            _write(
                tmp / "tasks" / "100-my-feature" / "task.md",
                _build_task_md(
                    task_id="100",
                    slug="my-feature",
                    created="2026-04-01",
                    affects_paths=["tools/my-feature.py"],
                ),
            )
            rc, out, err = _capture(
                [
                    "--today",
                    "2026-05-08",
                    "--stale-days",
                    "7",
                    "--repo-root",
                    str(tmp),
                ]
            )
            self.assertEqual(rc, 0)
            self.assertIn("MAINT.STALE.STILL_ACCURATE", out)
            self.assertIn("staleness-audit:", err)

    def test_json_format_is_parseable(self) -> None:
        import json

        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            _seed_repo(tmp, spec_mentions=["a"], spec_name="MAINTENANCE.md")
            (tmp / "a").write_text("x", encoding="utf-8")
            _write(
                tmp / "tasks" / "100-a" / "task.md",
                _build_task_md(
                    task_id="100",
                    slug="a",
                    created="2026-04-01",
                    affects_paths=["a"],
                ),
            )
            rc, out, _ = _capture(
                [
                    "--today",
                    "2026-05-08",
                    "--stale-days",
                    "7",
                    "--repo-root",
                    str(tmp),
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(rc, 0)
            payload = json.loads(out)
            self.assertEqual(payload["maint_stale_days"], 7)
            self.assertEqual(payload["task_count"], 1)
            self.assertEqual(payload["tasks"][0]["bucket"], "still_accurate")

    def test_bad_today_returns_1(self) -> None:
        rc, _, err = _capture(["--today", "not-a-date"])
        self.assertEqual(rc, 1)
        self.assertIn("--today", err)

    def test_bad_stale_days_env_returns_1(self) -> None:
        import os

        prev = os.environ.get("MAINT_STALE_DAYS")
        os.environ["MAINT_STALE_DAYS"] = "abc"
        try:
            rc, _, err = _capture(["--today", "2026-05-08"])
        finally:
            if prev is None:
                os.environ.pop("MAINT_STALE_DAYS", None)
            else:
                os.environ["MAINT_STALE_DAYS"] = prev
        self.assertEqual(rc, 1)
        self.assertIn("MAINT_STALE_DAYS", err)


class TestExitCodes(unittest.TestCase):
    def test_all_still_accurate_exits_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            _seed_repo(tmp, spec_mentions=["x"], spec_name="MAINTENANCE.md")
            (tmp / "x").write_text("y", encoding="utf-8")
            _write(
                tmp / "tasks" / "100-x" / "task.md",
                _build_task_md(
                    task_id="100",
                    slug="x",
                    created="2026-04-01",
                    affects_paths=["x"],
                ),
            )
            rc, _, _ = _capture(
                [
                    "--today",
                    "2026-05-08",
                    "--stale-days",
                    "7",
                    "--repo-root",
                    str(tmp),
                ]
            )
            self.assertEqual(rc, 0)

    def test_drifted_exits_two(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            _seed_repo(tmp, spec_mentions=["x"], spec_name="MAINTENANCE.md")
            (tmp / "x").write_text("y", encoding="utf-8")
            _write(
                tmp / "tasks" / "100-x" / "task.md",
                _build_task_md(
                    task_id="100",
                    slug="x",
                    created="2026-04-01",
                    affects_paths=["x"],
                    superseded_by=["200"],
                ),
            )
            rc, _, _ = _capture(
                [
                    "--today",
                    "2026-05-08",
                    "--stale-days",
                    "7",
                    "--repo-root",
                    str(tmp),
                ]
            )
            self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()
