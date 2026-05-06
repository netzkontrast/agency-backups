---
type: index
status: active
slug: task-038-folder
summary: "Folder index for Task 038 — FRUSTRATED.md spec integration. Justifies the FL0-mandatory rule with research-backed evidence, mechanically gates the FL declaration on commit, and adds Gherkin acceptance criteria."
created: 2026-05-06
updated: 2026-05-06
---

# Task 038 Folder

## What

Operational folder for Task 038, reciprocal to Task 037 on the §28-vs-§2 reconciliation.

## Files

- [`task.md`](./task.md)
- [`subtasks/`](./subtasks/) — 1 research, 1 tooling, 1 spec amendment.

## Assumptions Log

- The FL0 justification subtask analyses *every* closed-task `friction-log.md` in the repo — no sampling.
- The FL declaration linter (subtask 02) parses BOTH `/research/<slug>/reflection/friction-log.md` AND PR-description `## Frustration Log` sections so it can run in either surface per FRUSTRATED.md §FL.Log.1/2.
