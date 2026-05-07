"""Tests for fm-extract — SPEC §6 scenario F.6.4 + general behaviour."""
from __future__ import annotations

import io
import contextlib
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "tools" / "fm"))

import extract as fm_extract  # noqa: E402


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = fm_extract.main(argv)
    return rc, out.getvalue(), err.getvalue()


class TestExtractSection(unittest.TestCase):
    def test_section_basic(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("---\ntype: note\n---\n\n## Foo\nfoo body\n\n## Bar\nbar body\n")
            path = Path(f.name)
        try:
            rc, out, _ = _capture([str(path), "--section", "Foo"])
            self.assertEqual(rc, 0)
            self.assertIn("foo body", out)
            self.assertNotIn("bar body", out)
        finally:
            path.unlink()

    def test_section_em_dash_and_colon_tolerant(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("---\nx: 1\n---\n\n## Goal —:\nbody\n")
            path = Path(f.name)
        try:
            rc, out, _ = _capture([str(path), "--section", "Goal"])
            self.assertEqual(rc, 0)
            self.assertIn("body", out)
        finally:
            path.unlink()

    def test_section_missing_returns_3(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("---\nx: 1\n---\n\n## A\nbody\n")
            path = Path(f.name)
        try:
            rc, _, err = _capture([str(path), "--section", "Nope"])
            self.assertEqual(rc, 3)
            self.assertIn("not found", err)
        finally:
            path.unlink()

    def test_F_6_4_truncation(self):
        big = "x" * 6000
        text = f"---\nx: 1\n---\n\n## Reference files\n{big}\n"
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(text)
            path = Path(f.name)
        try:
            rc, out, _ = _capture([str(path), "--section", "Reference files"])
            self.assertEqual(rc, 0)
            self.assertLessEqual(len(out.encode("utf-8")),
                                 fm_extract.SECTION_CAP + 4)
            self.assertIn("[truncated; original", out)
        finally:
            path.unlink()


class TestExtractFrontmatter(unittest.TestCase):
    def test_whole_block(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("---\ntype: note\nstatus: active\n---\n\nbody\n")
            path = Path(f.name)
        try:
            rc, out, _ = _capture([str(path), "--frontmatter"])
            self.assertEqual(rc, 0)
            self.assertIn("type: note", out)
            self.assertIn("---", out)
        finally:
            path.unlink()

    def test_single_key(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("---\nslug: foo-bar\n---\n\nbody\n")
            path = Path(f.name)
        try:
            rc, out, _ = _capture([str(path), "--frontmatter", "slug"])
            self.assertEqual(rc, 0)
            self.assertIn("foo-bar", out)
        finally:
            path.unlink()

    def test_missing_key_returns_3(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("---\nslug: foo\n---\n\nbody\n")
            path = Path(f.name)
        try:
            rc, _, err = _capture([str(path), "--frontmatter", "absent"])
            self.assertEqual(rc, 3)
            self.assertIn("not found", err)
        finally:
            path.unlink()


class TestWholeFile(unittest.TestCase):
    def test_whole_file(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("---\nx: 1\n---\n\nfull body\n")
            path = Path(f.name)
        try:
            rc, out, _ = _capture([str(path), "--whole-file"])
            self.assertEqual(rc, 0)
            self.assertIn("full body", out)
            self.assertIn("x: 1", out)
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
