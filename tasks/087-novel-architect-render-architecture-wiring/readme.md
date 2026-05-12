---
type: index
status: active
slug: novel-architect-render-architecture-wiring
summary: "Directory index for Task 087 — sub-task of Epic 083. Wires skills/novel-architect/render/render_architecture.py Phase 2.13 status-view to consume <workspace>/<slug>/.architecture-validation.json produced by Task 084. Artefact-based coupling preserves skill portability per AGENTS.md Skills Architecture."
created: 2026-05-12
updated: 2026-05-12
---

# Task 087 — Render-Architecture Wiring

**What:** Sub-task of [Epic 083](../083-novel-architect-v120-enforcement-epic/). Wires [`skills/novel-architect/render/render_architecture.py`](../../skills/novel-architect/render/render_architecture.py) to read the JSON validation artefact produced by [Task 084's `tools/check-hard-rules.py`](../084-novel-architect-storyform-integrity-linter/) and surface H1–H12 pass/fail markers + worksheet_audit step completion in the Phase 2.13 status-view. Stale / missing / malformed artefact → renderer emits a warning and continues, never crashes.

**Why here:** Per [TASK.md §2](../../TASK.md), every coordination unit lives in `/tasks/<NNN>-<slug>/`. The coupling between the linter (under `tools/`) and the renderer (under `skills/`) is **artefact-based** (JSON file) rather than import-based so that skill deployment to claude.ai (where `tools/` is not present) continues to function — per [AGENTS.md "Skills Architecture"](../../AGENTS.md#skills-architecture--container-capabilities-and-citation-protocol) portability constraint. `task_blocked_by: [084]` because the JSON schema-version 1.0 contract is locked in 084's `validation_report.py`.

## Navigation

- [task.md](./task.md) — Sub-task spec: Goal, Context, Plan, Todo, Acceptance, Links.

## Assumptions Log

- (none)
