---
type: research
status: completed
slug: adr-spec-research-synthesis
summary: "Research workspace executing the adr-spec-research-synthesis prompt. Produces the repo-native ADR governance specification (output/SPEC.md) integrating the Gemini draft with this repo's actual conventions."
created: 2026-05-05
updated: 2026-05-05
research_phase: complete
research_executes_prompt: adr-spec-research-synthesis
research_friction_level: FL1
---

# Research — ADR Spec Research Synthesis

This workspace executes [`/prompts/adr-spec-research-synthesis/prompt.md`](../../prompts/adr-spec-research-synthesis/prompt.md). It is driven by [Task 027](../../tasks/027-adr-spec-research-synthesis/task.md) and produces the canonical ADR governance specification for `netzkontrast/agency`.

## Layout

- [`prompt.md`](./prompt.md) — Immutable run-start snapshot of the executing prompt.
- [`workspace/`](./workspace/) — Scratch artefacts: `/sc:analyze` notes, `/sc:brainstorm` notes, session log.
- [`synthesis/`](./synthesis/) — Structured synthesis: methodology, tracks, post-synthesis log, state checklist.
- [`reflection/`](./reflection/) — Critical-thinking method outputs (M06, M07, M08, M13) and friction log.
- [`output/`](./output/) — Final deliverable: [`SPEC.md`](./output/SPEC.md).

## State

`research_phase: complete`. SPEC.md is in force as the authoritative ADR governance document for the repo. Task 028 (tooling implementation plan) and Task 029 (assumption audit) remain `open`, gated on this output.

## Open Questions Surfaced

The five `[OPEN — needs human decision]` items recorded in [`workspace/brainstorm.md`](./workspace/brainstorm.md) are surfaced in §8 of [`output/SPEC.md`](./output/SPEC.md) and routed forward to Task 029. They are not re-filed as standalone follow-up prompts because Task 029's own prompt already enumerates them as audit targets — see [`prompts/adr-assumption-audit/prompt.md`](../../prompts/adr-assumption-audit/prompt.md).

## Workflow Assumptions

- The slug equals the executing prompt's slug per `RESEARCH.md §2`.
- Workspace scripts (`.py`, `.sh`) MUST be deleted before commit — none were created during this run.
- The Gemini draft at `research/gemini/agency-adr-governance-spec/adr-governance-spec.md` is reference material; every §0–§9 block in `output/SPEC.md` was re-derived from repo evidence per the prompt's narrowing rules.
