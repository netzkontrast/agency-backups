---
type: task
status: active
slug: successor-adr-0008-falsifier-fires
summary: "File one or more successor ADRs to ADR-0008 (narrative-skills-status-quo) after the 2026-05-16 adr-trigger-audit fired ADR-0008.F1, F2, F3, and F4 simultaneously. Per MAINTENANCE.md §3.6 MUST clause; structured per the Task 096 F29 proposed batching policy (one Task with per-trigger Plan sections)."
created: 2026-05-16
updated: 2026-05-16
task_id: "097"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - decisions/
  - AGENTS.md
---

# Task 097 — Successor ADR for ADR-0008 Falsifier Fires (2026-05-16 audit)

## Goal

Author one successor ADR (or per-trigger N-ADR batch) that closes the four falsifier-trigger fires recorded against [ADR-0008 (Narrative Skills Status Quo)](../../decisions/0008-narrative-skills-status-quo.md) by the 2026-05-16 [`tools/maintenance/adr-trigger-audit.py`](../../tools/maintenance/adr-trigger-audit.py) run. The Task closes when (a) the successor ADR is at `adr_status: Proposed` or `Accepted` in [`decisions/`](../../decisions/); (b) ADR-0008's `adr_superseded_by` frontmatter cites the successor; (c) [`tools/maintenance/adr-trigger-audit.py --format runlog`](../../tools/maintenance/adr-trigger-audit.py) no longer fires F1–F4 against `HEAD` (or the surviving fires are explicitly rationalised as intended in the successor's body).

## Background

[`MAINTENANCE.md §3.6`](../../MAINTENANCE.md) ratifies a MUST: *"When the audit reports `FIRED:<CODE>`, the maintenance agent … MUST file a Task whose Plan covers the successor ADR per [`decisions/readme.md`](../../decisions/readme.md), citing the audit's diagnostic line as the evidence anchor."* The 2026-05-16 audit emitted:

```
2026-05-16 | adr-trigger-audit | 8 triggers / window=14d / bundle~77926 tokens | FIRED:ADR-0008.F1,ADR-0008.F2,ADR-0008.F3,ADR-0008.F4 | manual=ADR-0008.F5
```

The four fired triggers are all owned by ADR-0008 and represent a coordinated signal that the *narrative-skills status-quo* decision has reached a falsification threshold. This Task is the §3.6-mandated successor-ADR planning artefact. The §3.6 MUST clause does not permit deferral; this Task discharges that obligation even though the concrete ADR drafting is non-trivial.

**Batching shape.** This Task implements the F29 proposed-but-unratified batching policy from [Task 096](../096-improve-maintenance-spec-may-16-2026/task.md): *one parent Task with per-trigger Plan sections, each section citing exactly one fired trigger code*. This shape is permitted today because §3.6 prose ("file a Task whose Plan covers the successor ADR") is silent on how to handle N≥2 simultaneous fires — until F29 is ratified, this batched-single-Task interpretation is the conservative reading. If F29 is rejected and the spec mandates N separate Tasks, this Task can be split into four successors with `task_supersedes: ["097"]` lineage.

## Plan

### Step 1 — ADR-0008.F1 successor (narrative skill count threshold)

Investigate the F1 trigger: count of narrative-* skills under [`skills/`](../../skills/) exceeded the ADR-0008 threshold. Recover the current count, the threshold, and the trigger semantics from `tools/maintenance/adr-trigger-audit.py` source. Decide: (a) raise the threshold in a successor ADR (status-quo continuation), (b) consolidate the narrative-* skills (action ADR), or (c) accept the growth and retire the trigger (relaxation ADR).

### Step 2 — ADR-0008.F2 successor (narrative-* bundle token threshold)

Investigate the F2 trigger: aggregate narrative-* bundle size in tokens (today: ~77,926 tokens). Recover the threshold; decide on the same three-way axis as Step 1.

### Step 3 — ADR-0008.F3 successor (sustained narrative-* friction)

Investigate the F3 trigger: friction-log aggregation over the 14-day window flagged sustained friction in narrative-* skill invocations. Recover the diagnostic line; decide whether the friction trace is structural (action ADR required) or cosmetic (relaxation ADR).

### Step 4 — ADR-0008.F4 successor (`task_affects_paths` scan)

Investigate the F4 trigger: scan of `task_affects_paths:` blocks across open Tasks for narrative-* path coverage. Recover the matching Task IDs; decide whether the open-Task pattern justifies an ADR amendment.

### Step 5 — Author the successor ADR(s)

Per [`decisions/readme.md`](../../decisions/readme.md) MADR 4.0.0 template, draft `decisions/<NNNN>-<slug>.md` with:
- `adr_id: "ADR-<NNNN>"` (next free slot after [ADR-0012](../../decisions/0012-skill-source-validator-diagnostic-codes.md)).
- `adr_status: Proposed` initially; flip to `Accepted` after review.
- `adr_supersedes: ["ADR-0008"]`.
- Body sections per the MADR template: Context, Decision, Consequences, Trigger Audit Evidence (cite the 2026-05-16 audit line verbatim).
- Per-trigger sub-sections explaining the F1/F2/F3/F4 disposition.

### Step 6 — Update ADR-0008's `adr_superseded_by`

Since `Accepted` ADRs are T4-immutable per [MAINTENANCE.md §1](../../MAINTENANCE.md), the ADR-0008 amendment is the **single permitted T4-exception**: setting `adr_superseded_by` on the predecessor is the reciprocity rule of [`tools/adr/cli.py validate`](../../tools/adr/cli.py). Bump `updated:` on ADR-0008 in the same commit.

### Step 7 — Re-run the trigger audit

`python3 tools/maintenance/adr-trigger-audit.py --format runlog` MUST emit `ok` for the F1–F4 codes against `HEAD` after the successor lands (or document any surviving fires as intended in the successor's body).

### Step 8 — Run `tools/adr/cli.py synthesize`

The `<!-- BEGIN AGENCY-ADR SYNTHESIS -->` block in [`AGENTS.md`](../../AGENTS.md) is agent-written; re-run synthesis to incorporate the successor's `bcp14-keyword` token-count and fidelity score.

### Step 9 — Close

Author `friction-log.md` with `Highest Frustration Level: FL[0-3]` and a Per-Trigger Disposition table. Flip `task_status: done`. Update [`tasks/readme.md`](../readme.md) per [TASK.md §4.8](../../TASK.md).

## Todo

- [ ] Step 1 — F1 trigger investigation + disposition decision
- [ ] Step 2 — F2 trigger investigation + disposition decision
- [ ] Step 3 — F3 trigger investigation + disposition decision
- [ ] Step 4 — F4 trigger investigation + disposition decision
- [ ] Step 5 — successor ADR(s) drafted under `decisions/`
- [ ] Step 6 — ADR-0008 `adr_superseded_by` set + `updated:` bumped
- [ ] Step 7 — `adr-trigger-audit.py` re-run returns `ok` for F1–F4
- [ ] Step 8 — `tools/adr/cli.py synthesize` re-run; AGENTS.md guarded block refreshed
- [ ] Step 9 — friction-log.md authored + `task_status: done` + tasks/readme.md updated

## Links

- [`decisions/0008-narrative-skills-status-quo.md`](../../decisions/0008-narrative-skills-status-quo.md) — the predecessor ADR; T4-immutable except for the `adr_superseded_by` amendment in Step 6.
- [`decisions/readme.md`](../../decisions/readme.md) — MADR 4.0.0 ADR-authoring template.
- [`tools/maintenance/adr-trigger-audit.py`](../../tools/maintenance/adr-trigger-audit.py) — Task 069 implementation; source for trigger semantics.
- [`tools/adr/cli.py`](../../tools/adr/cli.py) — validator + synthesizer.
- [`MAINTENANCE.md §3.6`](../../MAINTENANCE.md) — the falsifier-trigger audit cadence rule that mandated this Task.
- [`tasks/096-improve-maintenance-spec-may-16-2026/task.md`](../096-improve-maintenance-spec-may-16-2026/task.md) — proposes F29 batching policy; this Task is the canonical first implementation of that shape.
- [`maintenance/run-log.md`](../../maintenance/run-log.md) — 2026-05-16 coherence record cites the audit fire as the trigger for this Task.
