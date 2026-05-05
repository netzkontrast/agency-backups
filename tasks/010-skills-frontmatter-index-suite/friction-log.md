---
type: note
status: active
slug: 010-friction-log
summary: "Friction log for Task 010 closing as 'updated' — predecessor of Task 022."
created: 2026-05-05
updated: 2026-05-05
---

# Friction Log — Task 010

## FL Declaration

**FL0** — plan obsolesced cleanly. The original persistent-index strategy is explicitly superseded by the stateless toolchain shipped under Task 016. No friction encountered during closure: the supersession is documented in the source spec.

## Supersession Rationale

[`research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) §C1 states verbatim: *"supersedes the persistent-index strategy proposed in tasks/010-skills-frontmatter-index-suite/"*. The four-tool atomic surface (`fm-validate`, `fm-extract`, `fm-edit`, `fm-query`) replaces the proposed `tools/build-frontmatter-index.py` + `.agent_cache/frontmatter-index.json` approach with stateless walks. The spec's Q3/Q4 acceptance scenarios show how the ten canonical questions Task 010 enumerated can be answered via composable `fm-query` filters at no extra cost.

The continuation lives at [`/tasks/022-skills-query-cli-atop-fm-query/`](../022-skills-query-cli-atop-fm-query/), which carries forward the *user-facing* outcome (a thin convenience wrapper for the ten canonical questions) without rebuilding any index.

## Pointers

- Successor: [`../022-skills-query-cli-atop-fm-query/task.md`](../022-skills-query-cli-atop-fm-query/task.md)
- Source spec: [`research/flexible-frontmatter-toolchain/output/SPEC.md §C1`](../../research/flexible-frontmatter-toolchain/output/SPEC.md)
- Lineage governance: [`TASK.md §4.7`](../../TASK.md), [`MAINTENANCE.md §3.4`](../../MAINTENANCE.md).
