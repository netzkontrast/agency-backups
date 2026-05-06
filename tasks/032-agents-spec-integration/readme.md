---
type: index
status: active
slug: task-032-folder
summary: "Folder index for Task 032 — AGENTS.md spec integration. Lifts under-cited research (adr-assumption-audit ASM-001/004/005/009, skills-skill-container-capabilities U1-U2, gemini, ncp-novel-co-authoring) into AGENTS.md and closes two enforcement gaps (NO.5, §60-65)."
created: 2026-05-06
updated: 2026-05-06
---

# Task 032 Folder

## What

Operational folder for Task 032, which integrates four under-cited research outputs into `AGENTS.md` and ships three new linters that mechanically enforce previously prose-only AGENTS.md rules.

## Files

- [`task.md`](./task.md) — Goal, Plan, Todo, Links.
- [`subtasks/`](./subtasks/) — Self-contained subtask briefings (1 research, 3 tooling, 1 spec amendment).

## Assumptions Log

- AGENTS.md edits stay within T2-Additive bounds per `MAINTENANCE.md §1` (no T3 framing changes).
- Subtask 05 (spec amendment) runs only after subtask 01 (research) produces its SPEC, but tooling subtasks 02–04 are independent and run in parallel.
