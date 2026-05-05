"""Tests for fm-edit — SPEC §6 scenario F.6.5 + body-byte invariant + M01-P4."""
from __future__ import annotations

import io
import contextlib
import sys
import tempfile
import threading
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "tools" / "fm"))

import edit as fm_edit  # noqa: E402
import _core  # noqa: E402


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = fm_edit.main(argv)
    return rc, out.getvalue(), err.getvalue()


def _split_body(text: str) -> str:
    _, _, rest = fm_edit._split(text)
    return rest


class TestIdempotentAppend(unittest.TestCase):
    """SPEC §6 scenario F.6.5 + M01-P4: idempotent list append, body-byte stability."""

    def test_F_6_5_append_three_times(self):
        text = """---
slug: x
task_uses_prompts:
  - foo
---

## Section
body bytes
"""
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(text)
            path = Path(f.name)
        try:
            original_body = _split_body(text)
            for _ in range(3):
                rc, _, _ = _capture([str(path), "--append-list",
                                     "task_uses_prompts", "foo"])
                self.assertEqual(rc, 0)
            after = path.read_text(encoding="utf-8")
            self.assertEqual(_split_body(after), original_body,
                             "body bytes mutated by fm-edit")
            fm = _core.parse_frontmatter(after, strict=True)
            self.assertEqual(fm["task_uses_prompts"], ["foo"])
        finally:
            path.unlink()


class TestBumpUpdated(unittest.TestCase):
    def test_bump_updated_idempotent(self):
        import datetime
        today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        text = f"---\nslug: x\nupdated: {today}\n---\n\nbody\n"
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(text)
            path = Path(f.name)
        try:
            rc, _, _ = _capture([str(path), "--bump-updated"])
            self.assertEqual(rc, 0)
            self.assertEqual(path.read_text(encoding="utf-8"), text)
        finally:
            path.unlink()

    def test_bump_updates_when_stale(self):
        text = "---\nslug: x\nupdated: 2020-01-01\n---\n\nbody\n"
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(text)
            path = Path(f.name)
        try:
            rc, _, _ = _capture([str(path), "--bump-updated"])
            self.assertEqual(rc, 0)
            after = path.read_text(encoding="utf-8")
            self.assertNotIn("2020-01-01", after)
            self.assertEqual(_split_body(after), _split_body(text))
        finally:
            path.unlink()


class TestSetUnset(unittest.TestCase):
    def test_set_scalar(self):
        text = "---\nslug: x\nstatus: draft\n---\n\nbody\n"
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(text)
            path = Path(f.name)
        try:
            rc, _, _ = _capture([str(path), "--set", "status=active"])
            self.assertEqual(rc, 0)
            after = path.read_text(encoding="utf-8")
            self.assertIn("status: active", after)
            self.assertEqual(_split_body(after), _split_body(text))
        finally:
            path.unlink()

    def test_set_on_list_key_fails(self):
        text = "---\nlist_key:\n  - a\n  - b\n---\n\nbody\n"
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(text)
            path = Path(f.name)
        try:
            rc, _, err = _capture([str(path), "--set", "list_key=oops"])
            self.assertEqual(rc, fm_edit.EXIT_TYPE_ERROR)
            self.assertIn("type error", err)
        finally:
            path.unlink()

    def test_unset_missing_is_noop(self):
        text = "---\nslug: x\n---\n\nbody\n"
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(text)
            path = Path(f.name)
        try:
            rc, _, _ = _capture([str(path), "--unset", "absent"])
            self.assertEqual(rc, 0)
            self.assertEqual(path.read_text(encoding="utf-8"), text)
        finally:
            path.unlink()


class TestRemoveFromList(unittest.TestCase):
    def test_remove_from_list(self):
        text = "---\nl:\n  - a\n  - b\n  - c\n---\n\nbody\n"
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(text)
            path = Path(f.name)
        try:
            rc, _, _ = _capture([str(path), "--remove-from-list", "l", "b"])
            self.assertEqual(rc, 0)
            fm = _core.parse_frontmatter(path.read_text(encoding="utf-8"), strict=True)
            self.assertEqual(fm["l"], ["a", "c"])
        finally:
            path.unlink()


class TestParallelAppendNoDup(unittest.TestCase):
    """M01-P4: two parallel `--append-list` runs MUST NOT produce duplicates."""

    def test_concurrent_append_idempotent(self):
        text = "---\nl:\n  - foo\n---\n\nbody\n"
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(text)
            path = Path(f.name)
        try:
            errors: list[Exception] = []

            def worker():
                try:
                    fm_edit.main([str(path), "--append-list", "l", "foo"])
                except Exception as e:  # pragma: no cover
                    errors.append(e)

            threads = [threading.Thread(target=worker) for _ in range(8)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            self.assertFalse(errors)
            fm = _core.parse_frontmatter(path.read_text(encoding="utf-8"), strict=True)
            self.assertEqual(fm["l"].count("foo"), 1)
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
