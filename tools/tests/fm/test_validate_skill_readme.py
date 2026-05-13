"""Tests for fm-validate skill-subfolder readme.md audit (Task 093).

Covers diagnostic:
  - F.S.1  a skills/<slug>/ operational folder containing SKILL.md is missing
           the required sibling readme.md (SKILLS.md §2 + §9.6; CLAUDE.md §7).

Gherkin anchors from tasks/093-skill-subfolder-readme-audit-linter/task.md:
  - T093.1.1  Missing readme.md in a skill folder emits exactly one F.S.1.
  - T093.1.2  Skill folders with readme.md validate clean.
  - T093.1.3  Diagnostic explanation is registered in diagnostic-explanations.json.

Run: python3 -m unittest tools/tests/fm/test_validate_skill_readme.py
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "tools" / "fm"))

import validate as fm_validate  # noqa: E402


def _skill_md(extra_fm: str = "") -> str:
    return (
        "---\n"
        "name: example-skill\n"
        'description: "Trigger description that is long enough to be meaningful for testing purposes only."\n'
        f"{extra_fm}"
        "---\n"
        "\n"
        "# Example\n"
        "\n"
        "Body.\n"
    )


def _readme_md(slug: str) -> str:
    return (
        "---\n"
        "type: index\n"
        "status: active\n"
        f"slug: {slug}\n"
        f'summary: "Directory index for the {slug} skill."\n'
        "created: 2026-05-13\n"
        "updated: 2026-05-13\n"
        "---\n"
        "\n"
        f"# {slug}\n"
        "\n"
        "## Assumptions Log\n"
        "\n"
        "(none)\n"
    )


class _Sandbox:
    """In-memory repo with the canonical ontology."""

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
        cwd = os.getcwd()
        os.chdir(self.base)
        buf_err = io.StringIO()
        buf_out = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
                rc = fm_validate.main(list(argv))
        finally:
            os.chdir(cwd)
        return rc, buf_err.getvalue() + buf_out.getvalue()


class TestSkillReadmeAudit(unittest.TestCase):

    def _new_sandbox(self) -> tuple[_Sandbox, tempfile.TemporaryDirectory]:
        td = tempfile.TemporaryDirectory()
        return _Sandbox(Path(td.name)), td

    # anchor: T093.1.1
    def test_missing_readme_emits_exactly_one_F_S_1(self):
        """Skill folder with SKILL.md but no readme.md → exactly one F.S.1 ERROR, exit 1."""
        sb, td = self._new_sandbox()
        try:
            sb.write("skills/example-skill/SKILL.md", _skill_md())
            rc, output = sb.run("skills/example-skill/")
            self.assertEqual(rc, 1, output)
            self.assertEqual(output.count("F.S.1"), 1, output)
            self.assertIn("missing required readme.md", output)
            self.assertIn("skills/example-skill/", output)
        finally:
            td.cleanup()

    # anchor: T093.1.2 (synthetic sibling case)
    def test_present_readme_emits_no_F_S_1(self):
        """Skill folder with both SKILL.md and readme.md → 0 diagnostics, exit 0."""
        sb, td = self._new_sandbox()
        try:
            sb.write("skills/example-skill/SKILL.md", _skill_md())
            sb.write("skills/example-skill/readme.md", _readme_md("example-skill"))
            rc, output = sb.run("skills/example-skill/")
            self.assertEqual(rc, 0, output)
            self.assertNotIn("F.S.1", output)
        finally:
            td.cleanup()

    # anchor: T093.1.2 (live-corpus regression)
    def test_live_skills_corpus_validates_clean(self):
        """Every skills/<slug>/ folder on the current worktree MUST pass F.S.1."""
        cwd = os.getcwd()
        os.chdir(REPO)
        buf_err = io.StringIO()
        buf_out = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
                rc = fm_validate.main(["skills/"])
        finally:
            os.chdir(cwd)
        output = buf_err.getvalue() + buf_out.getvalue()
        self.assertEqual(rc, 0, output)
        self.assertNotIn("F.S.1", output)

    # anchor: T093.1.3
    def test_diagnostic_explanation_registered(self):
        """maintenance/schemas/diagnostic-explanations.json MUST register F.S.1
        with non-empty what / why / fix fields."""
        path = REPO / "maintenance" / "schemas" / "diagnostic-explanations.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        codes = data.get("codes", {})
        self.assertIn("F.S.1", codes, "F.S.1 missing from diagnostic-explanations.json")
        entry = codes["F.S.1"]
        for field in ("what", "why", "fix"):
            self.assertIn(field, entry, f"F.S.1 entry missing {field!r}")
            self.assertTrue(
                isinstance(entry[field], str) and entry[field].strip(),
                f"F.S.1 entry field {field!r} MUST be a non-empty string",
            )

    def test_emit_fires_only_for_SKILL_md_classification(self):
        """A non-SKILL.md file in skills/<slug>/ does not by itself trigger F.S.1."""
        sb, td = self._new_sandbox()
        try:
            sb.write("skills/example-skill/SKILL.md", _skill_md())
            sb.write("skills/example-skill/readme.md", _readme_md("example-skill"))
            sb.write("skills/example-skill/notes.md", _readme_md("example-skill"))
            rc, output = sb.run("skills/example-skill/")
            self.assertEqual(rc, 0, output)
            self.assertNotIn("F.S.1", output)
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
