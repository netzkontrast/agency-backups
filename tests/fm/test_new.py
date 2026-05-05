"""Tests for fm-new (Task 019 ST-3)."""
from __future__ import annotations

import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools" / "fm"))

import new as fm_new  # type: ignore
import validate as fm_validate  # type: ignore


class _ScratchRepo(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        # AGENTS.md marker so repo_root_from_cwd resolves here.
        (self.root / "AGENTS.md").write_text("# scratch\n", encoding="utf-8")
        (self.root / "tasks").mkdir()
        (self.root / "prompts").mkdir()
        (self.root / "research").mkdir()
        self._old = Path.cwd()
        os.chdir(self.root)
        self.addCleanup(lambda: os.chdir(self._old))

    def _run(self, *argv: str) -> int:
        err = io.StringIO()
        with redirect_stderr(err):
            return fm_new.main(list(argv))


class TestTask(_ScratchRepo):
    def test_first_task_id_is_000(self) -> None:
        code = self._run("task", "--slug", "alpha", "--summary", "first task")
        self.assertEqual(code, 0)
        self.assertTrue((self.root / "tasks" / "000-alpha" / "task.md").exists())
        self.assertTrue((self.root / "tasks" / "000-alpha" / "readme.md").exists())

    def test_next_task_id_increments(self) -> None:
        (self.root / "tasks" / "017-existing").mkdir()
        code = self._run("task", "--slug", "alpha", "--summary", "x")
        self.assertEqual(code, 0)
        self.assertTrue((self.root / "tasks" / "018-alpha").exists())

    def test_task_id_skips_existing(self) -> None:
        # next-id allocator avoids collision by construction.
        (self.root / "tasks" / "000-alpha").mkdir()
        code = self._run("task", "--slug", "alpha", "--summary", "x")
        self.assertEqual(code, 0)
        self.assertTrue((self.root / "tasks" / "001-alpha").exists())

    def test_task_validates_clean(self) -> None:
        self._run("task", "--slug", "beta", "--summary", "second task")
        # validate the new folder against the live ontology.
        rc = fm_validate.main([str(self.root / "tasks" / "000-beta")])
        self.assertEqual(rc, 0)


class TestPrompt(_ScratchRepo):
    def test_prompt_creates_folder(self) -> None:
        code = self._run("prompt", "--slug", "alpha", "--summary", "do a thing")
        self.assertEqual(code, 0)
        self.assertTrue((self.root / "prompts" / "alpha" / "prompt.md").exists())

    def test_prompt_validates_clean(self) -> None:
        self._run("prompt", "--slug", "alpha", "--summary", "do x")
        rc = fm_validate.main([str(self.root / "prompts" / "alpha")])
        self.assertEqual(rc, 0)

    def test_prompt_no_clobber(self) -> None:
        (self.root / "prompts" / "alpha").mkdir()
        code = self._run("prompt", "--slug", "alpha", "--summary", "x")
        self.assertEqual(code, fm_new.EXIT_EXISTS)


class TestResearch(_ScratchRepo):
    def test_research_creates_folder(self) -> None:
        code = self._run("research", "--slug", "alpha", "--summary", "x",
                         "--executes-prompt", "alpha")
        self.assertEqual(code, 0)
        self.assertTrue((self.root / "research" / "alpha" / "readme.md").exists())

    def test_research_validates_clean(self) -> None:
        self._run("research", "--slug", "alpha", "--summary", "x")
        rc = fm_validate.main([str(self.root / "research" / "alpha")])
        self.assertEqual(rc, 0)


class TestSlugValidation(_ScratchRepo):
    def test_invalid_slug_aborts(self) -> None:
        with self.assertRaises(SystemExit):
            fm_new.main(["task", "--slug", "Bad Slug", "--summary", "x"])


if __name__ == "__main__":
    unittest.main()
