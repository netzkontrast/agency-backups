"""Tests for fm-validate skill_source enforcement (ADR-0011, Task 091 ST-1).

Covers diagnostics:
  - F.B.8  skill_source set on a bare-slug (Agency-native) skill folder
  - F.B.9  skill_source value does not match '<vendor>@v<semver>'

Note: The §10.2 design draft listed F.B.7 / F.B.8 for these checks, but
F.B.7 is already in use by the existing task_list completion WARN check in
`_check_body_for_type`. ST-1 renumbers the new codes to F.B.8 / F.B.9 to
avoid the clash. See `tasks/091-port-external-skill-corpora/friction-log.md`.

Run: python3 -m unittest tools/tests/fm/test_validate_skill_source.py
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


class TestSkillSourceValidation(unittest.TestCase):

    def _new_sandbox(self) -> tuple[_Sandbox, tempfile.TemporaryDirectory]:
        td = tempfile.TemporaryDirectory()
        return _Sandbox(Path(td.name)), td

    def test_skill_source_accepted_on_vendor_prefix(self):
        """ADR-0011 D.2: imported skill with vendor prefix + valid value → 0 diagnostics."""
        sb, td = self._new_sandbox()
        try:
            sb.write(
                "skills/sc-example/SKILL.md",
                _skill_md('skill_source: "superclaude@v4.3.0"\n'),
            )
            rc, output = sb.run("skills/sc-example/SKILL.md")
            self.assertEqual(rc, 0, output)
            self.assertNotIn("F.B.8", output)
            self.assertNotIn("F.B.9", output)
        finally:
            td.cleanup()

    def test_skill_source_rejected_on_bare_slug(self):
        """ADR-0011 D.1: bare-slug (Agency-native) folder + skill_source → F.B.8 ERROR."""
        sb, td = self._new_sandbox()
        try:
            sb.write(
                "skills/example-native/SKILL.md",
                _skill_md('skill_source: "superclaude@v4.3.0"\n'),
            )
            rc, output = sb.run("skills/example-native/SKILL.md")
            self.assertEqual(rc, 1, output)
            self.assertIn("F.B.8", output)
            self.assertIn("vendor-prefixed", output)
        finally:
            td.cleanup()

    def test_skill_source_malformed_value(self):
        """ADR-0011 D.2: vendor-prefixed folder + malformed value → F.B.9 ERROR."""
        sb, td = self._new_sandbox()
        try:
            sb.write(
                "skills/sc-example/SKILL.md",
                _skill_md('skill_source: "superclaude@latest"\n'),
            )
            rc, output = sb.run("skills/sc-example/SKILL.md")
            self.assertEqual(rc, 1, output)
            self.assertIn("F.B.9", output)
            self.assertIn("<vendor>@v<semver>", output)
        finally:
            td.cleanup()

    def test_skill_source_absent_is_fine_for_natives(self):
        """ADR-0011 D.2: bare-slug folder with no skill_source key → 0 diagnostics."""
        sb, td = self._new_sandbox()
        try:
            sb.write("skills/example-native/SKILL.md", _skill_md())
            rc, output = sb.run("skills/example-native/SKILL.md")
            self.assertEqual(rc, 0, output)
            self.assertNotIn("F.B.8", output)
            self.assertNotIn("F.B.9", output)
        finally:
            td.cleanup()

    def test_existing_native_skills_still_validate(self):
        """Regression: every pre-existing skills/<slug>/SKILL.md MUST validate clean."""
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
        # No new F.B.8 / F.B.9 diagnostics raised by the extension.
        self.assertNotIn("F.B.8", output, output)
        self.assertNotIn("F.B.9", output, output)
        self.assertEqual(rc, 0, output)

    def test_superpowers_vendor_prefix_accepted(self):
        """ADR-0011 D.1: superpowers- prefix also accepted (forward compat for Phase 2)."""
        sb, td = self._new_sandbox()
        try:
            sb.write(
                "skills/superpowers-example/SKILL.md",
                _skill_md('skill_source: "superpowers@v4.0.3"\n'),
            )
            rc, output = sb.run("skills/superpowers-example/SKILL.md")
            self.assertEqual(rc, 0, output)
            self.assertNotIn("F.B.8", output)
            self.assertNotIn("F.B.9", output)
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
