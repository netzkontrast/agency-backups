---
type: note
status: active
slug: adr-assumption-audit-tracks
summary: "Per-subagent track breakdown. A/B/C run in parallel-by-design; merge in REPORT.md."
created: 2026-05-05
updated: 2026-05-05
---

# Tracks

Three parallel subagents per the prompt's narrowing. Sequential execution within this session is documented in `friction-log.md` Entry 1; the artefact shape preserves parallelism.

## Track A — Subagent A (M13 Hidden Assumptions)

- **Inputs:** SPEC.md (primary); Gemini draft (secondary).
- **Output:** [`../workspace/m13-hidden-assumptions.md`](../workspace/m13-hidden-assumptions.md) — 9 ASMs across four axes; worst-case composition documented.
- **Deliverable counts:** 4 high-blast technical + 1 high-blast cultural + 4 medium = 9 ASMs; ≥ 5 contract met.

## Track B — Subagent B (M07 Implicit ADRs)

- **Inputs:** all 9 root specs + 6 tooling files.
- **Output:** [`../workspace/m07-implicit-adrs.md`](../workspace/m07-implicit-adrs.md) — 11 IADRs with priority + recommended titles; 2 inter-IADR contradictions surfaced.
- **Deliverable counts:** 5 P1 + 4 P2 + 2 P3 = 11 IADRs; ≥ 8 contract met.

## Track C — Subagent C (M06+M08 Pending Decisions)

- **Inputs:** SPEC §8 (OQs); plan §6 (ODs); Track A output; Track B output.
- **Output:** [`../workspace/m06-m08-pending-decisions.md`](../workspace/m06-m08-pending-decisions.md) — 5 pre-specified PDs (PD-001..PD-005) + 2 novel (PD-006, PD-007).
- **Deliverable counts:** 7 PDs; ≥ 5 contract met (with PD-001..PD-005 explicitly addressed).

## Merge Track — REPORT.md

- **Inputs:** Tracks A, B, C outputs.
- **Output:** [`../output/REPORT.md`](../output/REPORT.md) — §0 Scope + §1–§4 (Hidden Assumptions / Implicit ADRs / Pending Decisions / Recommended Actions).
- **Synthesis discipline:** every Recommended Action in §4 maps back to ≥ 1 numbered finding in §1–§3 by ID.

## Sequencing Diagram

```text
A (M13) ─────────┐
B (M07) ─────────┼──► C (M06+M08) ──► REPORT.md §1–§3
                 │                          │
                 └──────────────────────────┴──► REPORT.md §4 (Recommended Actions)
```

C consumes A and B (per its triangulation contract); the synthesis into REPORT.md §1–§3 is a copy-with-restructure (sort by blast radius / priority / blocking dependency); §4 is the only synthetic content.
