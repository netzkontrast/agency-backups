---
type: index
status: active
slug: promote-check-hard-rules-error-tier-overlap
summary: "Directory index for Task 092 — promote check-hard-rules.py from WARN to ERROR tier after one validation cycle on v1.1.1. Mirrors Task 064's promotion pattern."
created: 2026-05-12
updated: 2026-05-12
---

# Task 092 — Promote check-hard-rules.py to ERROR tier

**What:** WARN→ERROR promotion follow-up for the hard-rules linter that lands in Task 090. Once one full coherence-check cycle confirms zero false positives, the linter gates the pre-commit hook on H1–H12 structural Dramatica invariants.

**Why here:** Per `/sc:design` Artifact 4 + Q3 answer, all 3 new linters in Task 090 land at WARN tier first; this Task is the planned promotion path for the one that semantically warrants ERROR tier (the other two — worksheet-order, canon-status — stay WARN by design). Filed at hardening start (not at-need) so the promotion contract is discoverable.

## Navigation

- [`task.md`](./task.md) — Task spec: Goal, Promotion Preconditions, Plan, Todo, Links.

## Assumptions Log

- Task 064's WARN→ERROR promotion of `--check-body` is the precedent pattern. The falsification clause "≤250 ms runtime regression" is borrowed from it.
- H1–H12 are structural invariants (not heuristics) per `skills/novel-architect-structure/methods/validation/hard-rules.md`; their ERROR-tier gating is semantically correct. The WARN-first landing in Task 090 is purely a "warm-up cycle" risk mitigation, not a permanent state.
