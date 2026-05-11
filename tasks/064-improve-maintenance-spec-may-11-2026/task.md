---
type: task
status: active
slug: improve-maintenance-spec-may-11-2026
summary: "Distil four findings (F20–F23) from the 2026-05-11 coherence run into concrete diffs against MAINTENANCE.md, prompts/repo-coherence-check/prompt.md, and tools/check-governance.sh. Companion to Tasks 025 (open), 032 (done), and 044 (open) which carry earlier findings."
created: 2026-05-11
updated: 2026-05-11
task_id: "064"
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
  - MAINTENANCE.md
  - prompts/repo-coherence-check/prompt.md
  - tools/check-governance.sh
---

# Task 064 — Improve Maintenance Spec from 2026-05-11 Coherence Run

## Goal

Each of the four findings F20–F23 below MUST land as either (a) a concrete diff against [`MAINTENANCE.md`](../../MAINTENANCE.md), [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md), or [`tools/check-governance.sh`](../../tools/check-governance.sh); OR (b) a documented `won't-fix` disposition in this Task's `friction-log.md` with rationale. The Task closes only when every finding has either a landed diff or a recorded disposition. Companion (NOT successor) to [Task 025](../025-maintenance-spec-remaining-findings/task.md) (F2/F3/F4/F7 from 2026-05-05), [Task 032](../032-improve-maintenance-spec-may-2026/task.md) (F8–F13 from 2026-05-06, `done`), and [Task 044](../044-improve-maintenance-spec-may-07-2026/task.md) (F14–F19 from 2026-05-07).

## Findings

### F20 — Body-schema check (`--check-body`) is advisory but catches real shape mismatches

**Symptom.** This session's coherence run executed `python3 tools/fm/validate.py --check-body $(changed .md files)` against the 36-file delta and surfaced two ERROR-tier diagnostics against [`tasks/039-maintenance-spec-integration/task.md`](../039-maintenance-spec-integration/task.md):

- `## Goal` — F.B.1 shape mismatch (expected `paragraph`, found `mixed`).
- `## Links` — F.B.1 shape mismatch (expected `link_list`, found `unordered_list`).

The body-schema check is NOT part of the gating sweep — [`tools/check-governance.sh`](../../tools/check-governance.sh) step `[1/6]` runs `tools/fm/validate.py --type-check` without `--check-body`. The coherence prompt at [`prompts/repo-coherence-check/prompt.md` Step 2.5](../../prompts/repo-coherence-check/prompt.md) mentions `--check-body` as: "When `--check-body` lands as default-on (Task 019), promote here." But [Task 019](../019-fm-toolchain-suite-integration/) closed (`task_status: done`) without that promotion. The body-schema check therefore runs in no routine surface today.

The two surfaced F.B.1 diagnostics are concrete, actionable shape mismatches. The repair tier is ambiguous in the §1 table: rewriting a single section's shape (e.g. flattening `## Goal` from "paragraph + anchor list" to a pure paragraph) is mechanical, but the agent must choose how to preserve the anchor information — that is structural judgement, hence T3.

**Concrete diffs (one or more):**

- [`MAINTENANCE.md §1`](../../MAINTENANCE.md) SHOULD add a sub-row to the tier table for body-schema violations: F.B.1 shape mismatch on a *single section* is T3 (structural — requires choosing the preserve-or-drop strategy); F.B.2/F.B.3 item-count and item_pattern violations are T1 (mechanical reshape of one bullet or one link).
- [`prompts/repo-coherence-check/prompt.md` Step 2.5](../../prompts/repo-coherence-check/prompt.md) SHOULD remove the "promote here when Task 019 lands" language (Task 019 is `done`) and MUST instead require `tools/fm/validate.py --check-body` as part of the linter sweep when the delta touches `task.md` / `prompt.md` / `readme.md`.
- [`tools/check-governance.sh`](../../tools/check-governance.sh) SHOULD add `--check-body` to the step `[1/6]` invocation behind a `FM_CHECK_BODY` env var (default `0` during the WARN→ERROR ladder per [Toolchain Flip SPEC §3.2](../../research/toolchain-flip-criteria/output/SPEC.md)).
- Triage the two existing F.B.1 ERRORs on `tasks/039/task.md` — either patch the sections to conform, or update the schema if the existing shape is legitimate.

### F21 — Trust-audit FL1+ findings recur across runs without filing Tasks

**Symptom.** This session's [`tools/check-governance.sh`](../../tools/check-governance.sh) suite listed 13 research workspaces with `WARN:MAINT.TRUST.FRICTION:FL1` or `FL3` diagnostics, all annotated `recommend-task`:

```
research/adr-corpus-extraction-from-governance-specs::WARN:MAINT.TRUST.FRICTION:FL3:0.70/0.00/0.80
research/agent-prompt-specs-3-systems-sdd::WARN:MAINT.TRUST.FRICTION:FL1:0.90/0.80/0.80
research/agentic-eval-trust-improvement-spec::WARN:MAINT.TRUST.FRICTION:FL1:0.90/1.00/0.80
research/agentic-session-continuity-spec::WARN:MAINT.TRUST.FRICTION:FL1:0.90/1.00/0.80
research/core-architecture-review-2026-05::WARN:MAINT.TRUST.FRICTION:FL3:0.70/0.00/0.80
research/fl0-value-justification::WARN:MAINT.TRUST.FRICTION:FL3:0.70/0.00/0.80
research/friction-pattern-synthesis::WARN:MAINT.TRUST.FRICTION:FL1:0.90/0.00/1.00
research/ncp-novel-co-authoring-spec::WARN:MAINT.TRUST.FRICTION:FL1:0.90/1.00/0.80
research/obsidian-frontmatter-agentic-spec::WARN:MAINT.TRUST.FRICTION:FL1:0.90/1.00/0.80
research/prompt-engineering-principle-mechanizability::WARN:MAINT.TRUST.FRICTION:FL3:0.70/0.00/0.80
research/repo-maintenance-protocol-spec::WARN:MAINT.TRUST.FRICTION:FL1:0.90/1.00/0.80
research/spec-driven-research-agentic-workflows::WARN:MAINT.TRUST.FRICTION:FL1:0.90/0.80/0.80
research/spec-staleness-decision-formalization::WARN:MAINT.TRUST.FRICTION:FL1:0.90/0.00/1.00
```

Aggregate: 13 workspaces, FL buckets `FL0=14 FL1=9 FL2=0 FL3=4`, "friction items recommending Task creation: 13". The same 13 workspaces have appeared in recent run-log records without any one of them being converted into a Task. [`MAINTENANCE.md §3.3`](../../MAINTENANCE.md) instructs:

> 2. **Package as Tasks** — for each FL1+ issue, create a Task in `/tasks/<NNN>-<slug>/task.md` per `TASK.md`.

Strict reading: the agent should have filed 13 new Tasks this run. Practical reality: the items have been silently deferred. The spec has no:

- "deferred-by-policy" annotation for research workspaces whose remediation is parked (the workspace knows it has trust-audit findings but is awaiting upstream tooling);
- batching rule (e.g. "if N+ FL1 items recur unchanged across 3+ runs, file ONE umbrella Task that covers the family rather than 13 individual Tasks");
- recurrence histogram so the agent can prioritise older recurrences over fresh ones.

The result: every coherence run shouts the same 13 items, the agent ignores them, the noise erodes signal. The §3.3 pipeline is mechanically suppressed by accumulated friction.

**Concrete diffs (one or more):**

- [`MAINTENANCE.md §3.3`](../../MAINTENANCE.md) SHOULD add a "Recurring Friction" sub-section: if a research workspace appears in N (default 3, env `MAINT_TRUST_FRICTION_RECURRENCE`) consecutive coherence-run friction recommendations, the agent MUST either (a) file an umbrella Task that covers the family of recurrences (e.g. "remediate trust-audit findings across 13 research workspaces"), or (b) annotate the workspace's `readme.md` with `research_trust_deferred: <YYYY-MM-DD>` + a one-line reason + a target Task # the deferral is parked under.
- [`tools/check-governance.sh`](../../tools/check-governance.sh) SHOULD emit a recurrence histogram alongside the per-workspace WARN line: e.g. `research/<slug>::WARN:...:recurrence-since=2026-05-04(runs=5)`. The agent can then prioritise older recurrences. The histogram source is `maintenance/run-log.md` parsed for prior `WARN:MAINT.TRUST.FRICTION` entries.
- Optionally: [`tools/maintenance/trust-audit.py`](../../tools/maintenance/trust-audit.py) AGGREGATOR SHOULD expose a `--since <date>` flag that suppresses workspaces whose `research_trust_deferred` date is newer than the cutoff, giving the agent a way to silence the noise without losing the data.

### F22 — Advisory ERROR-tier diagnostics map to T1 mechanical fixes that no agent picks up

**Symptom.** This session's `[opt]` FL-declaration linter ([`tools/check-fl-declaration.py`](../../tools/check-fl-declaration.py), [FRUSTRATED.md FR.B.4](../../FRUSTRATED.md)) emitted ERROR-tier diagnostics against two friction-logs:

```
tasks/033-task-spec-integration/friction-log.md::ERROR:FR.B.4:malformed:FL declared only in frontmatter (`summary:` field); body MUST carry a parseable declaration line (see FRUSTRATED.md §FL.Log; canonical: `Highest Frustration Level: FL[0-3]`)
tasks/030-cleanup-dramatica-skills-corpus/friction-log.md::ERROR:FR.B.4:malformed:FL token present but not on a recognised declaration line; see research/fl0-value-justification/output/SPEC.md §2.2 for the accepted variant set
```

Both are classifiable as T1 mechanical fixes (rewrite the declaration line to the canonical `Highest Frustration Level: FL[0-3]` form). The suite passes because the FL-declaration linter is advisory (`[opt]` block in [`tools/check-governance.sh`](../../tools/check-governance.sh)). These two friction-logs have remained malformed across multiple coherence runs. [Task 062](../062-frustrated-spec-followup-ac1-ac5/) blocks the `FM_FL_DECLARATION_STRICT=1` default-flip on remediating these two friction-logs — but no agent has been triggered to apply the T1 fix proactively during the advisory window.

The general pattern: advisory-tier ERROR diagnostics that map to T1 mechanical fixes per the §1 tier table are NOT applied during coherence runs, because the spec only mandates T1 repairs when the diagnostic surfaces in the GATING sweep. There is no "advisory-tier T1 sweep" rule.

**Concrete diffs (one or more):**

- [`MAINTENANCE.md §1`](../../MAINTENANCE.md) SHOULD add a clause: "Advisory-tier ERROR diagnostics emitted by `[opt]` linters that map to T1 mechanical fixes (per the §1 tier table) MUST be applied during the coherence run, not deferred until linter promotion to gating. Worked example: [`tools/check-fl-declaration.py`](../../tools/check-fl-declaration.py) ERRORs on `tasks/<NNN>/friction-log.md` are T1 fixes (rewrite the declaration line to the canonical surface form) — apply them; do not wait for `FM_FL_DECLARATION_STRICT=1` to default-flip."
- [`prompts/repo-coherence-check/prompt.md` Step 3](../../prompts/repo-coherence-check/prompt.md) T1 Checklist SHOULD add a row: "**Advisory-linter ERROR diagnostics** — run every `[opt]` linter under `tools/check-governance.sh` and apply T1 fixes for any ERROR-tier diagnostic whose remedy is mechanical (per §1 tier table). Do NOT wait for the linter to promote to gating."
- Apply the T1 fix to the two friction-logs in this session OR in a paired commit — both files are already T4-eligible (their parent Tasks are `done`/`updated`), so this is a meta-question: are friction-logs T4-immutable once the parent Task closes? §1 says research workspaces are T4 after `research_phase: complete`; the analogous rule for friction-logs is undefined.

### F23 — Run-log baseline falls forward to a `task-implementation` record, inflating delta scope

**Symptom.** This session's coherence run started at baseline `36e2611` (the `end_commit` of run 2026-05-08, which combined a coherence-check with a Task 037 closure). The delta to HEAD (`f5e9b0b`) included 36 files across 14 commits — most of them Task 039's implementation work (`tools/maintenance/staleness-audit.py`, `tools/maintenance/trust-audit.py`, etc.) and Task 037's PR-93 review trail. The maintenance prompt at [Step 1a](../../prompts/repo-coherence-check/prompt.md) explicitly does NOT filter on `routine_type:`:

> The awk fall-forward in `prompts/repo-coherence-check/prompt.md` Step 1a keys on `end_commit:` regardless of `routine_type:`, so `task-implementation` records remain valid baselines (they advance HEAD).

[`MAINTENANCE.md §2.3`](../../MAINTENANCE.md) documents this behavior but does NOT document the resulting delta-shape expectation. The agent reading the prompt for the first time would reasonably interpret a 36-file delta as "significant repo drift since the last sweep" rather than "one Task closed, and a paired coherence-check piggy-backed on its commit boundary, so the delta is dominated by that Task's implementation work."

The conflation is harmless in this run (the §3.4 staleness audit runs per-Task regardless of delta source), but it costs an agent reasoning-budget every time. A short note in the spec would prevent the unnecessary disambiguation.

**Concrete diffs (one or more):**

- [`MAINTENANCE.md §2.3`](../../MAINTENANCE.md) SHOULD add a note immediately after the "Record types (per Task 032 finding F9)" table:
  > **Delta-shape expectation under `task-implementation` baselines.** When a coherence run's baseline `routine_type` is `task-implementation`, the delta will be dominated by that Task's commits. The agent SHOULD apply the per-file triage uniformly across the delta but SHOULD NOT treat the delta size as a signal of skipped maintenance — it is the natural shape of a baseline that advanced through a Task closure. To recover the previous *coherence-scope* baseline for sweep-scope metrics ("how many T3 Tasks did coherence file in May 2026?"), filter the run-log on `routine_type: coherence-check` as already mandated in §2.3.
- [`prompts/repo-coherence-check/prompt.md` Step 1](../../prompts/repo-coherence-check/prompt.md) SHOULD print the baseline's `routine_type` alongside the `start_commit` so the agent can reason about delta shape without re-reading the run-log:
  ```bash
  BASELINE_TYPE=$(grep -B1 "end_commit: $BASELINE" maintenance/run-log.md | grep "routine_type:" | head -n1)
  echo "Baseline=$BASELINE (routine_type=$BASELINE_TYPE)"
  ```

## Plan

1. Review the four findings F20–F23 against the existing maintenance-spec improvement Tasks (025, 044) to confirm none is a duplicate.
2. For each finding, author the concrete diff against the cited file(s) — or record a `won't-fix` disposition in `friction-log.md` with rationale.
3. Run `tools/check-governance.sh` after each diff lands; verify the suite still exits 0 (the advisory-tier linters MAY change polarity but the gating layer MUST remain green).
4. When every finding has either landed or been declined, close the Task per `TASK.md §4.6` with `task_status: done` and a `friction-log.md` carrying an FL[0-3] declaration in the canonical surface form (per F22's own remedy).

## Todo

- [ ] 1. F20 — body-schema check `--check-body` documented + promoted (MAINTENANCE.md §1 sub-row; prompt Step 2.5 update; check-governance.sh `FM_CHECK_BODY` env var; existing F.B.1 ERRORs on tasks/039 triaged).
- [ ] 2. F21 — recurring trust-audit friction policy landed (MAINTENANCE.md §3.3 "Recurring Friction" sub-section; recurrence histogram in check-governance.sh; AGGREGATOR `--since` flag OR equivalent suppression mechanism).
- [ ] 3. F22 — advisory-tier T1 sweep clause landed (MAINTENANCE.md §1 advisory-tier clause; prompt Step 3 T1 checklist row; remediation policy for tasks/033 + tasks/030 friction-logs decided).
- [ ] 4. F23 — task-implementation baseline expectation documented (MAINTENANCE.md §2.3 note; prompt Step 1 routine_type print).
- [ ] 5. Run `tools/check-governance.sh` against `HEAD` post-changes; suite MUST exit 0.
- [ ] 6. Close the Task per `TASK.md §4.6`; produce `friction-log.md` with FL[0-3] in canonical surface form.

## Links

- Companion Tasks (open / done): [`Task 025`](../025-maintenance-spec-remaining-findings/task.md), [`Task 032`](../032-improve-maintenance-spec-may-2026/task.md), [`Task 044`](../044-improve-maintenance-spec-may-07-2026/task.md).
- Source of findings: [`maintenance/run-log.md` Run 2026-05-11](../../maintenance/run-log.md).
- Governing specs: [`MAINTENANCE.md`](../../MAINTENANCE.md), [`TASK.md`](../../TASK.md), [`FRUSTRATED.md`](../../FRUSTRATED.md).
- Coherence prompt: [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md).
- Found by: coherence check run `maintenance/run-log.md` entry 2026-05-11.
