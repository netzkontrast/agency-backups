---
type: note
status: completed
slug: session-continuity-methodology
summary: "Methodology — session-continuity protocol instantiation."
created: 2026-05-07
updated: 2026-05-07
---

# Methodology

## Methods Applied

- **M06 — Specification Distillation**: extract normative clauses from Spec-I and the RESEARCH.md §4 workflow, then reduce to the smallest concrete file format that satisfies them.
- **M13 — Worked-Example Validation**: validate the proposed `state.md` shape against an existing multi-session research workspace (`research/adr-spec-research-synthesis/`) to confirm the cadence rule fits real synthesis-step boundaries.

## Out of Scope

- JSON-Schema artefact (deferred per Assumptions Log A2 in `readme.md`).
- Cross-workspace continuity (belongs to MAINTENANCE.md AGGREGATOR, not this per-workspace GATE).
