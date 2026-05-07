"""Tests for tools/check-assumption-log.py.

Covers the three diagnostic codes (MISSING, EMPTY, STALE) plus the two
positive-case branches (`(none)` body and populated body) per Task 032 ST-4
acceptance criteria.
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
        "check_assumption_log",
        TOOLS / "check-assumption-log.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_assumption_log"] = module
    spec.loader.exec_module(module)
    return module


cal = _load_module()


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = cal.main(argv)
    return rc, out.getvalue(), err.getvalue()


def _write(path: Path, body: str) -> None:
    path.write_text(body, encoding="utf-8")


def _readme(updated: str = "2026-05-06", section: str | None = "- assumption one") -> str:
    head = (
        "---\n"
        "type: index\n"
        "status: active\n"
        "slug: example-folder\n"
        f"updated: {updated}\n"
        "---\n"
        "\n"
        "# Example\n"
        "\n"
    )
    if section is None:
        return head + "## What\n\nbody\n"
    return head + f"## Assumptions Log\n\n{section}\n"


def _task_md(updated: str = "2026-05-06") -> str:
    return (
        "---\n"
        "type: task\n"
        "status: active\n"
        "slug: example\n"
        f"updated: {updated}\n"
        "task_id: \"999\"\n"
        "---\n"
        "\n"
        "# Task\n"
    )


class TestMissingSection(unittest.TestCase):
    def test_missing_section_emits_MISSING(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "999-example"
            d.mkdir()
            _write(d / "readme.md", _readme(section=None))
            _write(d / "task.md", _task_md())
            rc, out, _ = _capture([str(Path(tmp))])
            self.assertEqual(rc, 2)
            self.assertIn("ASSUMPTION.LOG.MISSING", out)


class TestEmptySection(unittest.TestCase):
    def test_empty_section_emits_EMPTY(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "999-example"
            d.mkdir()
            _write(d / "readme.md", _readme(section="   \n\n<!-- comment only -->"))
            _write(d / "task.md", _task_md())
            rc, out, _ = _capture([str(Path(tmp))])
            self.assertEqual(rc, 2)
            self.assertIn("ASSUMPTION.LOG.EMPTY", out)
            self.assertNotIn("ASSUMPTION.LOG.MISSING", out)


class TestNonePermitted(unittest.TestCase):
    def test_explicit_none_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "999-example"
            d.mkdir()
            _write(d / "readme.md", _readme(section="(none)"))
            _write(d / "task.md", _task_md())
            rc, out, _ = _capture([str(Path(tmp))])
            self.assertEqual(rc, 0)
            self.assertEqual(out.strip(), "")

    def test_uppercase_none_with_whitespace_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "999-example"
            d.mkdir()
            _write(d / "readme.md", _readme(section="  (None)  "))
            _write(d / "task.md", _task_md())
            rc, out, _ = _capture([str(Path(tmp))])
            self.assertEqual(rc, 0)
            self.assertNotIn("EMPTY", out)


class TestPopulatedSection(unittest.TestCase):
    def test_populated_section_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "999-example"
            d.mkdir()
            _write(
                d / "readme.md",
                _readme(section="- assumption one\n- assumption two"),
            )
            _write(d / "task.md", _task_md())
            rc, out, _ = _capture([str(Path(tmp))])
            self.assertEqual(rc, 0)
            self.assertEqual(out.strip(), "")


class TestStaleCurrency(unittest.TestCase):
    def test_readme_older_than_task_emits_STALE(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "999-example"
            d.mkdir()
            _write(d / "readme.md", _readme(updated="2026-04-01", section="- a"))
            _write(d / "task.md", _task_md(updated="2026-05-06"))
            rc, out, _ = _capture([str(Path(tmp))])
            self.assertEqual(rc, 2)
            self.assertIn("ASSUMPTION.LOG.STALE", out)

    def test_readme_synced_with_task_no_STALE(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "999-example"
            d.mkdir()
            _write(d / "readme.md", _readme(updated="2026-05-06", section="- a"))
            _write(d / "task.md", _task_md(updated="2026-05-06"))
            rc, out, _ = _capture([str(Path(tmp))])
            self.assertEqual(rc, 0)
            self.assertNotIn("STALE", out)

    def test_no_sibling_task_md_no_STALE(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "research-example"
            d.mkdir()
            _write(d / "readme.md", _readme(updated="2024-01-01", section="(none)"))
            rc, out, _ = _capture([str(Path(tmp))])
            self.assertEqual(rc, 0)
            self.assertNotIn("STALE", out)


class TestSinglePathArg(unittest.TestCase):
    def test_direct_readme_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "999-example"
            d.mkdir()
            readme = d / "readme.md"
            _write(readme, _readme(section=None))
            _write(d / "task.md", _task_md())
            rc, out, _ = _capture([str(readme)])
            self.assertEqual(rc, 2)
            self.assertIn("ASSUMPTION.LOG.MISSING", out)


if __name__ == "__main__":
    unittest.main()
