---
type: task
status: active
slug: novel-architect-scene-audit-linter
summary: "Ship tools/check-scene-audit.py — the 4th deferred CLI linter from the v1.1.0 friction log. Validates Q1–Q5 audit completeness in scene matrices against skills/novel-architect-scene/methods/scene-level-bridge.md. Blocked by Task 083 because scene-level-bridge.md content shifts during scene graduation (B.1)."
created: 2026-05-12
updated: 2026-05-12
task_id: "086"
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
  - tools/check-scene-audit.py
  - tools/check-governance.sh
  - tools/tests/test_check_scene_audit.py
  - tools/tests/fixtures/scene-audit-valid.md
  - tools/tests/fixtures/scene-audit-q1q2-missing.md
---

# Task 086 — check-scene-audit.py linter

## Goal

Implement `tools/check-scene-audit.py`, the 4th deferred CLI linter from [Task 070 friction-log §"Sub-task summary"](../070-novel-architect-v110-epic/friction-log.md). Validates that scene-level entries (in `scene-matrix.md` files or NCP moment schemas) carry the Q1–Q5 audit fields per `skills/novel-architect-scene/methods/scene-level-bridge.md`.

The Task is `done` when:

1. `tools/check-scene-audit.py` exists; CLI matches the pattern in `tools/check-worksheet-order.py` (argparse, `nargs="+"`, exit 0/2 PASS/WARN).
2. Validates at least the 5 Q-axis rules:
   - **Q1** throughline-dominance is present and is one of {OS, MC, IC, SS}
   - **Q2** secondary throughlines listed (≥0 acceptable; presence checked)
   - **Q3** operating-level present and ∈ {Universe, Physics, Mind, Psychology, Variation, Element}
   - **Q4** plot-story-point present and resolvable via `tools/dramatica-nav/nav.py`
   - **Q5** motivation-elements present and each element resolves to a canonical ontology ID
3. pytest fixtures: one valid scene matrix, one with Q1+Q2 missing (the canonical failure mode).
4. Wired into `tools/check-governance.sh` at WARN tier.

## Plan

1. Wait for Task 083 to close — scene-level-bridge.md content stabilizes there.
2. Read post-hardening `skills/novel-architect-scene/methods/scene-level-bridge.md` to extract the canonical Q1–Q5 schema.
3. Implement `tools/check-scene-audit.py` following the C.1–C.3 pattern from Task 083 workflow.
4. Author fixture corpus: valid scene matrix, Q1+Q2 missing variant.
5. Author `tools/tests/test_check_scene_audit.py`.
6. Wire into `tools/check-governance.sh` (WARN tier, `|| true` wrapper).
7. Run linter against any existing scene-matrix files in `/home/claude/novel-projects/*/` or `skills/novel-architect/examples/`; triage diagnostics.
8. Friction log + PR.

## Todo

- [ ] 1. Wait for blocker [Task 083](../083-novel-architect-v111-hardening/task.md) to close
- [ ] 2. Extract Q1–Q5 schema from finalized `scene-level-bridge.md`
- [ ] 3. Implement `tools/check-scene-audit.py`
- [ ] 4. Author fixture corpus (valid + Q1+Q2-missing)
- [ ] 5. Author pytest test
- [ ] 6. Wire into governance gate (WARN tier)
- [ ] 7. Real-corpus dry run; triage
- [ ] 8. Run governance gate → exit 0
- [ ] 9. Friction log + PR

## Links

- Blocker: [Task 083 — novel-architect-v111-hardening](../083-novel-architect-v111-hardening/task.md)
- Originating deferral: [Task 070 friction-log §Sub-task summary "Task 075 sequel notes"](../070-novel-architect-v110-epic/friction-log.md)
- Linter source spec: [`skills/novel-architect-scene/methods/scene-level-bridge.md`](../../skills/novel-architect-scene/methods/scene-level-bridge.md)
- Sibling linters (pattern source): `tools/check-worksheet-order.py`, `tools/check-hard-rules.py`, `tools/check-canon-status.py` (all landing in Task 083)
- Governing specs: [`PRE_COMMIT.md`](../../PRE_COMMIT.md), [`SKILLS.md`](../../SKILLS.md)
