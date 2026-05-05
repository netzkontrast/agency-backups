---
type: task
status: active
slug: skills-query-cli-atop-fm-query
summary: "Successor to Task 010. The persistent-index strategy is explicitly superseded by the stateless fm-query toolchain (Task 016, SPEC §C1). Build the thin skills-query convenience wrapper that exposes Task 010's ten canonical questions atop fm-query, without rebuilding any index."
created: 2026-05-05
updated: 2026-05-05
task_id: "022"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_supersedes:
  - "010"
task_blocked_by:
  - "019"
task_affects_paths:
  - tools/fm/skills_query.py
  - tools/check-governance.sh
  - research/flexible-frontmatter-toolchain/output/SPEC.md
---

# Task 022 — Skills Query CLI atop fm-query

Successor to [Task 010](../010-skills-frontmatter-index-suite/task.md). The original Task proposed a `tools/build-frontmatter-index.py` + JSON cache strategy. That strategy is explicitly superseded by [`research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) §C1 ("supersedes the persistent-index strategy proposed in tasks/010-skills-frontmatter-index-suite/"). The current canonical surface is `tools/fm/query.py` — stateless, no cache file, walks the corpus on every call, scoped via filters.

## Goal

A `tools/fm/skills_query.py` (or equivalent thin wrapper) MUST answer the ten canonical questions from Task 010 by composing existing `fm-query` filters. No persistent index file. The Task is `done` when:

1. Each of Task 010's ten questions has a documented one-line invocation against `fm-query` or `skills_query`.
2. Token-cost measurements are recorded in `friction-log.md` (per Task 010 §Goal point 5), comparing the wrapper invocation cost vs. opening file bodies.
3. `tools/check-governance.sh` runs the wrapper as a smoke test (no diff; the wrapper is read-only).

## Plan

1. **Wait for Task 019.** This Task is gated by Task 019 (toolchain suite integration), which is delivering `fm-graph` and `fm-fix` — at least the `fm-graph` reciprocity outputs are dependencies for the skill-to-skill question.
2. **Map the ten questions.** Walk Task 010 §Plan and produce a one-row-per-question table in `notes.md` with: question, fm-query filter expression, cost-in-tokens estimate.
3. **Implement the wrapper.** A short Python module that shells into `tools/fm/query.py` with the right filter set and pretty-prints results.
4. **Document.** Add a section to [`research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) §C — keep the supersession note explicit; record the wrapper's existence as the v2 fulfilment of Task 010.
5. **Verify.** Smoke-test in `tools/check-governance.sh`.

## Todo

- [ ] 1. Confirm Task 019 has `task_status: done` before starting.
- [ ] 2. Map the ten canonical questions to `fm-query` filter expressions.
- [ ] 3. Ship `tools/fm/skills_query.py` with end-to-end tests.
- [ ] 4. Update SPEC §C with the v2 fulfilment note.
- [ ] 5. Append `friction-log.md` recording token-cost measurements (FL[0-3]).

## Links

- Predecessor: [`../010-skills-frontmatter-index-suite/task.md`](../010-skills-frontmatter-index-suite/task.md)
- Source spec: [`research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) §C1
- Blocker: [`../019-fm-toolchain-suite-integration/task.md`](../019-fm-toolchain-suite-integration/task.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`MAINTENANCE.md`](../../MAINTENANCE.md)
