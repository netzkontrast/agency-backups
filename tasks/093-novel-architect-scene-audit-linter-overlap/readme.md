---
type: index
status: active
slug: novel-architect-scene-audit-linter-overlap
summary: "Directory index for Task 093 — the 4th deferred CLI linter from v1.1.0. Validates Q1–Q5 scene-audit completeness; blocked by Task 090 because scene-level-bridge.md content shifts during scene graduation."
created: 2026-05-12
updated: 2026-05-12
---

# Task 093 — check-scene-audit.py linter

**What:** Ship the 4th deferred linter (`tools/check-scene-audit.py`) that validates scene-level entries carry the Q1–Q5 audit fields per `scene-level-bridge.md`. WARN-tier on initial landing.

**Why here:** The other 3 deferred linters (worksheet-order, hard-rules, canon-status) land in Task 090; this one was sequenced separately because its target spec (`scene-level-bridge.md`) shifts location and may shift content during Task 090's scene-graduation commit cluster (B.1). Filing scene-audit *after* scene graduation prevents authoring the linter against an obsolete spec path.

## Navigation

- [`task.md`](./task.md) — Task spec: Goal, Plan, Todo, Links.

## Assumptions Log

- The Q1–Q5 schema in the post-graduation `scene-level-bridge.md` is stable enough to encode as linter rules. If Task 090 reshapes the schema substantively, this Task's plan §2 may surface that change as a finding before linter implementation begins.
- WARN-tier on initial landing mirrors the other 3 linters in Task 090 (per `/sc:design` Artifact 4 + Q3 answer). Promotion to ERROR is out of scope for this Task; if warranted, a separate Task analogous to Task 092 would be filed.
