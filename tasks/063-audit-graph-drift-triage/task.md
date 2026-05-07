---
type: task
status: active
slug: audit-graph-drift-triage
summary: "Triage the 343 historical FOLDERS.md F.6 dual-surface-drift WARN findings surfaced by tools/check-audit-graph-consistency.py at Task 036 close. For each (source, target) pair, decide: add the missing frontmatter linkage, or rephrase the body to remove the implied edge. Then flip FM_AUDIT_GRAPH_STRICT=1 as the default."
created: 2026-05-07
updated: 2026-05-07
task_id: "063"
task_status: open
task_owner: "unassigned"
task_priority: P4
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - "036"
task_affects_paths:
  - tasks/
  - prompts/
  - research/
  - tools/check-governance.sh
---

# Task 063 — Audit-Graph Drift Triage

## Goal

Resolve the 343 WARN diagnostics surfaced by [`tools/check-audit-graph-consistency.py`](../../tools/check-audit-graph-consistency.py) (Task 036 ST-2) so that `FOLDERS.md F.6` dual-surface drift can be promoted from WARN to ERROR. Filed per [PR #89 review D4](../036-folders-spec-integration/review-pr89-claude-brave-darwin.md#d4) to satisfy `TASK.md §4` (discovered work-items MUST be captured as Tasks). The Task is `done` when (a) every WARN is either resolved by adding the missing frontmatter linkage, by rephrasing the body to remove the implied edge, or by an explicit waiver entry, (b) `tools/check-audit-graph-consistency.py` exits 0 against `tasks/`, `prompts/`, `research/`, and (c) `tools/check-governance.sh` flips `FM_AUDIT_GRAPH_STRICT=1` as the default in [step `[opt]`](../../tools/check-governance.sh).

## Context

Task 036 ST-2 shipped the F.6 dual-surface drift detector as WARN-tier `[opt]` precisely because the corpus carries 343 historical drift pairs — a body Markdown link cites a sibling operational folder without the corresponding frontmatter linkage. The advisory placement was a deliberate choice to land the rule without blocking Task 036's PR; this Task closes the loop.

The diagnostic shape is `<relpath>::WARN:F.6:body-link-without-frontmatter:<target-slug>`. Most findings are likely false positives from prose like "as discussed in Task 029" — the body link is informational, not a directed edge. The triage should:

1. Run `tools/check-audit-graph-consistency.py > drift-baseline.txt` and group by `(source-type, target-type)` pair.
2. For each cluster, classify the typical resolution: frontmatter-add vs. body-rephrase vs. waiver.
3. Apply the resolutions in batches (one PR per source-type to keep diffs reviewable).
4. Flip `FM_AUDIT_GRAPH_STRICT=1` as the default once the residual count is 0.

## Plan

1. Run the linter and bucket findings by `(source-type, target-type)`.
2. Sample 10 findings per bucket and classify resolution type.
3. For each bucket, batch-apply the resolution and re-scan.
4. Flip the gate.
5. Update `tasks/readme.md`, author `friction-log.md`, set `task_status: done`.

## Todo

- [ ] 1. Generate baseline snapshot of all 343 WARN findings.
- [ ] 2. Classify findings into (frontmatter-add | body-rephrase | waiver) buckets.
- [ ] 3. Apply resolutions per source-type batch (tasks → prompts → research).
- [ ] 4. Re-run linter to confirm 0 WARN.
- [ ] 5. Flip `FM_AUDIT_GRAPH_STRICT=1` in `tools/check-governance.sh`.
- [ ] 6. Run `tools/check-governance.sh` end-to-end.
- [ ] 7. Author `friction-log.md` with FL declaration.
- [ ] 8. Set `task_status: done`.

## Links

- Predecessor: [Task 036 — FOLDERS.md spec integration](../036-folders-spec-integration/task.md)
- Review of record: [`review-pr89-claude-brave-darwin.md`](../036-folders-spec-integration/review-pr89-claude-brave-darwin.md) §D4
- Governing specs: [`FOLDERS.md`](../../FOLDERS.md) §6, [`MAINTENANCE.md`](../../MAINTENANCE.md), [`TASK.md`](../../TASK.md) §4
