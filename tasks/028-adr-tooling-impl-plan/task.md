---
type: task
status: active
slug: adr-tooling-impl-plan
summary: "From the spec produced by Task 027, design the concrete implementation plan for the agency-adr CLI tool suite: validate, synthesize (MDL), DAG cycle-detection, JSON-Schema linter, and GitHub Actions integration."
created: 2026-05-05
updated: 2026-05-05
task_id: "028"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts:
  - adr-tooling-impl-plan
task_spawns_research: []
task_spawns_prompts: []
task_supersedes: []
task_blocked_by:
  - "027"
task_affects_paths:
  - tools/adr/
  - prompts/adr-tooling-impl-plan/
  - PRE_COMMIT.md
  - MAINTENANCE.md
  - .github/workflows/
---

# Task 028 — ADR Tooling Implementation Plan

## Goal

Produce a **concrete, executable implementation plan** for the `agency-adr` CLI tool suite specified in Task 027's output (`research/adr-spec-research-synthesis/output/SPEC.md`). The plan resolves every "interface contract yes, working code no" boundary of the spec into a sequenced build order, module decomposition, and acceptance test map — without writing the implementation itself.

The task is **done** when `prompts/adr-tooling-impl-plan/prompt.md` is ready to hand to an implementing agent and a `tasks/028-adr-tooling-impl-plan/implementation-plan.md` artefact exists that a developer can follow without ambiguity.

## Context

The ADR governance spec (Task 027 output) defines:
- `agency-adr validate` — checks ADR corpus against JSON-Schema
- `agency-adr synthesize --mdl-floor 0.95 --token-limit 2000` — MDL compression pipeline → `AGENTS.md`
- A DAG of supersession edges with cycle-detection
- Semantic fidelity floor (≥ 0.95) as a pipeline acceptance gate
- POSIX exit-code conventions (0 / >0)
- Integration with `PRE_COMMIT.md` hooks and the existing `tools/check-governance.sh`

The implementation plan MUST sequence these into build phases that respect the existing tooling surface (`tools/fm/`, `tools/check-governance.sh`) and the repo's Python-first tooling convention.

## Plan

### Phase 1 — Audit Existing Tooling Surface

1. Read `tools/fm/validate.py`, `tools/fm/extract.py`, `tools/fm/query.py`, `tools/fm/edit.py` to identify reusable primitives (frontmatter parsing, schema validation, file traversal).
2. Read `tools/check-governance.sh` to identify integration points and avoid duplication.
3. Identify the canonical Python version and dependency management approach used by the repo (requirements.txt, pyproject.toml, etc.).

### Phase 2 — Module Decomposition

Decompose `agency-adr` into independently testable modules:

| Module | Responsibility |
|--------|----------------|
| `tools/adr/schema.py` | JSON-Schema validation of ADR YAML frontmatter |
| `tools/adr/graph.py` | Build supersession DAG; cycle-detection (Kahn's algorithm) |
| `tools/adr/extract.py` | Extract normative content from Accepted ADRs (Decision Outcome + Consequences sections) |
| `tools/adr/compress.py` | MDL compression: token-counting, rule deduplication, fidelity estimation |
| `tools/adr/synthesize.py` | Orchestrator: runs extract → compress → write AGENTS.md |
| `tools/adr/cli.py` | Click/argparse entry-point exposing `validate` and `synthesize` sub-commands |
| `tests/adr/` | Gherkin-mapped pytest fixtures covering every acceptance criterion |

### Phase 3 — Acceptance Test Mapping

Map every Gherkin scenario in the spec (§3.2, §4.2, §5.2, §6.2, §7.2) to a concrete `tests/adr/test_<aspect>.py` file with parametrized fixtures. Define the minimum passing test suite for each phase of the build.

### Phase 4 — GitHub Actions Integration

Define `.github/workflows/adr-validate.yml`:
- Triggered on: push to any branch modifying `docs/decisions/**`
- Steps: `pip install`, `agency-adr validate`, `agency-adr synthesize --mdl-floor 0.95 --token-limit 2000`, check AGENTS.md diff is committed

### Phase 5 — PRE_COMMIT.md Hook Specification

Define the hook entry for `PRE_COMMIT.md`:
- Runs `agency-adr validate` before every commit that touches `docs/decisions/`
- Fails with clear error messages mapping to spec statement IDs (e.g., `[A.4.5] Cyclic Dependency Detected`)

### Phase 6 — Produce Implementation Plan Artefact

Write `tasks/028-adr-tooling-impl-plan/implementation-plan.md` containing:
1. Module decomposition table (Phase 2)
2. Build sequencing: which modules must exist before others
3. Test coverage map (Phase 3)
4. CI/CD integration spec (Phase 4 + 5)
5. Estimated complexity per module (S/M/L)
6. Open decisions requiring human input before implementation begins

## Todo

- [ ] 1. Read Task 027 output at `research/adr-spec-research-synthesis/output/SPEC.md` — block until Task 027 is done.
- [ ] 2. Audit existing tooling surface per Phase 1.
- [ ] 3. Produce module decomposition per Phase 2.
- [ ] 4. Map Gherkin scenarios to test files per Phase 3.
- [ ] 5. Draft GitHub Actions workflow spec per Phase 4.
- [ ] 6. Draft PRE_COMMIT.md hook spec per Phase 5.
- [ ] 7. Write `implementation-plan.md` per Phase 6.
- [ ] 8. Flesh out `prompts/adr-tooling-impl-plan/prompt.md` as a ready-to-execute task-spec prompt.
- [ ] 9. Run `tools/check-governance.sh`; fix failures.
- [ ] 10. Set `task_status: done`.

## Links

- Blocked by: [`027-adr-spec-research-synthesis/task.md`](../027-adr-spec-research-synthesis/task.md)
- Executing prompt: [`prompts/adr-tooling-impl-plan/prompt.md`](../../prompts/adr-tooling-impl-plan/prompt.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md), [`MAINTENANCE.md`](../../MAINTENANCE.md)
