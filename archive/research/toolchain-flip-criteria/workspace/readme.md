---
type: index
status: active
slug: toolchain-flip-criteria-workspace
summary: "Scratch workspace for the toolchain-flip-criteria research run — holds session.log only; no execution scripts (R.4.4)."
created: 2026-05-08
updated: 2026-05-08
---

# Workspace — toolchain-flip-criteria

## What and Why

Temporary work area for the run that produced [`../output/SPEC.md`](../output/SPEC.md). Per [RESEARCH.md §4.4](../../../RESEARCH.md), only raw notes, dumps, and `session.log` may live here; execution scripts (`.py` / `.sh`) MUST be deleted before commit (mechanical R.4.4).

## Linked Navigation

- [`session.log`](./session.log) — Chronological terminal/tool trace for the single-session run.

## Assumptions Log

- The run completed in one continuous session; no `state.md` checkpoint file is needed under this workspace because [RESEARCH.md §4.10](../../../RESEARCH.md) makes pause-and-resume `state.md` OPTIONAL for one-session runs.
- No third-party fetches were made; every input listed in `synthesis/methodology.md` is a repo-local file already on disk at session start.
