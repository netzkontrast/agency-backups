---
type: readme
status: active
slug: 069-operationalise-adr-falsifier-triggers
summary: "Index for Task 069. Wire ADR-0008 F1-F5 and ADR-0009 F1-F3 falsifier triggers into a single recurring audit, document the cadence in MAINTENANCE.md, and amend both ADRs to cite the audit as the binding measurement mechanism."
created: 2026-05-11
updated: 2026-05-11
---

# 069 — Operationalise the ADR-0008 / ADR-0009 Falsifier-Trigger Cadence

**Status:** `open` — see [`task.md`](./task.md).

## Contents

- [`task.md`](./task.md) — Goal, Plan, Todo, Out-of-scope, Provenance, Links.
- `notes.md` — *(pending)* trigger-classification table + audit-tool baseline.
- `friction-log.md` — *(pending closure)*.

## Provenance

Authored at user request during the same session that closed Tasks 056/057/060 (commit `af97d63`) — the most consequential unaddressed item from this session's `/sc:reflect` pass.

## Assumptions Log

- The eight ADR-0008/0009 trigger predicates are stable on this branch; if either ADR is amended before this Task starts, re-classify against the amended set.
- `tools/maintenance/bundle-size-snapshot.py` is the canonical bundle-size measurement. The audit tool MUST compose it, never duplicate it.
- The Nightly Maintenance Run is the right cadence anchor — running the audit on every commit would be wasteful (the predicates are slow-moving) and running it less frequently than nightly would let a trigger fire weeks before discovery.
