"""Tests for tools/check-readme-frontmatter.py.

Covers Acceptance Criteria from prompts/tooling-readme-frontmatter-validator/brief.md:
  3. Tests cover: clean, missing-key, slug-mismatch, exempt provider folder.

The linter is ERROR-tier (FOLDERS.md F.5 promoted from SHOULD to MUST by
Task 036 ST-3). Exit 1 is the gating signal.
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
        "check_readme_frontmatter",
        TOOLS / "check-readme-frontmatter.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_readme_frontmatter"] = module
    spec.loader.exec_module(module)
    return module


crf = _load_module()


def _capture(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = crf.main(argv)
    return rc, out.getvalue(), err.getvalue()


def _readme(
    *,
    type_: str = "index",
    status: str = "active",
    slug: str = "example",
    summary: str = "A folder readme used in tests.",
    created: str = "2026-05-07",
    updated: str = "2026-05-07",
    drop_keys: tuple[str, ...] = (),
) -> str:
    keys = {
        "type": type_,
        "status": status,
        "slug": slug,
        "summary": summary,
        "created": created,
        "updated": updated,
    }
    for k in drop_keys:
        keys.pop(k, None)
    fm = "\n".join(f"{k}: {v}" for k, v in keys.items())
    return f"---\n{fm}\n---\n\n# Example\n\nbody\n"


class TestCleanReadme(unittest.TestCase):
    def test_clean_readme_with_all_l1_keys_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tasks = root / "tasks"
            slug_dir = tasks / "001-example"
            slug_dir.mkdir(parents=True)
            (slug_dir / "readme.md").write_text(_readme(slug="example"), encoding="utf-8")
            rc, out, err = _capture([str(tasks), "--repo-root", str(root)])
            self.assertEqual(rc, 0, msg=out + err)
            self.assertNotIn("ERROR", out)
            self.assertIn("0 ERROR diagnostic(s)", err)

    def test_prompts_root_clean(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prompts = root / "prompts"
            slug_dir = prompts / "my-prompt"
            slug_dir.mkdir(parents=True)
            (slug_dir / "readme.md").write_text(
                _readme(slug="my-prompt"), encoding="utf-8"
            )
            rc, _, err = _capture([str(prompts), "--repo-root", str(root)])
            self.assertEqual(rc, 0, msg=err)


class TestMissingKey(unittest.TestCase):
    def test_missing_summary_emits_MISSING_KEY(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slug_dir = root / "tasks" / "002-bad"
            slug_dir.mkdir(parents=True)
            (slug_dir / "readme.md").write_text(
                _readme(slug="bad", drop_keys=("summary",)), encoding="utf-8"
            )
            rc, out, _ = _capture([str(root / "tasks"), "--repo-root", str(root)])
            self.assertEqual(rc, 1)
            self.assertIn("F.5.MISSING-KEY", out)
            self.assertIn("summary", out)

    def test_no_frontmatter_at_all_emits_MISSING_KEY(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slug_dir = root / "tasks" / "003-empty"
            slug_dir.mkdir(parents=True)
            (slug_dir / "readme.md").write_text(
                "# No frontmatter\n", encoding="utf-8"
            )
            rc, out, _ = _capture([str(root / "tasks"), "--repo-root", str(root)])
            self.assertEqual(rc, 1)
            self.assertIn("F.5.MISSING-KEY", out)


class TestSlugMismatch(unittest.TestCase):
    def test_slug_disagrees_with_folder_emits_SLUG_MISMATCH(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slug_dir = root / "tasks" / "010-real-slug"
            slug_dir.mkdir(parents=True)
            (slug_dir / "readme.md").write_text(
                _readme(slug="totally-different"), encoding="utf-8"
            )
            rc, out, _ = _capture([str(root / "tasks"), "--repo-root", str(root)])
            self.assertEqual(rc, 1)
            self.assertIn("F.5.SLUG-MISMATCH", out)
            self.assertIn("real-slug", out)

    def test_qualified_readme_slug_passes(self) -> None:
        # Per repo convention, vault-uniqueness forces the readme slug
        # to qualify itself (e.g. `task-<NNN>-<slug>` or `<slug>-readme`).
        # Containment of the bare folder slug is sufficient.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slug_dir = root / "tasks" / "020-foo-bar"
            slug_dir.mkdir(parents=True)
            (slug_dir / "readme.md").write_text(
                _readme(slug="task-020-foo-bar"), encoding="utf-8"
            )
            rc, _, err = _capture([str(root / "tasks"), "--repo-root", str(root)])
            self.assertEqual(rc, 0, msg=err)

    def test_prompt_readme_suffix_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slug_dir = root / "prompts" / "my-prompt"
            slug_dir.mkdir(parents=True)
            (slug_dir / "readme.md").write_text(
                _readme(slug="my-prompt-readme"), encoding="utf-8"
            )
            rc, _, err = _capture([str(root / "prompts"), "--repo-root", str(root)])
            self.assertEqual(rc, 0, msg=err)

    def test_task_prefix_is_stripped_for_slug_comparison(self) -> None:
        # `tasks/042-foo/` → expected slug is `foo`, not `042-foo`.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slug_dir = root / "tasks" / "042-foo"
            slug_dir.mkdir(parents=True)
            (slug_dir / "readme.md").write_text(_readme(slug="foo"), encoding="utf-8")
            rc, _, _ = _capture([str(root / "tasks"), "--repo-root", str(root)])
            self.assertEqual(rc, 0)

    def test_prompts_slug_must_match_folder_directly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slug_dir = root / "prompts" / "my-prompt"
            slug_dir.mkdir(parents=True)
            (slug_dir / "readme.md").write_text(
                _readme(slug="other-prompt"), encoding="utf-8"
            )
            rc, out, _ = _capture([str(root / "prompts"), "--repo-root", str(root)])
            self.assertEqual(rc, 1)
            self.assertIn("F.5.SLUG-MISMATCH", out)


class TestProviderExemption(unittest.TestCase):
    def test_provider_research_folder_is_skipped(self) -> None:
        # research/gemini/<slug>/ is a provider folder and is NOT an
        # operational orchestration folder. The linter MUST NOT emit
        # diagnostics for its readmes (FOLDERS.md F.1.1 / §8 exemption).
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            provider_dir = root / "research" / "gemini"
            provider_dir.mkdir(parents=True)
            # A bare provider readme without L1 keys MUST not trip the linter.
            (provider_dir / "readme.md").write_text(
                "# Gemini provider mirror\n", encoding="utf-8"
            )
            # And per-result subdirs MUST not be walked either.
            slug_dir = provider_dir / "some-result"
            slug_dir.mkdir(parents=True)
            (slug_dir / "readme.md").write_text(
                "# Provider result, no frontmatter\n", encoding="utf-8"
            )
            rc, out, _ = _capture([str(root / "research"), "--repo-root", str(root)])
            self.assertEqual(rc, 0)
            self.assertNotIn("ERROR", out)

    def test_non_provider_research_workspace_still_checked(self) -> None:
        # research/<slug>/ that is NOT a provider sub-tree still needs L1.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slug_dir = root / "research" / "my-research"
            slug_dir.mkdir(parents=True)
            (slug_dir / "readme.md").write_text(
                "# No frontmatter\n", encoding="utf-8"
            )
            rc, out, _ = _capture([str(root / "research"), "--repo-root", str(root)])
            self.assertEqual(rc, 1)
            self.assertIn("F.5.MISSING-KEY", out)


class TestIndexReadmesIgnored(unittest.TestCase):
    def test_top_level_index_readme_not_walked(self) -> None:
        # `tasks/readme.md` is the index page; this linter only walks
        # `<root>/<slug>/readme.md`. Index readmes are owned by fm-validate.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tasks = root / "tasks"
            tasks.mkdir(parents=True)
            (tasks / "readme.md").write_text("# tasks index\n", encoding="utf-8")
            rc, out, err = _capture([str(tasks), "--repo-root", str(root)])
            self.assertEqual(rc, 0, msg=out + err)


if __name__ == "__main__":
    unittest.main()
