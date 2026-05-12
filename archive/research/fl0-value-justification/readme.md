---
type: research
status: archived
slug: fl0-value-justification
summary: "Empirical study of the FL0-mandatory rule across all 60 closed-task and research friction logs. Distribution: 23 FL0 / 30 FL1 / 6 FL2 / 1 FL3. Verdict: mandate FL0 (clarified). FL0 entries provide a falsifiable null baseline that lets the maintenance run distinguish 'no friction' from 'no log'; absence-of-log is the failure mode the rule prevents."
created: 2026-05-07
updated: 2026-05-12
research_phase: archived
research_executes_prompt: research-fl0-value-justification
research_friction_level: FL0
---

# Research — fl0-value-justification

**What is this folder?** Execution workspace for the prompt at [`/prompts/research-fl0-value-justification/`](../../prompts/research-fl0-value-justification/).

**Why is it here?** Per [RESEARCH.md](../../RESEARCH.md), every research run lives in `/research/<slug>/` where the slug equals the executing prompt's slug.

## Contents

- [`output/SPEC.md`](./output/SPEC.md) — Final deliverable: empirical FL0 stats, drop-in §FL.0 paragraph for FRUSTRATED.md, verdict.
- [`reflection/friction-log.md`](./reflection/friction-log.md) — FL declaration for this run.
- `workspace/` — empty (analysis was inline).
- `synthesis/` — empty (single-output study).

## Open Questions Surfaced

None for this run. The §FL.Log mechanical-enforcement question is consumed downstream by Task 038 ST-2 (`tools/check-fl-declaration.py`).

## Assumptions Log

- The 60 friction-log corpus is the population, not a sample — `find tasks research -name friction-log.md` enumerated every log present in the tree at 2026-05-07.
- FL0 entries with bare `FL0` (no full canonical line) are still counted as FL0; the linter (ST-2) accepts a documented variant set so the empirical signal is not lost to format pedantry.
