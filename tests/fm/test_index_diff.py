"""Tests for fm-index-diff — TASK.md §7.11 Tasks-Index Freshness gate."""
from __future__ import annotations

import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "tools" / "fm"))

import index_diff as fm_index_diff  # noqa: E402


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = fm_index_diff.main(argv)
    return rc, out.getvalue(), err.getvalue()


def _task_md(task_id: str, slug: str, *, task_status: str,
             superseded_by: list[str] | None = None) -> str:
    sup = "[]" if not superseded_by else ""
    body = (
        "---\n"
        f"type: task\n"
        "status: active\n"
        f"slug: {slug}\n"
        'summary: "t"\n'
        "created: 2026-05-05\n"
        "updated: 2026-05-05\n"
        f'task_id: "{task_id}"\n'
        f"task_status: {task_status}\n"
        'task_owner: "x"\n'
        "task_priority: P1\n"
        "task_uses_prompts: []\n"
        "task_spawns_research: []\n"
        "task_spawns_prompts: []\n"
    )
    if superseded_by:
        body += "task_superseded_by:\n"
        for s in superseded_by:
            body += f'  - "{s}"\n'
    else:
        body += f"task_superseded_by: {sup}\n"
    body += "task_affects_paths: []\n---\n\n## Goal\ng\n"
    return body


class _Sandbox:
    def __init__(self, base: Path) -> None:
        self.base = base
        (base / "AGENTS.md").write_text("# stub\n", encoding="utf-8")

    def write_task(self, folder: str, content: str) -> None:
        d = self.base / "tasks" / folder
        d.mkdir(parents=True, exist_ok=True)
        (d / "task.md").write_text(content, encoding="utf-8")

    def write_index(self, body: str) -> Path:
        idx = self.base / "tasks" / "readme.md"
        idx.parent.mkdir(parents=True, exist_ok=True)
        idx.write_text(body, encoding="utf-8")
        return idx

    def run(self, *argv: str) -> tuple[int, str]:
        cwd = os.getcwd()
        os.chdir(self.base)
        try:
            rc, out, err = _capture(list(argv))
        finally:
            os.chdir(cwd)
        return rc, out + err


_INDEX_HEAD = (
    "---\n"
    "type: index\n"
    "status: active\n"
    "slug: tasks-root\n"
    'summary: "tasks index"\n'
    "created: 2026-05-04\n"
    "updated: 2026-05-07\n"
    "---\n\n"
    "# Tasks Root\n\n"
    "## Contents\n\n"
)


class IndexDiffTests(unittest.TestCase):
    def test_in_sync_emits_zero_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sb = _Sandbox(Path(tmp))
            sb.write_task("100-alpha", _task_md("100", "alpha", task_status="open"))
            sb.write_task("101-beta", _task_md("101", "beta", task_status="done"))
            sb.write_index(
                _INDEX_HEAD
                + "- [`100-alpha/`](./100-alpha/) — A. Status: `open`.\n"
                + "- [`101-beta/`](./101-beta/) — B. Status: `done`.\n"
            )
            rc, out = sb.run()
            self.assertEqual(rc, 0, out)
            self.assertEqual(out.strip(), "")

    def test_single_status_drift_emits_one_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sb = _Sandbox(Path(tmp))
            sb.write_task("100-alpha", _task_md("100", "alpha", task_status="done"))
            sb.write_index(
                _INDEX_HEAD
                + "- [`100-alpha/`](./100-alpha/) — A. Status: `open`.\n"
            )
            rc, out = sb.run()
            self.assertEqual(rc, 1)
            self.assertIn("100-alpha bullet status=`open`", out)
            self.assertIn("task_status=`done`", out)
            self.assertEqual(out.count("ERROR:T.7.11"), 1)

    def test_orphan_bullet_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sb = _Sandbox(Path(tmp))
            sb.write_index(
                _INDEX_HEAD
                + "- [`100-ghost/`](./100-ghost/) — Phantom. Status: `open`.\n"
            )
            rc, out = sb.run()
            self.assertEqual(rc, 1)
            self.assertIn("100-ghost", out)
            self.assertIn("no `tasks/100-ghost/` folder on disk", out)

    def test_missing_bullet_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sb = _Sandbox(Path(tmp))
            sb.write_task("200-omega", _task_md("200", "omega", task_status="open"))
            sb.write_index(_INDEX_HEAD)
            rc, out = sb.run()
            self.assertEqual(rc, 1)
            self.assertIn("200-omega", out)
            self.assertIn("no bullet in index", out)

    def test_supersession_pointer_required_when_status_updated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sb = _Sandbox(Path(tmp))
            sb.write_task(
                "100-old",
                _task_md("100", "old", task_status="updated",
                        superseded_by=["200"]),
            )
            sb.write_task("200-new", _task_md("200", "new", task_status="open"))
            # Bullet has the right status but missing supersession pointer.
            sb.write_index(
                _INDEX_HEAD
                + "- [`100-old/`](./100-old/) — Old. Status: `updated`.\n"
                + "- [`200-new/`](./200-new/) — New. Status: `open`.\n"
            )
            rc, out = sb.run()
            self.assertEqual(rc, 1)
            self.assertIn("100-old", out)
            self.assertIn("missing", out)

    def test_supersession_pointer_must_match_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sb = _Sandbox(Path(tmp))
            sb.write_task(
                "100-old",
                _task_md("100", "old", task_status="updated",
                        superseded_by=["200"]),
            )
            sb.write_task("200-new", _task_md("200", "new", task_status="open"))
            sb.write_task("300-other", _task_md("300", "other", task_status="open"))
            # Pointer points to 300, but frontmatter says 200.
            sb.write_index(
                _INDEX_HEAD
                + "- [`100-old/`](./100-old/) — Old. Status: `updated` "
                "→ superseded by [300](./300-other/).\n"
                + "- [`200-new/`](./200-new/) — New. Status: `open`.\n"
                + "- [`300-other/`](./300-other/) — Other. Status: `open`.\n"
            )
            rc, out = sb.run()
            self.assertEqual(rc, 1)
            self.assertIn("100-old", out)
            self.assertIn("supersession pointer", out)

    def test_supersession_pointer_accepts_correct_match(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sb = _Sandbox(Path(tmp))
            sb.write_task(
                "100-old",
                _task_md("100", "old", task_status="updated",
                        superseded_by=["200"]),
            )
            sb.write_task("200-new", _task_md("200", "new", task_status="open"))
            sb.write_index(
                _INDEX_HEAD
                + "- [`100-old/`](./100-old/) — Old. Status: `updated` "
                "→ superseded by [200](./200-new/).\n"
                + "- [`200-new/`](./200-new/) — New. Status: `open`.\n"
            )
            rc, out = sb.run()
            self.assertEqual(rc, 0, out)

    def test_repo_self_check_clean(self) -> None:
        """The repo's actual tasks/readme.md MUST be drift-free after the fixes
        applied in this Task. Acts as a regression guard."""
        cwd = os.getcwd()
        os.chdir(REPO)
        try:
            rc, out, err = _capture([])
        finally:
            os.chdir(cwd)
        self.assertEqual(rc, 0, f"unexpected drift:\n{out}\n{err}")


if __name__ == "__main__":
    unittest.main()
