"""Tests for tools/check-fl-declaration.py — Task 038 ST-2.

Coverage per acceptance criterion in
prompts/tooling-fl-declaration-linter/prompt.md §E:

  * clean FL0  — canonical line; exit 0.
  * clean FL2  — canonical line; exit 0.
  * missing log — folder without friction-log.md; exit 1.
  * malformed value — FL token in frontmatter only; exit 1.
  * both surfaces present (no warn) — friction-log.md takes precedence.
  * variant-form coverage — every form enumerated in
    research/fl0-value-justification/output/SPEC.md §2.2 must pass.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOLS = REPO / "tools"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "check_fl_declaration",
        TOOLS / "check-fl-declaration.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_fl_declaration"] = module
    spec.loader.exec_module(module)
    return module


cfd = _load_module()


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = cfd.main(argv)
    return rc, out.getvalue(), err.getvalue()


def _write(path: Path, body: str) -> None:
    path.write_text(body, encoding="utf-8")


class CleanFLDeclarations(unittest.TestCase):
    def test_clean_fl0_canonical(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            log = Path(td) / "friction-log.md"
            _write(log, "# Friction Log\n\nHighest Frustration Level: FL0\n")
            rc, _, err = _capture([str(log)])
            self.assertEqual(rc, 0, err)
            self.assertEqual(err, "")

    def test_clean_fl2_canonical(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            log = Path(td) / "friction-log.md"
            _write(
                log,
                "# Friction Log\n\n**Highest Frustration Level: FL2**\n\n"
                "FL2 because of conflicting prompts.\n",
            )
            rc, _, _ = _capture([str(log)])
            self.assertEqual(rc, 0)

    def test_clean_fl3_canonical(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            log = Path(td) / "friction-log.md"
            _write(log, "Highest Frustration Level: FL3\n")
            rc, _, _ = _capture([str(log)])
            self.assertEqual(rc, 0)


class VariantFormCoverage(unittest.TestCase):
    """Every form enumerated in SPEC §2.2 MUST pass."""

    def _assert_passes(self, body: str) -> None:
        with tempfile.TemporaryDirectory() as td:
            log = Path(td) / "friction-log.md"
            _write(log, body)
            rc, _, err = _capture([str(log)])
            self.assertEqual(rc, 0, f"{body!r} should pass, got: {err}")

    def test_variant_2_bold_canonical(self) -> None:
        self._assert_passes("**Highest Frustration Level: FL0**\n")

    def test_variant_3_phrasing(self) -> None:
        self._assert_passes("**Highest friction level experienced: FL0**\n")

    def test_variant_4_abbreviated(self) -> None:
        self._assert_passes("**Highest FL experienced: FL0**\n")

    def test_variant_5_bold_bare_prose(self) -> None:
        self._assert_passes("**FL0** — plan obsolesced cleanly.\n")

    def test_variant_6_list_form(self) -> None:
        self._assert_passes(
            "- **Friction Level:** FL0 (No unexpected blockers)\n"
        )

    def test_variant_7_bold_bare(self) -> None:
        self._assert_passes("**FL0**\n\nProse follows.\n")

    def test_variant_8_bare_em_dash(self) -> None:
        self._assert_passes("FL0 - Execution went flawlessly.\n")

    def test_variant_9_bare_own_line(self) -> None:
        self._assert_passes("# Friction Log\n\nFL0\n")

    def test_variant_11_friction_word(self) -> None:
        self._assert_passes("Highest Friction Level: FL1\n")

    def test_variant_12_heading(self) -> None:
        self._assert_passes("## Frustration Level: FL2\n")

    def test_variant_13_short_bold(self) -> None:
        self._assert_passes("**Frustration Level: FL0**\n")

    def test_variant_14_highest_fl_reached(self) -> None:
        self._assert_passes("**Highest FL reached this run: FL1.**\n")


class MalformedAndMissing(unittest.TestCase):
    def test_missing_log_returns_error(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            rc, _, err = _capture([str(folder)])
            self.assertEqual(rc, 1)
            self.assertIn("FR.B.4:missing", err)

    def test_empty_log_returns_error(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            log = Path(td) / "friction-log.md"
            _write(log, "")
            rc, _, err = _capture([str(log)])
            self.assertEqual(rc, 1)
            self.assertIn("FR.B.4:missing", err)

    def test_malformed_frontmatter_only(self) -> None:
        body = (
            "---\n"
            "summary: \"FL2 in frontmatter only\"\n"
            "---\n"
            "\n"
            "# Friction Log\n\nNo declaration in body.\n"
        )
        with tempfile.TemporaryDirectory() as td:
            log = Path(td) / "friction-log.md"
            _write(log, body)
            rc, _, err = _capture([str(log)])
            self.assertEqual(rc, 1)
            self.assertIn("FR.B.4:malformed", err)
            self.assertIn("frontmatter", err.lower())

    def test_malformed_token_in_prose(self) -> None:
        body = "# Friction Log\n\nThe FL2 case was nasty.\n"
        with tempfile.TemporaryDirectory() as td:
            log = Path(td) / "friction-log.md"
            _write(log, body)
            rc, _, err = _capture([str(log)])
            self.assertEqual(rc, 1)
            self.assertIn("FR.B.4:malformed", err)

    def test_no_fl_token_at_all(self) -> None:
        body = "# Friction Log\n\nNothing meaningful happened.\n"
        with tempfile.TemporaryDirectory() as td:
            log = Path(td) / "friction-log.md"
            _write(log, body)
            rc, _, err = _capture([str(log)])
            self.assertEqual(rc, 1)
            self.assertIn("FR.B.4:missing", err)


class TaskFolderSurface(unittest.TestCase):
    def test_folder_with_friction_log_passes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td) / "032-example-task"
            folder.mkdir()
            _write(folder / "task.md", "task body\n")
            _write(
                folder / "friction-log.md",
                "Highest Frustration Level: FL0\n",
            )
            rc, _, _ = _capture([str(folder)])
            self.assertEqual(rc, 0)

    def test_folder_with_pr_body_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td) / "032-example-task"
            folder.mkdir()
            _write(folder / "task.md", "task body\n")
            _write(
                folder / "session.pr-body.md",
                "## Summary\n\nstuff\n\n## Frustration Log\n\n"
                "Highest Frustration Level: FL1\n",
            )
            rc, _, _ = _capture([str(folder)])
            self.assertEqual(rc, 0)

    def test_folder_with_neither_surface(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td) / "032-example-task"
            folder.mkdir()
            _write(folder / "task.md", "task body\n")
            rc, _, err = _capture([str(folder)])
            self.assertEqual(rc, 1)
            self.assertIn("FR.B.4:missing", err)
            self.assertIn("neither", err)


class PRBodySurface(unittest.TestCase):
    def test_pr_body_with_section(self) -> None:
        body = (
            "# PR Title\n\n## Summary\n\nstuff\n\n"
            "## Frustration Log\n\nHighest Frustration Level: FL2\n\n"
            "FL2 — diagnostic of the issue.\n\n## Test plan\n\n- run\n"
        )
        with tempfile.TemporaryDirectory() as td:
            pr = Path(td) / "pr-body.md"
            _write(pr, body)
            rc, _, _ = _capture([str(pr)])
            self.assertEqual(rc, 0)

    def test_pr_body_missing_section(self) -> None:
        body = "# PR Title\n\n## Summary\n\nstuff\n\n## Test plan\n\n- run\n"
        with tempfile.TemporaryDirectory() as td:
            pr = Path(td) / "pr-body.md"
            _write(pr, body)
            rc, _, err = _capture([str(pr)])
            self.assertEqual(rc, 1)
            self.assertIn("FR.B.4:missing", err)

    def test_pr_body_section_without_declaration(self) -> None:
        body = (
            "# PR\n\n## Frustration Log\n\nNothing significant happened.\n\n"
            "## Test plan\n"
        )
        with tempfile.TemporaryDirectory() as td:
            pr = Path(td) / "pr-body.md"
            _write(pr, body)
            rc, _, err = _capture([str(pr)])
            self.assertEqual(rc, 1)
            self.assertIn("FR.B.4:missing", err)


class BothSurfacesPresent(unittest.TestCase):
    """When friction-log.md exists, it takes precedence — pr-body fallback
    is not consulted, so a malformed pr-body body does not poison the
    pass when the friction-log.md is clean."""

    def test_friction_log_wins_over_pr_body(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td) / "032-example-task"
            folder.mkdir()
            _write(folder / "task.md", "task body\n")
            _write(
                folder / "friction-log.md",
                "Highest Frustration Level: FL0\n",
            )
            _write(
                folder / "session.pr-body.md",
                "# malformed pr body without section\n",
            )
            rc, _, _ = _capture([str(folder)])
            self.assertEqual(rc, 0)


class MultiTargetSuiteFailure(unittest.TestCase):
    def test_failure_on_any_target_is_suite_failure(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ok = Path(td) / "ok.md"
            bad = Path(td) / "bad.md"
            _write(ok, "Highest Frustration Level: FL0\n")
            _write(bad, "no FL token here\n")
            rc, _, err = _capture([str(ok), str(bad)])
            self.assertEqual(rc, 1)
            self.assertIn("FR.B.4", err)


if __name__ == "__main__":
    unittest.main()
