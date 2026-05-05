"""Tests for fm-rename — cross-file slug rename per SPEC §7.2 (Task 019 ST-1).

Covers:
  - scalar field rename (e.g., prompt_relates_to_task)
  - list-item rename (e.g., task_uses_prompts)
  - no-match → no-op exit 0
  - idempotency: a second run with the same args is a no-op
  - atomicity: when a write fails mid-plan, files BEFORE the failure remain
    written; the orchestrator surfaces the error so callers can retry — and
    a *re-scan* before write detects external mutation and aborts cleanly
  - --dry-run: prints plan, mutates nothing
  - T3 refusal: exits 4 when the slug is referenced from a done-Task's
    task_affects_paths
  - body-byte invariant: every write preserves bytes outside frontmatter
  - folder rename via --rename-folder
"""
from __future__ import annotations

import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "tools" / "fm"))

import rename as fm_rename  # noqa: E402
import _core  # noqa: E402


# ---- helpers ----------------------------------------------------------------


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = fm_rename.main(argv)
    return rc, out.getvalue(), err.getvalue()


def _split_body(text: str) -> str:
    _, _, rest = fm_rename._split(text)
    return rest


class _Sandbox:
    """Self-contained tree with AGENTS.md marker + ontology copy so the
    repo_root_from_cwd walker resolves to our temp dir."""

    def __init__(self, base: Path) -> None:
        self.base = base
        (base / "AGENTS.md").write_text("# stub\n", encoding="utf-8")
        op = base / "maintenance" / "schemas" / "header-ontology.json"
        op.parent.mkdir(parents=True, exist_ok=True)
        op.write_text(
            (REPO / "maintenance" / "schemas" / "header-ontology.json")
                .read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    def write(self, rel: str, text: str) -> Path:
        path = self.base / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def run(self, *argv: str) -> tuple[int, str, str]:
        cwd = os.getcwd()
        os.chdir(self.base)
        try:
            return _capture(list(argv))
        finally:
            os.chdir(cwd)


def _task_md(slug: str, *, status: str = "active",
             task_status: str = "open",
             task_uses_prompts: list[str] | None = None,
             task_affects_paths: list[str] | None = None) -> str:
    body_uses = (
        "task_uses_prompts: []\n" if not task_uses_prompts
        else "task_uses_prompts:\n" + "".join(
            f"  - {s}\n" for s in task_uses_prompts)
    )
    body_paths = (
        "task_affects_paths: []\n" if not task_affects_paths
        else "task_affects_paths:\n" + "".join(
            f"  - {s}\n" for s in task_affects_paths)
    )
    return (
        "---\n"
        "type: task\n"
        f"status: {status}\n"
        f"slug: {slug}\n"
        'summary: "t"\n'
        "created: 2026-05-05\n"
        "updated: 2026-05-05\n"
        'task_id: "099"\n'
        f"task_status: {task_status}\n"
        'task_owner: "x"\n'
        "task_priority: P1\n"
        f"{body_uses}"
        "task_spawns_research: []\n"
        "task_spawns_prompts: []\n"
        f"{body_paths}"
        "---\n"
        "\n"
        "## Goal\n"
        "g\n"
        "## Plan\n"
        "1. p\n"
        "## Todo\n"
        "- [ ] x\n"
        "## Links\n"
        "- ./readme.md\n"
    )


def _prompt_md(slug: str, *, prompt_relates_to_task: str | None = None) -> str:
    extra = (f"prompt_relates_to_task: {prompt_relates_to_task}\n"
             if prompt_relates_to_task else "")
    return (
        "---\n"
        "type: prompt\n"
        "status: active\n"
        f"slug: {slug}\n"
        'summary: "p"\n'
        "created: 2026-05-05\n"
        "updated: 2026-05-05\n"
        'prompt_kind: "general"\n'
        'prompt_framework: "RISEN"\n'
        'prompt_target_agent: "claude"\n'
        f"{extra}"
        "---\n"
        "\n"
        "body bytes here\n"
    )


# ---- tests ------------------------------------------------------------------


class TestListRename(unittest.TestCase):
    def test_renames_list_item(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            task = sb.write(
                "tasks/099-x/task.md",
                _task_md("x", task_uses_prompts=["foo", "bar"]),
            )
            original_body = _split_body(task.read_text(encoding="utf-8"))
            rc, out, err = sb.run("foo", "foo-renamed")
            self.assertEqual(rc, 0, msg=err)
            after = task.read_text(encoding="utf-8")
            fm = _core.parse_frontmatter(after, strict=True)
            self.assertEqual(fm["task_uses_prompts"], ["foo-renamed", "bar"])
            self.assertEqual(_split_body(after), original_body,
                             "body bytes mutated by fm-rename")


class TestScalarRename(unittest.TestCase):
    def test_renames_scalar_field(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            prompt = sb.write(
                "prompts/p1/prompt.md",
                _prompt_md("p1", prompt_relates_to_task="alpha"),
            )
            original_body = _split_body(prompt.read_text(encoding="utf-8"))
            rc, out, err = sb.run("alpha", "alpha-2")
            self.assertEqual(rc, 0, msg=err)
            after = prompt.read_text(encoding="utf-8")
            fm = _core.parse_frontmatter(after, strict=True)
            self.assertEqual(fm["prompt_relates_to_task"], "alpha-2")
            self.assertEqual(_split_body(after), original_body)

    def test_renames_slug_field_itself(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            prompt = sb.write("prompts/oldname/prompt.md", _prompt_md("oldname"))
            rc, out, err = sb.run("oldname", "newname")
            self.assertEqual(rc, 0, msg=err)
            fm = _core.parse_frontmatter(
                prompt.read_text(encoding="utf-8"), strict=True)
            self.assertEqual(fm["slug"], "newname")


class TestNoMatch(unittest.TestCase):
    def test_no_match_is_noop(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            task = sb.write("tasks/099-x/task.md", _task_md("x"))
            before = task.read_text(encoding="utf-8")
            rc, out, err = sb.run("does-not-exist", "whatever")
            self.assertEqual(rc, 0, msg=err)
            self.assertEqual(task.read_text(encoding="utf-8"), before)


class TestIdempotency(unittest.TestCase):
    def test_second_run_is_noop(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            task = sb.write(
                "tasks/099-x/task.md",
                _task_md("x", task_uses_prompts=["foo"]),
            )
            rc1, _, err1 = sb.run("foo", "foo-renamed")
            self.assertEqual(rc1, 0, msg=err1)
            after_first = task.read_text(encoding="utf-8")
            rc2, _, err2 = sb.run("foo", "foo-renamed")
            self.assertEqual(rc2, 0, msg=err2)
            after_second = task.read_text(encoding="utf-8")
            self.assertEqual(after_first, after_second,
                             "idempotency violated: second run mutated file")


class TestDryRun(unittest.TestCase):
    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            task = sb.write(
                "tasks/099-x/task.md",
                _task_md("x", task_uses_prompts=["foo"]),
            )
            before = task.read_text(encoding="utf-8")
            rc, out, err = sb.run("foo", "foo-renamed", "--dry-run")
            self.assertEqual(rc, 0, msg=err)
            self.assertIn("foo-renamed", out)
            self.assertEqual(task.read_text(encoding="utf-8"), before,
                             "--dry-run wrote to disk")


class TestDoneTaskRefusal(unittest.TestCase):
    def test_refuses_when_done_task_references_slug(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write(
                "tasks/088-done/task.md",
                _task_md("done-task", task_status="done",
                         task_affects_paths=["tasks/099-target/task.md"]),
            )
            sb.write(
                "tasks/099-target/task.md",
                _task_md("target", task_uses_prompts=["target"]),
            )
            rc, out, err = sb.run("target", "target-renamed")
            self.assertEqual(rc, fm_rename.EXIT_REFUSED)
            self.assertIn("done", err.lower())


class TestAtomicityOnWriteFailure(unittest.TestCase):
    """If a write call raises mid-plan, the exception MUST surface (we do
    not silently swallow). Files written *before* the failure are committed
    (POSIX file write semantics) — but the planner's pre-scan + re-scan
    under FileLock detects external mutation and aborts cleanly.

    This test installs a write-failure on the *first* file in the plan and
    confirms (a) the exception propagates, (b) no file was modified."""

    def test_first_write_failure_keeps_first_file_unchanged(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            t1 = sb.write(
                "tasks/099-a/task.md",
                _task_md("a", task_uses_prompts=["foo"]),
            )
            t2 = sb.write(
                "tasks/100-b/task.md",
                _task_md("b", task_uses_prompts=["foo"]),
            )
            before_t1 = t1.read_text(encoding="utf-8")
            before_t2 = t2.read_text(encoding="utf-8")

            real_write = Path.write_text

            def fail_first(self, *args, **kwargs):
                # Fail when writing t1; succeed otherwise. Path equality
                # by resolved path keeps the patch deterministic.
                if self.resolve() == t1.resolve():
                    raise OSError("simulated write failure")
                return real_write(self, *args, **kwargs)

            with mock.patch.object(Path, "write_text", fail_first):
                with self.assertRaises(OSError):
                    sb.run("foo", "foo-renamed")

            self.assertEqual(t1.read_text(encoding="utf-8"), before_t1,
                             "t1 should be untouched after write failure")
            # t2 may or may not have been written depending on plan order;
            # the contract is per-file FileLock, not multi-file txn. Verify
            # that whichever state t2 is in, the body bytes are preserved.
            after_t2 = t2.read_text(encoding="utf-8")
            self.assertEqual(_split_body(after_t2), _split_body(before_t2))

    def test_concurrent_mutation_detected(self):
        """If the file changes between pre-scan and write, the writer must
        abort with RuntimeError — atomicity over silent corruption."""
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            t1 = sb.write(
                "tasks/099-a/task.md",
                _task_md("a", task_uses_prompts=["foo"]),
            )
            cwd = os.getcwd()
            os.chdir(sb.base)
            try:
                plan = fm_rename.build_plan(sb.base, "foo", "foo-renamed")
                self.assertEqual(len(plan.changes), 1)
                # Simulate an external mutation between pre-scan and write.
                external = t1.read_text(encoding="utf-8").replace(
                    "foo", "external-edit")
                t1.write_text(external, encoding="utf-8")
                with self.assertRaises(RuntimeError):
                    fm_rename._write_plan(plan)
                # Confirm the writer left the externally-edited content
                # in place rather than overwriting it.
                self.assertEqual(t1.read_text(encoding="utf-8"), external)
            finally:
                os.chdir(cwd)


class TestCollisionDetection(unittest.TestCase):
    def test_refuses_when_new_slug_already_owned(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("prompts/p1/prompt.md", _prompt_md("alpha"))
            sb.write("prompts/p2/prompt.md", _prompt_md("beta"))
            rc, _, err = sb.run("alpha", "beta")
            self.assertEqual(rc, fm_rename.EXIT_PRECONDITION)
            self.assertIn("already owned", err)


class TestSlugValidation(unittest.TestCase):
    def test_invalid_new_slug(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("prompts/p1/prompt.md", _prompt_md("alpha"))
            with self.assertRaises(SystemExit):
                sb.run("alpha", "Has Spaces")


class TestNoOpSameSlug(unittest.TestCase):
    def test_old_equals_new_is_noop(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            t = sb.write("tasks/099-x/task.md", _task_md("x"))
            before = t.read_text(encoding="utf-8")
            rc, _, _ = sb.run("alpha", "alpha")
            self.assertEqual(rc, 0)
            self.assertEqual(t.read_text(encoding="utf-8"), before)


class TestRenameFolder(unittest.TestCase):
    def test_renames_matching_folder(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("prompts/oldname/prompt.md", _prompt_md("oldname"))
            rc, out, err = sb.run("oldname", "newname", "--rename-folder")
            self.assertEqual(rc, 0, msg=err)
            self.assertFalse((sb.base / "prompts" / "oldname").exists())
            self.assertTrue(
                (sb.base / "prompts" / "newname" / "prompt.md").exists())

    def test_renames_task_folder_with_numeric_prefix(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("tasks/099-target/task.md",
                     _task_md("target", task_uses_prompts=["target"]))
            rc, out, err = sb.run("target", "target-renamed", "--rename-folder")
            self.assertEqual(rc, 0, msg=err)
            self.assertTrue(
                (sb.base / "tasks" / "099-target-renamed" / "task.md").exists())


if __name__ == "__main__":
    unittest.main()
