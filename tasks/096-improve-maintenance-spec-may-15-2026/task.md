---
type: task
status: active
slug: improve-maintenance-spec-may-15-2026
summary: "Surface five MAINTENANCE.md gaps observed during the 2026-05-15 manual maintenance run: (a) ADR-0008 multi-fire ambiguity (4-of-5 triggers fired same nightly, spec is silent on whether one or four successor Tasks); (b) §3.5 dup-id collision at slot 090 — autofile predicates pass but no run-log routine_type covers a manual coherence run; (c) §3.4 staleness audit flagged 4 Tasks but spec defers multi-finding remediation to humans without an aggregator; (d) [opt] FL-declaration linter (FR.B.4) emits ERROR-tier diagnostics that don't block the gate — UX confusion between linter level and gate effect; (e) run-log routine_type enum lacks a `manual-execution` value for ad-hoc human-invoked sweeps."
created: 2026-05-15
updated: 2026-05-15
task_id: "096"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - MAINTENANCE.md
  - maintenance/run-log.md
  - tools/maintenance/adr-trigger-audit.py
  - tools/maintenance/staleness-audit.py
  - tools/fm/check-duplicate-task-id.py
  - tools/check-governance.sh
---

# Task 096 — Improve MAINTENANCE.md from 2026-05-15 Manual Maintenance Run

## Goal

Land five concrete amendments to [`MAINTENANCE.md`](../../MAINTENANCE.md) that close gaps observed during the manual maintenance run on 2026-05-15. The Task is `done` when (a) every amendment below has merged, (b) `tools/check-governance.sh` exits 0 on the post-amendment commit, AND (c) re-running the same maintenance routine against the same HEAD produces zero ambiguity that this session encountered (specifically: multi-fire ADR resolution is deterministic, dup-id autofile under manual invocation is unambiguous, friction-log linter level matches user-visible severity).

## Plan

1. **Amendment A — §3.6 multi-fire resolution rule.** Add a normative paragraph after the "Action on a fire" paragraph stating: when N>1 mechanical/semi-mechanical triggers of the SAME ADR fire in one audit, the agent MUST file ONE successor-ADR Task whose `task_affects_paths` covers the ADR file and whose body cites EVERY fired diagnostic line. When triggers fire across DIFFERENT ADRs (ADR-0008.Fx + ADR-0009.Fy), the agent MUST file ONE successor Task per ADR. Add Gherkin scenario `M.B.9` to §6 to bind the rule.
2. **Amendment B — §2.3 `routine_type:` enum extension.** Add a fifth value `manual-execution` for ad-hoc human-invoked sweeps that don't fit `coherence-check` (delta-scoped) or `nightly-maintenance` (broader audit). Update the table in §2.3 + the prose in `maintenance/run-log.md` "How to Read This File". Counter semantics: identical to `coherence-check` but the agent MUST set `notes:` to include the invoking-user prompt fragment for traceability.
3. **Amendment C — §3.5 autofile under manual invocation.** Amend predicate (4) "current run is a Coherence Check" to also accept `manual-execution` (post-Amendment-B). Today the §3.5 spec literal-reads to "MUST escalate to a human" for manual runs, but the human IS the operator and they're asking for the autofile. Capture the rationale inline.
4. **Amendment D — §1 / §4.1 ERROR-at-opt-tier reconciliation.** Add a §1 footnote (or a new §1.0.2) clarifying that a linter labelled `[opt]` MAY emit `ERROR`-tier diagnostic lines without blocking `tools/check-governance.sh`. The diagnostic level describes the SEVERITY of the finding for the file under audit; the linter's slot ([opt] vs gating) describes the GATE effect. The two are orthogonal. Currently a user reading "ERROR" thinks the gate failed, but the gate is green because the linter is opt-tier. Add a worked example citing FR.B.4 (FL declaration linter) which is opt-tier today but emits ERROR per the FRUSTRATED.md mandate.
5. **Amendment E — §3.4 multi-finding aggregator.** Add a §3.4.1 subsection covering the case when `tools/maintenance/staleness-audit.py` flags MORE than one Task in a single run. The current §3.4 spec authorises "ordinary 1→1 supersessions" inline but is silent on bulk batches. Specify: the agent MAY apply each 1→1 transition independently if and only if the bucket is `completed_by_drift` (mechanical: flip `task_status: done` + close-by-drift friction-log) or `no_longer_desirable` (mechanical: flip `task_status: abandoned` + brief friction-log); for the `drifted` bucket, even a single finding requires a successor Task because the re-frame text is creative. Cap inline batches at **3 per run**; above 3 → human-confirmed annotation in run-log. Rationale for cap=3 (not 5): the historical run-log shows max `t3_tasks_created: 2` in any run, so a cap of 3 surfaces "unusually noisy maintenance run" as a smell while leaving headroom for the typical 1–2 batch.
6. **Amendment F — `tools/maintenance/trust-audit.py` AGGREGATOR `routine_type` parameterisation.** The AGGREGATOR currently HARDCODES `- routine_type: nightly-maintenance` at [`tools/maintenance/trust-audit.py:422`](../../tools/maintenance/trust-audit.py). After Amendment B introduces `manual-execution`, the AGGREGATOR MUST accept the invoking routine_type (e.g. via a new `--routine-type` CLI flag defaulting to `nightly-maintenance` for backwards compatibility) so manual invocations are tagged correctly in the run-log roll-up. Update `MAINTENANCE.md §3.2` "Aggregator integration" paragraph to cite the new flag.
7. **Amendment G — Cross-reference §1.0.1 in Amendment A's filing rule.** When Amendment A's "MUST file ONE successor-ADR Task" fires against an `adr_status: Accepted` predecessor, the Task's Plan MUST explicitly cite `MAINTENANCE.md §1.0.1` (closed-research T1/T2 allowance) and the `adr_status: Accepted` T4-immutability rule from §1, so the executing agent does not attempt an in-place amendment to the predecessor. One-line cross-reference inside the Amendment-A normative paragraph.

Each Amendment lands as ONE commit on the same branch. Amendments A and C reference Amendment B's `routine_type:` enum, so B MUST land first. Amendment F also depends on B (it parameterises against the new enum). Amendments D, E, G are independent.

## Todo

- [ ] 1. Amendment A — §3.6 multi-fire resolution rule + Gherkin `M.B.9`.
- [ ] 2. Amendment B — `routine_type: manual-execution` enum extension in §2.3 + `maintenance/run-log.md`.
- [ ] 3. Amendment C — §3.5 autofile predicate (4) accepts `manual-execution`.
- [ ] 4. Amendment D — §1 / §4.1 footnote on `[opt]` ↔ ERROR-tier orthogonality (worked examples: FR.B.4 FL-declaration linter AND `tools/maintenance/staleness-audit.py` exit-2-on-finding).
- [ ] 5. Amendment E — §3.4.1 multi-finding aggregator with per-bucket inline-vs-Task rules; cap=3.
- [ ] 6. Amendment F — parameterise `tools/maintenance/trust-audit.py` AGGREGATOR `routine_type` via `--routine-type` CLI flag.
- [ ] 7. Amendment G — Amendment-A normative paragraph cross-references §1.0.1 + §1 T4-immutability for `adr_status: Accepted` predecessors.
- [ ] 8. Re-run `tools/check-governance.sh` against the post-amendment HEAD; gate MUST exit 0.
- [ ] 9. Re-run `tools/maintenance/adr-trigger-audit.py --format runlog`; the audit's behaviour MUST be unchanged (the spec amendment doesn't alter the predicate set).
- [ ] 10. After Amendments A+B+C+F land, re-run the §3.6 audit and the §3.5 dup-id linter; the deferred ADR-0008 successor Task and the 090 dedup Task MUST be autofile-able under the post-amendment predicates without manual interpretation.

## Findings (Evidence Anchors)

The five amendments above are motivated by concrete signals captured during the 2026-05-15 manual run; each is reproducible against `HEAD=867453e`.

### Finding 1 — ADR-0008 4-of-5 falsifier triggers fired same audit (severity P1 — fires today, blocks mechanical §3.6 loop)

`python3 tools/maintenance/adr-trigger-audit.py --format runlog` on 2026-05-15 emits:

```
2026-05-15 | adr-trigger-audit | 8 triggers / window=14d / bundle~77926 tokens | FIRED:ADR-0008.F1,ADR-0008.F2,ADR-0008.F3,ADR-0008.F4 | manual=ADR-0008.F5
```

Per §3.6 "Action on a fire", the agent MUST file a Task. The spec is silent on whether 4 fires require 1 or 4 Tasks. Filing 4 invites duplicate-tracking churn; filing 1 risks losing the per-trigger trace. Amendment A binds the answer. **Severity: P1** — this Finding fires today (4-of-5 ADR-0008 triggers) AND every subsequent run that satisfies the same predicates will re-stall at the same "1 vs N Tasks" decision until the spec binds it.

### Finding 2 — Dup-task-id collision at slot 090, autofile predicate (4) fails for manual run

`python3 tools/fm/check-duplicate-task-id.py` reports:

```
ERROR: task_id='090' appears in 2 active tasks without supersession reciprocity:
  /home/user/agency/tasks/090-codex-pr-review/task.md (in_progress)
  /home/user/agency/tasks/090-review-pr109-archive-spec/task.md (done)
```

§3.5 predicates 1 + 2 + 3 hold; predicate 4 ("current run is `routine_type: coherence-check`") FAILS because this is a manual user invocation. Amendments B + C close the gap.

### Finding 3 — Staleness audit flagged 4 Tasks; spec authorises only 1→1 supersession inline

`python3 tools/maintenance/staleness-audit.py` flags:

| Task | Bucket |
|---|---|
| 008-harden-coherence-baseline-protocol | COMPLETED_BY_DRIFT |
| 048-task-tooling-impl-spec | NO_LONGER_DESIRABLE |
| 053-core-architecture-review-followups | DRIFTED |
| 066-review-pr28-readme-spec | NO_LONGER_DESIRABLE |

§3.4 says "the maintenance agent MAY perform the transition directly because every step is mechanical … For ordinary 1→1 supersessions". With four findings of three bucket types, the agent has no spec guidance on whether to batch them, file separate Tasks, or escalate. Amendment E binds the answer per-bucket.

### Finding 4 — `[opt]` FL-declaration linter emits ERROR, gate stays green

`tools/check-governance.sh` step `[opt] FL declaration linter` outputs:

```
tasks/033-task-spec-integration/friction-log.md::ERROR:FR.B.4:malformed:FL declared only in frontmatter
tasks/030-cleanup-dramatica-skills-corpus/friction-log.md::ERROR:FR.B.4:malformed:FL token present but not on a recognised declaration line
```

The lines say `ERROR` but the gate exits `0` and prints `=== PASS: all governance checks passed. ===`. A new operator reading the trace cannot tell whether the build is broken or fine. Amendment D adds a footnote on `[opt]` ↔ ERROR-tier orthogonality and a worked example.

### Finding 5 — `routine_type:` enum doesn't fit a manual sweep

The 2026-05-15 run was invoked by a human prompt ("Execute Maintenance.md"), included BOTH a delta-scoped Coherence Check (§2) AND the §3.6 falsifier-trigger audit (which §3.6 says is a Nightly-cadence routine). Neither `coherence-check` nor `nightly-maintenance` quite fits. Amendment B adds `manual-execution` and clarifies counter semantics.

## Out of Scope

- Filing the dedup Task for the 090 collision (§3.5) and the ADR-0008 successor Task (§3.6) is deferred until Amendments A/B/C land — at that point the autofile predicates are unambiguous and a follow-up coherence run will file them mechanically. This Task explicitly does NOT pre-create those follow-ups.
- The four staleness-flagged Tasks are NOT touched by this Task. They will be triaged by a follow-up coherence run after Amendment E specifies the per-bucket batch rules.
- No actual ADR-0008 successor is authored here. Filing the successor is a separate Task downstream of Amendment A's filing rule.

## Links

- Source spec(s): [`MAINTENANCE.md`](../../MAINTENANCE.md), [`research/spec-staleness-decision-formalization/output/SPEC.md`](../../research/spec-staleness-decision-formalization/output/SPEC.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`AGENTS.md`](../../AGENTS.md), [`FRUSTRATED.md`](../../FRUSTRATED.md)
- Related Tasks (prior maintenance-spec amendments): [`044-improve-maintenance-spec-may-07-2026`](../044-improve-maintenance-spec-may-07-2026/), [`068-improve-maintenance-spec-may-2026`](../068-improve-maintenance-spec-may-2026/), [`069-operationalise-adr-falsifier-triggers`](../069-operationalise-adr-falsifier-triggers/)
- Found by: 2026-05-15 manual maintenance run; run-log entry under `maintenance/run-log.md`
