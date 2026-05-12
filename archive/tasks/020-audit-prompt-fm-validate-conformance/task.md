---
type: task
status: archived
slug: audit-prompt-fm-validate-conformance
summary: "Successor to Task 004. The two prompts now exist; bring every /prompts/<slug>/prompt.md into full conformance with the prompt-type required-headings contract shipped by Task 016 (fm-validate)."
created: 2026-05-05
updated: 2026-05-12
task_id: "020"
task_status: archived
task_owner: "claude-code"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_supersedes:
  - "004"
task_blocked_by: []
task_affects_paths:
  - prompts/
  - tools/fm/validate.py
---

# Task 020 — Audit Prompts Against fm-validate Prompt Schema

Successor to [Task 004](../004-create-missing-prompts/task.md). The original Task asked for the two missing prompts (`refactor-governance-from-specs`, `token-efficiency-tool-suite`) to be authored. Both prompt.md files now exist, but `fm-validate` flags `prompts/refactor-governance-from-specs/prompt.md` for missing required headings (`## I — Input`, `## S — Steps`, `## E — Expectations`, `## Constraints`) per [`maintenance/schemas/header-ontology.json`](../../maintenance/schemas/header-ontology.json) (the canonical encoding shipped by Task 016). The Task 004 plan ("draft prompts according to PROMPT.md guidelines") predates that ontology and does not enumerate the required headings.

## Goal

Every `/prompts/<slug>/prompt.md` MUST pass `python3 tools/fm/validate.py` with zero `F.4.x` (heading) and `F.3.x` (frontmatter) diagnostics. The Task is `done` when the validator's prompt-type checks are clean across the whole `/prompts/` tree.

## Plan

1. Run `python3 tools/fm/validate.py prompts/` and capture every `F.3.x`/`F.4.x` diagnostic into `notes.md`.
2. For each diagnostic, add the missing heading or fix the frontmatter via `tools/fm/edit.py` (T1/T2 mutations only — body authorship requires care, T3 prose changes get their own review).
3. Re-run the validator after each batch; commit when a contiguous group of prompts passes cleanly.
4. Cross-check against [`research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) §4 (required headings per type) — if any prompt cannot reasonably express the canonical RISEN headings, surface the divergence as a finding for Task 019 (toolchain suite integration) rather than forcing a fit.

## Todo

- [x] 1. Capture the current diagnostic baseline (`fm-validate` over `/prompts/`).
- [x] 2. Bring `prompts/refactor-governance-from-specs/prompt.md` to zero `F.4.x` diagnostics.
- [x] 3. Sweep every other prompt and resolve its diagnostics or escalate via `notes.md`.
- [x] 4. Re-run `tools/check-governance.sh` end-to-end; verify zero new lint regressions.
- [x] 5. Append a `friction-log.md` with FL[0-3] declaration on closure.

## Links

- Predecessor: [`../004-create-missing-prompts/task.md`](../004-create-missing-prompts/task.md)
- Canonical prompt schema: [`maintenance/schemas/header-ontology.json`](../../maintenance/schemas/header-ontology.json) (`types.prompt`)
- Source spec: [`research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) §4
- Governing specs: [`TASK.md`](../../TASK.md), [`PROMPT.md`](../../PROMPT.md)
