"""Tests for fm-section (SPEC §13)."""
from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools" / "fm"))

import section as fm_section  # type: ignore
import _core  # type: ignore


TASK_FIXTURE = """\
---
type: task
status: active
slug: section-fixture
summary: "Fixture for fm-section tests."
created: 2026-05-05
updated: 2026-05-05
task_id: "999"
task_status: open
task_owner: "test"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths: []
---

# Task — Fixture

## Goal

Demonstrate the surface.

## Plan

1. Step one.
2. Step two.

## Todo

- [ ] First item.
- [ ] Second item.
- [x] Third item.

## Links

- [/spec](../../research/example/output/SPEC.md)
"""


class _CLI(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "task.md"
        self.path.write_text(TASK_FIXTURE, encoding="utf-8")
        self._old_cwd = Path.cwd()
        # Run from repo root so classify_path can find header-ontology.
        # The fixture path lives under tmp, not the operational tree, so
        # classify_path returns expected_type=None and the schema check is
        # skipped — that's the right behaviour for unit tests.

    def _run(self, *argv: str, stdin: str = "") -> tuple[int, str, str]:
        out = io.StringIO()
        err = io.StringIO()
        old_stdin = sys.stdin
        sys.stdin = io.StringIO(stdin)
        try:
            with redirect_stdout(out), redirect_stderr(err):
                code = fm_section.main(list(argv))
        finally:
            sys.stdin = old_stdin
        return code, out.getvalue(), err.getvalue()


class TestReplace(_CLI):
    def test_replace_replaces_body_and_preserves_others(self) -> None:
        code, _, _ = self._run(str(self.path), "--replace", "Goal", "--from-stdin",
                                stdin="Replaced.\n")
        self.assertEqual(code, 0)
        new_text = self.path.read_text(encoding="utf-8")
        self.assertIn("## Goal\nReplaced.\n", new_text)
        self.assertNotIn("Demonstrate the surface.", new_text)
        self.assertIn("## Plan", new_text)
        self.assertIn("- [ ] First item.", new_text)


class TestAppendTo(_CLI):
    def test_append_to_appends_paragraph(self) -> None:
        code, _, err = self._run(str(self.path), "--append-to", "Goal",
                                  "--text", "More context.")
        self.assertEqual(code, 0, err)
        new_text = self.path.read_text(encoding="utf-8")
        self.assertIn("Demonstrate the surface.", new_text)
        self.assertIn("More context.", new_text)

    def test_append_to_three_times_no_drift(self) -> None:
        for _ in range(3):
            code, _, _ = self._run(str(self.path), "--append-to", "Goal",
                                    "--text", "More.")
            self.assertEqual(code, 0)
        new_text = self.path.read_text(encoding="utf-8")
        # F.6.5 analogue: bytes outside the section unchanged.
        # Here we check the link survived intact.
        self.assertIn("[/spec](../../research/example/output/SPEC.md)", new_text)


class TestAppendListItem(_CLI):
    def test_append_list_item_to_ordered(self) -> None:
        code, _, _ = self._run(str(self.path), "--append-list-item", "Plan",
                                "Step three.")
        self.assertEqual(code, 0)
        new_text = self.path.read_text(encoding="utf-8")
        self.assertIn("3. Step three.", new_text)

    def test_append_list_item_to_task_list(self) -> None:
        code, _, _ = self._run(str(self.path), "--append-list-item", "Todo",
                                "[ ] Fourth item.")
        self.assertEqual(code, 0)
        new_text = self.path.read_text(encoding="utf-8")
        self.assertIn("- [ ] First item.", new_text)
        self.assertIn("Fourth item.", new_text)


class TestCheckTask(_CLI):
    def test_check_task_marks_first_match(self) -> None:
        code, _, _ = self._run(str(self.path), "--check-task", "Todo", "First")
        self.assertEqual(code, 0)
        new_text = self.path.read_text(encoding="utf-8")
        self.assertIn("- [x] First item.", new_text)
        self.assertIn("- [ ] Second item.", new_text)
        self.assertIn("- [x] Third item.", new_text)

    def test_check_task_no_match_exits_3(self) -> None:
        code, _, _ = self._run(str(self.path), "--check-task", "Todo", "ZZZZ")
        self.assertEqual(code, 3)


class TestInsert(_CLI):
    def test_insert_after_creates_new_section(self) -> None:
        code, _, _ = self._run(str(self.path), "--insert-after", "Plan",
                                "--new-heading", "Risks", "--from-stdin",
                                stdin="None today.\n")
        self.assertEqual(code, 0)
        new_text = self.path.read_text(encoding="utf-8")
        # Risks section appears between Plan and Todo.
        self.assertLess(new_text.index("## Plan"), new_text.index("## Risks"))
        self.assertLess(new_text.index("## Risks"), new_text.index("## Todo"))

    def test_insert_before_creates_new_section(self) -> None:
        code, _, _ = self._run(str(self.path), "--insert-before", "Links",
                                "--new-heading", "Notes", "--from-stdin",
                                stdin="See README.\n")
        self.assertEqual(code, 0)
        new_text = self.path.read_text(encoding="utf-8")
        self.assertLess(new_text.index("## Notes"), new_text.index("## Links"))


class TestDelete(_CLI):
    def test_delete_removes_section(self) -> None:
        code, _, _ = self._run(str(self.path), "--delete", "Todo")
        self.assertEqual(code, 0)
        new_text = self.path.read_text(encoding="utf-8")
        self.assertNotIn("## Todo", new_text)
        self.assertIn("## Plan", new_text)
        self.assertIn("## Links", new_text)


class TestRename(_CLI):
    def test_rename_changes_heading_text(self) -> None:
        code, _, _ = self._run(str(self.path), "--rename", "Goal", "Objective")
        self.assertEqual(code, 0)
        new_text = self.path.read_text(encoding="utf-8")
        self.assertIn("## Objective", new_text)
        self.assertNotIn("## Goal", new_text)
        # Body bytes preserved.
        self.assertIn("Demonstrate the surface.", new_text)


class TestAddressing(_CLI):
    def test_ambiguous_address_exits_5(self) -> None:
        # Inject a duplicate heading.
        text = self.path.read_text(encoding="utf-8")
        text += "\n## Goal\n\nDuplicate.\n"
        self.path.write_text(text, encoding="utf-8")
        code, _, err = self._run(str(self.path), "--append-to", "Goal",
                                  "--text", "X")
        self.assertEqual(code, 5)
        self.assertIn("ambiguous", err)

    def test_nth_resolves_duplicate(self) -> None:
        text = self.path.read_text(encoding="utf-8")
        text += "\n## Goal\n\nDuplicate.\n"
        self.path.write_text(text, encoding="utf-8")
        code, _, _ = self._run(str(self.path), "--append-to", "Goal",
                                "--text", "Added to second.", "--nth", "2")
        self.assertEqual(code, 0)
        new_text = self.path.read_text(encoding="utf-8")
        self.assertIn("Demonstrate the surface.", new_text)
        self.assertIn("Added to second.", new_text)

    def test_anchor_resolves_duplicate(self) -> None:
        text = self.path.read_text(encoding="utf-8")
        text += "\n<!-- anchor: alt-goal -->\n## Goal\n\nDuplicate.\n"
        self.path.write_text(text, encoding="utf-8")
        code, _, _ = self._run(str(self.path), "--append-to", "Goal",
                                "--text", "Anchor-addressed.",
                                "--anchor", "alt-goal")
        self.assertEqual(code, 0)
        new_text = self.path.read_text(encoding="utf-8")
        self.assertIn("Anchor-addressed.", new_text)


class TestNotFound(_CLI):
    def test_missing_heading_exits_3(self) -> None:
        code, _, err = self._run(str(self.path), "--delete", "Nonexistent")
        self.assertEqual(code, 3)
        self.assertIn("not found", err)


class TestByteInvariant(_CLI):
    def test_frontmatter_byte_identical_after_op(self) -> None:
        before = self.path.read_text(encoding="utf-8")
        fm_block, _ = before.split("---\n", 2)[0], before
        fm_end = before.index("---\n", 4) + len("---\n")
        original_fm = before[:fm_end]
        code, _, _ = self._run(str(self.path), "--append-to", "Goal",
                                "--text", "X.")
        self.assertEqual(code, 0)
        after = self.path.read_text(encoding="utf-8")
        self.assertEqual(after[:fm_end], original_fm)

    def test_other_sections_byte_identical(self) -> None:
        before = self.path.read_text(encoding="utf-8")
        plan_block = before[before.index("## Plan"): before.index("## Todo")]
        code, _, _ = self._run(str(self.path), "--append-to", "Goal",
                                "--text", "X.")
        self.assertEqual(code, 0)
        after = self.path.read_text(encoding="utf-8")
        self.assertIn(plan_block, after)


class TestSpans(unittest.TestCase):
    def test_anchor_above_heading_is_captured(self) -> None:
        text = """---\nx: 1\n---\n\n<!-- anchor: my-id -->\n## Foo\n\nBody.\n"""
        spans = _core.find_section_spans(text, "Foo")
        self.assertEqual(len(spans), 1)
        self.assertEqual(spans[0].anchor_id, "my-id")


class TestRenameTierGuard(unittest.TestCase):
    """SPEC §13.2: --rename refuses when other operational files reference the heading."""

    def test_rename_refuses_with_external_anchor_link(self) -> None:
        # Create two operational files: target task.md and an external prompt.md
        # that links to target's heading.
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            (td_path / "tasks" / "999-fixture").mkdir(parents=True)
            target = td_path / "tasks" / "999-fixture" / "task.md"
            target.write_text(TASK_FIXTURE, encoding="utf-8")
            (td_path / "prompts" / "fixture-prompt").mkdir(parents=True)
            ref = td_path / "prompts" / "fixture-prompt" / "prompt.md"
            ref.write_text(
                "---\ntype: prompt\nstatus: active\nslug: fixture-prompt\n"
                'summary: "x"\ncreated: 2026-05-05\nupdated: 2026-05-05\n'
                "prompt_kind: x\nprompt_framework: x\nprompt_target_agent: x\n---\n\n"
                "See [Goal](../../tasks/999-fixture/task.md#goal) for context.\n",
                encoding="utf-8",
            )
            old_cwd = Path.cwd()
            try:
                import os
                os.chdir(td)
                code = fm_section.main([
                    str(target.relative_to(td_path)),
                    "--rename", "Goal", "Objective",
                ])
            finally:
                import os
                os.chdir(old_cwd)
            self.assertEqual(code, 6)


if __name__ == "__main__":
    unittest.main()
