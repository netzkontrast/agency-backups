"""Tests for fm-validate skill_bundles_tools enforcement (ADR-0007).

Covers diagnostics:
  - F.B.5  malformed entry (type, prefix, traversal, duplicate, non-existent)
  - F.B.6  transitive dependency missing per _core.BUNDLE_DEPS

Run: python3 -m unittest tools/tests/fm/test_validate_skill_bundles.py
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

import _core  # noqa: E402
import validate as fm_validate  # noqa: E402


class _Sandbox:
    """In-memory repo with the canonical ontology and stub tool directories."""

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
        # Provide stub tools directories so bundle paths resolve.
        for slug in ("fm", "adr", "dramatica-nav"):
            (base / "tools" / slug).mkdir(parents=True, exist_ok=True)
            (base / "tools" / slug / "__placeholder__").write_text("", encoding="utf-8")

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


def _skill_md(body_extra: str = "") -> str:
    return (
        "---\n"
        "name: example-skill\n"
        'description: "Trigger description that is long enough to be meaningful for testing purposes only."\n'
        f"{body_extra}"
        "---\n"
        "\n"
        "# Example\n"
        "\n"
        "Body.\n"
    )


class TestSkillBundlesValidation(unittest.TestCase):

    def _new_sandbox(self) -> tuple[_Sandbox, tempfile.TemporaryDirectory]:
        td = tempfile.TemporaryDirectory()
        return _Sandbox(Path(td.name)), td

    def test_absent_key_is_ok(self):
        sb, td = self._new_sandbox()
        try:
            sb.write("skills/example-skill/SKILL.md", _skill_md())
            rc, output = sb.run("skills/example-skill/SKILL.md")
            self.assertEqual(rc, 0, output)
            self.assertNotIn("F.B.5", output)
            self.assertNotIn("F.B.6", output)
        finally:
            td.cleanup()

    def test_valid_single_bundle(self):
        sb, td = self._new_sandbox()
        try:
            sb.write(
                "skills/example-skill/SKILL.md",
                _skill_md("skill_bundles_tools:\n  - tools/fm\n"),
            )
            rc, output = sb.run("skills/example-skill/SKILL.md")
            self.assertEqual(rc, 0, output)
            self.assertNotIn("F.B.5", output)
            self.assertNotIn("F.B.6", output)
        finally:
            td.cleanup()

    def test_valid_multi_bundle_with_transitive_satisfied(self):
        sb, td = self._new_sandbox()
        try:
            sb.write(
                "skills/example-skill/SKILL.md",
                _skill_md("skill_bundles_tools:\n  - tools/fm\n  - tools/adr\n"),
            )
            rc, output = sb.run("skills/example-skill/SKILL.md")
            self.assertEqual(rc, 0, output)
        finally:
            td.cleanup()

    def test_missing_directory_emits_F_B_5(self):
        sb, td = self._new_sandbox()
        try:
            sb.write(
                "skills/example-skill/SKILL.md",
                _skill_md("skill_bundles_tools:\n  - tools/nonexistent\n"),
            )
            rc, output = sb.run("skills/example-skill/SKILL.md")
            self.assertEqual(rc, 1, output)
            self.assertIn("F.B.5", output)
            self.assertIn("does not resolve", output)
        finally:
            td.cleanup()

    def test_missing_tools_prefix_emits_F_B_5(self):
        sb, td = self._new_sandbox()
        try:
            sb.write(
                "skills/example-skill/SKILL.md",
                _skill_md("skill_bundles_tools:\n  - fm\n"),
            )
            rc, output = sb.run("skills/example-skill/SKILL.md")
            self.assertEqual(rc, 1, output)
            self.assertIn("F.B.5", output)
            self.assertIn("MUST start with 'tools/'", output)
        finally:
            td.cleanup()

    def test_path_traversal_emits_F_B_5(self):
        sb, td = self._new_sandbox()
        try:
            sb.write(
                "skills/example-skill/SKILL.md",
                _skill_md("skill_bundles_tools:\n  - tools/../etc\n"),
            )
            rc, output = sb.run("skills/example-skill/SKILL.md")
            self.assertEqual(rc, 1, output)
            self.assertIn("F.B.5", output)
            self.assertIn("path traversal forbidden", output)
        finally:
            td.cleanup()

    def test_duplicate_entry_emits_F_B_5(self):
        sb, td = self._new_sandbox()
        try:
            sb.write(
                "skills/example-skill/SKILL.md",
                _skill_md("skill_bundles_tools:\n  - tools/fm\n  - tools/fm\n"),
            )
            rc, output = sb.run("skills/example-skill/SKILL.md")
            self.assertEqual(rc, 1, output)
            self.assertIn("F.B.5", output)
            self.assertIn("duplicated", output)
        finally:
            td.cleanup()

    def test_non_list_value_emits_F_B_5(self):
        sb, td = self._new_sandbox()
        try:
            sb.write(
                "skills/example-skill/SKILL.md",
                _skill_md("skill_bundles_tools: tools/fm\n"),
            )
            rc, output = sb.run("skills/example-skill/SKILL.md")
            self.assertEqual(rc, 1, output)
            self.assertIn("F.B.5", output)
            self.assertIn("YAML list", output)
        finally:
            td.cleanup()

    def test_transitive_dependency_missing_emits_F_B_6(self):
        sb, td = self._new_sandbox()
        try:
            sb.write(
                "skills/example-skill/SKILL.md",
                _skill_md("skill_bundles_tools:\n  - tools/adr\n"),
            )
            rc, output = sb.run("skills/example-skill/SKILL.md")
            self.assertEqual(rc, 1, output)
            self.assertIn("F.B.6", output)
            self.assertIn("transitive bundle", output)
        finally:
            td.cleanup()

    def test_bundle_deps_constant_shape(self):
        # ADR-0007 invariant: BUNDLE_DEPS values are tuples of repo-relative paths
        # all of which start with "tools/".
        self.assertIn("tools/adr", _core.BUNDLE_DEPS)
        for key, deps in _core.BUNDLE_DEPS.items():
            self.assertTrue(key.startswith("tools/"))
            self.assertIsInstance(deps, tuple)
            for d in deps:
                self.assertIsInstance(d, str)
                self.assertTrue(d.startswith("tools/"))


if __name__ == "__main__":
    unittest.main()
