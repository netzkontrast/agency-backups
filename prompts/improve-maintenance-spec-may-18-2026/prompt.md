---
type: prompt
status: active
slug: improve-maintenance-spec-may-18-2026
summary: "Land the seven findings F27-F33 from the 2026-05-18 coherence run as concrete diffs against MAINTENANCE.md (§1, §2.3, §3.3, §3.4, §4.1), prompts/repo-coherence-check/prompt.md (Step 1a), and tools/adr/cli.py (no-op suppression). Each finding either lands a diff or records a won't-fix disposition in friction-log.md."
created: 2026-05-18
updated: 2026-05-18
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: improve-maintenance-spec-may-18-2026
---

# Improve Maintenance Spec (2026-05-18 Coherence Run) — Task-Spec Prompt

## Framework

RISEN+ReAct. Declared in frontmatter (`prompt_framework: RISEN+ReAct`) and restated here for `fm-validate` header conformance. R/I/S/E sections carry canonical roles; a final **Constraints** section groups normative scope and failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute [Task 096 — Improve Maintenance Spec from 2026-05-18 Coherence Run](../../tasks/096-improve-maintenance-spec-may-18-2026/task.md). Your remit is bounded by the seven findings F27–F33 in `task.md` `## Findings`; you MUST NOT expand scope beyond them without surfacing the divergence in `friction-log.md`.

**Parallelism:** Sequential. The findings touch interlocking sections of MAINTENANCE.md; landing them in `task.md ## Plan` order avoids merge conflicts in the prose.

## I — Input

- [`tasks/096-improve-maintenance-spec-may-18-2026/task.md`](../../tasks/096-improve-maintenance-spec-may-18-2026/task.md) — canonical Goal + Findings + Plan + Todo.
- [`MAINTENANCE.md`](../../MAINTENANCE.md) — target spec (sections §1, §2.3, §3.3, §3.4, §4.1).
- [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) — coherence prompt Step 1a (awk filter for F29).
- [`tools/adr/cli.py`](../../tools/adr/cli.py) — `synthesize` subcommand (no-op suppression for F33).
- Cross-cutting precedents to read before drafting diffs:
  - Task 044 F14 ([FL canonicalisation](../../tasks/044-improve-maintenance-spec-may-07-2026/task.md)).
  - Task 064 F21 ([one-open-Task cadence](../../tasks/064-improve-maintenance-spec-may-08-2026/task.md)), F23 (gating vs advisory output), F26 (skip-with-citation).

## S — Steps

1. **Pre-condition: execute the [TASK.md §4.9](../../TASK.md#49-planning-pipeline-for-t3-structural-tasks-sc-ladder) planning ladder.** This Task crosses the T3 threshold (root-spec edit, >3 files). Run `/sc:analyze → /sc:brainstorm → /sc:design → /sc:workflow` and commit `tasks/096-improve-maintenance-spec-may-18-2026/workflow.md` per T.4.9.2.
2. **For each finding F27–F33 in `task.md ## Findings`:** (a) read the cited spec section; (b) draft the concrete diff; (c) apply via [`tools/fm/edit.py`](../../tools/fm/edit.py) for frontmatter, in-place Edit for body content; (d) re-run `tools/check-governance.sh` and verify it exits 0; (e) mark the corresponding `## Todo` checkbox.
3. **For findings where the diff is unsafe or requires upstream coordination:** record a `won't-fix: <reason>` disposition in `friction-log.md` with rationale. Do NOT mutate the spec under uncertainty.
4. **Coordinate with sibling Tasks 025 / 044 / 064.** If F27/F28 land while Task 064 is still open, cite Task 064 F21 / F23 / F26 as cross-references in the amended prose so the lineage is discoverable.
5. **Close the Task per [TASK.md §4.6](../../TASK.md#4-workflow-task-lifecycle).** Set `task_status: done`, bump `updated:`, produce `friction-log.md` with canonical `**Highest Frustration Level: FL[0-3]**` declaration and a per-finding disposition table (`landed: <commit>` | `won't-fix: <reason>` | `delegated to Task NNN`).

## E — Expectations

- Modified files (per scope):
  - [`MAINTENANCE.md`](../../MAINTENANCE.md) — §1 (F27 tier rows; F31 T3 cross-link), §2.3 (F29 baseline rule), §3.3 (F28 dedup predicate), §3.4 (F30 triage threshold), §4.1 (F32 advisory clarification).
  - [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) — Step 1a awk filter (F29).
  - [`tools/adr/cli.py`](../../tools/adr/cli.py) — `synthesize` no-op suppression (F33).
- New files:
  - [`tasks/096-improve-maintenance-spec-may-18-2026/workflow.md`](../../tasks/096-improve-maintenance-spec-may-18-2026/) — `/sc:workflow` artefact per T.4.9.2.
  - [`tasks/096-improve-maintenance-spec-may-18-2026/friction-log.md`](../../tasks/096-improve-maintenance-spec-may-18-2026/) — closure log with FL declaration + per-finding disposition.
- Frontmatter mutations: bump `updated:` on every touched file via [`tools/fm/edit.py --bump-updated`](../../tools/fm/edit.py).
- Index sync: update [`tasks/readme.md`](../../tasks/readme.md) bullet to `Status: done` when closing (TASK.md §4.8 / §7.11).

## N — Norms

- **Acceptance** lives in [`brief.md`](./brief.md) (Gherkin scenarios). The prompt body MUST NOT re-state acceptance criteria — single source of truth.
- **Governance gate:** `tools/check-governance.sh` MUST exit 0 after every commit. If it fails, fix the underlying issue; do NOT bypass.
- **Frontmatter mutations:** [`tools/fm/edit.py`](../../tools/fm/edit.py) ONLY — never `sed`/`awk`. T3/T4 operations are refused by construction.
- **No new T3 scope:** F27–F33 are the closed finding set. New findings discovered mid-execution MUST be filed as a separate Task or `notes.md` deferral; do not silently expand scope.
- **Friction log MUST carry a canonical FL declaration line** matching one of the 15 accepted variants in [`tools/check-fl-declaration.py`](../../tools/check-fl-declaration.py) (per Task 044 F14 ratification + F27 tier classification).

## Constraints

- **MUST follow the [TASK.md §4.9](../../TASK.md#49-planning-pipeline-for-t3-structural-tasks-sc-ladder) `/sc:*` ladder before authoring detailed diffs** (T.4.9.1 SHOULD escalates to MUST here because the spec edits cross three root files).
- **MUST NOT alter `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` blocks** in `AGENTS.md` by hand — agent-written per Task 028 / ADR-0011.
- **MUST cite Task 044 F14 in F27's amended prose** so the canonical-form + tier-classification rules are jointly discoverable.
- **MUST file F33 against `tools/adr/cli.py`** (the synthesize command), not against `maintenance/run-log.md` directly — the run-log records are the symptom, the synthesize command is the source.
- **MUST honour Task 064 F21 dynamics in `notes.md`** — record whether F27–F33 landed before or after Task 064 closure; if before, the cadence rule's evidence base grows.

## Acceptance

See [`brief.md`](./brief.md) for the executable Gherkin acceptance criteria.
