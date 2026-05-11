---
type: task
status: active
slug: operationalise-adr-falsifier-triggers
summary: "ADR-0008 (F1-F5) and ADR-0009 (F1-F3) record eight falsifier triggers that re-open the decisions when fired. Without a recurring measurement cadence none of them fire on their own; the decisions stay 'Proposed' forever. This Task wires each mechanical trigger into a single check + documents the cadence in MAINTENANCE.md."
created: 2026-05-11
updated: 2026-05-11
task_id: "069"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - tools/maintenance/
  - tools/maintenance/bundle-size-snapshot.py
  - tools/maintenance/adr-trigger-audit.py
  - MAINTENANCE.md
  - maintenance/run-log.md
  - decisions/0008-narrative-skills-status-quo.md
  - decisions/0009-root-spec-no-consolidation.md
---

# Task 069 — Operationalise the ADR-0008 / ADR-0009 Falsifier-Trigger Cadence

## Goal

[ADR-0008](../../decisions/0008-narrative-skills-status-quo.md) and [ADR-0009](../../decisions/0009-root-spec-no-consolidation.md) (landed by Tasks 056 + 057, this session) each ratify *status quo* with a set of falsifier triggers: when any trigger fires, a successor ADR MUST be authored that re-evaluates the chosen option. There are eight triggers in total — five in ADR-0008 (F1–F5) and three in ADR-0009 (F1–F3).

**The triggers are mechanical predicates with no operational cadence.** [`tools/maintenance/bundle-size-snapshot.py`](../../tools/maintenance/bundle-size-snapshot.py) (shipped this session, commit `af97d63`) makes ADR-0009 F1 measurable on demand, but nothing runs it on a schedule, and the other seven triggers have no measurement script at all. As-is, the "measure the friction, then act" pattern collapses to "guess-and-hope."

The single falsifiable outcome of this Task: a maintainer can run **one** CLI invocation (`python3 tools/maintenance/adr-trigger-audit.py` or equivalent) and receive a single report covering every ADR-0008 / ADR-0009 trigger's current state (under/over threshold), with the report format wired into `maintenance/run-log.md` and the audit's invocation cadence documented in `MAINTENANCE.md §X` as a binding routine (not a SHOULD-suggestion).

## Plan

1. **Classify each trigger.** Audit all eight triggers and tag each as `mechanical` (computable from filesystem + frontmatter), `semi-mechanical` (computable but requires aggregating prose, e.g. friction-log lines), or `manual` (requires human judgement, e.g. third-party-adopter feedback). Record the classification table in `notes.md`.

   - ADR-0008 F1 — skill count > 10 → **mechanical** (count `skills/<narrative-name>/` directories).
   - ADR-0008 F2 — bootstrap bundle > 60K tokens → **mechanical** (overlaps with ADR-0009 F1; bundle-size-snapshot.py already handles).
   - ADR-0008 F3 — sustained NO.5-cited FL1+ friction across 3+ sessions in 14 days → **semi-mechanical** (grep friction-logs for NO.5 mentions + FL1+).
   - ADR-0008 F4 — narrative T3 amendment of non-AGENTS root spec → **mechanical** (audit `task_affects_paths` of recent narrative-tagged tasks).
   - ADR-0008 F5 — third-party adopter blocker → **manual** (no signal in repo).
   - ADR-0009 F1 — bundle > 100K tokens → **mechanical** (bundle-size-snapshot.py already handles).
   - ADR-0009 F2 — either spec < 1000 tokens AND < 50 dependents → **mechanical** (extend bundle-size-snapshot.py with per-spec dependent-count via grep).
   - ADR-0009 F3 — sustained bundle-size-cited FL1+ friction across 3+ sessions in 14 days → **semi-mechanical**.

2. **Ship `tools/maintenance/adr-trigger-audit.py`.** A pure-stdlib (+ optional PyYAML) script that:
   - Calls `bundle-size-snapshot.measure_bundle()` (reuse, do not duplicate).
   - Counts narrative-skill directories via the `AGENTS.md NO.*` rule glob.
   - Aggregates FL declarations from `tasks/*/friction-log.md` over the last N days (N defaults to 14 per the spec).
   - Walks each ADR's frontmatter for an `adr_triggers:` list (or hard-codes the ADR-0008 / ADR-0009 trigger set; the trigger-discovery mechanism is a sub-decision recorded in `notes.md`).
   - Emits one diagnostic line per trigger in canonical `<path>::<level>:<code>:<msg>` form.
   - Exits 0 on no fires; 2 on advisory fires (one or more triggers crossed threshold).

3. **Extend `bundle-size-snapshot.py` with per-spec dependent counts.** ADR-0009 F2 needs `< 50 dependents`; add a `dependents` field to each per-spec record via `grep -rl <spec> --include="*.md" --include="*.py" --include="*.sh"`. Update the existing 9-test pytest suite to cover the new field.

4. **Add 6+ new tests for `adr-trigger-audit.py`.** One per trigger classification: mechanical-clean, mechanical-fires, semi-mechanical-aggregation, manual-skip, all-clean roll-up, exit-code matrix.

5. **Wire the audit into `MAINTENANCE.md §3.X`** (new subsection — pick the lowest-impact insertion point). The audit MUST run on the Nightly Maintenance Run cadence (`MAINTENANCE.md §2`). Document the runlog format the audit appends: one line per ADR per trigger, the same shape `bundle-size-snapshot.py --format runlog` already emits.

6. **Update both ADRs' `## Decision Outcome` sections** (still `adr_status: Proposed`, so mutable per the protocol) to cite the new audit tool as the binding measurement mechanism for the trigger set. The trigger predicate prose stays unchanged; only the "how we test this" footnote is added.

7. **Verify by running the audit end-to-end** against the current repo. Record the baseline in `notes.md`. Confirm bundle-size-snapshot's existing baseline (~70,676 tokens / 11 specs) is reproduced and no trigger currently fires.

## Todo

- [ ] 1. Classify all eight triggers in `notes.md` (mechanical / semi-mechanical / manual table).
- [ ] 2. Ship `tools/maintenance/adr-trigger-audit.py` (composes `bundle-size-snapshot.py`; never duplicates its logic).
- [ ] 3. Extend `bundle-size-snapshot.py` to emit a `dependents` count per spec; backport into the existing 9-test suite.
- [ ] 4. Author ≥ 6 tests for `adr-trigger-audit.py` under `tools/tests/maintenance/test_adr_trigger_audit.py`.
- [ ] 5. Amend `MAINTENANCE.md` with a new subsection wiring the audit into the Nightly Maintenance Run cadence; document the runlog projection format.
- [ ] 6. Amend ADR-0008 + ADR-0009 (`Proposed` → still `Proposed`) to cite `tools/maintenance/adr-trigger-audit.py` as the binding measurement mechanism.
- [ ] 7. Run the audit; record baseline in `notes.md`; assert no trigger fires (regression-tested against ADR-0009 F1 = 70,676 tokens).
- [ ] 8. Write `friction-log.md` with FL[0–3] declaration on closure.

## Out of scope

- **Manual triggers** (ADR-0008 F5 — third-party-adopter blocker) MUST surface as `MANUAL` in the audit report rather than a fire/no-fire predicate; the audit cannot synthesise the missing signal.
- **Ratifying ADR-0008 / ADR-0009 from `Proposed` → `Accepted`.** Status promotion is a maintainer call (sustained-90-day window or explicit confirmation per the ADRs' §"Status note"); this Task only makes the trigger measurements available, not the ratification itself.
- **Falsifier triggers in earlier ADRs (ADR-0001..ADR-0007).** Those ADRs do not use the falsifier-trigger pattern; this Task is scoped to ADR-0008 and ADR-0009. If a future ADR adopts the pattern, this Task's `adr-trigger-audit.py` SHOULD generalise via the `adr_triggers:` frontmatter approach noted in Plan step 2.

## Provenance

This Task was authored at user request during the same session that closed Tasks 056/057/060 and shipped `tools/maintenance/bundle-size-snapshot.py` (commit `af97d63`). It is the most consequential unaddressed item from the `/sc:reflect` pass — see the reflection summary, "Insights worth carrying forward", item #3 ("Bootstrap-bundle measurements drift fast … the falsifier triggers need a re-measurement cadence to remain testable — currently none exists.").

## Links

- Parent decisions:
  - [`decisions/0008-narrative-skills-status-quo.md`](../../decisions/0008-narrative-skills-status-quo.md) §"Falsifier triggers" (F1–F5).
  - [`decisions/0009-root-spec-no-consolidation.md`](../../decisions/0009-root-spec-no-consolidation.md) §"Falsifier triggers" (F1–F3).
- Existing infrastructure to compose: [`tools/maintenance/bundle-size-snapshot.py`](../../tools/maintenance/bundle-size-snapshot.py) (Task 057 follow-on, commit `af97d63`).
- Maintenance routine to extend: [`MAINTENANCE.md §2`](../../MAINTENANCE.md) (Nightly Maintenance Run) and [§3.X](../../MAINTENANCE.md) (new subsection TBD).
- Governing specs: [`TASK.md`](../../TASK.md), [`MAINTENANCE.md`](../../MAINTENANCE.md), [`research/adr-spec-research-synthesis/output/SPEC.md`](../../research/adr-spec-research-synthesis/output/SPEC.md).
