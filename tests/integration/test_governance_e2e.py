"""End-to-end governance gate test for the Task -> Prompt -> Research triptych.

Builds the seed triptych in a tmpdir, asserts the §7.0 linter mapping fires
(or doesn't fire) per the documented invariants. One parametrised mutator
per TASK.md §7.0 row.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS = REPO_ROOT / "tools"
TASK_DIR = "tasks/099-fixture-task"
TASK_MD = f"{TASK_DIR}/task.md"
README_MD = f"{TASK_DIR}/readme.md"
FRICTION_MD = f"{TASK_DIR}/friction-log.md"
PROMPT_MD = "prompts/fixture-prompt/prompt.md"
TASKS_INDEX = "tasks/readme.md"


def _run(args: list[str], cwd: Path, env_extra: dict | None = None,
         ) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["FM_LEGACY_QUIET"] = "1"
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, *args],
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
    )


def _fm_validate(cwd: Path, *extra: str) -> subprocess.CompletedProcess:
    return _run([str(TOOLS / "fm" / "validate.py"), *extra], cwd)


def _patch_text(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, f"old token not found in {path}: {old!r}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# --------------------------- happy-path ---------------------------


def test_happy_path_all_linters_pass(triptych_fixture: Path) -> None:
    proc = _fm_validate(triptych_fixture, "--type-check", "--check-body")
    assert proc.returncode == 0, proc.stdout + proc.stderr

    proc = _run(
        [str(TOOLS / "lint-structure.py")], triptych_fixture,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr

    proc = _run(
        [str(TOOLS / "check-readme-frontmatter.py")], triptych_fixture,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr

    proc = _run(
        [str(TOOLS / "fm" / "index_diff.py")], triptych_fixture,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr

    proc = _run(
        [str(TOOLS / "check-trust.py")], triptych_fixture,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr

    proc = _run(
        [
            str(TOOLS / "check-fl-declaration.py"),
            f"{TASK_DIR}/friction-log.md",
            "research/fixture-research/reflection/friction-log.md",
        ],
        triptych_fixture,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr

    proc = _run(
        [str(TOOLS / "fm" / "check-duplicate-task-id.py"), "tasks/"],
        triptych_fixture,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


# --------------------------- mutators ---------------------------
# One parametrised mutator per TASK.md §7.0 row.


def _mutate_7_1_frontmatter_integrity(base: Path) -> None:
    _patch_text(base / TASK_MD, "type: task", "tpye: task")


def _mutate_7_2_body_schema(base: Path) -> None:
    p = base / PROMPT_MD
    text = p.read_text(encoding="utf-8")
    pre, _, _ = text.partition("## S — Steps")
    p.write_text(
        pre + "## S — Steps\n\n1. only one item.\n\n## E — Expectations\n\n"
        "- foo\n\n## Constraints\n\n- bar\n",
        encoding="utf-8",
    )


def _mutate_7_3_prompt_linkage(base: Path) -> None:
    _patch_text(
        base / TASK_MD,
        "task_uses_prompts:\n  - fixture-prompt",
        "task_uses_prompts:\n  - nonexistent-prompt-slug",
    )


def _mutate_7_4_research_linkage(base: Path) -> None:
    _patch_text(
        base / TASK_MD,
        "task_spawns_research:\n  - fixture-research",
        "task_spawns_research:\n  - nonexistent-research-slug",
    )


def _mutate_7_6_todo_completion(base: Path) -> None:
    # F.B.7 WARN fires when every Todo item is checked but task_status
    # disagrees with the schema's completion_field expectation of "done".
    # Flip task_status to in_progress so the mismatch surfaces.
    _patch_text(
        base / TASK_MD,
        "task_status: done",
        "task_status: in_progress",
    )


def _mutate_7_7_readme_audit(base: Path) -> None:
    (base / README_MD).unlink()


def _mutate_7_8_friction_log(base: Path) -> None:
    (base / FRICTION_MD).unlink()


def _mutate_7_9_blocker_satisfaction(base: Path) -> None:
    _patch_text(
        base / TASK_MD,
        "task_blocked_by: []",
        "task_blocked_by:\n  - nonexistent-blocker-slug",
    )


def _mutate_7_10_supersession_reciprocity(base: Path) -> None:
    # §7.10's reciprocity rule is described in TASK.md but not yet wired
    # into header-ontology.json's `reciprocity.rules` (only the
    # task_uses_prompts ↔ prompt_relates_to_task pair is mechanically
    # enforced). The closest mechanical surface today is F.T.1 dangling
    # when task_supersedes names a slug that does not resolve at all.
    _patch_text(
        base / TASK_MD,
        "task_supersedes: []",
        "task_supersedes:\n  - nonexistent-predecessor-slug",
    )


def _mutate_7_11_tasks_index_freshness(base: Path) -> None:
    _patch_text(
        base / TASKS_INDEX,
        "- [`099-fixture-task/`](./099-fixture-task/) — Minimal fixture task. "
        "Status: `done`.\n",
        "",
    )


def _mutate_8_1_duplicate_task_id(base: Path) -> None:
    # Clone 099 into a 100-* folder with the same task_id "099".
    second = base / "tasks" / "100-fixture-duplicate"
    src = base / "tasks" / "099-fixture-task"
    shutil.copytree(src, second)
    _patch_text(
        second / "task.md",
        "slug: fixture-task",
        "slug: fixture-duplicate",
    )
    _patch_text(
        second / "readme.md",
        "slug: fixture-task",
        "slug: fixture-duplicate",
    )
    _patch_text(
        second / "friction-log.md",
        "slug: fixture-task-friction-log",
        "slug: fixture-duplicate-friction-log",
    )


# Row registry: (id, mutator, runner, expected token, comment).
# `runner` returns a CompletedProcess for the row's linter; the test asserts
# the expected diagnostic token is in stdout+stderr and exit code is non-zero.


def _run_fm_validate(base: Path) -> subprocess.CompletedProcess:
    return _fm_validate(base)


def _run_fm_validate_body(base: Path) -> subprocess.CompletedProcess:
    return _fm_validate(base, "--check-body")


def _run_fm_validate_body_strict(base: Path) -> subprocess.CompletedProcess:
    return _fm_validate(base, "--check-body", "--strict")


def _run_fm_validate_typecheck(base: Path) -> subprocess.CompletedProcess:
    return _fm_validate(base, "--type-check")


def _run_lint_structure(base: Path) -> subprocess.CompletedProcess:
    return _run([str(TOOLS / "lint-structure.py")], base)


def _run_check_trust(base: Path) -> subprocess.CompletedProcess:
    return _run([str(TOOLS / "check-trust.py")], base)


def _run_index_diff(base: Path) -> subprocess.CompletedProcess:
    return _run([str(TOOLS / "fm" / "index_diff.py")], base)


def _run_duplicate_task_id(base: Path) -> subprocess.CompletedProcess:
    return _run(
        [str(TOOLS / "fm" / "check-duplicate-task-id.py"), "tasks/"],
        base,
        {"FM_DUPLICATE_TASK_ID_STRICT": "1"},
    )


MUTATORS = [
    pytest.param(
        _mutate_7_1_frontmatter_integrity,
        _run_fm_validate,
        "F.3.4",
        id="7.1-frontmatter-integrity",
    ),
    pytest.param(
        _mutate_7_2_body_schema,
        _run_fm_validate_body,
        "F.B.2",
        id="7.2-body-schema",
    ),
    pytest.param(
        _mutate_7_3_prompt_linkage,
        _run_fm_validate_typecheck,
        "F.T.1",
        id="7.3-prompt-linkage",
    ),
    pytest.param(
        _mutate_7_4_research_linkage,
        _run_fm_validate_typecheck,
        "F.T.1",
        id="7.4-research-linkage",
    ),
    pytest.param(
        None, None, None,
        id="7.5-path-containment",
        marks=pytest.mark.skip(
            reason="§7.5 is human-review only; no mechanical check (TASK.md §7.0).",
        ),
    ),
    pytest.param(
        _mutate_7_6_todo_completion,
        _run_fm_validate_body_strict,
        "F.B.7",
        id="7.6-todo-completion",
    ),
    pytest.param(
        _mutate_7_7_readme_audit,
        _run_lint_structure,
        "missing required readme.md",
        id="7.7-readme-audit",
    ),
    pytest.param(
        _mutate_7_8_friction_log,
        _run_check_trust,
        "has no friction-log.md",
        id="7.8-friction-log",
    ),
    pytest.param(
        _mutate_7_9_blocker_satisfaction,
        _run_fm_validate_typecheck,
        "F.T.1",
        id="7.9-blocker-satisfaction",
    ),
    pytest.param(
        _mutate_7_10_supersession_reciprocity,
        _run_fm_validate_typecheck,
        "F.T.1",
        id="7.10-supersession-reciprocity",
    ),
    pytest.param(
        _mutate_7_11_tasks_index_freshness,
        _run_index_diff,
        "099-fixture-task",
        id="7.11-tasks-index-freshness",
    ),
    pytest.param(
        _mutate_8_1_duplicate_task_id,
        _run_duplicate_task_id,
        "duplicate",
        id="8.1-duplicate-task-id",
    ),
]


@pytest.mark.parametrize("mutator,runner,expected_token", MUTATORS)
def test_mutator_surfaces_documented_diagnostic(
    triptych_fixture: Path,
    mutator,
    runner,
    expected_token,
) -> None:
    mutator(triptych_fixture)
    proc = runner(triptych_fixture)
    combined = proc.stdout + proc.stderr
    assert proc.returncode != 0, (
        f"expected non-zero exit; got 0\nstdout:\n{proc.stdout}\n"
        f"stderr:\n{proc.stderr}"
    )
    assert expected_token.lower() in combined.lower(), (
        f"expected token {expected_token!r} not found in output\n"
        f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
    )
