---
type: task
status: active
slug: promote-check-hard-rules-error-tier
summary: "Promote tools/check-hard-rules.py from WARN (exit 2, advisory) to ERROR (exit 1, gating) in tools/check-governance.sh after one validation cycle on v1.1.1. Mirrors Task 064's --check-body WARN→ERROR promotion pattern. Blocked by Task 083 (hardening introduces the linter at WARN tier; promotion requires real-corpus evidence of zero false positives)."
created: 2026-05-12
updated: 2026-05-12
task_id: "085"
task_status: blocked
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - 083
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - tools/check-hard-rules.py
  - tools/check-governance.sh
  - tools/tests/test_check_hard_rules.py
---

# Task 085 — Promote check-hard-rules.py to ERROR tier

## Goal

Promote `tools/check-hard-rules.py` from WARN-tier advisory (exit 2, wrapped in `... || true` in `check-governance.sh`) to ERROR-tier gating (exit 1, blocks the pre-commit hook). H1–H12 are structural Dramatica invariants — violating them breaks the storyform model — so they SHOULD gate the pre-commit hook once we have evidence the linter does not produce false positives on the existing corpus.

The Task is `done` when:

1. `check-governance.sh` invokes `check-hard-rules.py` without the `|| true` wrapper.
2. A passing test corpus is documented (`tools/tests/fixtures/storyform-valid-corpus/`).
3. Promotion is reviewed against a falsification clause analogous to Task 064: if the promotion adds >250 ms to `check-governance.sh` on the 498-file corpus, the wiring is wrong and the promotion is reverted.

## Promotion Preconditions

This Task remains `task_status: blocked` until ALL hold:

- **(a)** Task 083 has landed (the linter exists at WARN tier).
- **(b)** At least one full coherence-check cycle (per `MAINTENANCE.md §2`) has run with the WARN-tier linter active, and the operator confirms **zero false positives** on the existing corpus.
- **(c)** Any real-corpus H-rule violations surfaced by the WARN cycle have been either (i) fixed in their source files, or (ii) documented with explicit override rationales.

## Plan

1. Audit WARN-tier diagnostic output across the existing storyform corpus (`/home/claude/novel-projects/*/canon/*.yaml` if accessible; `skills/novel-architect/examples/*.yaml` otherwise).
2. For each diagnostic: classify as TRUE_POSITIVE (fix or override) or FALSE_POSITIVE (linter bug — fix in this Task before promoting).
3. Edit `tools/check-governance.sh`: drop the `|| true` wrapper from the `check-hard-rules.py` invocation; ensure exit propagation.
4. Add a regression test: `tools/tests/test_check_governance_hard_rules_gating.py` that synthesizes a known-failing storyform and asserts `check-governance.sh` exits 1.
5. Measure `check-governance.sh` runtime delta before/after promotion; record in friction-log. If delta > 250 ms, profile and optimize (e.g., cache nav.py ontology lookups) before promoting.
6. Update `MAINTENANCE.md §1` repair-tier table if needed (H-rule violations become T2/T3 categories).

## Todo

- [ ] 1. Wait for blocker [Task 083](../083-novel-architect-v111-hardening/task.md) to close
- [ ] 2. Run `check-governance.sh` with WARN-tier hard-rules active across full corpus; capture diagnostic output
- [ ] 3. Triage diagnostics → fix-list + override-list
- [ ] 4. Drop `|| true` wrapper in `check-governance.sh`
- [ ] 5. Add gating regression test
- [ ] 6. Measure runtime delta; profile if >250 ms
- [ ] 7. Update `MAINTENANCE.md §1` repair tiers if applicable
- [ ] 8. Run governance gate → exit 0
- [ ] 9. Friction log + PR

## Links

- Blocker: [Task 083 — novel-architect-v111-hardening](../083-novel-architect-v111-hardening/task.md)
- Precedent pattern: [Task 064 — promote-check-body-to-gating](../064-improve-maintenance-spec-may-08-2026/) (analogous WARN→ERROR promotion)
- Linter source spec: [`skills/novel-architect-structure/methods/validation/hard-rules.md`](../../skills/novel-architect-structure/methods/validation/hard-rules.md)
- Governing specs: [`MAINTENANCE.md`](../../MAINTENANCE.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md)
