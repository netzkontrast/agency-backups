---
type: readme
status: active
slug: 069-operationalise-adr-falsifier-triggers
summary: "Index for Task 069. Wire ADR-0008 F1-F5 and ADR-0009 F1-F3 falsifier triggers into a single recurring audit, document the cadence in MAINTENANCE.md, and amend both ADRs to cite the audit as the binding measurement mechanism."
created: 2026-05-11
updated: 2026-05-13
---

# 069 — Operationalise the ADR-0008 / ADR-0009 Falsifier-Trigger Cadence

**Status:** `done` — see [`task.md`](./task.md).

## Contents

- [`task.md`](./task.md) — Goal, Plan, Todo, Out-of-scope, Provenance, Links.
- [`notes.md`](./notes.md) — Trigger-classification table, baseline audit run, design notes.
- [`friction-log.md`](./friction-log.md) — FL1 declaration + entries.

## Outcome

- Shipped [`tools/maintenance/adr-trigger-audit.py`](../../tools/maintenance/adr-trigger-audit.py) — 8-trigger audit, composes `bundle-size-snapshot.py`, emits canonical diagnostics.
- Extended [`tools/maintenance/bundle-size-snapshot.py`](../../tools/maintenance/bundle-size-snapshot.py) with `count_dependents()` + `--include-dependents` flag for ADR-0009 F2.
- Authored 14 pytest cases at [`tools/tests/maintenance/test_adr_trigger_audit.py`](../../tools/tests/maintenance/test_adr_trigger_audit.py) (8+ required); extended bundle-size suite from 9 → 13 tests.
- Amended [`MAINTENANCE.md §3.6`](../../MAINTENANCE.md) wiring the audit into the Nightly cadence; added Gherkin anchor M.B.8.
- Amended [`decisions/0008-narrative-skills-status-quo.md`](../../decisions/0008-narrative-skills-status-quo.md) and [`decisions/0009-root-spec-no-consolidation.md`](../../decisions/0009-root-spec-no-consolidation.md) (`Decision Outcome` "How the triggers are measured" subsection) to cite the audit as the binding measurement mechanism. Trigger predicates unchanged.

Baseline audit run (2026-05-13) surfaced two genuine ADR-0008 fires (F1 narrative-skill count + F2 bundle-token growth); see [`notes.md §3`](./notes.md) for the disposition. ADR-0009 triggers all clean.

## Provenance

Authored at user request during the same session that closed Tasks 056/057/060 (commit `af97d63`) — the most consequential unaddressed item from this session's `/sc:reflect` pass.

## Assumptions Log

- The eight ADR-0008/0009 trigger predicates are stable on this branch; if either ADR is amended before this Task starts, re-classify against the amended set.
- `tools/maintenance/bundle-size-snapshot.py` is the canonical bundle-size measurement. The audit tool MUST compose it, never duplicate it.
- The Nightly Maintenance Run is the right cadence anchor — running the audit on every commit would be wasteful (the predicates are slow-moving) and running it less frequently than nightly would let a trigger fire weeks before discovery.
