---
type: research
status: active
slug: integrate-dramatica-ncp-skills
summary: "Research workspace for the kickoff phase of Task 013 — corpus inventory, cross-skill ID audit, and scenario-tag survey of the dramatica skills, NCP, and novel-architect."
created: 2026-05-04
updated: 2026-05-04
research_phase: kickoff
research_executes_prompt: integrate-dramatica-ncp-skills
research_friction_level: FL0
---

# Research — Integrate Dramatica Skills With NCP and Novel-Architect

## What this workspace is

The kickoff research that executes [`/prompts/integrate-dramatica-ncp-skills/prompt.md`](../../prompts/integrate-dramatica-ncp-skills/prompt.md) (currently `status: draft`) and feeds [`Task 013`](../../tasks/013-integrate-dramatica-ncp-skills/task.md). It produces three evidence streams the Task plan demands before any schema is authored: a corpus inventory of the two dramatica skills, a cross-skill ID audit, and a scenario-tag survey for the eleven persona scenarios.

## Layout

- [`prompt.md`](./prompt.md) — immutable snapshot of the executing prompt at run start.
- [`workspace/`](./workspace/) — scratch notes + chronological session log; no executable scripts.
- [`synthesis/`](./synthesis/) — flattened evidence (`inventory.md`, `id-audit.md`, `scenario-survey.md`) plus methodology, post-synthesis log, and state checklist.
- [`reflection/`](./reflection/) — per-method critical-thinking files (`M01-falsification.md`, `M07-contradiction-log.md`) plus the mandatory friction log.
- [`output/SPEC.md`](./output/SPEC.md) — the deliverable: kickoff specification consolidating findings + recommendations for downstream Task 013 plan steps 2–11.

## Open Questions Surfaced

The kickoff surfaced three open questions (OQ-A, OQ-B, OQ-C) that block the schema-authoring step. They are filed as the open-questions block of `output/SPEC.md` — promoting them to follow-up prompts under `/prompts/` is deferred until Task 013 step 14 authors the main prompt body, since the open questions partly concern *what that prompt's scope should be*.

## Governing specs

Behaviour in this folder is bound by [`RESEARCH.md`](../../RESEARCH.md). Pre-commit hygiene is enforced by `tools/check-governance.sh`.
