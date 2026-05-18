---
type: index
status: active
slug: skills-skill-jules-portability
summary: "Research output: Jules loads AGENTS.md as native custom-instruction format; SKILL.md is incompatible and requires an AGENTS.md adapter. Source: external Jules architecture analysis (Gemini 3 era)."
created: 2026-05-18
updated: 2026-05-18
---

# /research/skills-skill-jules-portability/

Research output for the `skills-skill-jules-portability` follow-up prompt. Closes U4 in `research/skills-skill-architecture/output/SPEC.md`.

The original question (filed 2026-05-04) was: *how does Jules load custom instructions, is SKILL.md natively compatible, and is an adapter needed?* This output answers that question on the basis of an externally-captured Jules architecture analysis (Gemini 3 era), pasted by the user on 2026-05-18.

## Linked Navigation

| File | Purpose |
|---|---|
| [output/SPEC.md](./output/SPEC.md) | The answer: AGENTS.md is Jules' native format, SKILL.md is not compatible, an adapter is required. |
| [output/source-jules-architecture.md](./output/source-jules-architecture.md) | Verbatim source: external Jules architecture analysis, captured 2026-05-18. |
| [../../prompts/skills-skill-jules-portability/](../../prompts/skills-skill-jules-portability/) | The originating follow-up prompt sibling. |

## Assumptions Log

- The research source is an externally-pasted architecture analysis rather than a live empirical inspection of a Jules sandbox. Findings are taken at face value; FL2 (external research consumed) is the appropriate friction level for this kind of output.
- This run produces only `readme.md` + `output/` and intentionally omits `workspace/`, `synthesis/`, and `reflection/` — the research was not executed inside the repo; it was an ingestion of external material.
- The recommended adapter at §4 of `output/SPEC.md` is described at the conceptual level only. Implementation is a future feature, not a deliverable of this research.
