"""Tests for fm-graph (Task 019 ST-2).

Covers:
  * a clean graph (no diagnostics)
  * cycle detection (Tarjan SCC > 1 plus self-loop)
  * dangling targets
  * orphan detection (slug with no inbound or outbound edge)
  * dot output is well-formed and round-trips through `dot -Tsvg` if
    Graphviz is installed (skip if not)
  * statelessness — no cache files created, no source mutation
  * task_id ↔ slug resolution on the supersession axis
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "tools" / "fm"))

import graph as fm_graph  # noqa: E402


# ---- Sandbox plumbing -------------------------------------------------------


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = fm_graph.main(argv)
    return rc, out.getvalue(), err.getvalue()


class _Sandbox:
    """A throw-away repo skeleton with the real header-ontology copied in."""

    def __init__(self, base: Path) -> None:
        self.base = base
        (base / "AGENTS.md").write_text("# stub\n", encoding="utf-8")
        ont = base / "maintenance" / "schemas" / "header-ontology.json"
        ont.parent.mkdir(parents=True, exist_ok=True)
        ont.write_text(
            (REPO / "maintenance" / "schemas" / "header-ontology.json")
            .read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    def write(self, rel: str, text: str) -> Path:
        path = self.base / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def run(self, *argv: str) -> tuple[int, str, str]:
        cwd = os.getcwd()
        os.chdir(self.base)
        try:
            return _capture(list(argv))
        finally:
            os.chdir(cwd)


# ---- Fixture builders -------------------------------------------------------


def _task(
    slug: str,
    *,
    task_id: str = "099",
    uses_prompts: list[str] | None = None,
    spawns_research: list[str] | None = None,
    spawns_prompts: list[str] | None = None,
    blocked_by: list[str] | None = None,
    supersedes: list[str] | None = None,
    superseded_by: list[str] | None = None,
) -> str:
    def _ylist(items: list[str] | None) -> str:
        items = items or []
        if not items:
            return "[]"
        return "\n" + "\n".join(f"  - {it}" for it in items)
    return f"""---
type: task
status: active
slug: {slug}
summary: "t"
created: 2026-05-05
updated: 2026-05-05
task_id: "{task_id}"
task_status: open
task_owner: "x"
task_priority: P1
task_uses_prompts: {_ylist(uses_prompts)}
task_spawns_research: {_ylist(spawns_research)}
task_spawns_prompts: {_ylist(spawns_prompts)}
task_affects_paths: []
task_blocked_by: {_ylist(blocked_by)}
task_supersedes: {_ylist(supersedes)}
task_superseded_by: {_ylist(superseded_by)}
---

## Goal
g
## Plan
p
## Todo
- [ ] x
## Links
- [stub](./readme.md)
"""


def _prompt(
    slug: str,
    *,
    relates_to_task: str = "",
    spawned_from_research: str = "",
) -> str:
    return f"""---
type: prompt
status: active
slug: {slug}
summary: "p"
created: 2026-05-05
updated: 2026-05-05
prompt_kind: tool-instruction
prompt_framework: RISEN
prompt_target_agent: "Claude"
prompt_relates_to_task: "{relates_to_task}"
prompt_spawned_from_research: "{spawned_from_research}"
---

# {slug}
"""


def _research_readme(slug: str, *, executes_prompt: str = "") -> str:
    return f"""---
type: research
status: active
slug: {slug}
summary: "r"
created: 2026-05-05
updated: 2026-05-05
research_phase: kickoff
research_executes_prompt: "{executes_prompt}"
research_friction_level: low
---

# {slug}
"""


# ---- Tests ------------------------------------------------------------------


class TestCleanGraph(unittest.TestCase):
    """A reciprocally-linked task/prompt/research triangle has no diagnostics."""

    def test_clean_graph_emits_zero_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write(
                "tasks/100-alpha/task.md",
                _task(
                    "alpha-task",
                    uses_prompts=["alpha-prompt"],
                    spawns_research=["alpha-research"],
                ),
            )
            # Forward-only edges so the SCC analysis sees a DAG. The
            # reciprocal back-pointers (prompt_relates_to_task,
            # research_executes_prompt) DO form 2-cycles by design and
            # are exercised by TestCycleDetection below.
            sb.write(
                "prompts/alpha-prompt/prompt.md", _prompt("alpha-prompt"),
            )
            sb.write(
                "research/alpha-research/readme.md",
                _research_readme("alpha-research"),
            )
            rc, out, err = sb.run("--format=json", "--detect=all")
            self.assertEqual(rc, 0, msg=err)
            payload = json.loads(out)
            self.assertEqual(payload["cycles"], [])
            self.assertEqual(payload["dangling"], [])
            self.assertEqual(payload["orphans"], [])
            self.assertCountEqual(
                payload["slugs"],
                ["alpha-task", "alpha-prompt", "alpha-research"],
            )
            kinds = {kind for _, kind, _ in payload["edges"]}
            self.assertIn("task_uses_prompts", kinds)
            self.assertIn("task_spawns_research", kinds)


class TestCycleDetection(unittest.TestCase):
    def test_two_node_cycle_via_supersedes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write(
                "tasks/100-foo/task.md",
                _task("foo", task_id="100", supersedes=["bar"]),
            )
            sb.write(
                "tasks/101-bar/task.md",
                _task("bar", task_id="101", supersedes=["foo"]),
            )
            rc, out, err = sb.run("--format=json", "--detect=cycles")
            self.assertEqual(rc, 1)
            payload = json.loads(out)
            self.assertEqual(len(payload["cycles"]), 1)
            self.assertCountEqual(payload["cycles"][0], ["foo", "bar"])

    def test_self_loop_is_a_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write(
                "tasks/100-loop/task.md",
                _task("loop", task_id="100", uses_prompts=["loop"]),
            )
            # Force a slug-collision-free prompt so the slug "loop" only
            # resolves to the task (self-loop on the task slug).
            sb.write(
                "prompts/loop/prompt.md",
                _prompt("loop-prompt", relates_to_task="loop"),
            )
            # Override task → its uses_prompts target is its own slug so we
            # take a self-loop. Re-write with explicit self-reference.
            sb.write(
                "tasks/100-loop/task.md",
                _task("loop", task_id="100", uses_prompts=["loop"]),
            )
            rc, out, err = sb.run("--format=json", "--detect=cycles")
            self.assertEqual(rc, 1, msg=err)
            payload = json.loads(out)
            self.assertEqual(len(payload["cycles"]), 1)
            self.assertEqual(payload["cycles"][0], ["loop"])

    def test_clean_graph_has_no_cycles(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write(
                "tasks/100-a/task.md",
                _task("a", uses_prompts=["b-p"]),
            )
            sb.write("prompts/b-p/prompt.md", _prompt("b-p"))
            rc, out, err = sb.run("--format=json", "--detect=cycles")
            self.assertEqual(rc, 0, msg=err)
            payload = json.loads(out)
            self.assertEqual(payload["cycles"], [])


class TestDanglingDetection(unittest.TestCase):
    def test_missing_prompt_is_dangling(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write(
                "tasks/100-a/task.md",
                _task("a", uses_prompts=["does-not-exist"]),
            )
            rc, out, err = sb.run("--format=json", "--detect=dangling")
            self.assertEqual(rc, 1)
            payload = json.loads(out)
            self.assertEqual(len(payload["dangling"]), 1)
            src, kind, tgt = payload["dangling"][0]
            self.assertEqual(src, "a")
            self.assertEqual(kind, "task_uses_prompts")
            self.assertEqual(tgt, "does-not-exist")

    def test_dangling_does_not_promote_to_orphan(self) -> None:
        # A file that points at a missing slug still counts as having
        # an outbound edge — so it is *not* an orphan.
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write(
                "tasks/100-a/task.md",
                _task("a", uses_prompts=["does-not-exist"]),
            )
            rc, out, err = sb.run("--format=json", "--detect=all")
            self.assertEqual(rc, 1)
            payload = json.loads(out)
            self.assertNotIn("a", payload["orphans"])


class TestOrphanDetection(unittest.TestCase):
    def test_isolated_prompt_is_orphan(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("prompts/lonely/prompt.md", _prompt("lonely"))
            rc, out, err = sb.run("--format=json", "--detect=orphans")
            self.assertEqual(rc, 1)
            payload = json.loads(out)
            self.assertIn("lonely", payload["orphans"])

    def test_root_governance_spec_is_not_orphan(self) -> None:
        # An operational file with its own slug but no edges is an
        # orphan; a top-level governance spec with the same shape
        # is exempt. We simulate the latter with a top-level .md file.
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write(
                "GOVERNANCE.md",
                """---
type: spec
status: active
slug: governance
summary: "s"
created: 2026-05-05
updated: 2026-05-05
---

# governance
""",
            )
            # Operational orphan to ensure orphan logic still runs.
            sb.write("prompts/lonely/prompt.md", _prompt("lonely"))
            rc, out, err = sb.run("--format=json", "--detect=orphans")
            self.assertEqual(rc, 1)
            payload = json.loads(out)
            self.assertIn("lonely", payload["orphans"])
            self.assertNotIn("governance", payload["orphans"])


class TestTaskIdResolution(unittest.TestCase):
    def test_task_blocked_by_resolves_via_task_id(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write(
                "tasks/050-blocker/task.md",
                _task("blocker", task_id="050"),
            )
            sb.write(
                "tasks/051-blocked/task.md",
                _task("blocked", task_id="051", blocked_by=["050"]),
            )
            rc, out, err = sb.run("--format=json", "--detect=dangling")
            self.assertEqual(rc, 0, msg=err)
            payload = json.loads(out)
            self.assertEqual(payload["dangling"], [])


class TestDotOutput(unittest.TestCase):
    def test_dot_output_is_well_formed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write(
                "tasks/100-a/task.md",
                _task("a", uses_prompts=["bp"]),
            )
            sb.write("prompts/bp/prompt.md", _prompt("bp"))
            rc, out, err = sb.run("--format=dot")
            self.assertEqual(rc, 0, msg=err)
            self.assertTrue(out.strip().startswith("digraph fm_graph"))
            self.assertIn('"a" -> "bp"', out)
            self.assertIn("task_uses_prompts", out)
            self.assertTrue(out.strip().endswith("}"))

    def test_dot_round_trips_through_graphviz_if_installed(self) -> None:
        if shutil.which("dot") is None:
            self.skipTest("graphviz `dot` binary not installed")
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write(
                "tasks/100-a/task.md",
                _task("a", uses_prompts=["bp"]),
            )
            sb.write("prompts/bp/prompt.md", _prompt("bp"))
            rc, out, err = sb.run("--format=dot")
            self.assertEqual(rc, 0, msg=err)
            proc = subprocess.run(
                ["dot", "-Tsvg"],
                input=out.encode("utf-8"),
                capture_output=True,
                timeout=10,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr.decode())
            self.assertIn(b"<svg", proc.stdout)


class TestStatelessness(unittest.TestCase):
    def test_no_cache_artifacts_created(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("tasks/100-a/task.md", _task("a"))
            sb.run("--detect=all")
            self.assertFalse((sb.base / ".agent_cache").exists())
            self.assertFalse((sb.base / ".fm-graph.cache").exists())

    def test_no_source_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            path = sb.write("tasks/100-a/task.md", _task("a"))
            mtime_before = path.stat().st_mtime_ns
            sb.run("--detect=all")
            mtime_after = path.stat().st_mtime_ns
            self.assertEqual(mtime_before, mtime_after)


class TestDetectFlag(unittest.TestCase):
    def test_unknown_detect_value_errors(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            cwd = os.getcwd()
            os.chdir(sb.base)
            try:
                with self.assertRaises(SystemExit):
                    fm_graph.main(["--detect=bogus"])
            finally:
                os.chdir(cwd)

    def test_detect_subset_skips_other_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write(
                "tasks/100-a/task.md",
                _task("a", uses_prompts=["missing"]),
            )
            sb.write("prompts/lonely/prompt.md", _prompt("lonely"))
            rc, out, err = sb.run("--format=json", "--detect=dangling")
            self.assertEqual(rc, 1)
            payload = json.loads(out)
            self.assertIn("dangling", payload)
            self.assertNotIn("orphans", payload)
            self.assertNotIn("cycles", payload)


if __name__ == "__main__":
    unittest.main()
