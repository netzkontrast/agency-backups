"""Tests for fm-validate covering SPEC §6 Gherkin scenarios + M01 attacks.

Spec: /research/flexible-frontmatter-toolchain/output/SPEC.md
Falsifications: /research/flexible-frontmatter-toolchain/reflection/M01-falsification.md

Run: python3 -m unittest discover tools/tests/fm
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "tools" / "fm"))

import _core  # noqa: E402
import validate as fm_validate  # noqa: E402


class _Sandbox:
    """A minimal in-memory repo with the ontology and a tasks/prompts/research tree."""

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

    def run(self, *argv: str) -> tuple[int, str]:
        """Run validate.main with cwd=base, capture stderr+stdout."""
        cwd = os.getcwd()
        os.chdir(self.base)
        import io, contextlib
        buf_err = io.StringIO()
        buf_out = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
                rc = fm_validate.main(list(argv))
        finally:
            os.chdir(cwd)
        return rc, buf_err.getvalue() + buf_out.getvalue()


def _good_task(slug: str = "x") -> str:
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


def _good_prompt() -> str:
    return """---
type: prompt
status: active
slug: y
summary: "p"
created: 2026-05-05
updated: 2026-05-05
prompt_kind: tool-instruction
prompt_framework: RISEN
prompt_target_agent: any
---

# P

## Framework
f

## R — Role
r

## I — Input
i

## S — Steps
s

## E — Expectations
e

## Constraints
c
"""


class TestRequiredKeyValidation(unittest.TestCase):
    """SPEC §6 scenario F.6.1: required-only key validation."""

    def test_F_6_1_task_missing_summary(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task("x").replace('summary: "test"\n', "")
            sb.write("tasks/099-x/task.md", text)
            rc, out = sb.run()
            self.assertEqual(rc, 1)
            self.assertIn("F.3.1", out)
            self.assertIn("summary", out)

    def test_F_6_1_prompt_missing_slug(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_prompt().replace("slug: y\n", "")
            sb.write("prompts/y/prompt.md", text)
            rc, out = sb.run()
            self.assertEqual(rc, 1)
            self.assertIn("F.3.1", out)
            self.assertIn("slug", out)

    def test_F_6_1_research_missing_type(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = """---
status: active
slug: z
summary: "r"
created: 2026-05-05
updated: 2026-05-05
research_phase: kickoff
research_executes_prompt: foo
research_friction_level: FL0
---

# R
"""
            sb.write("research/z/output/SPEC.md", text)
            rc, out = sb.run()
            self.assertEqual(rc, 1)
            self.assertIn("F.3.1", out)
            self.assertIn("type", out)

    def test_F_6_1_skill_missing_name(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = """---
description: a skill
---

# Skill
"""
            sb.write("skills/abc/SKILL.md", text)
            rc, out = sb.run()
            self.assertEqual(rc, 1)
            self.assertTrue("F.3.1" in out or "F.3.2" in out)
            self.assertIn("name", out)


class TestExtrasPass(unittest.TestCase):
    """SPEC §6 scenario F.6.2: extras MUST NOT fail validation."""

    def test_F_6_2_many_extra_headings_and_l0_keys_pass(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            base = _good_task()
            base = base.replace(
                "task_id: \"099\"\n",
                "task_id: \"099\"\ntags:\n  - foo\n  - bar\naliases:\n  - old-slug\n",
            )
            base += "\n## Extra1\n\n## Extra2\n\n## Extra3\n" * 6
            sb.write("tasks/099-x/task.md", base)
            rc, out = sb.run()
            self.assertEqual(rc, 0, msg=out)
            self.assertNotIn("F.4.2", out)


class TestRequiredHeadingMissing(unittest.TestCase):
    """SPEC §6 scenario F.6.3."""

    def test_F_6_3_missing_todo(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task().replace(
                "## Todo\n- [ ] x\n\n", ""
            )
            sb.write("tasks/099-x/task.md", text)
            rc, out = sb.run()
            self.assertEqual(rc, 1)
            self.assertIn("F.4.2", out)
            self.assertIn("Todo", out)

    def test_heading_with_em_dash_and_colon_normalises(self):
        """Ensure `## Goal:` and `## Goal —` both match `## Goal`."""
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task().replace("## Goal\ng\n", "## Goal:\ng\n")
            sb.write("tasks/099-x/task.md", text)
            rc, out = sb.run()
            self.assertEqual(rc, 0, msg=out)


class TestDidYouMean(unittest.TestCase):
    """SPEC §6 scenario F.6.7 + M01-P1 attack."""

    def test_F_6_7_typo_caught(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_prompt().replace("type: prompt", "tpye: prompt")
            sb.write("prompts/y/prompt.md", text)
            rc, out = sb.run()
            self.assertEqual(rc, 1)
            self.assertIn("F.3.4", out)
            self.assertIn("did you mean 'type'", out)


class TestStatusAndSlug(unittest.TestCase):
    """SPEC §3.3 enum + slug pattern."""

    def test_unknown_status_fails(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task().replace("status: active", "status: weird")
            sb.write("tasks/099-x/task.md", text)
            rc, out = sb.run()
            self.assertEqual(rc, 1)
            self.assertIn("F.3.3", out)

    def test_slug_with_space_fails(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            text = _good_task().replace("slug: x", "slug: bad slug")
            sb.write("tasks/099-x/task.md", text)
            rc, out = sb.run()
            self.assertEqual(rc, 1)


class TestJSONFormat(unittest.TestCase):
    def test_json_format_emits_machine_readable(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("tasks/099-x/task.md", _good_task())
            rc, out = sb.run("--format=json")
            self.assertEqual(rc, 0)
            text = out.strip()
            self.assertIn("\"checked\"", text)
            self.assertIn("\"diagnostics\"", text)
            payload = json.loads(text[text.index("{"): text.rindex("}") + 1])
            self.assertEqual(payload["errors"], 0)


class TestStrictPromotesWarn(unittest.TestCase):
    def test_strict_flag_promotes_warns(self):
        # Today validate emits no WARN (per CONSTRAINTS); just ensure the
        # flag is accepted and clean files still pass under --strict.
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("tasks/099-x/task.md", _good_task())
            rc, _ = sb.run("--strict")
            self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
