"""Tests for tools/maintenance/dynamic-readme-partition.py.

Covers the four diagnostic outcomes per Task 039 ST-4 acceptance criterion 4:

* clean partition (no diagnostics)
* missing markers (advisory ``missing-marker``)
* mutated / unbalanced static section (``unbalanced-marker``)
* missing readme stub (silent — _iter_readmes yields nothing)

Also exercises ``misplaced-section`` (static-below / dynamic-above) and
``multiple-markers`` for completeness.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
TOOLS = REPO / "tools"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "dynamic_readme_partition",
        TOOLS / "maintenance" / "dynamic-readme-partition.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["dynamic_readme_partition"] = module
    spec.loader.exec_module(module)
    return module


drp = _load_module()


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = drp.main(argv)
    return rc, out.getvalue(), err.getvalue()


FRONTMATTER = (
    "---\n"
    "type: index\n"
    "status: active\n"
    "slug: example-folder\n"
    "summary: \"fixture\"\n"
    "created: 2026-05-08\n"
    "updated: 2026-05-08\n"
    "---\n\n"
)


def _partitioned_readme() -> str:
    return (
        FRONTMATTER
        + "# Example\n\n"
        + "## Purpose\n\nWhy this folder exists.\n\n"
        + "## Linked Navigation\n\n- [`a`](./a)\n\n"
        + "## Assumptions Log\n\n(none)\n\n"
        + "<!-- BEGIN DYNAMIC -->\n\n"
        + "## Current State\n\nopen.\n\n"
        + "## Open Blockers\n\n(none)\n\n"
        + "<!-- END DYNAMIC -->\n"
    )


def _no_marker_readme() -> str:
    return (
        FRONTMATTER
        + "# Example\n\n"
        + "## Purpose\n\nWhy.\n\n"
        + "## Files\n\n- [`a`](./a)\n\n"
        + "## Assumptions Log\n\n(none)\n"
    )


def _unbalanced_readme() -> str:
    """BEGIN marker without matching END."""
    return (
        FRONTMATTER
        + "# Example\n\n"
        + "## Purpose\n\nWhy.\n\n"
        + "<!-- BEGIN DYNAMIC -->\n\n"
        + "## Current State\n\nopen.\n"
    )


def _misplaced_static_below() -> str:
    """Static heading appears below the BEGIN marker (mutated static section)."""
    return (
        FRONTMATTER
        + "# Example\n\n"
        + "## Purpose\n\nWhy.\n\n"
        + "<!-- BEGIN DYNAMIC -->\n\n"
        + "## Current State\n\nopen.\n\n"
        + "## Assumptions Log\n\nstale entry below the boundary.\n\n"
        + "<!-- END DYNAMIC -->\n"
    )


def _misplaced_dynamic_above() -> str:
    """Dynamic heading appears above BEGIN."""
    return (
        FRONTMATTER
        + "# Example\n\n"
        + "## Purpose\n\nWhy.\n\n"
        + "## Current State\n\noops, dynamic above the marker.\n\n"
        + "<!-- BEGIN DYNAMIC -->\n\n"
        + "## Open Blockers\n\n(none)\n\n"
        + "<!-- END DYNAMIC -->\n"
    )


def _multiple_markers_readme() -> str:
    return (
        FRONTMATTER
        + "# Example\n\n"
        + "## Purpose\n\nWhy.\n\n"
        + "<!-- BEGIN DYNAMIC -->\n\n"
        + "## Current State\n\nopen.\n\n"
        + "<!-- BEGIN DYNAMIC -->\n\n"
        + "## Open Blockers\n\n(none)\n\n"
        + "<!-- END DYNAMIC -->\n"
    )


def _markers_in_fence_readme() -> str:
    """Markers inside a fenced code block MUST be ignored — false-positive guard."""
    return (
        FRONTMATTER
        + "# Example\n\n"
        + "## Purpose\n\nWhy.\n\n"
        + "## Files\n\n"
        + "```markdown\n"
        + "<!-- BEGIN DYNAMIC -->\n"
        + "## Current State\n"
        + "<!-- END DYNAMIC -->\n"
        + "```\n"
    )


def _write_readme_at(parent: Path, slug: str, body: str) -> Path:
    folder = parent / slug
    folder.mkdir(parents=True, exist_ok=True)
    readme = folder / "readme.md"
    readme.write_text(body, encoding="utf-8")
    return readme


class DynamicReadmePartitionTests(unittest.TestCase):
    # --- Acceptance criterion 4: clean partition ---------------------------

    def test_clean_partition_emits_no_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            readme = _write_readme_at(tmp_path / "tasks", "001-x", _partitioned_readme())
            rc, stdout, _ = _capture([str(readme)])
            self.assertEqual(rc, 0, msg=stdout)
            self.assertEqual(stdout, "")

    # --- Acceptance criterion 4: missing markers ---------------------------

    def test_no_markers_emits_advisory_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            readme = _write_readme_at(Path(tmp) / "tasks", "002-y", _no_marker_readme())
            rc, stdout, _ = _capture([str(readme)])
            self.assertEqual(rc, 2)
            self.assertIn("WARN:M.B.6:missing-marker", stdout)
            # Falsification mitigation: never an ERROR.
            self.assertNotIn("ERROR", stdout)
            # One-time advisory, not one per heading.
            self.assertEqual(stdout.count("WARN:M.B.6"), 1)

    # --- Acceptance criterion 4: mutated static section --------------------

    def test_unbalanced_marker_emits_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            readme = _write_readme_at(Path(tmp) / "tasks", "003-z", _unbalanced_readme())
            rc, stdout, _ = _capture([str(readme)])
            self.assertEqual(rc, 2)
            self.assertIn("WARN:M.B.6:unbalanced-marker", stdout)

    def test_static_heading_below_begin_marker_emits_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            readme = _write_readme_at(
                Path(tmp) / "tasks", "004-a", _misplaced_static_below()
            )
            rc, stdout, _ = _capture([str(readme)])
            self.assertEqual(rc, 2)
            self.assertIn("WARN:M.B.6:misplaced-section", stdout)
            self.assertIn("Assumptions Log", stdout)
            self.assertIn("appears below", stdout)

    def test_dynamic_heading_above_begin_marker_emits_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            readme = _write_readme_at(
                Path(tmp) / "tasks", "005-b", _misplaced_dynamic_above()
            )
            rc, stdout, _ = _capture([str(readme)])
            self.assertEqual(rc, 2)
            self.assertIn("WARN:M.B.6:misplaced-section", stdout)
            self.assertIn("Current State", stdout)
            self.assertIn("appears above", stdout)

    def test_multiple_begin_markers_emits_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            readme = _write_readme_at(
                Path(tmp) / "tasks", "006-c", _multiple_markers_readme()
            )
            rc, stdout, _ = _capture([str(readme)])
            self.assertEqual(rc, 2)
            self.assertIn("WARN:M.B.6:multiple-markers", stdout)

    def test_markers_inside_fence_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            readme = _write_readme_at(
                Path(tmp) / "tasks", "007-d", _markers_in_fence_readme()
            )
            rc, stdout, _ = _capture([str(readme)])
            # Fenced markers do not count; this readme has no real markers,
            # so the advisory `missing-marker` should fire (never anything else).
            self.assertEqual(rc, 2)
            self.assertIn("WARN:M.B.6:missing-marker", stdout)
            self.assertNotIn("multiple-markers", stdout)
            self.assertNotIn("misplaced-section", stdout)

    # --- Acceptance criterion 4: missing readme stub -----------------------

    def test_missing_readme_stub_yields_no_diagnostics(self) -> None:
        """A folder with no readme.md MUST NOT produce a diagnostic from
        this linter (the stub-presence rule is owned by tools/lint-structure.py
        per FOLDERS.md F.3 — out of scope here)."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "tasks" / "008-empty").mkdir(parents=True)
            rc, stdout, stderr = _capture([str(tmp_path / "tasks")])
            self.assertEqual(rc, 0, msg=stdout)
            self.assertEqual(stdout, "")
            self.assertIn("0 WARN", stderr)

    # --- Directory walking + provider exemption ----------------------------

    def test_directory_walk_picks_up_operational_readmes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            _write_readme_at(tmp_path / "tasks", "010-clean", _partitioned_readme())
            _write_readme_at(tmp_path / "tasks", "011-bad", _unbalanced_readme())
            rc, stdout, _ = _capture([str(tmp_path / "tasks")])
            self.assertEqual(rc, 2)
            # Exactly one folder produces a diagnostic.
            self.assertEqual(stdout.count("WARN:M.B.6"), 1)
            self.assertIn("011-bad", stdout)
            self.assertNotIn("010-clean", stdout)

    def test_provider_research_subtree_is_exempt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # Two operational readmes — one under research/<slug>/, one under
            # research/gemini/<slug>/. The provider one MUST be skipped.
            _write_readme_at(
                tmp_path / "research", "real-slug", _no_marker_readme()
            )
            provider_folder = tmp_path / "research" / "gemini" / "external-slug"
            provider_folder.mkdir(parents=True)
            (provider_folder / "readme.md").write_text(
                _no_marker_readme(), encoding="utf-8"
            )
            rc, stdout, _ = _capture([str(tmp_path / "research")])
            self.assertEqual(rc, 2)
            self.assertIn("real-slug", stdout)
            self.assertNotIn("external-slug", stdout)

    # --- Frontmatter delimited by --- is parsed safely ---------------------

    def test_frontmatter_is_stripped_before_marker_scan(self) -> None:
        # A `<!-- BEGIN DYNAMIC -->` token planted inside the frontmatter
        # block (here as a fake key value) MUST NOT be treated as a real
        # marker. We simulate by embedding the exact token in a comment-style
        # line inside the body to confirm the body-only scan still works.
        body = (
            "---\n"
            "type: index\n"
            "status: active\n"
            "slug: fm-example\n"
            "summary: \"contains the literal token <!-- BEGIN DYNAMIC --> in summary\"\n"
            "created: 2026-05-08\n"
            "updated: 2026-05-08\n"
            "---\n\n"
            "# Example\n\n"
            "## Purpose\n\nFM-only token must not count.\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            readme = _write_readme_at(Path(tmp) / "tasks", "012-fm", body)
            rc, stdout, _ = _capture([str(readme)])
            # The body has no markers, so we expect missing-marker, not
            # multiple-markers.
            self.assertEqual(rc, 2)
            self.assertIn("missing-marker", stdout)
            self.assertNotIn("multiple-markers", stdout)


if __name__ == "__main__":
    unittest.main()
