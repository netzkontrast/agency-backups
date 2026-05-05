"""Tests for fm-fix — closed-set T1/T2 repair + T3 stub generation.

Spec: /research/flexible-frontmatter-toolchain/output/SPEC.md (§5.1, §7.2, §12.4)
MAINTENANCE.md §1: Tier ladder.

Run: python3 -m unittest discover tests/fm
"""
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

import _core  # noqa: E402
import fix as fm_fix  # noqa: E402
import validate as fm_validate  # noqa: E402


# ---- Fixtures ---------------------------------------------------------------

class _Sandbox:
    """In-memory repo with the canonical ontology copied in.

    Mirrors tests/fm/test_validate.py's sandbox so fix and validate share
    the same path-classification rules.
    """

    def __init__(self, base: Path) -> None:
        self.base = base
        (base / "AGENTS.md").write_text("# stub root marker\n", encoding="utf-8")
        ontology_path = base / "maintenance" / "schemas" / "header-ontology.json"
        ontology_path.parent.mkdir(parents=True, exist_ok=True)
        ontology_path.write_text(
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
        """Run fix.main with cwd=base, capture stdout & stderr."""
        cwd = os.getcwd()
        os.chdir(self.base)
        buf_out = io.StringIO()
        buf_err = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
                rc = fm_fix.main(list(argv))
        finally:
            os.chdir(cwd)
        return rc, buf_out.getvalue(), buf_err.getvalue()


def _good_task(slug: str = "x") -> str:
    """A clean task.md the validator passes."""
    return f"""---
type: task
status: active
slug: {slug}
summary: "test"
created: 2026-05-05
updated: 2026-05-05
task_id: "099"
task_status: open
task_owner: "claude-code"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths: []
---

# Task

## Goal
g

## Plan
p

## Todo
- [ ] x

## Links
- foo
"""


# ---- Recipe-by-recipe coverage ---------------------------------------------

class TestF31MissingUpdated(unittest.TestCase):
    """F.3.1 missing 'updated' → T1 bump-updated."""

    def test_apply_writes_today(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task().replace("updated: 2026-05-05\n", "")
            p = sb.write("tasks/099-x/task.md", text)
            rc, out, _ = sb.run("--apply")
            self.assertEqual(rc, 0, msg=out)
            self.assertIn("T1=1", out)
            fm = _core.parse_frontmatter(p.read_text(encoding="utf-8"), strict=True)
            self.assertIn("updated", fm)

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task().replace("updated: 2026-05-05\n", "")
            p = sb.write("tasks/099-x/task.md", text)
            before = p.read_text(encoding="utf-8")
            rc, out, _ = sb.run()  # default = dry-run
            self.assertEqual(rc, 0)
            self.assertEqual(p.read_text(encoding="utf-8"), before)
            self.assertIn("DRYRUN", out)
            self.assertIn("T1", out)


class TestF31MissingCreated(unittest.TestCase):
    def test_apply_sets_today(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task().replace("created: 2026-05-05\n", "")
            p = sb.write("tasks/099-x/task.md", text)
            rc, out, _ = sb.run("--apply")
            self.assertEqual(rc, 0, msg=out)
            fm = _core.parse_frontmatter(p.read_text(encoding="utf-8"), strict=True)
            self.assertIn("created", fm)
            self.assertRegex(fm["created"], r"^\d{4}-\d{2}-\d{2}$")


class TestF31MissingType(unittest.TestCase):
    """F.3.1 missing 'type' → T2 set type=<expected> when path is unambiguous."""

    def test_path_unambiguous_sets_type(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task().replace("type: task\n", "")
            p = sb.write("tasks/099-x/task.md", text)
            rc, out, _ = sb.run("--apply")
            self.assertEqual(rc, 0, msg=out)
            self.assertIn("T2", out)
            fm = _core.parse_frontmatter(p.read_text(encoding="utf-8"), strict=True)
            self.assertEqual(fm["type"], "task")


class TestF31MissingSlug(unittest.TestCase):
    def test_slug_derived_from_folder(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task().replace("slug: x\n", "")
            p = sb.write("tasks/099-foo/task.md", text)
            rc, out, _ = sb.run("--apply")
            self.assertEqual(rc, 0, msg=out)
            fm = _core.parse_frontmatter(p.read_text(encoding="utf-8"), strict=True)
            self.assertEqual(fm["slug"], "foo")


class TestF32MissingL2List(unittest.TestCase):
    """F.3.2 missing list-typed L2 key (e.g. task_uses_prompts) → T2 empty list."""

    def test_inserts_empty_list(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task().replace("task_uses_prompts: []\n", "")
            p = sb.write("tasks/099-x/task.md", text)
            rc, out, _ = sb.run("--apply")
            self.assertEqual(rc, 0, msg=out)
            self.assertIn("T2", out)
            fm = _core.parse_frontmatter(p.read_text(encoding="utf-8"), strict=True)
            self.assertEqual(fm["task_uses_prompts"], [])


class TestF32MissingL2Scalar(unittest.TestCase):
    """F.3.2 missing scalar L2 key (e.g. prompt_kind) → T3 stub (deferred)."""

    def test_scalar_l2_defers_to_stub(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            prompt = """---
type: prompt
status: active
slug: y
summary: "p"
created: 2026-05-05
updated: 2026-05-05
prompt_framework: RISEN
prompt_target_agent: any
---

# P

## Framework
f

## R - Role
r

## I - Input
i

## S - Steps
s

## E - Expectations
e

## Constraints
c
"""
            p = sb.write("prompts/y/prompt.md", prompt)
            rc, out, _ = sb.run("--apply")
            # Apply mode + deferred → exit 1.
            self.assertEqual(rc, 1)
            self.assertIn("deferred to Tasks: 1", out)
            stubs = list((sb.base / "tasks").glob("*-fix-*"))
            self.assertEqual(len(stubs), 1, msg=out)


class TestF33TypeDisagreementAltPermitted(unittest.TestCase):
    """F.3.3: declared type wrong, but path's classification has alt_types →
    T2 set to expected primary."""

    def test_alt_permitted_path_repairs_in_place(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            # research/<slug>/output/SPEC.md has alt_types=["spec"], primary
            # = "research". A file declaring `type: task` here is F.3.3.
            text = """---
type: task
status: active
slug: r
summary: "x"
created: 2026-05-05
updated: 2026-05-05
research_phase: kickoff
research_executes_prompt: foo
research_friction_level: FL0
---

# R
"""
            p = sb.write("research/r/output/SPEC.md", text)
            rc, out, _ = sb.run("--apply")
            self.assertIn("T2", out)
            fm = _core.parse_frontmatter(p.read_text(encoding="utf-8"), strict=True)
            self.assertEqual(fm["type"], "research")


class TestF34DidYouMeanRefused(unittest.TestCase):
    """F.3.4 → REFUSED (warning), no auto-fix, no stub."""

    def test_typo_refused_not_repaired(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            # 'tpye' instead of 'type' → F.3.4 + F.3.1 (missing 'type'). Use
            # --code F.3.4 to isolate the refusal recipe.
            text = _good_task().replace("type: task", "tpye: task")
            p = sb.write("tasks/099-x/task.md", text)
            before = p.read_text(encoding="utf-8")
            rc, out, _ = sb.run("--apply", "--code", "F.3.4")
            self.assertIn("REFUSE", out)
            self.assertIn("refused: 1", out)
            # Apply mode + only refusal → exit 1.
            self.assertEqual(rc, 1)
            self.assertEqual(p.read_text(encoding="utf-8"), before)


class TestF42HeadingRefused(unittest.TestCase):
    """F.4.2 → REFUSED (body authoring required)."""

    def test_missing_heading_refused(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task().replace("## Todo\n- [ ] x\n\n", "")
            p = sb.write("tasks/099-x/task.md", text)
            before = p.read_text(encoding="utf-8")
            rc, out, _ = sb.run("--apply", "--code", "F.4.2")
            self.assertIn("REFUSE", out)
            self.assertIn("Todo", out)
            self.assertEqual(p.read_text(encoding="utf-8"), before)


# ---- T3 stub path -----------------------------------------------------------

class TestT3StubGeneration(unittest.TestCase):
    def test_stub_passes_fm_validate(self):
        """The generated stub must itself be a valid Task per fm-validate."""
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            # Trigger a defer: missing summary (no recipe).
            text = _good_task().replace('summary: "test"\n', "")
            sb.write("tasks/099-x/task.md", text)
            rc, out, _ = sb.run("--apply")
            self.assertIn("STUB", out)
            stubs = list((sb.base / "tasks").glob("*-fix-*/task.md"))
            self.assertEqual(len(stubs), 1)
            # Now run the validator on the stub.
            cwd = os.getcwd()
            os.chdir(sb.base)
            try:
                buf = io.StringIO()
                with contextlib.redirect_stderr(buf), contextlib.redirect_stdout(buf):
                    vrc = fm_validate.main([str(stubs[0])])
            finally:
                os.chdir(cwd)
            self.assertEqual(vrc, 0,
                             msg=f"stub failed fm-validate: {buf.getvalue()}")

    def test_stub_dry_run_does_not_create(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task().replace('summary: "test"\n', "")
            sb.write("tasks/099-x/task.md", text)
            rc, out, _ = sb.run()
            self.assertIn("DRY-STUB", out)
            stubs = list((sb.base / "tasks").glob("*-fix-*/task.md"))
            self.assertEqual(len(stubs), 0)


# ---- Dry-run / apply contrast ----------------------------------------------

class TestDryRunVsApply(unittest.TestCase):
    def test_dry_run_then_apply_match(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task().replace("updated: 2026-05-05\n", "")
            p = sb.write("tasks/099-x/task.md", text)
            before = p.read_text(encoding="utf-8")
            rc1, out1, _ = sb.run()
            self.assertEqual(rc1, 0)
            self.assertEqual(p.read_text(encoding="utf-8"), before)
            rc2, out2, _ = sb.run("--apply")
            self.assertEqual(rc2, 0)
            self.assertNotEqual(p.read_text(encoding="utf-8"), before)


# ---- Unknown-code refusal ---------------------------------------------------

class TestUnknownCodeRefusal(unittest.TestCase):
    def test_unknown_code_exits_4(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("tasks/099-x/task.md", _good_task())
            rc, _, err = sb.run("--apply", "--code", "F.99.9")
            self.assertEqual(rc, fm_fix.EXIT_UNKNOWN_CODE)
            self.assertIn("F.99.9", err)


# ---- Atomicity: a file with multiple repairs is one read-modify-write ------

class TestAtomicMultiRepair(unittest.TestCase):
    def test_two_l1_repairs_apply_together(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task() \
                .replace("updated: 2026-05-05\n", "") \
                .replace("created: 2026-05-05\n", "")
            p = sb.write("tasks/099-x/task.md", text)
            rc, out, _ = sb.run("--apply")
            self.assertEqual(rc, 0, msg=out)
            fm = _core.parse_frontmatter(p.read_text(encoding="utf-8"), strict=True)
            self.assertIn("updated", fm)
            self.assertIn("created", fm)
            self.assertIn("T1=2", out)


# ---- Final summary line is always emitted ----------------------------------

class TestSummaryLine(unittest.TestCase):
    def test_summary_present_clean_tree(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("tasks/099-x/task.md", _good_task())
            rc, out, _ = sb.run()
            self.assertEqual(rc, 0)
            self.assertIn("Fixed 0", out)
            self.assertIn("deferred to Tasks: 0", out)
            self.assertIn("refused: 0", out)


if __name__ == "__main__":
    unittest.main()
