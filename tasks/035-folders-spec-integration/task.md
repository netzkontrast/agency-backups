---
type: task
status: active
slug: folders-spec-integration
summary: "Add Gherkin acceptance scenarios to FOLDERS.md, clarify F.1.1 readme-required scope on /research/<provider>/<slug>/ external folders, mechanically enforce F.5 readme.md L1 frontmatter, and define a frontmatter-vs-body-link consistency check for the F.6 audit graph."
created: 2026-05-06
updated: 2026-05-06
task_id: "035"
task_status: open
task_owner: "unassigned"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - FOLDERS.md
  - tools/check-readme-frontmatter.py
  - tools/check-audit-graph-consistency.py
---

# Task 035 — FOLDERS.md Spec Integration

## Goal

Close FOLDERS.md governance gaps with mechanical enforcement and clearer scope language. The Task is `done` when (a) FOLDERS.md §F.5 readme.md L1 frontmatter is checked by a linter, (b) F.1.1 explicitly states which `/research/<provider>/<slug>/` paths are exempt from the readme.md requirement, (c) F.6 has a tooling-backed consistency check that warns when a body-level Markdown link references a sibling folder *without* the corresponding frontmatter linkage being set, (d) ≥4 Gherkin scenarios cover the load-bearing F.1, F.2, F.4.1.1, F.6 rules.

## Context

FOLDERS.md governance debt (mostly mechanical):

- **F.1.1 (FOLDERS.md:42)** — "non-provider `/research/<slug>/`" — the term "provider" is defined in RESEARCH.md §6 but FOLDERS.md does not enumerate the exemption. `tools/lint-structure.py` may or may not match spec intent; the rule is ambiguous in prose.
- **F.5 (FOLDERS.md:70)** — "`readme.md` files in operational folders SHOULD carry L1 Vault Core frontmatter" — SHOULD, not MUST; no linter; readme.md files exist without frontmatter.
- **F.6 audit-graph dual-surface (FOLDERS.md:86–98)** — frontmatter is "source of truth" but body Markdown links are "encouraged for human navigation". Agents may keep body links current and frontmatter stale; linter cannot detect the divergence today.
- **No Gherkin scenarios** — load-bearing rules F.1 (every folder MUST have readme.md), F.2 (slug naming), F.4.1.1 (prompt scaffold) lack acceptance tests.

This task is purely additive (T2 per MAINTENANCE.md §1) and does not require new research.

## Plan

1. **Phase 1 — Tooling.** Subtask `01-tooling-readme-frontmatter-validator` (closes F.5 SHOULD→MUST). Subtask `02-tooling-audit-graph-consistency-checker` (warns on body-link/frontmatter divergence).
2. **Phase 2 — Spec amendment.** Subtask `03-spec-amendment-folders-md`: F.1.1 provider-exemption clause, F.5 promotion to MUST, F.6 dual-surface guidance, Gherkin scenarios.

## Todo

- [ ] 1. Dispatch subtask `01-tooling-readme-frontmatter-validator` (Phase A).
- [ ] 2. Dispatch subtask `02-tooling-audit-graph-consistency-checker` (Phase A).
- [ ] 3. Dispatch subtask `03-spec-amendment-folders-md` (Phase B).
- [ ] 4. Run `tools/check-governance.sh`.
- [ ] 5. Update `README.md §6` (linter table) per R.7.
- [ ] 6. Update `tasks/readme.md`.
- [ ] 7. Author `friction-log.md`.
- [ ] 8. Set `task_status: done`.

## Links

- Subtask index: [`subtasks/readme.md`](./subtasks/readme.md)
- Source research:
  - [`research/governance-specs-update-research/output/SPEC.md`](../../research/governance-specs-update-research/output/SPEC.md) §3 (FOLDERS.md amendments)
- Governing specs: [`FOLDERS.md`](../../FOLDERS.md), [`RESEARCH.md`](../../RESEARCH.md) §6, [`README.md`](../../README.md) §11.3
