---
type: index
status: active
slug: novel-architect-hard-rules-validation
summary: "Directory index for Task 073 — implement 12 Hard Rules validation as Phase 2 Gate 3 pre-write check in novel-architect-structure."
created: 2026-05-11
updated: 2026-05-11
---

# Task 073 — Hard Rules Validation (H1-H12)

**What:** Inserts a pre-Gate-3 validation step that runs the 12 Hard Rules (H1-H12) from `dramatica-theory/00-storyform-validation.md` against architecture.yaml. Failures surface in the status-view; user must fix or override before approval.

**Why here:** Without this gate, v1.0.0's Gate 3 only checks NCP schema compliance — not Dramatica storyform integrity. Schema-pass architectures can still violate Dramatica fundamentals (e.g. OS+MC in same Class), leading to drafting confusion downstream.

## Navigation

- [task.md](./task.md) — Task spec with H1-H12 checklist.

## Assumptions Log

- (none)
