---
type: index
status: active
slug: output
summary: "Final deliverable for the spec-staleness-decision-formalization research workspace."
created: 2026-05-07
updated: 2026-05-07
---

# Output

Contains [`SPEC.md`](./SPEC.md) — the deterministic staleness-decision algorithm consumed by `tools/fm/check-task-lifecycle-classification.py` (Task 033 ST-4 / Task 039 ST-4).

## Assumptions Log

- The §1 pseudocode is the authoritative contract for ST-4; any §2 signal change MUST update §1 in lockstep.
- No alternative output format (JSON/YAML SPEC) is needed — the consuming Python helper reads §1 as documentation, not as input.
