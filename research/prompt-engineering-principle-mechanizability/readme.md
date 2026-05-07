---
type: index
status: active
slug: prompt-engineering-principle-mechanizability
summary: "Research index for the per-principle empirical assessment of PROMPT.md §5.1–§5.7 (mechanizability of prompt-engineering principles)."
created: 2026-05-06
updated: 2026-05-07
research_phase: complete
research_friction_level: FL0
---

# Prompt-Engineering Principle Mechanizability

This folder records the corpus-empirical assessment of the seven prompt-engineering principles enumerated in `PROMPT.md` §5.1–§5.7. For each principle the research evaluates: (a) whether it is mechanically expressible as a linter rule, (b) the proposed tool/heuristic, (c) the false-positive rate measured against the active `/prompts/<slug>/prompt.md` corpus (n=15 stratified sample drawn from N=72), and (d) the recommended verdict (ERROR, WARN, or human-review).

- [Output](./output/) — `SPEC.md` (the main deliverable) and its index.
- [Reflection](./reflection/) — friction log and reflection index.
- [Prompt](./prompt.md) — the rendered research prompt that produced this folder.

## Assumptions Log

- The active prompt corpus at execution time is the set returned by `find /home/user/agency/prompts -maxdepth 2 -name prompt.md` (N=72 files). New prompts authored after 2026-05-07 are out of scope for the empirical FPR figures in `output/SPEC.md`.
- The eight canonical external-context phrases listed in `output/SPEC.md` §3.1.2 are the agreed-upon WARN-tier signal set for the v1 self-containedness checker. Expanding or pruning the phrase list MUST trigger an FPR re-measurement against the current corpus.
- The five canonical framework values in `output/SPEC.md` §3.2.1 (`RISEN`, `RISE-DX`, `ReAct`, `RISEN+ReAct`, `CoT`) match `PROMPT.md` §3 frontmatter schema and §4.3 selection guide. Any extension MUST be ratified via an ADR amending `PROMPT.md` §4.3.
- The `prompt.md` sibling in this folder is a `type: note` snapshot of the canonical executable prompt at `/prompts/research-prompt-engineering-principle-mechanizability/prompt.md`; the canonical version is the source of truth for re-runs.
