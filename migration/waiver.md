---
type: note
status: active
slug: migration-waiver
summary: "Governance fully suspended during the refactor. The user has revoked all governance for the duration of the migration. tools/check-governance.sh runs are informational only; --no-verify is universally authorised for migration-related commits."
created: 2026-05-13
updated: 2026-05-13
---

# Waiver — ALL GOVERNANCE REVOKED for the duration of the migration

**The user has explicitly suspended all repository governance for the refactor window.** Quote, turn 13:

> *"The repo is Undergoing a Complete and extreme refactoring - so every Governance is Revoked"*

This document records that authorisation, defines the scope of the suspension, and lists the sunset criteria. **Until this waiver retires, `tools/check-governance.sh` runs are informational only** — its FAIL exit code does not block, gate, or imply any obligation. `--no-verify` is universally authorised for migration-related commits.

This is an **escalation** of the original waiver (which scoped the bypass to "pre-existing baseline failures only" for commits that touched `/migration/`). Turn 13 broadened the scope to **the entire refactor window**, not just baseline failures and not just migration-folder commits.

---

## 1. What's waived

`tools/check-governance.sh` currently exits non-zero on the `claude/repo-refactoring-plan-CfLY5` branch and on every recent ancestor branch. The failures fall into four pre-existing categories — **none of them are caused by the migration workspace itself**:

1. **`research/*` trust-audit shortfalls** — 13 research workspaces fail the Spec-J/K/L trust audit (schema / behavioral / governance dimensions below threshold). Inherited from prior commits.
2. **`tasks/readme.md` index-staleness** — `093-skill-subfolder-readme-audit-linter` is `done` in `task.md` but `open` in the master index. Stale index; pre-existing.
3. **`tasks/*/friction-log.md` malformed declarations** — two task friction-logs lack the canonical `Highest Frustration Level: FL[0-3]` line. Pre-existing.
4. **`tasks/*/readme.md` missing `## Assumptions Log`** — ~25 task readmes are advisory-WARN tier for the missing section; these are advisory and don't fail the gate alone, but compound with the above into the overall FAIL state.

Verified by filtering: `tools/check-governance.sh 2>&1 | grep -E '::ERROR:' | grep -v 'research/' | grep -v 'tasks/'` returns empty. **Zero errors are introduced by the migration workspace, the banner edits to CLAUDE.md / AGENTS.md, or the supersede pointer on the Roundtable 7 recap.**

## 2. Why the waiver

The migration is a **design-phase commitment** to capture in-flight planning state before context is lost. Resolving the four pre-existing categories above is **out of scope** for this work:

- Category (1) is the work of [Task 039 ST-5](../tasks/039-maintenance-spec-integration/) (trust-audit aggregator) and per-research-workspace remediation Tasks.
- Category (2) requires running `python3 tools/fm/index_diff.py` and is the close-out responsibility of whoever marked Task 093 done — not this session.
- Category (3) is the work of [Task 038 ST-2](../tasks/038-frustrated-spec-integration/) (FL linter compliance).
- Category (4) tracks against the assumption-log substance linter, advisory-tier; FOLDERS.md F.3 allows `(none)` lines, but many task readmes predate that allowance.

Forcing the migration commit to fix all four categories would either (i) bloat this PR with ~30 unrelated changes, or (ii) silently abandon the design-phase capture in this session. Both are worse than a documented bypass.

## 3. Scope of the waiver (post turn-13 escalation)

The waiver now covers **every commit during the refactor window**, regardless of which paths it touches:

- `/migration/**` — the design workspace.
- `CLAUDE.md`, `AGENTS.md`, and other root specs — banner additions + migration-phase edits to governance language.
- `decisions/` — ADR drafts + lock files when promoted from `/migration/`.
- `tools/` — `agency` CLI + `tools/fm/` + `tools/lint-*.py` changes implementing the new conventions.
- `tasks/`, `prompts/`, `research/`, `skills/` — any artifact moved to `archive/` during big-bang migration; any artifact authored under the new conventions.
- `maintenance/schemas/` — schema deltas (L1 type enum +5; L1 `purpose`/`assumptions`; new L2 schemas).
- Anything else.

The previous restriction (waiver scoped to `/migration/`-touching commits only) is **lifted by turn 13**. The next agent does not need to confirm path scope before committing.

**One narrow constraint remains:** commits should still be **single-purpose** — do not bundle unrelated work into a migration commit just because the waiver opens the gate. Maintain readable git history.

## 4. Mechanism

All commits during the refactor window use `git commit --no-verify` with this waiver cited in the commit message body:

```
Waiver: migration/waiver.md (governance suspended during refactor — turn 13).
```

Do **not** modify `.githooks/pre-commit` or `tools/check-governance.sh` to disable the gate globally — that would leak the suspension past the sunset criteria. The gate remains structurally in place; `--no-verify` is the per-commit mechanism that honours it while bypassing it.

Per [CLAUDE.md §11](../CLAUDE.md), `--no-verify` requires explicit user instruction. The user's instruction recorded for this waiver:

- Original (turn 12): *"Add a Waiver for Blocks for now"*
- Escalation (turn 13): *"The repo is Undergoing a Complete and extreme refactoring - so every Governance is Revoked"*

Both are preserved verbatim in [`original-prompt.md`](./original-prompt.md) and [`session-log.md`](./session-log.md).

## 5. Sunset criteria

The waiver retires automatically when **any one** of the following holds:

- **W.1** ADR-0013 promotes to `decisions/` and the four pre-existing failure categories are addressed by their respective owning Tasks (or by the cascade PR itself).
- **W.2** The migration is executed (`/migration/` folder deleted; locks promoted to `decisions/locks/`; root specs cascaded).
- **W.3** A maintainer formally retracts the waiver by editing this file's `status:` to `archived`.

When the waiver retires, **delete this file**, remove the `--no-verify` note from `CLAUDE.md` / `AGENTS.md` banners, and confirm `tools/check-governance.sh` exits 0 on the next migration-related commit.

## 6. Audit trail

| Commit | Files | Justification |
|---|---|---|
| (initial migration capture; SHA pending) | `/migration/*`, `CLAUDE.md`, `AGENTS.md`, `.claude/plans/roundtable-7-ontology-locks-recap.md` | Design-phase capture per user directive 2026-05-13 |

Append a row per migration-phase commit that uses the waiver.

## 7. Assumptions Log

- **Assumption W1.** `tools/check-maintenance-bypass.py` is **not** the right mechanism for this kind of bypass — it covers narrower per-error exceptions (specific diagnostic codes per file), not entire-branch waivers. Using `--no-verify` is therefore the simplest authorised path. *Status: not verified by reading the bypass script; revisit if a more elegant mechanism exists.*
- **Assumption W2.** The pre-existing failure categories listed in §1 are not regressing on this branch — i.e. baseline was already FAILing before any commit on `claude/repo-refactoring-plan-CfLY5`. *Status: verified by inspecting recent commit history; the most recent ten commits all landed atop the same baseline.*
