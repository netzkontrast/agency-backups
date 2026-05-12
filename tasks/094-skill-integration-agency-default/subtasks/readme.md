---
type: index
status: active
slug: task-094-subtasks
summary: "Subtask index for Task 094 (Skill Integration & Agency Default Surface Epic). Four sequential subtasks: ST-1 root-spec hookup + T3 enum + T1 typo sweep, ST-2 .claude/ + plugin, ST-3 5 event-driven hooks, ST-4 cleanup + Epic close."
created: 2026-05-12
updated: 2026-05-12
---

# Task 094 — Subtasks

Four sequential subtasks per the [Epic Plan section](../task.md#plan-four-sequential-subtasks). ST-1 → ST-2 → ST-3 → ST-4; each depends on its predecessor being closed `done`.

## Files

- [`01-root-spec-hookup.md`](./01-root-spec-hookup.md) — Cite every imported skill in ≥ 1 root spec; ratify the expanded `skill_kind` enum (T3 carry-forward); fix triage-note typos (T1 carry-forward).
- [`02-claude-dir-and-plugin.md`](./02-claude-dir-and-plugin.md) — Create `.claude/` directory (settings.json + skills symlink + agents re-exports) + `.claude-plugin/plugin.json` declaring `agency@1.0.0`.
- [`03-event-driven-hooks.md`](./03-event-driven-hooks.md) — Author 5 D.7-compliant hooks under `tools/hooks/`; register in `.claude/settings.json`; add `tools/check-hooks.py` governance check + test fixtures; document in `CLAUDE.md §14`.
- [`04-cleanup-and-close.md`](./04-cleanup-and-close.md) — Final governance run; flip Epic to `task_status: done`; update `tasks/readme.md`; author the Epic-level friction-log summary.

## Acceptance criteria coverage

| Epic AC anchor | Closed by |
|---|---|
| BR.94.1 — zero orphan skills | ST-1 (T094.1.1) |
| BR.94.2 — `.claude/skills/` auto-discovery | ST-2 (T094.2.1) |
| BR.94.3 — plugin validates | ST-2 (T094.2.2) |
| BR.94.4 — 5 hooks D.7-compliant | ST-3 (T094.3.1–T094.3.3) |
| BR.94.5 — T3 enum + T1 typos | ST-1 (T094.1.2 + T094.1.3) |

## Assumptions Log

- Each subtask MAY be authored as a separate PR per Agency's standard one-PR-per-subtask cadence (mirror Task 092). The dependency chain (ST-1 → ST-2 → ST-3 → ST-4) means each PR waits for its predecessor to merge.
- The carried-forward T3 + T1 absorption lands in ST-1 rather than in a separate PR; this keeps the root-spec edit surface in one commit.
