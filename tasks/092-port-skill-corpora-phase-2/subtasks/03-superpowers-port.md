---
type: note
status: active
slug: task-092-st3-superpowers-port
summary: "ST-3 (Task 092 Epic): port the Superpowers v4.0.3 keep-list into skills/superpowers-<slug>/. First port that exercises the superpowers- vendor prefix (forward-compat test already green from Task 091 ST-1)."
created: 2026-05-12
updated: 2026-05-12
---

# ST-3 — Superpowers full corpus port

**Executor:** main-agent invoking `/sc:implement` over the `Vendor=superpowers` rows of ST-1's matrix.

**Parallelism:** MAY proceed in parallel with ST-2 ONLY IF the triage matrix partitions their work non-overlappingly. Otherwise sequential after ST-2.

**Depends on:** ST-1 ([`01-triage.md`](./01-triage.md)) at `task_status: done`.

## Scope

For every row in [`../references/triage-matrix.md`](../references/triage-matrix.md) with `Vendor=superpowers` and `Decision ∈ {port, adapt}`:

- **SKILL.md.** Author `skills/superpowers-<slug>/SKILL.md` with `skill_source: "superpowers@v4.0.3"` pin. The vendor prefix is accepted by `tools/fm/validate.py::_check_skill_source` per Task 091 ST-1's `test_superpowers_vendor_prefix_accepted` regression test (already green).
- **Verbatim mirror.** Place the snapshot file's verbatim body at `skills/superpowers-<slug>/references/upstream-superpowers-<slug>.md` with the canonical attribution header.
- **Readme.** `skills/superpowers-<slug>/readme.md` per CLAUDE.md §7.
- **Hooks / lib / docs / `.claude-plugin`.** Decide per triage row: if a SessionStart hook is in scope of the upstream skill (e.g. Superpowers' `using-superpowers` injection per [Task 091 ST-1 friction-log mention of D.7](../../091-port-external-skill-corpora/friction-log.md)), the SessionStart MUST NOT ship — adapt the skill body to operate without it. Library files (`lib/*.py`, `hooks/*.sh`) bundle into `skills/superpowers-<slug>/scripts/` only when (a) they have a clear single-skill owner and (b) bundling does not pull SessionStart behaviour with them.
- **`skills/readme.md`.** New section: `## Imported from Superpowers (v4.0.3)` listing all new entries.

## Out of scope

- SuperClaude content — ST-2's scope.
- Auto-pull / re-sync from a newer Superpowers release — ADR-0011 D.9.
- Plugin packaging conformance (`.claude-plugin/plugin.json` shape) — Agency is a governance repo, not a plugin host (per ADR-0011 §10.8 out-of-scope clause).

## Special cases flagged for triage

These three Superpowers artifacts get explicit per-row triage attention because their upstream design assumes session-injection (D.7 risk):

1. **`using-superpowers`** — the meta-skill that upstream injects at SessionStart to advertise the rest of the corpus. ADR-0011 D.7 prohibits porting the injection mechanism; the skill body itself MAY port if rewritten as opt-in (user invokes `/superpowers:using-superpowers` explicitly).
2. **`hooks/session-start.sh`** — upstream SessionStart hook. ADR-0011 D.7 explicitly prohibits porting; flag as `skip` with rationale.
3. **`hooks/pre-tool-use.sh`** — if it functions as a global gate, it conflicts with Agency's pre-commit hook (`.githooks/pre-commit` → `tools/check-governance.sh`). Triage MUST decide whether the upstream hook adapts into a per-skill gate or is `skip`-classified.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: ST-3 lands the Superpowers keep-list

  # anchor: T092.3.1
  Scenario: superpowers- vendor prefix passes the validator
    Given a new skills/superpowers-<slug>/SKILL.md is committed
    When `python3 tools/fm/validate.py skills/superpowers-*/` runs
    Then exit code MUST be 0
    And every SKILL.md MUST carry skill_source: "superpowers@v4.0.3"

  # anchor: T092.3.2
  Scenario: D.7 SessionStart enforcement
    Given ST-3 is complete
    When a reader greps the new SKILL.md bodies for "SessionStart" patterns
    Then no body MUST instruct an upstream-style SessionStart injection
    And the upstream hooks/session-start.sh MUST NOT have shipped under skills/superpowers-*/

  # anchor: T092.3.3
  Scenario: T2 body cap holds across the batch
    Given ST-3 is complete
    When `python3 tools/fm/validate.py --check-body skills/superpowers-*/SKILL.md` runs
    Then exit code MUST be 0 (every body ≤ 5 KB per ADR-0011 D.6)
```

## Branch + PR shape

Branch: `claude/task-092-st3-…`. PR title: `Task 092 ST-3: Superpowers v4.0.3 corpus (~N skills)`. PR body MUST cite the special-case triage outcomes (using-superpowers, session-start.sh, pre-tool-use.sh) so the reviewer can verify D.7 enforcement.
