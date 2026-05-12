---
type: research
status: completed
slug: toolchain-flip-criteria
summary: "Mechanical flip criteria + single-commit flip procedure + post-flip cleanup checklist + rollback procedure for retiring the Legacy column of the three-way Legacy / Flexible / ADR toolchain matrix."
created: 2026-05-08
updated: 2026-05-08
research_phase: complete
research_executes_prompt: research-toolchain-flip-criteria
research_friction_level: FL0
---

# Research — toolchain-flip-criteria

## What and Why

Execution workspace for the prompt at [`/prompts/research-toolchain-flip-criteria/`](../../prompts/research-toolchain-flip-criteria/). The run produced [`output/SPEC.md`](./output/SPEC.md), the deliverable required by Task 039 ST-1 (Phase A, Phase 1 — Research head).

Per [RESEARCH.md](../../RESEARCH.md), every research run lives in `/research/<slug>/` where the slug equals the executing prompt's slug.

## Linked Navigation

- [`prompt.md`](./prompt.md) — Immutable run-start snapshot of the executing prompt (verbatim copy of [`../../prompts/research-toolchain-flip-criteria/prompt.md`](../../prompts/research-toolchain-flip-criteria/prompt.md)).
- [`research-prompt.md`](./research-prompt.md) — Phase 1–3 render of the executing prompt per the prompt's "research-prompt-optimizer" preamble.
- [`workspace/`](./workspace/) — Scratch notes and `session.log` (terminal/tool trace).
- [`synthesis/`](./synthesis/) — `methodology.md`, `state.md`, `post-synthesis-log.md`, `tracks.md`.
- [`reflection/`](./reflection/) — `M07-contradictions.md`, `friction-log.md` (FL0).
- [`output/`](./output/) — `SPEC.md` (the deliverable).

## Open Questions Surfaced

None. Every counter-question raised by M13 (adversarial-query expansion, `synthesis/methodology.md`) was resolvable from the on-disk corpus; no follow-up prompt under `/prompts/<new-slug>/` was needed. Per [RESEARCH.md §4.9](../../RESEARCH.md), absence of follow-ups is recorded explicitly.

## Workflow Assumptions

- The executing prompt's preamble step ("Run research-prompt-optimizer Phase 1–3. Skip Phase 1 askuser; intent canonical.") was honoured by rendering [`research-prompt.md`](./research-prompt.md) in place; no askuser pass was performed.
- The three-toolchain reality (Legacy / Flexible / ADR) — which the prompt's `brief.md` Inputs section did not pre-flag — was incorporated directly into `output/SPEC.md` §0.1 / §1 / §3.4 because Task 039 §1.1.2 makes it normative.
- Every input listed in `synthesis/methodology.md` M06 is a repo-local file already on disk at session start; no third-party fetches were performed.
- The trust-audit gate (`tools/check-trust-audit.py research/toolchain-flip-criteria/`) was rehearsed against the workspace structure before declaring `research_phase: complete`.
