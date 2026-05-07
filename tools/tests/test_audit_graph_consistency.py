"""Tests for tools/check-audit-graph-consistency.py.

Covers Acceptance Criteria from prompts/tooling-audit-graph-consistency-checker/brief.md:
  4. Tests cover: link+frontmatter both present (pass), link only (warn),
     frontmatter only (no warn — body links are encouraged but not required).

The linter is WARN-tier (FOLDERS.md F.6, advisory). Exit 2 is the WARN signal.
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
        "check_audit_graph_consistency",
        TOOLS / "check-audit-graph-consistency.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_audit_graph_consistency"] = module
    spec.loader.exec_module(module)
    return module


cag = _load_module()


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = cag.main(argv)
    return rc, out.getvalue(), err.getvalue()


def _yaml_list(items: list[str]) -> str:
    if not items:
        return " []"
    return "\n" + "\n".join(f"  - {x}" for x in items)


def _task_md(*, slug: str, uses_prompts: list[str], body: str) -> str:
    fm = (
        "---\n"
        "type: task\n"
        "status: active\n"
        f"slug: {slug}\n"
        "summary: \"x\"\n"
        "created: 2026-05-07\n"
        "updated: 2026-05-07\n"
        f"task_id: \"{slug.split('-')[0] if slug[0].isdigit() else '999'}\"\n"
        "task_status: open\n"
        "task_owner: \"x\"\n"
        "task_priority: P3\n"
        f"task_uses_prompts:{_yaml_list(uses_prompts)}\n"
        "task_spawns_research: []\n"
        "task_spawns_prompts: []\n"
        "task_affects_paths: []\n"
        "---\n"
    )
    return fm + "\n# Task\n\n" + body + "\n"


def _prompt_md(slug: str = "p", body: str = "") -> str:
    return (
        "---\n"
        "type: prompt\n"
        "status: active\n"
        f"slug: {slug}\n"
        "summary: \"x\"\n"
        "created: 2026-05-07\n"
        "updated: 2026-05-07\n"
        "prompt_kind: task-spec\n"
        "prompt_framework: RISEN+ReAct\n"
        "prompt_target_agent: \"Claude Code\"\n"
        "---\n"
        "\n# P\n\n" + body + "\n"
    )


def _scaffold_repo(tmp: Path) -> Path:
    (tmp / "tasks").mkdir()
    (tmp / "prompts").mkdir()
    (tmp / "research").mkdir()
    return tmp


class TestLinkPlusFrontmatterPasses(unittest.TestCase):
    def test_body_link_to_prompt_with_matching_task_uses_prompts_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _scaffold_repo(Path(tmp))
            task_dir = root / "tasks" / "001-example"
            task_dir.mkdir()
            prompt_dir = root / "prompts" / "my-prompt"
            prompt_dir.mkdir()
            (prompt_dir / "prompt.md").write_text(_prompt_md("my-prompt"), encoding="utf-8")
            (task_dir / "task.md").write_text(
                _task_md(
                    slug="001-example",
                    uses_prompts=["my-prompt"],
                    body="See [the prompt](../../prompts/my-prompt/prompt.md).",
                ),
                encoding="utf-8",
            )
            rc, out, err = _capture([str(root / "tasks"), "--repo-root", str(root)])
            self.assertEqual(rc, 0, msg=out + err)
            self.assertNotIn("WARN", out)


class TestLinkOnlyWarns(unittest.TestCase):
    def test_body_link_without_frontmatter_emits_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _scaffold_repo(Path(tmp))
            task_dir = root / "tasks" / "002-orphan"
            task_dir.mkdir()
            prompt_dir = root / "prompts" / "orphan-prompt"
            prompt_dir.mkdir()
            (prompt_dir / "prompt.md").write_text(
                _prompt_md("orphan-prompt"), encoding="utf-8"
            )
            (task_dir / "task.md").write_text(
                _task_md(
                    slug="002-orphan",
                    uses_prompts=[],  # FRONTMATTER MISSING
                    body="Discusses [the orphan prompt](../../prompts/orphan-prompt/prompt.md).",
                ),
                encoding="utf-8",
            )
            rc, out, err = _capture(
                [str(root / "tasks"), str(root / "prompts"), "--repo-root", str(root)]
            )
            self.assertEqual(rc, 2, msg=out + err)
            self.assertIn("F.6", out)
            self.assertIn("orphan-prompt", out)
            self.assertIn("body-link-without-frontmatter", out)


class TestFrontmatterOnlyDoesNotWarn(unittest.TestCase):
    def test_frontmatter_present_body_silent_passes(self) -> None:
        # Per F.6: body links are encouraged, not required. The inverse
        # asymmetry (frontmatter present, body silent) MUST NOT warn.
        with tempfile.TemporaryDirectory() as tmp:
            root = _scaffold_repo(Path(tmp))
            task_dir = root / "tasks" / "003-silent"
            task_dir.mkdir()
            prompt_dir = root / "prompts" / "silent-prompt"
            prompt_dir.mkdir()
            (prompt_dir / "prompt.md").write_text(
                _prompt_md("silent-prompt"), encoding="utf-8"
            )
            (task_dir / "task.md").write_text(
                _task_md(
                    slug="003-silent",
                    uses_prompts=["silent-prompt"],
                    body="No body links to the prompt at all.",
                ),
                encoding="utf-8",
            )
            rc, out, err = _capture(
                [str(root / "tasks"), str(root / "prompts"), "--repo-root", str(root)]
            )
            self.assertEqual(rc, 0, msg=out + err)


class TestProviderResearchSkipped(unittest.TestCase):
    def test_link_to_research_provider_subtree_does_not_warn(self) -> None:
        # research/gemini/<slug>/result.md is an external mirror; it is
        # NOT in the audit graph (RESEARCH.md §6 / FOLDERS.md §8).
        with tempfile.TemporaryDirectory() as tmp:
            root = _scaffold_repo(Path(tmp))
            task_dir = root / "tasks" / "004-cite-gemini"
            task_dir.mkdir()
            (root / "research" / "gemini").mkdir(parents=True)
            (root / "research" / "gemini" / "some-result").mkdir()
            (root / "research" / "gemini" / "some-result" / "result.md").write_text(
                "# external\n", encoding="utf-8"
            )
            (task_dir / "task.md").write_text(
                _task_md(
                    slug="004-cite-gemini",
                    uses_prompts=[],
                    body="See [Gemini result](../../research/gemini/some-result/result.md).",
                ),
                encoding="utf-8",
            )
            rc, out, err = _capture(
                [str(root / "tasks"), "--repo-root", str(root)]
            )
            self.assertEqual(rc, 0, msg=out + err)


class TestExternalLinksIgnored(unittest.TestCase):
    def test_http_link_does_not_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _scaffold_repo(Path(tmp))
            task_dir = root / "tasks" / "005-external"
            task_dir.mkdir()
            (task_dir / "task.md").write_text(
                _task_md(
                    slug="005-external",
                    uses_prompts=[],
                    body="See [GitHub](https://github.com/x).",
                ),
                encoding="utf-8",
            )
            rc, out, err = _capture(
                [str(root / "tasks"), "--repo-root", str(root)]
            )
            self.assertEqual(rc, 0, msg=out + err)

    def test_anchor_link_does_not_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _scaffold_repo(Path(tmp))
            task_dir = root / "tasks" / "006-anchor"
            task_dir.mkdir()
            (task_dir / "task.md").write_text(
                _task_md(
                    slug="006-anchor",
                    uses_prompts=[],
                    body="See [section](#goal).",
                ),
                encoding="utf-8",
            )
            rc, _, _ = _capture(
                [str(root / "tasks"), "--repo-root", str(root)]
            )
            self.assertEqual(rc, 0)


class TestPromptToTask(unittest.TestCase):
    def test_prompt_links_to_task_without_prompt_relates_to_task_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _scaffold_repo(Path(tmp))
            task_dir = root / "tasks" / "007-target"
            task_dir.mkdir()
            (task_dir / "task.md").write_text(
                _task_md(slug="007-target", uses_prompts=[], body=""),
                encoding="utf-8",
            )
            prompt_dir = root / "prompts" / "linker"
            prompt_dir.mkdir()
            # Use the prompt body to link to the task without setting
            # `prompt_relates_to_task`.
            prompt_md = (
                "---\n"
                "type: prompt\n"
                "status: active\n"
                "slug: linker\n"
                "summary: \"x\"\n"
                "created: 2026-05-07\n"
                "updated: 2026-05-07\n"
                "prompt_kind: task-spec\n"
                "prompt_framework: RISEN+ReAct\n"
                "prompt_target_agent: \"Claude Code\"\n"
                "---\n"
                "\n# Linker\n\n"
                "See [target](../../tasks/007-target/task.md).\n"
            )
            (prompt_dir / "prompt.md").write_text(prompt_md, encoding="utf-8")
            rc, out, err = _capture(
                [str(root / "tasks"), str(root / "prompts"), "--repo-root", str(root)]
            )
            self.assertEqual(rc, 2, msg=out + err)
            self.assertIn("prompt_relates_to_task", out)
            self.assertIn("target", out)


class TestSelfReference(unittest.TestCase):
    def test_link_to_own_subfolder_does_not_warn(self) -> None:
        # A task linking `[subtasks](./subtasks/)` is structural, not an
        # audit-graph edge to a sibling task.
        with tempfile.TemporaryDirectory() as tmp:
            root = _scaffold_repo(Path(tmp))
            task_dir = root / "tasks" / "008-self"
            task_dir.mkdir()
            (task_dir / "subtasks").mkdir()
            (task_dir / "task.md").write_text(
                _task_md(
                    slug="008-self",
                    uses_prompts=[],
                    body="See [subtasks](./subtasks/readme.md).",
                ),
                encoding="utf-8",
            )
            rc, _, err = _capture(
                [str(root / "tasks"), "--repo-root", str(root)]
            )
            self.assertEqual(rc, 0, msg=err)


if __name__ == "__main__":
    unittest.main()
