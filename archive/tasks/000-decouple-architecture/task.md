---
type: task
status: archived
slug: decouple-architecture
summary: "Bootstrap meta-task: introduce /tasks/, the Frontmatter Ontology, TASK.md, refactor PROMPT.md/RESEARCH.md/FOLDERS.md, ship templates and a frontmatter validator."
created: 2026-05-04
updated: 2026-05-12
task_id: "000"
task_status: archived
task_owner: "claude-code"
task_priority: P0
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - TASK.md
  - PROMPT.md
  - RESEARCH.md
  - FOLDERS.md
  - PRE_COMMIT.md
  - AGENTS.md
  - prompts/
  - tasks/
  - templates/
  - tools/
  - research/readme.md
---

# Task 000 — Decouple Architecture (Meta-Task)

## Goal

Decouple Tasks (orchestration) from Prompts (instruction) and Research (execution). Introduce a Layered-Schema-with-Namespacing Frontmatter Ontology so cross-directory linkage is queryable. Ship the new architecture as governance specs (`TASK.md`, refactored `PROMPT.md`/`RESEARCH.md`/`FOLDERS.md`), copy-and-edit templates, and a self-enforcing validator. Done condition: a clean clone validates with zero diagnostics on staged files.

## Plan

This Task was executed inline as the "decouple-architecture" branch was authored. Plan steps reflect the actual sequence:

1. Read prior governance (`AGENTS.md`, `RESEARCH.md`, `PROMPT.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `FRUSTRATED.md`) and the obsidian-frontmatter spec to anchor the ontology.
2. Author `TASK.md` with L0/L1/L2 ontology, Gherkin scenarios, pre-commit checks, anti-patterns.
3. Refactor `PROMPT.md` so research proposals and follow-ups deposit in `/prompts/`.
4. Refactor `RESEARCH.md` to execution-only; route open questions outward to `/prompts/`.
5. Refactor `FOLDERS.md` to document the `Task → Prompt → Research` audit graph and frontmatter-as-source-of-truth.
6. Rename `/prompt/` → `/prompts/`.
7. Update `AGENTS.md` with task-type routing.
8. Instantiate `/tasks/001-refactor-governance-from-specs/` with linked prompt skeleton.
9. *(Second pass)* Update `PRE_COMMIT.md` to invoke `TASK.md` and `tools/validate-frontmatter.py`.
10. Ship `/templates/` (task.md, prompt.md, research-readme.md, readme.md).
11. Ship `tools/validate-frontmatter.py` plus waiver mechanism.
12. Retrofit `/prompts/research-prompt-from-annotations/` frontmatter.
13. Add §8 Edge Cases to `TASK.md` (concurrent numbering, multi-prompt, abandonment, resumption, sub-tasks, ad-hoc research).
14. Self-document this work as Task-000 with M10/M07/M13 reflection artifacts.

## Todo

- [x] 1. Read prior governance and ontology source.
- [x] 2. Author `TASK.md`.
- [x] 3. Refactor `PROMPT.md`.
- [x] 4. Refactor `RESEARCH.md`.
- [x] 5. Refactor `FOLDERS.md`.
- [x] 6. Rename `/prompt/` → `/prompts/`.
- [x] 7. Update `AGENTS.md`.
- [x] 8. Instantiate Task-001 (open).
- [x] 9. Update `PRE_COMMIT.md` to reference `TASK.md` and the validator.
- [x] 10. Ship `/templates/`.
- [x] 11. Ship `tools/validate-frontmatter.py` + waivers.
- [x] 12. Retrofit `/prompts/research-prompt-from-annotations/` frontmatter.
- [x] 13. Add §8 Edge Cases to `TASK.md`.
- [x] 14. Author M10/M07/M13 reflection artifacts.

## Reflection Artifacts (Constraint Block 0)

The originating prompt's frontmatter mandated three critical-thinking methods:

- [`reflection-M10-first-principles.md`](./reflection-M10-first-principles.md) — First-Principles Decomposition of Task / Prompt / Research.
- [`reflection-M07-contradictions.md`](./reflection-M07-contradictions.md) — Contradiction Log: old root specs vs. new architecture.
- [`reflection-M13-adversarial-queries.md`](./reflection-M13-adversarial-queries.md) — Adversarial Query Expansion against the chosen architecture.
- [`friction-log.md`](./friction-log.md) — FRUSTRATED.md entry.

## Links

- Spawned task: [`/tasks/001-refactor-governance-from-specs/`](../001-refactor-governance-from-specs/)
- Ontology source: [`/research/obsidian-frontmatter-agentic-spec/output/SPEC.md`](../../research/obsidian-frontmatter-agentic-spec/output/SPEC.md)
- Governing specs introduced/refactored: [`TASK.md`](../../TASK.md), [`PROMPT.md`](../../PROMPT.md), [`RESEARCH.md`](../../RESEARCH.md), [`FOLDERS.md`](../../FOLDERS.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md)
- Validator: [`tools/validate-frontmatter.py`](../../tools/validate-frontmatter.py)
- Templates: [`templates/`](../../templates/)
