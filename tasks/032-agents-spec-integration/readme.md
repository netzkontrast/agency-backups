---
type: index
status: active
slug: task-032-folder
summary: "Folder index for Task 032 — AGENTS.md spec integration. Lifts under-cited research (adr-assumption-audit ASM-001/004/005/009, skills-skill-container-capabilities U1-U2, gemini, ncp-novel-co-authoring) into AGENTS.md and closes two enforcement gaps (NO.5, §60-65)."
created: 2026-05-06
updated: 2026-05-07
---

# Task 032 Folder

## What

Operational folder for Task 032, which integrates four under-cited research outputs into `AGENTS.md` and ships three new linters that mechanically enforce previously prose-only AGENTS.md rules.

## Files

- [`task.md`](./task.md) — Goal, Plan, Todo, Links.
- [`subtasks/`](./subtasks/) — Self-contained subtask briefings (1 research, 3 tooling, 1 spec amendment).

## Assumptions Log

- AGENTS.md edits stayed within T2-Additive bounds per `MAINTENANCE.md §1` (no T3 framing changes). Confirmed at closure: only additive sections introduced (§"Theoretical Foundations", §"Skills Architecture", §"Assumption-Log Substance", a polarity advisory inside the existing RFC 2119 subsection, and a citation amendment to NO.5).
- Subtask 05 (spec amendment) ran after subtask 01 (research) produced its SPEC; tooling subtasks 02–04 were dispatched in parallel as planned.
- Pre-existing governance ERRORs surfaced by `tools/check-governance.sh` against `tasks/046-github-workflow-research/task.md` and the missing 045/046 index bullets are baseline drift outside Task 032's `task_affects_paths`; tracked by `031-sync-tasks-index-status-drift`. No remediation here per scope discipline.
- The three new linters (`check-narrative-ontology-load`, `check-rfc2119-polarity`, `check-assumption-log`) ship WARN-tier and never set FAIL=1; therefore README §6 § "linters that join the pre-commit gating pipeline" does NOT need an update (R.7 trigger does not fire). If a future task promotes any of them to gating, R.7 fires at that point.
- The 5 ratified ADRs landed at `adr_status: Proposed` so they remain excluded from the `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` block until a maintainer flips them to `Accepted`. This preserves the current empty guarded section and avoids inadvertent T3 framing changes.
