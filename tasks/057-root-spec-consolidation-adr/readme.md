---
type: readme
status: active
slug: 057-root-spec-consolidation-adr
summary: "Index for Task 057. ADR-class evaluation of consolidating PRE_COMMIT.md -> AGENTS.md and FRUSTRATED.md -> MAINTENANCE.md."
created: 2026-05-07
updated: 2026-05-11
---

# 057 — Root-Spec Consolidation (ADR)

**Status:** `done` — see [`task.md`](./task.md). Outcome: [ADR-0009 `root-spec-no-consolidation`](../../decisions/0009-root-spec-no-consolidation.md) ratified at `adr_status: Proposed` with three falsifier triggers (F1–F3). Measured bundle: 11 specs, ~70,676 tokens. Optimistic merge saving: ~0.85–1.55 %. Migration cost: 381 cross-reference rewrites + 5 in-flight Tasks disrupted. Verdict: below-threshold ratio; defer.

## Contents

- [`task.md`](./task.md) — Goal, Plan, Todo, Links.
- [`notes.md`](./notes.md) — Bundle measurements (11-file table), cross-reference rewrite-cost audit (381 files, 2 anchors), in-flight Task dependency audit (5 Tasks), sibling-pattern note with ADR-0008.
- [`friction-log.md`](./friction-log.md) — FL0 closure.

## Assumptions Log

(none)

## Provenance

Dispatched from [Task 053](../053-core-architecture-review-followups/) finding B.6 (root-spec proliferation; high session-boot token cost).
