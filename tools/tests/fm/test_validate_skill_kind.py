"""Tests for fm-validate skill_kind enforcement (Task 094 ST-1).

Covers diagnostic F.B.11 (skill_kind closed-enum check) — the 9-value
enum ratified by SKILLS.md §3.3 absorbing the Task 092 PR #120 review A1
carry-forward T3.

Valid values: domain, tool, orchestrator, meta, discipline, workflow,
              persona, analysis, agent-template.

Run: python3 -m pytest tools/tests/fm/test_validate_skill_kind.py
"""
from __future__ import annotations

import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "tools" / "fm"))

import validate as fm_validate  # noqa: E402


VALID_KINDS = (
    "domain", "tool", "orchestrator", "meta",
    "discipline", "workflow", "persona", "analysis", "agent-template",
)
INVALID_KINDS = ("bogus", "Discipline", "agent_template")  # case + underscore vs hyphen


def _skill_md(skill_kind: str | None = None, extra_fm: str = "") -> str:
    kind_line = f"skill_kind: {skill_kind}\n" if skill_kind is not None else ""
    return (
        "---\n"
        "name: example-skill\n"
        'description: "Trigger description that is long enough to be meaningful for testing purposes only."\n'
        f"{kind_line}"
        f"{extra_fm}"
        "---\n"
        "\n"
        "# Example\n"
        "\n"
        "Body.\n"
    )


class _Sandbox:
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
        if path.name == "SKILL.md":
            sibling = path.parent / "readme.md"
            if not sibling.exists():
                sibling.write_text("# stub\n", encoding="utf-8")
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


class TestSkillKindValidation(unittest.TestCase):

    def _new_sandbox(self) -> tuple[_Sandbox, tempfile.TemporaryDirectory]:
        td = tempfile.TemporaryDirectory()
        return _Sandbox(Path(td.name)), td

    def test_each_valid_kind_passes(self):
        """All 9 enum values MUST validate without F.B.11."""
        for kind in VALID_KINDS:
            with self.subTest(skill_kind=kind):
                sb, td = self._new_sandbox()
                try:
                    sb.write(
                        f"skills/example-{kind}/SKILL.md",
                        _skill_md(skill_kind=kind),
                    )
                    rc, output = sb.run(f"skills/example-{kind}/SKILL.md")
                    self.assertEqual(rc, 0, output)
                    self.assertNotIn("F.B.11", output)
                finally:
                    td.cleanup()

    def test_invalid_kind_emits_fb11(self):
        """Every out-of-enum value MUST emit F.B.11 ERROR and fail the gate."""
        for kind in INVALID_KINDS:
            with self.subTest(skill_kind=kind):
                sb, td = self._new_sandbox()
                try:
                    sb.write(
                        "skills/example-bad/SKILL.md",
                        _skill_md(skill_kind=kind),
                    )
                    rc, output = sb.run("skills/example-bad/SKILL.md")
                    self.assertEqual(rc, 1, output)
                    self.assertIn("F.B.11", output)
                    self.assertIn("9-value enum", output)
                finally:
                    td.cleanup()

    def test_absent_skill_kind_is_fine(self):
        """Absence of skill_kind MUST NOT emit F.B.11 (key is optional)."""
        sb, td = self._new_sandbox()
        try:
            sb.write("skills/example-noop/SKILL.md", _skill_md())
            rc, output = sb.run("skills/example-noop/SKILL.md")
            self.assertEqual(rc, 0, output)
            self.assertNotIn("F.B.11", output)
        finally:
            td.cleanup()

    def test_null_skill_kind_emits_fb11(self):
        """`skill_kind:` (parsed as YAML null / empty) MUST emit F.B.11 —
        present-but-empty is a malformed declaration, distinct from absent
        (which is permitted). Covers the PR #123 review A5 advisory gap."""
        sb, td = self._new_sandbox()
        try:
            # `skill_kind:` (bare key, no value) — the parser surfaces this
            # as a non-string sentinel; the enum check MUST still flag it.
            sb.write(
                "skills/example-null/SKILL.md",
                _skill_md(extra_fm="skill_kind:\n"),
            )
            rc, output = sb.run("skills/example-null/SKILL.md")
            self.assertEqual(rc, 1, output)
            self.assertIn("F.B.11", output)
            self.assertIn("9-value enum", output)
        finally:
            td.cleanup()

    def test_explicit_yaml_null_emits_fb11(self):
        """Explicit `skill_kind: null` MUST also emit F.B.11."""
        sb, td = self._new_sandbox()
        try:
            sb.write(
                "skills/example-explicit-null/SKILL.md",
                _skill_md(extra_fm="skill_kind: null\n"),
            )
            rc, output = sb.run("skills/example-explicit-null/SKILL.md")
            self.assertEqual(rc, 1, output)
            self.assertIn("F.B.11", output)
        finally:
            td.cleanup()

    def test_existing_skills_validate_clean(self):
        """Regression: every pre-existing skills/<slug>/SKILL.md MUST validate clean
        against the new F.B.11 enum check."""
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
        self.assertNotIn("F.B.11", output, output)
        self.assertEqual(rc, 0, output)


if __name__ == "__main__":
    unittest.main()
