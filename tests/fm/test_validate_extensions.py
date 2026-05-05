"""Tests for fm-validate --explain / --baseline / --type-check (Task 019 ST-5)."""
from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools" / "fm"))

import _core  # type: ignore
import validate as fm_validate  # type: ignore


_ONTOLOGY = json.loads(
    (REPO_ROOT / "maintenance" / "schemas" / "header-ontology.json").read_text(encoding="utf-8")
)


class _Scratch(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "AGENTS.md").write_text("# scratch\n", encoding="utf-8")
        (self.root / "tasks").mkdir()
        (self.root / "prompts").mkdir()
        (self.root / "research").mkdir()
        # Mirror the ontology + explanations into the scratch repo so
        # _load_explanations and load_ontology resolve.
        (self.root / "maintenance" / "schemas").mkdir(parents=True)
        for f in ("header-ontology.json", "diagnostic-explanations.json"):
            (self.root / "maintenance" / "schemas" / f).write_text(
                (REPO_ROOT / "maintenance" / "schemas" / f).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        self._old = Path.cwd()
        os.chdir(self.root)
        self.addCleanup(lambda: os.chdir(self._old))

    def _write_task(self, num: str, slug: str, *,
                    uses_prompts: list[str] | None = None,
                    blocked_by: list[str] | None = None) -> Path:
        d = self.root / "tasks" / f"{num}-{slug}"
        d.mkdir(parents=True)
        uses = "\n".join(f"  - {u}" for u in (uses_prompts or [])) or "[]"
        if uses != "[]":
            uses = "\n" + uses
        blocked = "\n".join(f"  - {b}" for b in (blocked_by or []))
        body = (
            "---\n"
            "type: task\n"
            "status: active\n"
            f"slug: {slug}\n"
            f'summary: "x"\n'
            "created: 2026-05-05\n"
            "updated: 2026-05-05\n"
            f'task_id: "{num}"\n'
            "task_status: open\n"
            'task_owner: "test"\n'
            "task_priority: P3\n"
            f"task_uses_prompts: {uses}\n"
            "task_spawns_research: []\n"
            "task_spawns_prompts: []\n"
            "task_affects_paths: []\n"
        )
        if blocked:
            body += f"task_blocked_by:\n{blocked}\n"
        body += "---\n\n# T\n\n## Goal\n\nx.\n\n## Plan\n\n1. x.\n\n## Todo\n\n- [ ] 1. x.\n\n## Links\n\n- [/x](../x)\n"
        (d / "task.md").write_text(body, encoding="utf-8")
        return d / "task.md"

    def _write_prompt(self, slug: str, *, relates_to_task: str = "") -> Path:
        d = self.root / "prompts" / slug
        d.mkdir(parents=True)
        body = (
            "---\n"
            "type: prompt\n"
            "status: active\n"
            f"slug: {slug}\n"
            'summary: "x"\n'
            "created: 2026-05-05\n"
            "updated: 2026-05-05\n"
            "prompt_kind: task-spec\n"
            "prompt_framework: RISEN\n"
            'prompt_target_agent: "any"\n'
            f'prompt_relates_to_task: "{relates_to_task}"\n'
            "---\n\n# P\n"
        )
        (d / "prompt.md").write_text(body, encoding="utf-8")
        return d / "prompt.md"


class TestTypeCheckDangling(_Scratch):
    def test_dangling_task_uses_prompts_emits_FT1(self) -> None:
        self._write_task("000", "alpha", uses_prompts=["nonexistent-prompt"])
        diags = fm_validate.type_check(self.root, _ONTOLOGY)
        codes = {d.code for d in diags}
        self.assertIn("F.T.1", codes)

    def test_dangling_blocked_by_task_id_emits_FT1(self) -> None:
        self._write_task("000", "alpha", blocked_by=["999"])
        diags = fm_validate.type_check(self.root, _ONTOLOGY)
        self.assertTrue(any(d.code == "F.T.1" and "999" in d.message for d in diags))


class TestTypeCheckReciprocity(_Scratch):
    def test_one_way_link_emits_FT2(self) -> None:
        # Task names beta; prompt names a *different* task → genuine
        # reciprocity break (not shared/general).
        self._write_task("000", "alpha", uses_prompts=["beta"])
        self._write_task("001", "gamma")
        self._write_prompt("beta", relates_to_task="gamma")
        diags = fm_validate.type_check(self.root, _ONTOLOGY)
        codes = {d.code for d in diags}
        self.assertIn("F.T.2", codes)

    def test_empty_back_edge_is_shared_general(self) -> None:
        # Empty `prompt_relates_to_task` means the prompt is shared across
        # multiple tasks; reciprocity check is skipped.
        self._write_task("000", "alpha", uses_prompts=["beta"])
        self._write_prompt("beta", relates_to_task="")
        diags = fm_validate.type_check(self.root, _ONTOLOGY)
        codes = {d.code for d in diags}
        self.assertNotIn("F.T.2", codes)

    def test_reciprocal_pair_is_clean(self) -> None:
        self._write_task("000", "alpha", uses_prompts=["beta"])
        self._write_prompt("beta", relates_to_task="alpha")
        diags = fm_validate.type_check(self.root, _ONTOLOGY)
        codes = {d.code for d in diags}
        self.assertNotIn("F.T.2", codes)


class TestExplain(_Scratch):
    def test_explain_loads_each_required_code(self) -> None:
        explanations = fm_validate._load_explanations(self.root)
        codes = explanations.get("codes", {})
        for required in ("F.3.1", "F.3.2", "F.3.3", "F.3.4", "F.4.2", "F.T.1", "F.T.2"):
            self.assertIn(required, codes, f"missing explanation for {required}")
            entry = codes[required]
            for k in ("severity_hint", "what", "why", "fix"):
                self.assertIn(k, entry, f"{required} missing field {k}")

    def test_annotate_appends_trailer(self) -> None:
        explanations = fm_validate._load_explanations(self.root)
        d = _core.Diagnostic(
            path="x.md", line=None, severity="ERROR",
            code="F.3.1", message="missing L1 keys ['type']",
        )
        annotated = fm_validate._annotate(d, explanations)
        self.assertIn("what:", annotated)
        self.assertIn("why:", annotated)
        self.assertIn("fix:", annotated)


class TestBaseline(_Scratch):
    """Smoke-tests the baseline path without spinning up a git repo.

    The git-show invocation returns non-zero for missing refs, which we
    tolerate; verify the path-iteration scaffolding doesn't error.
    """

    def test_missing_baseline_ref_returns_empty_set(self) -> None:
        # We're in a non-git tmpdir; git show should fail and we should get [].
        result = fm_validate._diags_for_baseline(
            "nonexistent-ref",
            [self.root / "AGENTS.md"],
            self.root,
            _ONTOLOGY,
            check_body=False,
        )
        self.assertEqual(result, set())


if __name__ == "__main__":
    unittest.main()
