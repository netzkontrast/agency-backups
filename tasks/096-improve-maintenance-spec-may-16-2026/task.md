---
type: task
status: active
slug: improve-maintenance-spec-may-16-2026
summary: "Distil eight findings (F27–F34) from the 2026-05-16 coherence run into concrete diffs against MAINTENANCE.md, prompts/repo-coherence-check/prompt.md, tools/check-governance.sh, and templates/. Companion to Tasks 025 (F2/F3/F4/F7), 044 (F14–F19), and 064 (F20–F26) which carry earlier findings."
created: 2026-05-16
updated: 2026-05-16
task_id: "096"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts:
  - repo-coherence-check
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - MAINTENANCE.md
  - prompts/repo-coherence-check/prompt.md
  - tools/check-governance.sh
  - templates/
---

# Task 096 — Improve Maintenance Spec from 2026-05-16 Coherence Run

## Goal

Each of the eight findings F27–F34 below MUST land as either (a) a concrete diff against [`MAINTENANCE.md`](../../MAINTENANCE.md), [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md), [`tools/check-governance.sh`](../../tools/check-governance.sh), or [`templates/`](../../templates/); OR (b) a documented `won't-fix` disposition in this Task's `friction-log.md` with rationale. The Task closes only when every finding has either a landed diff or a recorded disposition. Companion (NOT successor) to [Task 025](../025-maintenance-spec-remaining-findings/task.md) (F2/F3/F4/F7, open), [Task 044](../044-improve-maintenance-spec-may-07-2026/task.md) (F14–F19, open), and [Task 064](../064-improve-maintenance-spec-may-08-2026/task.md) (F20–F26, open).

## Background

This Task continues the improve-maintenance-spec lineage:

- **Task 025** (2026-05-05 origin) carries findings F2–F7 against root specs.
- **Task 044** (2026-05-07 coherence run) carries F14–F19 against MAINTENANCE.md, FRUSTRATED.md, TASK.md, and `tools/check-trust.py`.
- **Task 064** (2026-05-08 coherence run) carries F20–F26 against MAINTENANCE.md, the coherence prompt, `tools/check-governance.sh`, and `CLAUDE.md`.
- **Task 096** (this Task, 2026-05-16 coherence run) carries F27–F34 — surfaced during a session whose mandate was *execute MAINTENANCE.md, then file improvements*.

The 2026-05-16 session was invoked on branch `claude/peaceful-carson-hXNWW` at HEAD `867453e`. The coherence sweep was triggered manually after `./install.sh` and `tools/check-governance.sh` bootstrap. The session pre-applied a T1 mechanical repair to `tasks/readme.md` (the Task 093 bullet showed `Status: \`open\`` despite `task.md` carrying `task_status: done`; bumped `updated:` on `tasks/readme.md`). All other observed defects required spec-level work and are captured below.

## Findings

### F27 — Awk fall-forward baseline conflates delta-scope with metric-scope

**One-line summary.** [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 1a picks the most-recent reachable `end_commit:` across *any* `routine_type:`, producing oversize deltas after a flurry of `adr-synthesize` records.

**Symptom.** Today's run resolved baseline to `6e4859d` — an `adr-synthesize` record from 2026-05-12 — yielding a 756-file delta. The most-recent `routine_type: coherence-check` record (`36e2611`) would have given a tractable delta. [`MAINTENANCE.md §2.3`](../../MAINTENANCE.md) lines 141–151 explicitly document the awk-keys-on-any-record behaviour, but the prose only notes the routine-type filter is required for *aggregate metrics*, not for the *delta itself*. A delta-scope agent following the spec literally inherits the over-large baseline.

**Concrete diffs:**

- [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 1a SHOULD accept a `--prefer-routine-type coherence-check` flag (or environment override `COHERENCE_BASELINE_ROUTINE`) and prefer the most-recent matching record when the variable is set. The current awk MUST remain the default to preserve `task-implementation` fall-forward semantics for sweeps that legitimately start there.
- [`MAINTENANCE.md §2.3`](../../MAINTENANCE.md) MUST add one paragraph below line 150 distinguishing **delta baseline** (the value used for `git log <baseline>..HEAD`) from **metric baseline** (the value used for "Tasks filed by coherence runs in window X"). The paragraph MUST cite the recovery semantics so future agents do not assume the two are interchangeable.

**Acceptance.** A coherence run with `COHERENCE_BASELINE_ROUTINE=coherence-check` exported MUST resolve the baseline via `awk '/routine_type: coherence-check/{flag=1} flag && /end_commit:/{print; flag=0}'`. Without the variable, behaviour MUST remain identical to today's.

---

### F28 — §3.5 discovery loop lacks an audit-window predicate

**One-line summary.** [`MAINTENANCE.md §3.5`](../../MAINTENANCE.md) tells the agent to file a renumber Task *when a collision is observed*, but does not require the agent to *run the dup-id linter at every coherence sweep*.

**Symptom.** `tasks/090-codex-pr-review/` and `tasks/090-review-pr109-archive-spec/` have shared `task_id: "090"` for ≥ 4 days. Multiple coherence-check runs since 2026-05-12 have not filed a renumber Task. `tools/fm/check-duplicate-task-id.py` reports the collision but exits 0 (advisory-tier). [`tools/check-governance.sh`](../../tools/check-governance.sh) runs the linter only under `FM_DUPLICATE_TASK_ID_STRICT=1`, which is not the default.

**Concrete diffs:**

- [`MAINTENANCE.md`](../../MAINTENANCE.md) MUST add §3.5.1 *"Coherence-run audit-window predicates"* listing the linters the agent SHOULD invoke at Step 2.5 of every coherence sweep: `tools/fm/check-duplicate-task-id.py`, `tools/maintenance/staleness-audit.py`, and `tools/maintenance/adr-trigger-audit.py`. The section MUST be paired with the existing §3.5 four-predicate gate.
- [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 2.5 MUST add these three commands to the linter-first triage block.

**Acceptance.** A coherence sweep on a HEAD with an unresolved 090 collision MUST surface the collision via the new Step 2.5 invocation, and the agent MUST file a renumber Task unless an open Task already covers the colliding folders (per the existing §3.5 four-predicate gate).

---

### F29 — §3.6 multi-trigger ADR fires lack a batching policy

**One-line summary.** [`MAINTENANCE.md §3.6`](../../MAINTENANCE.md) addresses single-trigger fires; it is silent on what to do when N ≥ 2 triggers fire in the same audit.

**Symptom.** Today's `tools/maintenance/adr-trigger-audit.py --format runlog` emitted `FIRED:ADR-0008.F1,ADR-0008.F2,ADR-0008.F3,ADR-0008.F4` (4 simultaneous fires + 1 MANUAL). §3.6 prose ("Action on a fire") describes a single successor-ADR Task per fire. Four separate Tasks risk decision-conflation across overlapping evidence; one mega-Task hides individual trigger semantics. The M.B.8 Gherkin anchor only covers single-fire scenarios.

**Concrete diffs:**

- [`MAINTENANCE.md §3.6`](../../MAINTENANCE.md) MUST add a "Multi-trigger batching policy" paragraph: when N ≥ 2 mechanical triggers fire in the same audit window, the agent SHOULD file one parent Task with N subtasks (one per trigger), each subtask citing exactly one fired trigger code. The agent MAY file separate Tasks if the triggers belong to *different ADRs* (e.g. ADR-0008.F1 + ADR-0009.F2); same-ADR fires SHOULD batch.
- [`MAINTENANCE.md §6`](../../MAINTENANCE.md) MUST add anchor `M.B.9` Gherkin scenario covering the N-trigger batching contract.

**Acceptance.** With 4 ADR-0008 fires in a single audit, a single-Task implementation MUST be permitted by the spec; the M.B.9 anchor MUST be authored as the acceptance contract for the batching rule.

---

### F30 — §3.2 dynamic-readme markers asserted MUST without mechanical enforcement

**One-line summary.** [`MAINTENANCE.md §3.2`](../../MAINTENANCE.md) lines 175–186 declare `<!-- BEGIN DYNAMIC -->` / `<!-- END DYNAMIC -->` markers MANDATORY, but the corpus is not compliant and `tools/maintenance/dynamic-readme-partition.py` is advisory-tier.

**Symptom.** A spot-check of any operational `readme.md` in `/tasks/`, `/research/`, or `/prompts/` reveals zero `BEGIN DYNAMIC` markers. The M.B.6 Gherkin anchor at MAINTENANCE.md lines 456–469 asserts behaviour the linter cannot enforce. The MUST is a paper rule.

**Concrete diffs (decision point — pick exactly one):**

- **Option A — Promote the linter to gating.** This requires a corpus migration: every operational `readme.md` SHOULD acquire the marker pair as a separate Task. The promotion is scheduled for a follow-up Task; this Task lands the §3.2 amendment that schedules it.
- **Option B — Downgrade §3.2 prose.** Change MUST to SHOULD; add a falsification trigger (e.g. "when ≥ 50% of operational readmes carry the markers, the rule promotes to MUST and the linter promotes to gating").

The Task author MUST pick exactly one option during execution and record the rationale in the Task's `friction-log.md`. **Recommendation: Option B** (lower risk; defers corpus work to a dedicated Task) unless evidence emerges that the corpus is closer to compliance than today's spot-check suggests.

**Acceptance.** Either Option A or Option B landed in `MAINTENANCE.md §3.2`; rationale recorded in this Task's friction-log; if Option A, a follow-up Task filed at the next free `<NNN>`.

---

### F31 — `/sc:*` closing ladder lacks spec authority; `/review` is built-in, not `/sc:review`

**One-line summary.** The operator's standing closing sequence `/sc:analyze → /sc:reflect → /sc:improve → /review → /sc:createPR` is observably stable across sessions but no spec owns it. Task 064 finding F20 raised this earlier; today's session confirmed a critical nuance — `/review` is a **built-in Claude Code skill**, not an `/sc:*` import.

**Symptom.** A user instruction "run /sc:Review" routes ambiguously today: there is no `/sc:review` skill in the imported corpus ([`skills/sc-*`](../../skills/) — 39 skills, no `sc-review`), but there IS a built-in `/review` skill (PR-review on the current branch). Task 064 F20 ([`tasks/064-improve-maintenance-spec-may-08-2026/task.md`](../064-improve-maintenance-spec-may-08-2026/task.md)) anchored the closing-ladder gap but does not flag the `/review` vs `/sc:review` distinction.

**Concrete diffs:**

- [`MAINTENANCE.md`](../../MAINTENANCE.md) MUST add §4.2 *"Operator-side `/sc:*` Closing Ladder"* citing [`AGENTS.md` CR.1–CR.7](../../AGENTS.md) and listing the RECOMMENDED 5-step sequence `/sc:analyze → /sc:reflect → /sc:improve → /review → /sc:createPR`. The section MUST explicitly note: *`/review` is a built-in skill, not an `/sc:*` import; no skill named `/sc:review` exists in the imported corpus*.
- [`MAINTENANCE.md §4.2`](../../MAINTENANCE.md) MUST cross-cite Task 064 F20 so the lineage is recoverable; this Task extends F20 with operator-confirmed evidence from the 2026-05-16 session.
- The amendment SHOULD use the RECOMMENDED keyword (not MUST) to preserve cross-platform symmetry — Jules / Gemini sessions cannot invoke `/sc:*` skills and MUST close via their platform-native equivalents per AGENTS.md CR-step-4.

**Acceptance.** A new agent reading `MAINTENANCE.md §4.2` MUST be able to reproduce the closing sequence without operator instruction. The `/review` vs `/sc:review` distinction MUST be unambiguous.

---

### F32 — §3.4 multi-bucket prioritization order undefined

**One-line summary.** When a single staleness audit flags ≥ 2 buckets across multiple Tasks, [`MAINTENANCE.md §3.4`](../../MAINTENANCE.md) is silent on closure order.

**Symptom.** Today's `tools/maintenance/staleness-audit.py` flagged 4 Tasks across 3 buckets: Task 008 `COMPLETED_BY_DRIFT`, Task 053 `DRIFTED`, Tasks 048 + 066 `NO_LONGER_DESIRABLE`. Two agents working the same HEAD MAY close in different orders, producing different friction-log lineage shapes. The audit-trail readability suffers without an order convention.

**Concrete diffs:**

- [`MAINTENANCE.md §3.4`](../../MAINTENANCE.md) MUST add a "Multi-bucket prioritization order" paragraph: the agent SHOULD close in the order `NO_LONGER_DESIRABLE` → `COMPLETED_BY_DRIFT` → `DRIFTED` → `STILL_ACCURATE` (close-out-first, re-frame-last). The order MUST be advisory (SHOULD) because legitimate exceptions exist (e.g. a `DRIFTED` Task that blocks a `NO_LONGER_DESIRABLE` closure).

**Acceptance.** A coherence run flagging Tasks across multiple buckets MUST follow the SHOULD order or record the deviation in `notes:` of the run-log entry.

---

### F33 — F-number registry has no spec authority

**One-line summary.** The improve-maintenance Task pattern uses ascending F-numbers (F2/F3/F4/F7 in 025; F14–F19 in 044; F20–F26 in 064; F27–F34 in this Task) but no spec owns the registry. Future Tasks risk F-number collisions.

**Symptom.** Task 044's findings start at F14 with no documentation of where F1–F13 originate; Task 064 implicitly continues from F19 → F20. Three concurrent improve-maintenance Tasks could file overlapping F-numbers. Reverse-traceability is fragile.

**Concrete diffs:**

- [`templates/task.md`](../../templates/) (or a new `templates/improve-maintenance.md`) SHOULD ship a stub that documents the F-number convention: *the next free F-number = max(F<N>) + 1 across all open improve-maintenance Tasks; the registry is implicit but recoverable via `grep '^### F[0-9]'`*.
- [`MAINTENANCE.md`](../../MAINTENANCE.md) MUST add a one-paragraph note in §3 or §5.1 pointing at the template and naming the convention.

**Acceptance.** A new agent filing an improve-maintenance Task MUST be able to compute the next free F-number from the existing corpus without operator help.

---

### F34 — Bootstrap script is verbose; the success path leaks 5 lines of pip output

**One-line summary.** `./install.sh` prints jsonschema download progress lines even when the dependency is already satisfied (today's run printed 8 lines of `Downloading` / `Installing collected packages` chatter despite typing-extensions being satisfied).

**Symptom.** The bootstrap's success-path output is noisy — 8 lines of pip output before the "All dependencies installed" verification. New agents reading the install transcript may mistakenly diagnose this as a failure mode.

**Concrete diffs:**

- [`install.sh`](../../install.sh) SHOULD pass `-q` to `pip install` when run from `tools/check-governance.sh` or under a `CI=1` environment, suppressing the progress chatter. Default-interactive invocations MAY keep the verbose output.
- The change is **minor polish**, NOT mandatory; this finding MAY be deferred to a `won't-fix` disposition if the maintainer decides verbose output is preferable for debugging.

**Acceptance.** Either the install-script flag landed, or the `won't-fix` rationale recorded in this Task's friction-log.

---

## Plan

1. Read each finding F27–F34 and decide its disposition (`landed-diff` or `won't-fix`). Record the decision in `friction-log.md` before mutating any file.
2. For findings disposed `landed-diff`, author the concrete diff against the cited line range in `MAINTENANCE.md`, `prompts/repo-coherence-check/prompt.md`, `tools/check-governance.sh`, or `templates/`. Each diff MUST land in a separate commit so reviewers can bisect.
3. For finding F30, the agent MUST pick exactly one of Options A or B and record the rationale.
4. Run `tools/check-governance.sh` after every diff commit; the suite MUST exit 0 before staging the next diff.
5. On the final commit, author this Task's `friction-log.md` with `Highest Frustration Level: FL[0-3]` and per-finding disposition table.
6. Flip `task_status` to `done` (or `updated` if the work re-frames into a successor) per [TASK.md §4](../../TASK.md).
7. Update [`tasks/readme.md`](../readme.md) in the same closing commit per [TASK.md §4.8](../../TASK.md).
8. Close the run via [AGENTS.md Closing Run Procedure](../../AGENTS.md) — `/sc:createPR` step.

## Todo

- [ ] F27 — Awk baseline routine-type preference (MAINTENANCE.md §2.3 + coherence prompt Step 1a)
- [ ] F28 — Audit-window predicates section (MAINTENANCE.md §3.5.1 + coherence prompt Step 2.5)
- [ ] F29 — Multi-trigger ADR batching policy (MAINTENANCE.md §3.6 + anchor M.B.9)
- [ ] F30 — Dynamic-readme MUST/SHOULD decision (MAINTENANCE.md §3.2; Option A or B)
- [ ] F31 — `/sc:*` closing-ladder spec authority + `/review` distinction (MAINTENANCE.md §4.2)
- [ ] F32 — Multi-bucket prioritization order (MAINTENANCE.md §3.4)
- [ ] F33 — F-number registry convention (templates/ + MAINTENANCE.md §3 or §5.1)
- [ ] F34 — Install-script quiet mode (install.sh; or `won't-fix`)
- [ ] friction-log.md authored with FL declaration + per-finding disposition table
- [ ] tasks/readme.md updated in the closing commit

## Links

- [`MAINTENANCE.md`](../../MAINTENANCE.md) — the target spec; primary edit surface.
- [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) — Step 1a / Step 2.5 edits.
- [`AGENTS.md`](../../AGENTS.md) — CR.1–CR.7 cross-reference for F31.
- [`tasks/025-maintenance-spec-remaining-findings/task.md`](../025-maintenance-spec-remaining-findings/task.md) — sibling (F2/F3/F4/F7).
- [`tasks/044-improve-maintenance-spec-may-07-2026/task.md`](../044-improve-maintenance-spec-may-07-2026/task.md) — sibling (F14–F19).
- [`tasks/064-improve-maintenance-spec-may-08-2026/task.md`](../064-improve-maintenance-spec-may-08-2026/task.md) — sibling (F20–F26); F31 extends F20.
- [`maintenance/run-log.md`](../../maintenance/run-log.md) — 2026-05-16 coherence record (this session).
