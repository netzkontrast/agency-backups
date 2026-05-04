---
type: index
status: active
slug: task-003-analyze-skillmd-novel-authoring
summary: "Folder index for Task 003 — analyze Gemini SKILL.md novel-authoring research (DE/EN) and extract actionable recommendations."
created: 2026-05-04
updated: 2026-05-04
---

# Task 003 — Folder Index

**What is this folder?** Workspace for the downstream analysis of the externally-sourced Gemini research on SKILL.md-conformant novel-authoring GitHub repositories (DE/EN).

**Why is it here?** Per `RESEARCH.md` §6.5, every ingested external result MUST have an open downstream analysis Task created in the same commit. This folder fulfils that requirement for `research/gemini/github-skillmd-novel-authoring-de-en/result.md`.

## Contents

- [`task.md`](./task.md) — The Task spec (goal, plan, todo, links).

## Workflow Assumptions

- `output/RECOMMENDATIONS.md` will be committed here once analysis is complete.
- Follow-up prompts spawned during analysis live in `/prompts/`, not here.
- If analysis warrants a full synthesis run, a research workspace will be created under `/research/` and its slug listed in `task_spawns_research`.
