---
type: note
status: draft
slug: task-048-st3-spec-task-tooling-impl
summary: "ST-3 (Phase B; sequential): author research/task-tooling-impl-spec/output/SPEC.md per the §1–§7 build-contract pattern (Task 028 template), integrating ST-1 inspiration patterns and ST-2 inventory + gap analysis into ≥6 concrete tool proposals."
created: 2026-05-07
updated: 2026-05-07
---

# ST-3: SPEC Synthesis — `research/task-tooling-impl-spec/output/SPEC.md`

**Executor:** system-architect or technical-writer subagent (model: opus).

**Parallelism:** Phase B (sequential) — depends on ST-1 + ST-2. MUST wait for Phase A to converge.

## Goal

Produce the implementation-ready SPEC at `research/task-tooling-impl-spec/output/SPEC.md`, synthesising ST-1 (inspiration patterns) and ST-2 (existing-tooling inventory + gap analysis) into ≥6 concrete tool proposals, each with the §3 entry shape declared in the parent task.md.

## Inputs

- ST-1 output: `research/task-tooling-impl-spec/workspace/01-skills-inspiration.md`.
- ST-2 output: `research/task-tooling-impl-spec/workspace/02-tooling-inventory.md`.
- Build-contract template: [Task 028 implementation-plan.md](../../../tasks/028-adr-tooling-impl-plan/implementation-plan.md) §1–§7.
- `TASK.md` (root spec) — every normative clause the SPEC's §5 integration column cross-references.
- `maintenance/schemas/header-ontology.json` — the schema every proposed tool MUST consume.
- `research/flexible-frontmatter-toolchain/output/SPEC.md` — the contract every `tools/fm/*` tool inherits.

## Acceptance Criteria

1. SPEC at `research/task-tooling-impl-spec/output/SPEC.md` with frontmatter `type: research`, `research_phase: complete`, `research_executes_prompt: spec-task-tooling-impl`, `research_friction_level: FL[0-3]`.
2. **§1 Inputs** — cites the ST-1 and ST-2 workspace files plus the TASK.md anchors the SPEC operates against.
3. **§2 Architecture** — answers the directory-namespace question (`tools/fm/` vs new `tools/task/`); declares the shared library each tool consumes; declares the integration pattern with `tools/check-governance.sh`.
4. **§3 Per-Tool Spec** — **≥6** tool entries. Each follows the shape declared in `task.md` §"Sample SPEC §3 Entry Shape": purpose, inspiration source, surface, integration, schema dependency, test surface, falsification.
5. **§4 Tests** — each tool's test surface listed at file-path granularity (`tools/tests/fm/test_<name>.py`); shared fixtures (e.g. tmp-tasks-tree builder) declared once.
6. **§5 Integration** — table mapping each proposed tool to: TASK.md anchor, pre-commit row in §7.0, README.md §6 row addition (per R.7), MAINTENANCE.md run-log impact (if any).
7. **§6 Rollout** — phased migration plan: which tools land first (advisory), which gate the suite, what the migration window looks like (parallel to Task 033's `FM_DUPLICATE_TASK_ID_STRICT=1` precedent).
8. **§7 Falsification** — reiterates the parent task.md falsifiers + adds SPEC-internal ones (e.g. "the §3 tool count is the wrong cut iff two proposed tools could be merged into one without loss").
9. **`research_phase: complete`**; `friction-log.md` present at `research/task-tooling-impl-spec/reflection/friction-log.md`.
10. Folder index `research/task-tooling-impl-spec/readme.md` lists the workspace layout.
11. `research/readme.md` updated with the new bullet.
12. `tools/check-governance.sh` exits 0 (or remaining ERRORs are documented as out-of-scope per the Task 032 / Task 033 friction-log precedent).

## Falsification

Wrong cut **iff** the SPEC's §3 produces fewer than 6 tools, OR §3 produces a list that ST-2's gap analysis already covers (i.e. no novel synthesis), OR §5 forces > 3 TASK.md amendments (signals scope creep). Mitigation: ST-1 patterns + ST-2 gaps are independent corpora; cross-product yields > 6 candidates with confidence.

## Dependencies

ST-1 + ST-2 MUST land first.

## Estimated Effort

Large (~4–5 hours: integration + cross-reference verification + Gherkin scenarios if any).
