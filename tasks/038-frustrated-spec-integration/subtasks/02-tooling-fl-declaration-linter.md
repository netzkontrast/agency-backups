---
type: note
status: draft
slug: task-038-st2-tooling-fl-declaration-linter
summary: "Subtask ST-2: ship tools/check-fl-declaration.py — parses friction-log.md + PR descriptions for the canonical 'Highest Frustration Level: FL[0-3]' line; rejects malformed/missing on task closure."
created: 2026-05-06
updated: 2026-05-06
---

# ST-2: `check-fl-declaration` — Mechanical FL-Declaration Gate

**Executor:** main-agent

**Insertion point:** `[trust]` step — extends `tools/check-trust.py` rather than introducing a parallel pipeline.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — runs alongside ST-1 but soft-depends on ST-1 SPEC §2 (variant-form set). Phase A may ship with strict canonical form + upgrade post-ST-1.

## Goal

Ship `tools/check-fl-declaration.py` that parses `friction-log.md` (research) and PR-description `## Frustration Log` sections (standard), validates the presence of a canonical `Highest Frustration Level: FL[0-3]` line, and rejects task closure when the declaration is missing or malformed. Closes the FRUSTRATED.md enforcement gap.

## Falsification

Wrong cut **iff** the canonical-format regex is too strict and rejects legitimate variations (`Final FL: FL2`, `FL2 declared`). Mitigation: ST-1's research output enumerates the variant forms found in the existing corpus; the linter accepts that bounded set.

## Inputs

- ST-1 output: `research/fl0-value-justification/output/SPEC.md` §2 (variant forms in corpus).
- `FRUSTRATED.md` (FL.Log.1, FL.Log.2 — both surfaces).
- `TASK.md` §313 (existence enforcement; ST-2 adds substance enforcement).
- `tools/check-trust.py` (the existing extension point).
- `tools/adr/runlog.py` (diagnostic format prior art).

## Acceptance Criteria

1. **Surface.** `python3 tools/check-fl-declaration.py <task-folder-or-pr-body>` exits 0/1.
2. **Heuristic.** Parse `friction-log.md` first; fall back to PR-description `## Frustration Log` section; reject only if neither surface has a parseable declaration.
3. **Diagnostic format.** `<relpath>::ERROR:FR.B.4:<missing|malformed>:<details>`.
4. **Tests.** `tests/test_fl_declaration.py` covers: clean FL0, clean FL2, missing log, malformed value, both surfaces present (no warn).
5. **Integration.** Hooked into `tools/check-trust.py` for tasks transitioning to `done`.

## Dependencies

ST-1 SHOULD land first (provides variant-form set). If absent, ST-2 ships with the strict canonical form only and is upgraded post-ST-1.

## Estimated Effort

Small (~80 LOC + 80 LOC tests).
