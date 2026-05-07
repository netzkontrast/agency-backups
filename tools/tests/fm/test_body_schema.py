"""Tests for SPEC §12 body-data schema (fm-validate --check-body) and the
fm-extract reading extensions from §13.3 + §14.1."""
from __future__ import annotations

import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "tools" / "fm"))

import _core  # noqa: E402
import validate as fm_validate  # noqa: E402
import extract as fm_extract  # noqa: E402


class _Sandbox:
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

    def run(self, *argv: str) -> tuple[int, str]:
        cwd = os.getcwd()
        os.chdir(self.base)
        out, err = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                rc = fm_validate.main(list(argv))
        finally:
            os.chdir(cwd)
        return rc, err.getvalue() + out.getvalue()


# ---- Shape detection -------------------------------------------------------

class TestDetectShape(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(_core.detect_shape("This is one paragraph of prose."),
                         "paragraph")

    def test_two_paragraphs_still_paragraph(self):
        text = "First paragraph.\n\nSecond paragraph here.\n"
        self.assertEqual(_core.detect_shape(text), "paragraph")

    def test_ordered_list(self):
        text = "1. First\n2. Second\n3. Third\n"
        self.assertEqual(_core.detect_shape(text), "ordered_list")

    def test_unordered_list(self):
        text = "- foo\n- bar\n- baz\n"
        self.assertEqual(_core.detect_shape(text), "unordered_list")

    def test_task_list(self):
        text = "- [ ] do thing\n- [x] done thing\n"
        self.assertEqual(_core.detect_shape(text), "task_list")

    def test_link_list(self):
        text = ("- [Goal](./goal.md)\n"
                "- [Plan](../plan.md)\n")
        self.assertEqual(_core.detect_shape(text), "link_list")

    def test_gherkin_block(self):
        text = "```gherkin\nFeature: x\n  Scenario: y\n```\n"
        self.assertEqual(_core.detect_shape(text), "gherkin_block")

    def test_mixed_when_partial_list(self):
        # First line is prose, rest is list → mixed.
        text = "Some intro.\n- a\n- b\n"
        self.assertEqual(_core.detect_shape(text), "mixed")

    def test_empty_is_mixed(self):
        self.assertEqual(_core.detect_shape(""), "mixed")
        self.assertEqual(_core.detect_shape("   \n  \n"), "mixed")


# ---- Body validation -------------------------------------------------------

def _good_task_body(plan_items: int = 1, todo_items: int = 1) -> str:
    plan = "\n".join(f"{i}. step {i}" for i in range(1, plan_items + 1))
    todo = "\n".join(f"- [ ] item {i}" for i in range(1, todo_items + 1))
    return f"""## Goal
This is a goal paragraph long enough to satisfy min_chars.

## Plan
{plan}

## Todo
{todo}

## Links
- [foo](./foo.md)
- [bar](../bar.md)
"""


def _good_task(slug: str = "x", body: str | None = None) -> str:
    fm = f"""---
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

"""
    return fm + (body if body is not None else _good_task_body())


class TestCheckBodyOptIn(unittest.TestCase):
    def test_default_off_clean_pass(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("tasks/099-x/task.md", _good_task())
            rc, _ = sb.run()
            self.assertEqual(rc, 0)

    def test_check_body_clean_pass(self):
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("tasks/099-x/task.md", _good_task())
            rc, out = sb.run("--check-body")
            self.assertEqual(rc, 0, msg=out)


class TestShapeMismatch(unittest.TestCase):
    """SPEC §12 F.B.1."""

    def test_F_B_1_plan_paragraph_instead_of_list(self):
        body = ("## Goal\nThis is a perfectly long goal paragraph for tests.\n"
                "\n## Plan\nNot a list — just prose.\n"
                "\n## Todo\n- [ ] x\n"
                "\n## Links\n- [a](./a.md)\n")
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("tasks/099-x/task.md", _good_task(body=body))
            rc, out = sb.run("--check-body")
            self.assertEqual(rc, 1)
            self.assertIn("F.B.1", out)
            self.assertIn("Plan", out)
            self.assertIn("ordered_list", out)


class TestMinItems(unittest.TestCase):
    """SPEC §12 F.B.2."""

    def test_F_B_2_empty_plan(self):
        body = ("## Goal\nThis is a perfectly long goal paragraph for tests.\n"
                "\n## Plan\n\n## Todo\n- [ ] x\n"
                "\n## Links\n- [a](./a.md)\n")
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("tasks/099-x/task.md", _good_task(body=body))
            rc, out = sb.run("--check-body")
            # An empty Plan section detects shape='mixed' → F.B.1, not F.B.2.
            # Either diagnostic is acceptable for "Plan is broken".
            self.assertEqual(rc, 1)
            self.assertTrue("F.B.1" in out or "F.B.2" in out, msg=out)


class TestLinkPattern(unittest.TestCase):
    """SPEC §12 F.B.6."""

    def test_F_B_6_external_link_rejected(self):
        body = _good_task_body().replace(
            "- [foo](./foo.md)\n", "- [foo](https://example.com)\n",
        )
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("tasks/099-x/task.md", _good_task(body=body))
            rc, out = sb.run("--check-body")
            self.assertEqual(rc, 1)
            self.assertIn("F.B.6", out)


class TestPromptItemPatternWarn(unittest.TestCase):
    """SPEC §12 F.B.3 with item_pattern_severity=WARN."""

    def test_F_B_3_warn_only(self):
        prompt_text = """---
type: prompt
status: active
slug: y
summary: "p"
created: 2026-05-05
updated: 2026-05-05
prompt_kind: tool-instruction
prompt_framework: RISEN
prompt_target_agent: any
---

## Framework
f

## R — Role
The role is to do a thing thoughtfully and well.

## I — Input
- one input

## S — Steps
1. first step
2. second step
3. third step

## E — Expectations
- one expectation

## Constraints
- this constraint has no normative keyword
"""
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("prompts/y/prompt.md", prompt_text)
            rc, out = sb.run("--check-body")
            self.assertEqual(rc, 0, msg=out)
            self.assertIn("F.B.3", out)  # WARN still emitted, not gating
            # Promote to ERROR via --strict.
            rc2, out2 = sb.run("--check-body", "--strict")
            self.assertEqual(rc2, 1)
            self.assertIn("F.B.3", out2)


class TestTodoCompletionWarn(unittest.TestCase):
    """SPEC §12 F.B.7: all-checked Todo + status != done → WARN."""

    def test_F_B_7_disagreement(self):
        body = ("## Goal\nThis is a perfectly long goal paragraph for tests.\n"
                "\n## Plan\n1. step one\n"
                "\n## Todo\n- [x] one\n- [x] two\n"
                "\n## Links\n- [a](./a.md)\n")
        with tempfile.TemporaryDirectory() as td:
            sb = _Sandbox(Path(td))
            sb.write("tasks/099-x/task.md", _good_task(body=body))
            rc, out = sb.run("--check-body")
            self.assertEqual(rc, 0, msg=out)  # WARN doesn't gate
            self.assertIn("F.B.7", out)


# ---- fm-extract reading extensions -----------------------------------------

def _capture_extract(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = fm_extract.main(argv)
    return rc, out.getvalue(), err.getvalue()


class TestExtractBodyToc(unittest.TestCase):
    def _write(self, content: str) -> Path:
        f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        f.write(content)
        f.close()
        return Path(f.name)

    def test_body_strips_frontmatter(self):
        path = self._write("---\nx: 1\n---\n\n# H1\n\n## Foo\nbody here\n")
        try:
            rc, out, _ = _capture_extract([str(path), "--body"])
            self.assertEqual(rc, 0)
            self.assertNotIn("x: 1", out)
            self.assertIn("body here", out)
        finally:
            path.unlink()

    def test_toc_lists_h2_only(self):
        path = self._write("---\nx: 1\n---\n\n# Title\n\n## Foo\nb\n## Bar\nb\n### Baz\n")
        try:
            rc, out, _ = _capture_extract([str(path), "--toc"])
            self.assertEqual(rc, 0)
            self.assertIn("Foo", out)
            self.assertIn("Bar", out)
            self.assertNotIn("Baz", out)
            self.assertNotIn("Title", out)
        finally:
            path.unlink()


class TestExtractSectionNthAndAll(unittest.TestCase):
    def _write(self, content: str) -> Path:
        f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        f.write(content)
        f.close()
        return Path(f.name)

    def test_nth_picks_second(self):
        text = ("---\nx: 1\n---\n\n## Notes\nfirst notes\n"
                "## Other\n\n## Notes\nsecond notes\n")
        path = self._write(text)
        try:
            rc, out, _ = _capture_extract([str(path), "--section", "Notes",
                                            "--nth", "2"])
            self.assertEqual(rc, 0)
            self.assertIn("second notes", out)
            self.assertNotIn("first notes", out)
        finally:
            path.unlink()

    def test_all_emits_form_feed_separated(self):
        text = ("---\nx: 1\n---\n\n## Notes\nfirst\n## Other\n\n## Notes\nsecond\n")
        path = self._write(text)
        try:
            rc, out, _ = _capture_extract([str(path), "--section", "Notes", "--all"])
            self.assertEqual(rc, 0)
            self.assertIn("\f", out)
            self.assertIn("first", out)
            self.assertIn("second", out)
        finally:
            path.unlink()

    def test_nth_out_of_range_returns_3(self):
        text = "---\nx: 1\n---\n\n## Notes\nonly\n"
        path = self._write(text)
        try:
            rc, _, err = _capture_extract([str(path), "--section", "Notes",
                                            "--nth", "5"])
            self.assertEqual(rc, 3)
            self.assertIn("not found", err)
        finally:
            path.unlink()


class TestExtractSectionsBatch(unittest.TestCase):
    def _write(self, content: str) -> Path:
        f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        f.write(content)
        f.close()
        return Path(f.name)

    def test_batch_read_form_feed_separated(self):
        text = "---\nx: 1\n---\n\n## A\nalpha\n## B\nbeta\n## C\ngamma\n"
        path = self._write(text)
        try:
            rc, out, _ = _capture_extract([str(path), "--sections", "A,B,C"])
            self.assertEqual(rc, 0)
            parts = out.split("\f")
            self.assertEqual(len(parts), 3)
            self.assertIn("alpha", parts[0])
            self.assertIn("beta", parts[1])
            self.assertIn("gamma", parts[2])
        finally:
            path.unlink()

    def test_batch_missing_section_returns_3(self):
        text = "---\nx: 1\n---\n\n## A\nalpha\n"
        path = self._write(text)
        try:
            rc, _, err = _capture_extract([str(path), "--sections", "A,Missing"])
            self.assertEqual(rc, 3)
            self.assertIn("not found", err)
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
