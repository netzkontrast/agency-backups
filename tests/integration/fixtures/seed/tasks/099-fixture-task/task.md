---
type: task
status: active
slug: fixture-task
summary: "Minimal valid Task in the integration-test triptych fixture; exists so the validator and lint-structure linters have a real folder to walk."
created: 2026-05-13
updated: 2026-05-13
task_id: "099"
task_status: done
task_owner: "fixture"
task_priority: P3
task_uses_prompts:
  - fixture-prompt
task_spawns_research:
  - fixture-research
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - tests/integration/fixtures/seed/
---

# Task 099 — Fixture Task

## Goal

Hold a falsifiable single-line outcome the integration test can mutate.

## Plan

1. Be valid against every TASK.md §7.0 invariant by default.
2. Allow each mutator test to invert exactly one invariant.

## Todo

- [x] 1. Provide a minimal but complete task.md.
- [x] 2. Link to the fixture-prompt and fixture-research siblings.

## Links

- Executing prompt: [`/prompts/fixture-prompt/prompt.md`](../../prompts/fixture-prompt/prompt.md)
- Spawned research: [`/research/fixture-research/`](../../research/fixture-research/)
