---
type: note
status: draft
slug: task-032-st4-tooling-assumption-log-substance
summary: "Subtask ST-4: ship tools/check-assumption-log.py — a linter that validates the substance of `## Assumptions Log` sections in operational-folder readme.md files (FOLDERS.md F.3 + AGENTS.md §60-65), enforcing minimum-substance and currency."
created: 2026-05-06
updated: 2026-05-06
---

# ST-4: `check-assumption-log` — FOLDERS.md F.3 / AGENTS.md §60-65 Enforcement

**Executor:** main-agent
**Insertion point:** `[opt]` WARN-tier — invoked over operational `readme.md` files only; never gating.

## Goal

Ship `tools/check-assumption-log.py` that scans every operational-folder `readme.md` for an `## Assumptions Log` section and validates: (a) section exists when the parent task involved a non-trivial decision, (b) entries are not stale (currency check via `updated:` frontmatter), (c) entries are non-empty (substance check).

## Falsification

Wrong cut **iff** the substance check produces too many false positives on legitimate "no assumptions" cases. Mitigation: empty section with explicit "(none)" line is permitted; the linter only flags absent-or-truly-empty.

## Inputs

- [`FOLDERS.md`](../../../FOLDERS.md) §3 (Required Content for readme.md including Assumptions Log).
- [`AGENTS.md`](../../../AGENTS.md) §60–65 (assumption-logging rule).
- All `tasks/<NNN>-<slug>/readme.md` (test corpus).
- All `research/<slug>/readme.md` (test corpus).
- `tools/fm/extract.py` (section extraction).

## Acceptance Criteria

1. **Surface.** `python3 tools/check-assumption-log.py <folder>` exits 0 (pass) or 2 (WARN).
2. **Checks.**
   - Section heading `## Assumptions Log` present.
   - Section body non-empty OR contains exact line `(none)`.
   - If parent folder's frontmatter `updated` is more recent than the readme's, surface `STALE` warning.
3. **Tests.** `tests/test_assumption_log.py` covers all three checks.
4. **Integration.** `tools/check-governance.sh` runs WARN-tier on `tasks/<NNN>-<slug>/readme.md` and `research/<slug>/readme.md`.

## Dependencies

Reuses `tools/fm/extract.py` — gracefully degrade to grep if not available.

## Estimated Effort

Small (~80 LOC + 60 LOC tests).

## Execution Brief (for the main agent — do NOT dispatch via /sc:agent)

```text
Implement tools/check-assumption-log.py.

Repo root: /home/user/agency
Branch: claude/integrate-repo-specs-cIWtI

Read first: FOLDERS.md §3, AGENTS.md §60-65, tools/fm/extract.py.

Acceptance: as documented. Python 3.11 stdlib only. WARN-tier exits.
Tests cover present/absent/stale.

When done:
  python3 -m unittest discover -s tests
  python3 tools/check-governance.sh
  Commit "feat(tools): assumption-log substance linter (Task 032 ST-4)".
  Do NOT push.
```
