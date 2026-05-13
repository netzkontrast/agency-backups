"""Tests for the Task 094 ST-3 event-driven hooks.

Each hook module under `tools/hooks/_<event>.py` is imported via a
spec-loader so the test harness shares the runtime path the live `.sh`
shim uses (`exec python3 _<event>.py`). Fixtures live in
`tools/tests/fixtures/hooks/<event>.json` per the subtask spec.

Coverage per AC `T094.3.1`:

  * Every hook exits 0 on its happy-path fixture.
  * Stop hook exits 2 when the active Task's friction-log lacks a
    parseable FL declaration.
  * PreToolUse hook exits 2 when the Skill slug is missing from
    `<repo>/skills/`.

Coverage per AC `T094.3.2` / `T094.3.3` (check-hooks.py):

  * Clean repo: exit 0.
  * Orphan script: H.1.1 emitted, exit 1.
  * Orphan registration: H.1.2 emitted, exit 1.
  * SessionStart violation: H.1.3 emitted, exit 1.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import sys
import textwrap
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

REPO = Path(__file__).resolve().parents[2]
HOOKS = REPO / "tools" / "hooks"
FIXTURES = REPO / "tools" / "tests" / "fixtures" / "hooks"


def _load(module_name: str, source: Path):
    """Import a Python module from a file path under a unique module name."""
    spec = importlib.util.spec_from_file_location(module_name, source)
    assert spec is not None and spec.loader is not None, f"cannot load {source}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


# Make tools/hooks/ importable so `_common` is resolvable from the
# per-event modules' `from _common import ...` lines.
if str(HOOKS) not in sys.path:
    sys.path.insert(0, str(HOOKS))

ups = _load("hook_user_prompt_submit", HOOKS / "_user_prompt_submit.py")
pre = _load("hook_pre_tool_use", HOOKS / "_pre_tool_use.py")
post = _load("hook_post_tool_use", HOOKS / "_post_tool_use.py")
stop_mod = _load("hook_stop", HOOKS / "_stop.py")
subagent = _load("hook_subagent_stop", HOOKS / "_subagent_stop.py")
common = _load("hook_common", HOOKS / "_common.py")

check_hooks = _load("check_hooks", REPO / "tools" / "check-hooks.py")


def _run(module, payload: dict) -> tuple[int, str, str]:
    """Invoke `module.main` with a JSON payload on stdin and capture output."""
    stdin = io.StringIO(json.dumps(payload))
    stdout = io.StringIO()
    stderr = io.StringIO()
    rc = module.main(stdin, stdout, stderr)
    return rc, stdout.getvalue(), stderr.getvalue()


def _load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class UserPromptSubmitHook(unittest.TestCase):
    def test_bug_keyword_suggests_troubleshoot(self) -> None:
        payload = _load_fixture("user-prompt-submit.json")
        rc, out, err = _run(ups, payload)
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        body = json.loads(out)
        self.assertIn(
            "troubleshoot",
            body["hookSpecificOutput"]["additionalContext"].lower(),
        )

    def test_done_keyword_suggests_verification(self) -> None:
        rc, out, _ = _run(ups, {"prompt": "I think we're done — ready to ship"})
        self.assertEqual(rc, 0)
        body = json.loads(out)
        self.assertIn(
            "verification-before-completion",
            body["hookSpecificOutput"]["additionalContext"],
        )

    def test_tdd_keyword_suggests_tdd(self) -> None:
        rc, out, _ = _run(ups, {"prompt": "let's write a tdd test for this"})
        self.assertEqual(rc, 0)
        body = json.loads(out)
        ctx = body["hookSpecificOutput"]["additionalContext"]
        self.assertIn("tdd", ctx.lower())

    def test_review_keyword_suggests_review_skill(self) -> None:
        rc, out, _ = _run(ups, {"prompt": "got some review feedback — lgtm?"})
        self.assertEqual(rc, 0)
        body = json.loads(out)
        ctx = body["hookSpecificOutput"]["additionalContext"]
        self.assertIn("receiving-code-review", ctx)

    def test_no_match_emits_nothing(self) -> None:
        rc, out, _ = _run(ups, {"prompt": "what is 2 + 2"})
        self.assertEqual(rc, 0)
        self.assertEqual(out, "")

    def test_empty_payload_is_safe(self) -> None:
        stdin = io.StringIO("")
        out, err = io.StringIO(), io.StringIO()
        rc = ups.main(stdin, out, err)
        self.assertEqual(rc, 0)
        self.assertEqual(out.getvalue(), "")


class PreToolUseHook(unittest.TestCase):
    def test_real_skill_passes(self) -> None:
        payload = _load_fixture("pre-tool-use.json")
        rc, _, err = _run(pre, payload)
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")

    def test_missing_skill_blocks(self) -> None:
        rc, _, err = _run(
            pre,
            {"tool_name": "Skill", "tool_input": {"skill": "non-existent-skill-xyz"}},
        )
        self.assertEqual(rc, 2)
        self.assertIn("non-existent-skill-xyz", err)

    def test_completion_verb_emits_context(self) -> None:
        rc, out, _ = _run(
            pre,
            {
                "tool_name": "Skill",
                "tool_input": {
                    "skill": "sc-implement",
                    "prompt": "I am done with the implementation",
                },
            },
        )
        self.assertEqual(rc, 0)
        body = json.loads(out)
        self.assertIn(
            "verification-before-completion",
            body["hookSpecificOutput"]["additionalContext"],
        )

    def test_agent_invocation_does_not_require_skill_md(self) -> None:
        # Agent slugs are not authoritatively bound to skills/<slug>/SKILL.md;
        # the hook should not block on them.
        rc, _, err = _run(
            pre,
            {"tool_name": "Agent", "tool_input": {"subagent_type": "explore-agent"}},
        )
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")


class PostToolUseHook(unittest.TestCase):
    def test_chain_suggestion_for_implement(self) -> None:
        payload = _load_fixture("post-tool-use.json")
        rc, out, err = _run(post, payload)
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        # sc-implement may carry skill_references_skills frontmatter; if it
        # does, additionalContext lands. If it doesn't, the hook is silent.
        # The contract here is "exit 0 either way".

    def test_no_skill_slug_does_not_crash(self) -> None:
        rc, _, _ = _run(
            post,
            {"tool_name": "Bash", "tool_input": {}, "tool_response": "ok"},
        )
        self.assertEqual(rc, 0)


class StopHook(unittest.TestCase):
    """The Stop hook resolves the active task against the real repo; the
    test harness can't easily fake an isolated repo without confusing the
    other linters. So we cover the FL-parser directly + smoke-test the
    happy path against the live repo (where Task 094 has a friction-log
    with an FL0 declaration in scope)."""

    def test_fl_declared_canonical(self) -> None:
        self.assertTrue(stop_mod._fl_declared("Highest Frustration Level: FL0\n"))
        self.assertTrue(
            stop_mod._fl_declared("**Highest Frustration Level: FL2**\n")
        )
        self.assertTrue(stop_mod._fl_declared("- **Friction Level:** FL0\n"))

    def test_fl_declared_missing(self) -> None:
        self.assertFalse(stop_mod._fl_declared("# Friction Log\n\nFL is fine.\n"))
        self.assertFalse(stop_mod._fl_declared(""))

    def test_fl_declared_bare_form(self) -> None:
        self.assertTrue(stop_mod._fl_declared("**FL0** — plan cleared.\n"))

    def test_happy_path_against_live_repo(self) -> None:
        # The active Task 094 carries an FL0 declaration in its
        # friction-log; the live repo run should never block.
        payload = _load_fixture("stop.json")
        rc, _, err = _run(stop_mod, payload)
        # Either exit 0 (clean) or exit 0 with an additionalContext
        # nudge. The Stop hook never blocks unless FL is missing, and
        # Task 094's friction-log carries one.
        self.assertEqual(rc, 0, err)


class SubagentStopHook(unittest.TestCase):
    def test_code_reviewer_routes_to_receiving_review(self) -> None:
        payload = _load_fixture("subagent-stop.json")
        rc, out, _ = _run(subagent, payload)
        self.assertEqual(rc, 0)
        body = json.loads(out)
        self.assertIn(
            "receiving-code-review",
            body["hookSpecificOutput"]["additionalContext"],
        )

    def test_deep_research_routes_to_verification(self) -> None:
        rc, out, _ = _run(subagent, {"subagent_type": "deep-research"})
        self.assertEqual(rc, 0)
        body = json.loads(out)
        self.assertIn(
            "verification",
            body["hookSpecificOutput"]["additionalContext"].lower(),
        )

    def test_unknown_agent_default_message(self) -> None:
        rc, out, _ = _run(subagent, {"subagent_type": "unfamiliar-agent"})
        self.assertEqual(rc, 0)
        body = json.loads(out)
        # Default message still routes through the receiving-review gate.
        self.assertIn(
            "receiving-code-review",
            body["hookSpecificOutput"]["additionalContext"],
        )


class CheckHooks(unittest.TestCase):
    """`tools/check-hooks.py` bidirectional consistency tests."""

    def _make_fake_repo(self, settings: dict, scripts: list[str]) -> TemporaryDirectory:
        td = TemporaryDirectory()
        root = Path(td.name)
        (root / ".claude").mkdir()
        (root / "tools" / "hooks").mkdir(parents=True)
        (root / ".claude" / "settings.json").write_text(
            json.dumps(settings), encoding="utf-8"
        )
        for name in scripts:
            script = root / "tools" / "hooks" / name
            script.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
            script.chmod(0o755)
        return td

    def _audit(self, td: TemporaryDirectory) -> list[str]:
        root = Path(td.name)
        return check_hooks.audit(
            root,
            root / ".claude" / "settings.json",
            root / "tools" / "hooks",
        )

    def test_clean_repo_no_diagnostics(self) -> None:
        settings = {
            "hooks": {
                "UserPromptSubmit": [
                    {"matcher": "", "hooks": [{"type": "command", "command": "tools/hooks/foo.sh"}]}
                ]
            }
        }
        td = self._make_fake_repo(settings, ["foo.sh"])
        try:
            self.assertEqual(self._audit(td), [])
        finally:
            td.cleanup()

    def test_orphan_script_h_1_1(self) -> None:
        settings = {"hooks": {}}
        td = self._make_fake_repo(settings, ["orphan.sh"])
        try:
            diags = self._audit(td)
            self.assertEqual(len(diags), 1)
            self.assertIn("H.1.1", diags[0])
            self.assertIn("orphan.sh", diags[0])
        finally:
            td.cleanup()

    def test_orphan_registration_h_1_2(self) -> None:
        settings = {
            "hooks": {
                "Stop": [
                    {"matcher": "", "hooks": [{"type": "command", "command": "tools/hooks/missing.sh"}]}
                ]
            }
        }
        td = self._make_fake_repo(settings, [])
        try:
            diags = self._audit(td)
            self.assertEqual(len(diags), 1)
            self.assertIn("H.1.2", diags[0])
            self.assertIn("missing.sh", diags[0])
        finally:
            td.cleanup()

    def test_session_start_violation_h_1_3(self) -> None:
        settings = {
            "hooks": {
                "SessionStart": [
                    {"matcher": "", "hooks": [{"type": "command", "command": "tools/hooks/foo.sh"}]}
                ]
            }
        }
        td = self._make_fake_repo(settings, ["foo.sh"])
        try:
            diags = self._audit(td)
            self.assertTrue(any("H.1.3" in d for d in diags))
            self.assertTrue(any("D.7" in d for d in diags))
        finally:
            td.cleanup()

    def test_live_repo_is_clean(self) -> None:
        diags = check_hooks.audit(
            REPO,
            REPO / ".claude" / "settings.json",
            REPO / "tools" / "hooks",
        )
        self.assertEqual(diags, [], f"live repo: {diags}")


class FLRegexVariants(unittest.TestCase):
    """Cover the variant FL declarations enumerated in
    research/fl0-value-justification/output/SPEC.md §2.2."""

    def test_variant_phrasing_friction_experienced(self) -> None:
        self.assertTrue(
            stop_mod._fl_declared("**Highest friction level experienced: FL0**")
        )

    def test_variant_abbreviated_fl(self) -> None:
        self.assertTrue(stop_mod._fl_declared("**Highest FL experienced: FL0**"))


if __name__ == "__main__":
    unittest.main()
