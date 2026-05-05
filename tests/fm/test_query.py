"""Tests for fm-query — SPEC §6 scenario F.6.6 + statelessness invariant."""
from __future__ import annotations

import io
import contextlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "tools" / "fm"))

import query as fm_query  # noqa: E402


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = fm_query.main(argv)
    return rc, out.getvalue(), err.getvalue()


class _Sandbox:
    def __init__(self, base: Path) -> None:
        self.base = base
        (base / "AGENTS.md").write_text("# stub\n", encoding="utf-8")
        op = base / "maintenance" / "schemas" / "header-ontology.json"
        op.parent.mkdir(parents=True, exist_ok=True)
        op.write_text(
            (REPO / "maintenance" / "schemas" / "header-ontology.json")
                .read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    def write(self, rel: str, text: str) -> Path:
        path = self.base / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def run(self, *argv: str) -> tuple[int, str]:
        cwd = os.getcwd()
        os.chdir(self.base)
        try:
            rc, out, err = _capture(list(argv))
        finally:
            os.chdir(cwd)
        return rc, out + err


def _good_task(slug: str, status: str = "active") -> str:
    return f"""---
type: task
status: {status}
slug: {slug}
summary: "t"
created: 2026-05-05
updated: 2026-05-05
task_id: "099"
task_status: open
task_owner: "x"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths: []
---

## Goal
g
## Plan
p
## Todo
- [ ] x
## Links
- foo
"""


class TestSelectors(unittest.TestCase):
    def test_type_selector(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("tasks/099-x/task.md", _good_task("x"))
            sb.write("tasks/100-y/task.md", _good_task("y"))
            rc, out = sb.run("type=task")
            self.assertEqual(rc, 0)
            self.assertIn("tasks/099-x/task.md", out)
            self.assertIn("tasks/100-y/task.md", out)

    def test_status_and_type(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("tasks/099-x/task.md", _good_task("x", "active"))
            sb.write("tasks/100-y/task.md", _good_task("y", "draft"))
            rc, out = sb.run("type=task,status=active")
            self.assertIn("099-x", out)
            self.assertNotIn("100-y", out)

    def test_missing_key(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task("x").replace("task_owner: \"x\"\n", "")
            sb.write("tasks/099-x/task.md", text)
            sb.write("tasks/100-y/task.md", _good_task("y"))
            rc, out = sb.run("missing-key=task_owner")
            self.assertIn("099-x", out)
            self.assertNotIn("100-y", out)


class TestStateless(unittest.TestCase):
    """SPEC §6 scenario F.6.6: stateless query under live mutation."""

    def test_F_6_6_no_cache_artefact(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task("x").replace("task_owner: \"x\"\n", "")
            sb.write("tasks/099-x/task.md", text)
            sb.run("missing-key=task_owner")
            # Re-write the file with key present.
            sb.write("tasks/099-x/task.md", _good_task("x"))
            rc, out = sb.run("missing-key=task_owner")
            self.assertEqual(rc, 0)
            self.assertNotIn("099-x", out)
            # No cache directory anywhere.
            self.assertFalse((sb.base / ".agent_cache").exists())

    def test_no_writes_in_repo_during_query(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("tasks/099-x/task.md", _good_task("x"))
            mtime_before = (sb.base / "tasks/099-x/task.md").stat().st_mtime_ns
            sb.run("type=task")
            mtime_after = (sb.base / "tasks/099-x/task.md").stat().st_mtime_ns
            self.assertEqual(mtime_before, mtime_after)


class TestOutputCap(unittest.TestCase):
    def test_default_output_cap_under_1kb(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            for i in range(40):
                sb.write(f"tasks/{i:03d}-task-with-very-long-slug-{i}/task.md",
                         _good_task(f"slug-{i}"))
            rc, out = sb.run("type=task")
            self.assertEqual(rc, 0)
            # Either the output is ≤ cap or it ends with the truncation marker.
            if len(out.encode("utf-8")) > 1024:
                self.assertIn("[truncated;", out)


if __name__ == "__main__":
    unittest.main()
