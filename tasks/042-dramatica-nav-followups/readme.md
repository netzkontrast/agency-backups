---
type: readme
status: active
slug: dramatica-nav-followups
summary: "Index for Task 042 — three Task-030 follow-up items (precompile governance wire-in, term.py/aliases.py over-engineering audit, Bucket C structural-prose decision)."
created: 2026-05-06
updated: 2026-05-06
---

# Task 042 — Dramatica-Nav Follow-Ups

## Linked Navigation

- [`task.md`](./task.md) — the three follow-up items, plan, and Gherkin acceptance.
- [`/tasks/030-cleanup-dramatica-skills-corpus/`](../030-cleanup-dramatica-skills-corpus/) — predecessor; closed all four §Goal gates and surfaced these three items via `/sc:improve --introspection`.
- [`/tasks/029-adr-assumption-audit/`](../029-adr-assumption-audit/) — receives item-3 Option B input if chosen.

## Why this task exists

Task 030 closed all four §Goal gates. The post-closure `/sc:reflect` plus the PR #68 independent review surfaced ten items that belong in a follow-up rather than 030's closure commit. Three of them came from the introspection retrospective (precompile wire-in, term/aliases over-engineering audit, Bucket C structural-prose decision). Four came from subtask friction reports that 030 deliberately scoped out (alias conflicts, six entries without source YAML blocks, derived-kind schema decision, `## Mental Sex` body misattribution). Three came from PR #68 review (Bucket D triage, AGENTS.md §NO.5 amendment for precompiled, hardcoded test-count drift).

Each item carries an explicit decision point and acceptance — closure means either "shipped" or "filed as ADR input / superseded / deferred with rationale", never silent age-out.

## Phasing

1. **Phase 1 (mechanical, ship now):** Items 1, 2, 9, 10.
2. **Phase 2 (decisions, sequential):** Items 3, 4, 6, 7.
3. **Phase 3 (schema-touching, may file ADR inputs):** Items 5, 8.
