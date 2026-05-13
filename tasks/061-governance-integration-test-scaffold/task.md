---
type: task
status: active
slug: governance-integration-test-scaffold
summary: "Scaffold an end-to-end integration test that creates a minimal Task -> Prompt -> Research triptych in a tmpdir and verifies tools/check-governance.sh exits zero, then mutates each tier to verify each linter row in TASK.md §7.0 emits the documented diagnostic."
created: 2026-05-07
updated: 2026-05-13
task_id: "061"
task_status: done
task_owner: "claude-code"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - tests/integration/
  - tests/integration/test_governance_e2e.py
  - tests/integration/conftest.py
  - tests/integration/fixtures/
---

# Task 061 — End-to-End Governance Integration Test

## Goal

The `tests/fm/` suite covers individual fm-tools well, but no test simulates a complete `Task → Prompt → Research → check-governance.sh` cycle. The single falsifiable outcome of this Task: `tests/integration/test_governance_e2e.py` (a) constructs a minimal valid triptych in a `tempfile.TemporaryDirectory`, (b) asserts `tools/check-governance.sh` exits zero, and (c) for every row of the `TASK.md §7.0` linter mapping, mutates the fixture to violate that specific row and asserts the documented diagnostic surfaces (and only that diagnostic, modulo unavoidable cascade).

## Plan

1. **Build** the minimal triptych fixture under `tests/integration/fixtures/`: one `tasks/<NNN>-<slug>/` (task.md + readme.md + friction-log.md + ontology stubs), one `prompts/<slug>/`, one `research/<slug>/` — copy or stub the schema files needed by `tools/fm/validate.py` (`maintenance/schemas/header-ontology.json`).
2. **Author** `tests/integration/conftest.py` with a `triptych_fixture` pytest fixture that copies the seed fixture into a tmpdir, runs `git init` if required, and returns the tmpdir path.
3. **Author** `tests/integration/test_governance_e2e.py` with the happy-path assertion (zero exit, no diagnostics).
4. **Add** one parameterised mutator-test per `TASK.md §7.0` row (12 rows: §7.1–§7.11 + §8.1). Each mutator inverts a specific invariant and asserts the documented diagnostic ID/message appears.
5. **Wire** `pytest tests/integration/` into `tools/check-governance.sh` (or a separate `tools/check-integration.sh`), advisory by default; gated when `INTEGRATION=1` is set.

## Todo

- [x] Build seed triptych fixture under `tests/integration/fixtures/`.
- [x] Author `tests/integration/conftest.py` with `triptych_fixture`.
- [x] Author happy-path test asserting `check-governance.sh` exits zero.
- [x] Add 12 mutator tests covering each row of `TASK.md §7.0`.
- [x] Wire `pytest tests/integration/` into `tools/check-governance.sh` (advisory).
- [x] Run the full suite locally; record runtime in `notes.md`.
- [x] Write `friction-log.md` with FL[0–3] declaration on closure.

## Links

- Parent dispatch: [Task 053](../053-core-architecture-review-followups/) finding B.10.
- Linter mapping under test: [`TASK.md §7.0`](../../TASK.md).
- Reference test style: [`tests/fm/test_falsification_attacks.py`](../../tests/fm/test_falsification_attacks.py).
