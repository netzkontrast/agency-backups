"""Tests covering the M01 falsification attacks P1–P5.

Source: /research/flexible-frontmatter-toolchain/reflection/M01-falsification.md
"""
from __future__ import annotations

import io
import contextlib
import os
import sys
import tempfile
import threading
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "tools" / "fm"))

import _core  # noqa: E402
import validate as fm_validate  # noqa: E402
import edit as fm_edit  # noqa: E402
import query as fm_query  # noqa: E402


def _ontology_into(base: Path) -> None:
    (base / "AGENTS.md").write_text("# stub\n", encoding="utf-8")
    op = base / "maintenance" / "schemas" / "header-ontology.json"
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_text(
        (REPO / "maintenance" / "schemas" / "header-ontology.json")
            .read_text(encoding="utf-8"),
        encoding="utf-8",
    )


def _good_task(slug: str = "x") -> str:
    return f"""---
type: task
status: active
slug: {slug}
summary: "t"
created: 2026-05-05
updated: 2026-05-05
task_id: "099"
task_status: open
task_owner: "x"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths: []
---

## Goal
g
## Plan
p
## Todo
- [ ] x
## Links
- foo
"""


def _run(main, argv: list[str]) -> tuple[int, str]:
    out = io.StringIO(); err = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = main(argv)
    return rc, out.getvalue() + err.getvalue()


class TestP1RequiredOnlyValidation(unittest.TestCase):
    """P1: typo `tpye:` for `type:` MUST fail with did-you-mean."""

    def test_P1_typo_caught(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            _ontology_into(base)
            text = _good_task().replace("type: task", "tpye: task")
            target = base / "tasks/099-x/task.md"
            target.parent.mkdir(parents=True)
            target.write_text(text, encoding="utf-8")
            cwd = os.getcwd()
            os.chdir(base)
            try:
                rc, out = _run(fm_validate.main, [])
            finally:
                os.chdir(cwd)
            self.assertEqual(rc, 1)
            self.assertIn("F.3.4", out)
            self.assertIn("did you mean 'type'", out)


class TestP2StatelessScan(unittest.TestCase):
    """P2: scope MUST be capped to operational roots; large external trees ignored."""

    def test_P2_scope_default_cap(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            _ontology_into(base)
            # Plant a "decoy" file outside operational roots.
            (base / "junk").mkdir()
            (base / "junk" / "decoy.md").write_text(
                "---\ntype: task\nstatus: active\nslug: decoy\n---\n",
                encoding="utf-8",
            )
            (base / "tasks" / "099-x").mkdir(parents=True)
            (base / "tasks" / "099-x" / "task.md").write_text(
                _good_task(), encoding="utf-8"
            )
            cwd = os.getcwd()
            os.chdir(base)
            try:
                rc, out = _run(fm_query.main, ["type=task"])
            finally:
                os.chdir(cwd)
            self.assertEqual(rc, 0)
            self.assertIn("099-x", out)
            self.assertNotIn("decoy", out)


class TestP3RequiredHeadingsOnlyH2(unittest.TestCase):
    """P3: validator MUST only check `## ` headings; deeper nesting is author-owned."""

    def test_P3_h3_changes_do_not_fail(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            _ontology_into(base)
            text = _good_task() + "\n### subsection\nbody\n"
            (base / "tasks" / "099-x").mkdir(parents=True)
            (base / "tasks" / "099-x" / "task.md").write_text(text, encoding="utf-8")
            cwd = os.getcwd()
            os.chdir(base)
            try:
                rc, out = _run(fm_validate.main, [])
            finally:
                os.chdir(cwd)
            self.assertEqual(rc, 0, msg=out)


class TestP4FmEditRace(unittest.TestCase):
    """P4: parallel `--append-list` MUST NOT duplicate items."""

    def test_P4_thread_race_no_duplicates(self):
        text = "---\nl:\n  - a\n---\n\nbody\n"
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(text)
            path = Path(f.name)
        try:
            def worker():
                fm_edit.main([str(path), "--append-list", "l", "a"])
            threads = [threading.Thread(target=worker) for _ in range(16)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            fm = _core.parse_frontmatter(path.read_text(encoding="utf-8"), strict=True)
            self.assertEqual(fm["l"], ["a"])
        finally:
            path.unlink()


class TestP6ReadFmDiagnoses(unittest.TestCase):
    """P6 (Task 058): read_fm MUST distinguish missing vs malformed frontmatter.

    A file with `---\\nkey: [unbalanced\\n---\\n# body` MUST surface a
    parse-error diagnostic, NOT a cascade of "missing required key" errors.
    """

    def test_P6_malformed_yaml_emits_warn_not_missing_keys(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            _ontology_into(base)
            # Plant a task file with malformed YAML (depth 2 nesting).
            target = base / "tasks/099-x/task.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "---\n"
                "type: task\n"
                "deeply:\n"
                "  nested:\n"
                "    forbidden: yes\n"
                "---\n\n## Goal\nbody\n",
                encoding="utf-8",
            )
            fm, diag = _core.read_fm_with_diag(target, strict=False)
            # Non-strict salvages what it can but the WARN surfaces.
            self.assertIsNotNone(diag)
            assert diag is not None  # for type-checker
            self.assertEqual(diag.severity, "WARN")
            self.assertEqual(diag.code, "F.3.3")
            self.assertIn("malformed frontmatter", diag.message)
            self.assertIn("nested deeper", diag.message)

    def test_P6_strict_promotes_to_error(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "x.md"
            target.write_text(
                "---\nkey:\n  nested:\n    deep: x\n---\n", encoding="utf-8",
            )
            fm, diag = _core.read_fm_with_diag(target, strict=True)
            self.assertEqual(fm, {})
            assert diag is not None
            self.assertEqual(diag.severity, "ERROR")
            self.assertEqual(diag.code, "F.3.3")

    def test_P6_no_frontmatter_returns_none_diag(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "x.md"
            target.write_text("# just a body\nno fences here\n", encoding="utf-8")
            fm, diag = _core.read_fm_with_diag(target, strict=False)
            self.assertEqual(fm, {})
            self.assertIsNone(diag)

    def test_P6_empty_file_returns_none_diag(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "x.md"
            target.write_text("", encoding="utf-8")
            fm, diag = _core.read_fm_with_diag(target, strict=False)
            self.assertEqual(fm, {})
            self.assertIsNone(diag)

    def test_P6_well_formed_frontmatter_returns_none_diag(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "x.md"
            target.write_text(
                "---\ntype: task\nslug: x\n---\n\nbody\n", encoding="utf-8",
            )
            fm, diag = _core.read_fm_with_diag(target, strict=False)
            self.assertEqual(fm.get("slug"), "x")
            self.assertIsNone(diag)

    def test_P6_read_fm_back_compat_unchanged(self):
        """The legacy read_fm() signature MUST still return only the dict."""
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "x.md"
            target.write_text(
                "---\ntype: task\nslug: y\n---\n", encoding="utf-8",
            )
            fm = _core.read_fm(target, strict=False)
            self.assertEqual(fm.get("slug"), "y")


class TestP5LoopUsesRepoSurfaces(unittest.TestCase):
    """P5: the toolchain MUST run with no subagents and no browser — just stdlib."""

    def test_P5_no_third_party_imports(self):
        # Ensure the four tools import cleanly with stdlib-only modules.
        # (Smoke test; a tougher import audit lives in the build infra.)
        for mod_name in ("validate", "extract", "edit", "query"):
            mod_path = REPO / "tools" / "fm" / f"{mod_name}.py"
            text = mod_path.read_text(encoding="utf-8")
            for forbidden in ("import yaml", "from yaml", "import pydantic",
                              "import jsonschema", "import requests"):
                self.assertNotIn(forbidden, text,
                                 msg=f"{mod_name} imports forbidden module")


if __name__ == "__main__":
    unittest.main()
