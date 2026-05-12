---
type: index
status: active
slug: toolchain-flip-criteria-synthesis
summary: "Synthesis artifacts for the toolchain-flip-criteria research run — methodology, state, post-synthesis log, tracks."
created: 2026-05-08
updated: 2026-05-08
---

# Synthesis — toolchain-flip-criteria

## What and Why

Holds the structured merge artifacts produced while drafting [`../output/SPEC.md`](../output/SPEC.md). Per [RESEARCH.md §4.6](../../../RESEARCH.md), synthesis is the flat structured layer between scratch (workspace) and reflection.

## Linked Navigation

- [`methodology.md`](./methodology.md) — M06 source triangulation, M08 pre-commitment, M07 / M13 cross-references.
- [`state.md`](./state.md) — Synthesis-step checklist (S0–S6).
- [`post-synthesis-log.md`](./post-synthesis-log.md) — Chronological merge log keyed to the state checklist.
- [`tracks.md`](./tracks.md) — Per-track work breakdown (A: checklist; B: procedure + cleanup + rollback).

## Assumptions Log

- Synthesis is flat (single-file-per-purpose) per FOLDERS.md §3.5; nesting is unnecessary at the four-file scale of this run.
- `methodology.md` is treated as REQUIRED for trust-audit behavioral score, even though RESEARCH.md §5 does not yet make it normatively REQUIRED (see PR #88 review D1 in `tools/check-trust-audit.py`). Including it is cheap and keeps the workspace at the post-flip 0.90 threshold rather than only the 0.80 migration-window floor.
