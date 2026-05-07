"""Tests for tools/check-narrative-ontology-load.py (AGENTS.md NO.5).

Covers the three contract scenarios from the brief:
  * positive: narrative task references the ontology → exit 0 (allowed).
  * negative: non-narrative task reads the ontology → exit 2 (WARN).
  * edge: missing task context → exit 0 (no claim, no diagnostic).

The linter is executed via runpy from inside an isolated tempdir so the
tests do not depend on git state. Frontmatter-only mode is forced via
`--paths-from-frontmatter-only` to keep the heuristic deterministic.

Run: python3 -m pytest tools/tests/test_narrative_ontology_load.py -v
"""
from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from tempfile import TemporaryDirectory

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = REPO_ROOT / "tools"
sys.path.insert(0, str(TOOLS_DIR))

# Import the linter as a module via importlib (the filename has hyphens).
import importlib.util as _ilu

_SPEC = _ilu.spec_from_file_location(
    "check_narrative_ontology_load",
    TOOLS_DIR / "check-narrative-ontology-load.py",
)
assert _SPEC is not None and _SPEC.loader is not None
checker = _ilu.module_from_spec(_SPEC)
_SPEC.loader.exec_module(checker)


def _write_task(task_dir: Path, affects: list[str]) -> Path:
    """Write a minimal but well-formed task.md with the given task_affects_paths."""
    task_dir.mkdir(parents=True, exist_ok=True)
    if affects:
        affects_block = "task_affects_paths:\n" + "\n".join(
            f"  - {p}" for p in affects
        )
    else:
        affects_block = "task_affects_paths: []"
    body = (
        "---\n"
        "type: task\n"
        "status: active\n"
        "slug: fixture-task\n"
        'summary: "test fixture"\n'
        "created: 2026-05-07\n"
        "updated: 2026-05-07\n"
        'task_id: "999"\n'
        "task_status: open\n"
        'task_owner: "unassigned"\n'
        "task_priority: P3\n"
        f"{affects_block}\n"
        "---\n\n"
        "# Fixture\n"
    )
    task_md = task_dir / "task.md"
    task_md.write_text(body, encoding="utf-8")
    return task_md


def _run(*argv: str) -> tuple[int, str]:
    buf = io.StringIO()
    with redirect_stderr(buf):
        rc = checker.main(list(argv))
    return rc, buf.getvalue()


class NarrativeOntologyLoadTests(unittest.TestCase):
    def test_positive_narrative_task_with_ontology_passes(self) -> None:
        """A task that owns skills/dramatica-* AND references the ontology
        is in narrative scope and MUST exit 0."""
        with TemporaryDirectory() as tmp:
            task_dir = Path(tmp) / "tasks" / "100-narrative"
            _write_task(
                task_dir,
                affects=[
                    "skills/dramatica-foo/",
                    "maintenance/schemas/narrative-ontology/ontology.json",
                ],
            )
            rc, err = _run(
                str(task_dir),
                "--paths-from-frontmatter-only",
            )
            self.assertEqual(rc, 0, msg=f"unexpected WARN: {err!r}")
            self.assertEqual(err, "")

    def test_negative_non_narrative_task_loading_ontology_warns(self) -> None:
        """A task whose affects-list omits narrative scope but reads the
        ontology MUST emit a WARN diagnostic and exit 2."""
        with TemporaryDirectory() as tmp:
            task_dir = Path(tmp) / "tasks" / "101-tooling"
            _write_task(
                task_dir,
                affects=[
                    "tools/some-helper.py",
                    "maintenance/schemas/narrative-ontology/ontology.json",
                ],
            )
            rc, err = _run(
                str(task_dir),
                "--paths-from-frontmatter-only",
            )
            self.assertEqual(rc, 2, msg=f"expected WARN exit 2, got {rc}: {err!r}")
            self.assertIn("::WARN:NO.5:", err)
            self.assertIn("narrative-ontology load detected", err)

    def test_edge_no_task_context_exits_clean(self) -> None:
        """If the target is neither a task folder nor a task.md, the linter
        MUST stay silent and exit 0 (NO.5 is silent without context)."""
        with TemporaryDirectory() as tmp:
            empty_dir = Path(tmp) / "not-a-task"
            empty_dir.mkdir()
            rc, err = _run(
                str(empty_dir),
                "--paths-from-frontmatter-only",
            )
            self.assertEqual(rc, 0)
            self.assertEqual(err, "")

    def test_accepts_task_md_file_argument(self) -> None:
        """Passing the task.md path directly is equivalent to passing the
        folder — exercised here against the negative case."""
        with TemporaryDirectory() as tmp:
            task_dir = Path(tmp) / "tasks" / "102-tooling"
            task_md = _write_task(
                task_dir,
                affects=[
                    "tools/some-helper.py",
                    "maintenance/schemas/narrative-ontology/ontology.json",
                ],
            )
            rc, err = _run(
                str(task_md),
                "--paths-from-frontmatter-only",
            )
            self.assertEqual(rc, 2)
            self.assertIn("NO.5", err)

    def test_non_narrative_task_without_ontology_passes(self) -> None:
        """A purely tooling task with no narrative-ontology reads must not
        WARN — the heuristic only fires when both signals are present."""
        with TemporaryDirectory() as tmp:
            task_dir = Path(tmp) / "tasks" / "103-tooling"
            _write_task(
                task_dir,
                affects=["tools/some-helper.py", "AGENTS.md"],
            )
            rc, err = _run(
                str(task_dir),
                "--paths-from-frontmatter-only",
            )
            self.assertEqual(rc, 0)
            self.assertEqual(err, "")


if __name__ == "__main__":
    unittest.main()
