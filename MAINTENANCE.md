---
type: spec
status: active
slug: maintenance-spec
summary: "Governs the Nightly Maintenance Run and the Repo Coherence Check routine. Defines scope, repair permissions, run-log protocol, and Task delegation rules for all automated maintenance agents."
created: 2026-05-02
updated: 2026-05-13
---

# Repository Maintenance Protocol

Welcome, maintenance agent. This document governs two complementary automated processes:

1. **Nightly Maintenance Run** — updates dynamic documentation and delegates accumulated friction to the Task pipeline.
2. **Repo Coherence Check** — a git-delta-aware self-improvement routine that runs regularly (e.g. at session start) to catch and repair drift before it accumulates.

**Execution logs for both routines** live in [`/maintenance/run-log.md`](./maintenance/run-log.md).
**Canonical language definitions** (RFC 2119, Gherkin, Frontmatter Ontology) live in [`/maintenance/language-spec.md`](./maintenance/language-spec.md).

If you are an agent executing either routine, you MUST read this document in full before making any changes.

---

## 1. Repair Permission Tiers

Not all fixes are equal. Before touching any file, the agent MUST classify the change:

| Tier | Description | Permitted action | Canonical mutation surface |
|---|---|---|---|
| **T1 — Mechanical** | Missing or stale `updated:` date; missing `slug:` that can be derived from folder name; broken relative Markdown link where target exists; missing `readme.md` stub (per FOLDERS.md). | Fix immediately, in-place. | `tools/fm/edit.py --bump-updated` / `--set` / `--unset` |
| **T2 — Additive** | Adding a missing L1 or L2 frontmatter key whose value is unambiguous from context (e.g. adding `type: task` to a `task.md`). | Fix immediately, in-place. | `tools/fm/edit.py --set` / `--append-list` / `--remove-from-list` |
| **T3 — Structural** | Changing section headings, rewriting content, altering schema definitions, adding new L2 keys to the ontology, modifying root governance specs beyond T1/T2. Includes cross-file slug renames. | MUST NOT fix directly. Write a Task in `/tasks/` instead. | (deferred to `tools/fm/section.py` per Task 018, and `tools/fm/rename.py` per Task 019) |
| **T4 — Research-touching (content)** | Any change to *content semantics* in a `/research/<slug>/` workspace that is `research_phase: complete` — body prose, synthesis findings, evidence claims, scenario outcomes. | MUST NOT touch. Research content is immutable after closure. | — |

### 1.0.1 Closed-research T1/T2 Repair Allowance (Task 059)

Closed research is *content*-immutable, not *metadata*-immutable. Two
narrow repair classes are permitted on a `research_phase: complete`
workspace:

- **T1 on closed research** — `updated:` date bumps when surrounding
  artifacts move, slug derivations fixed to match a renamed folder,
  and `tools/fm/edit.py --bump-updated` / `--set` / `--unset` calls
  that touch only frontmatter scalars.
- **T2 on closed research** — repairs to broken *relative* Markdown
  links whose target file moved (the link points at the new path; the
  surrounding sentence is unchanged) and additions of L1 / L2 keys
  whose values are unambiguous from context.

Any other body-content edit — typo fixes in prose, finding rewrites,
scenario-outcome changes, table-cell corrections — remains T4 and
MUST be written as a Task that supersedes the closed workspace via a
new `research_phase: open` successor. T3 structural edits (heading
rewrites, schema migrations, section reorders) are also forbidden on
closed research regardless of trivial appearance.

**Lifecycle interaction (§4.7):** A T1 / T2 repair on closed research
MUST NOT trip the originating Task's `task_status` lifecycle. The
Task that produced the workspace remains `done`; the repair commit
SHOULD cite the Task slug in its message but MUST NOT mutate the
Task's `task_status`.

**Audit trail:** Every T1 / T2 repair commit on closed research MUST
carry a one-line rationale in the commit message naming the trigger
(typically the upstream rename or move that broke the link), and
MUST bump the workspace's own `updated:` field via
`tools/fm/edit.py --bump-updated` so the change is discoverable.

**Root governance specs** (`AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `FRUSTRATED.md`, `PRE_COMMIT.md`, `MAINTENANCE.md`) are subject to T1/T2 repairs only. Structural changes to these files MUST be written as Tasks.

**Accepted ADRs are T4-immutable.** Any file under [`/decisions/`](./decisions/) whose frontmatter declares `adr_status: Accepted` MUST NOT be mutated by maintenance routines at any tier — not even a T1 `updated:` bump. The Repo Coherence Check and the Nightly Maintenance Run MUST refuse to mutate Accepted ADRs and MUST file a successor ADR (or a Task that authors one) instead. This rule mirrors the assertion at [`FOLDERS.md` line 191](./FOLDERS.md) ("Once `adr_status: Accepted`, the file is T4-immutable per `MAINTENANCE.md` §1") and back-fills the cross-reference that was previously asserted only in `FOLDERS.md`. The T4-immutability is enforced two ways: (i) the mechanical refusal is implemented by [`tools/maintenance/staleness-audit.py`](./tools/maintenance/staleness-audit.py), which excludes `decisions/` from its scan by construction; (ii) the `adr_*` namespace is owned by [`tools/adr/cli.py validate`](./tools/adr/cli.py) (PRE_COMMIT.md §7.C), which runs as step `[5/6]` of [`tools/check-governance.sh`](./tools/check-governance.sh) and rejects supersession-DAG cycles. Coherence-run agents that observe a defect in an Accepted ADR MUST author a successor ADR per `decisions/readme.md` rather than editing the predecessor in place. The acceptance contract for this rule is anchor [`M.B.7`](#6-acceptance-criteria-gherkin-scenarios) below.

**Mutation surface stability.** `tools/fm/edit.py` is the canonical T1/T2 mutator for frontmatter; coherence-check agents SHOULD prefer it over `sed`/`awk` because it preserves body bytes and quoting, takes a file lock, and rejects T3/T4 operations by construction (per [SPEC.md §7.2](./research/flexible-frontmatter-toolchain/output/SPEC.md)). Body-section mutations are deferred to `tools/fm/section.py` (Task 018).

### 1.1 Toolchain Surface (Post-Migration)

#### 1.1.1 Two-toolchain (Legacy ↔ Flexible) baseline

The flexible-frontmatter toolchain is canonical and gating; the migration tracked by [Task 017](./tasks/017-migrate-repo-to-flexible-toolchain/) and [Task 019](./tasks/019-fm-toolchain-suite-integration/) is `done` (per Task 032 finding F12).

| Toolchain | Entry point | Enforcement state | Owner |
|---|---|---|---|
| **Flexible** (default) | `tools/fm/validate.py --type-check` invoked by `tools/check-governance.sh` | **Gating** — non-zero exit blocks the pre-commit hook. | Tasks 016 / 017 / 019 lineage. |
| **Legacy** (archive; not wired into the gate) | `tools/legacy/{validate-frontmatter,lint-structure,lint-linkage}.py` | Not invoked by `tools/check-governance.sh`. Retained because `tools/check-maintenance-bypass.py` still folds their structural and cross-reference output into the bypass index. | Task 001 lineage; scheduled for removal once those structural rules are folded into `fm/validate.py` / a successor `fm-graph`. |

The `FM_TOOLCHAIN` env var was retired by [Task 054](./tasks/054-flip-fm-toolchain-default/). `tools/fm/validate.py` is invoked unconditionally; there is no longer a configuration that promotes the legacy linters to the gate.

Maintenance agents MUST be aware that:

1. T1/T2 mutations through `tools/fm/edit.py` are the canonical mutator path. The file lock and per-section preservation behave identically across the toolchain.
2. The maintenance-bypass mode in `.githooks/pre-commit` (§4.1) harvests `<path>::<level>:<code>:<msg>` diagnostics from `tools/fm/validate.py` and folds the legacy `lint-structure` / `lint-linkage` shims in for the gaps fm-validate does not yet cover (per Task 017 Batch 2c). There is no separate waiver file at `tools/.frontmatter-waivers`; waivers, when needed, are expressed inline against `tools/fm/validate.py`'s diagnostic codes (`F.3.x`, `F.4.x`, etc.) rather than a path list. An agent that finds a legitimately-bypassable error MUST file a Task with the diagnostic code and the rationale rather than introducing an out-of-band waiver mechanism.
3. The coherence-check routine is wired to `tools/check-governance.sh` (Step 2.5 linter-first triage); it MUST NOT silently disable either toolchain. If the advisory legacy shim points at a real defect that fm-validate misses, file a Task to fold the rule into fm-validate rather than papering over the warning.

#### 1.1.2 Three-way Legacy / Flexible / ADR transition matrix

Post-Task-031, the gate composes **three** toolchains rather than two: the **Legacy** linters retained as a one-release escape hatch, the **Flexible** frontmatter toolchain that is the canonical gate, and the **ADR Governance Validator** ([`tools/adr/cli.py validate`](./tools/adr/cli.py)) that runs unconditionally as step `[5/6]` of [`tools/check-governance.sh`](./tools/check-governance.sh). The matrix below restates [PRE_COMMIT.md §7.A](./PRE_COMMIT.md) in maintenance-routine vocabulary; the columns are exactly three and the matrix MUST NOT silently grow a fourth column for MCP servers (per [Task 040 §C](./tasks/040-superclaude-spec-evaluation/synthesis.md): zero MCP servers are configured today). The vocabulary lifted into this section's prose — *nightly maintenance* as the framing for `/sc:improve` + `/sc:cleanup` + `/sc:build` — is a MERGE-INTO-EXISTING-TASK-039 outcome from [Task 040 §A row §8](./tasks/040-superclaude-spec-evaluation/synthesis.md); the citation is informational only and MUST NOT be read as importing Tavily, Playwright, MorphLLM-Fast-Apply, or Chrome DevTools as repo-tooling dependencies.[^morphllm]

| Toolchain | Canonical entry point | Enforcement state | Flip-criteria predicate (mechanically verifiable) |
|---|---|---|---|
| **Legacy** | `tools/legacy/{validate-frontmatter,lint-structure,lint-linkage}.py` | Advisory shim (`FM_LEGACY_QUIET=1` by default). One-release retirement window. | Retired when [`research/toolchain-flip-criteria/output/SPEC.md` §1 TFC.1.1 through TFC.1.7](./research/toolchain-flip-criteria/output/SPEC.md) all hold simultaneously: gating-step coverage (TFC.1.1), legacy no-op under the gate (TFC.1.2), waivers carry zero legacy diagnostic codes (TFC.1.3), Tasks 016/017/019 closed (TFC.1.4), no live consumer outside the gate (TFC.1.5), pytest green canonical-only (TFC.1.6), trust-audit AGGREGATOR landed or threshold raised to 0.90 (TFC.1.7). The flip is the single atomic commit enumerated in §2 of that SPEC. |
| **Flexible** (canonical) | `tools/fm/validate.py --type-check` invoked by `tools/check-governance.sh` step `[1/6]` | **Gating** — non-zero exit blocks the pre-commit hook. | Already canonical. The flexible column is gating before, during, and after the Legacy retirement; no flip predicate applies. |
| **ADR** | [`tools/adr/cli.py validate`](./tools/adr/cli.py) (PRE_COMMIT.md §7.C) | **Gating** — runs unconditionally as step `[5/6]` of `tools/check-governance.sh`; graceful no-op when `decisions/` is empty. | Composes orthogonally to the Legacy-flip; ADR semantics MUST NOT change at flip time. After the Legacy column retires, step numbering re-flows from `[*/6]` to `[*/5]` and the ADR validator anchors at step `[5/5]` per `research/toolchain-flip-criteria/output/SPEC.md` §3.4. |

**Flip semantics.** The maintenance agent MUST treat the Legacy column as live (advisory) until *every* TFC.1.x predicate holds against `HEAD`. The flip is non-negotiable atomic: it MUST land as a single commit per [SPEC §2.1 enumeration](./research/toolchain-flip-criteria/output/SPEC.md), and it MUST NOT bundle WARN-tier promotions (those are sequenced into separate post-flip Tasks per SPEC §3.2). Rollback is by `git revert <flip-sha>` per SPEC §4; the maintenance run-log MUST record the flip with a `routine_type: task-implementation` record (§2.3 record types).

**Trust-audit composition.** The AGGREGATOR ([`tools/maintenance/trust-audit.py`](./tools/maintenance/trust-audit.py), Task 039 ST-5) imports the GATE schema from [`tools/check-trust-audit.py`](./tools/check-trust-audit.py) (Task 035 ST-4); the two are schema-locked. After the Legacy flip, the AGGREGATOR continues to run as part of the nightly maintenance roll-up regardless of which toolchain column is canonical — it composes orthogonally to Legacy/Flexible/ADR.

[^morphllm]: MorphLLM-Fast-Apply is a known external editing tool that *could* prove useful for bulk T1/T2 mutations against `tools/fm/edit.py`, but it is **not** configured in this repository today. Any future Task that proposes MorphLLM as a repo-tooling dependency MUST file its own scaffolded chain (research → tooling → spec amendment) rather than retrofitting it as a fourth toolchain column. See [`tasks/040-superclaude-spec-evaluation/synthesis.md`](./tasks/040-superclaude-spec-evaluation/synthesis.md) §C for the reality-check matrix that motivated this footnote.

---

## 2. Repo Coherence Check (Primary Routine)

The **Repo Coherence Check** is a recurring, git-delta-aware self-improvement routine. Its prompt lives at [`/prompts/repo-coherence-check/prompt.md`](./prompts/repo-coherence-check/prompt.md).

### 2.1 When to Run

The agent SHOULD run the Repo Coherence Check:
- At the start of every new Claude Code session in this repository.
- Before opening any new Task (to ensure the working base is coherent).
- After any merge or rebase that brings in ≥ 3 changed files.

The prompt MUST be configured as a Claude Code SessionStart hook or invoked via `/loop` at the operator's discretion. See the prompt for wiring instructions.

### 2.2 What it Does

1. Reads `maintenance/run-log.md` to retrieve the `end_commit` from the last run.
2. Computes `git log <last_end_commit>..HEAD` to produce the delta since the last run.
3. Scans only the changed files in the delta (never a full-repo rescan).
4. Applies T1 and T2 repairs immediately.
5. Writes Tasks for T3 findings.
6. Appends a run record to `maintenance/run-log.md`.
7. Commits all repairs in a single atomic commit.

### 2.3 Run-Log Protocol

Every run MUST append one record to `maintenance/run-log.md` before the run's commit. The record format is defined in that file's header.
The baseline is recorded as a *content-hash of the run-log entry* in addition to the commit hash.
The agent MUST determine the baseline by reading the most recent reachable `end_commit` field (falling forward). If no recent `end_commit` is reachable, the agent MUST fail loudly and require a human-confirmed reseed (a tagged "coherence-reseed" annotation in `maintenance/run-log.md`). If the field is absent entirely (first run ever), the agent MUST use the repository's initial commit as the baseline.

**Record types (per Task 032 finding F9).** Each record carries a `routine_type:` enum field with one of four values:

| `routine_type` | Appended by | Counter semantics |
|---|---|---|
| `bootstrap` | The very first run-log seed. | All counters are zero by definition. |
| `coherence-check` | A Repo Coherence Check sweep (this section's primary routine). | `t1/t2/t3_tasks_created` count repairs/Tasks produced over the delta since the previous baseline. |
| `nightly-maintenance` | A Nightly Maintenance Run (§3). | Same counter semantics as `coherence-check` but over the audit's broader scope. |
| `task-implementation` | The closing commit of a Task implementation; logged so subsequent agents see the new tools/files. | Counters describe Task-internal work, NOT a coherence sweep. Administrative closures of superseded Tasks also use this value. |

The awk fall-forward in `prompts/repo-coherence-check/prompt.md` Step 1a keys on `end_commit:` regardless of `routine_type:`, so `task-implementation` records remain valid baselines (they advance HEAD). However, when computing aggregate metrics ("how many T3 Tasks were filed by coherence runs in May 2026?") an agent MUST filter on `routine_type: coherence-check` to avoid conflating Task-scope counters with sweep-scope counters.

**Trust-audit gating before research closure.** Before any research workspace transitions from `research_phase: in_progress` to `research_phase: complete`, the agent owning the workspace MUST invoke the trust-audit GATE ([`tools/check-trust-audit.py`](./tools/check-trust-audit.py), Task 035 ST-4) against that workspace and obtain a green result. The GATE evaluates the three trust dimensions defined by [`research/agentic-eval-trust-improvement-spec/output/SPEC.md`](./research/agentic-eval-trust-improvement-spec/output/SPEC.md) (Spec-J multi-dimensional evaluation, Spec-K trust calibration, Spec-L governance improvement loop). The GATE is the per-workspace contract; the cross-workspace AGGREGATOR ([`tools/maintenance/trust-audit.py`](./tools/maintenance/trust-audit.py), Task 039 ST-5) imports the GATE's `DIAGNOSTIC_SCHEMA` and rolls findings up into the nightly maintenance run-log. The two MUST NOT duplicate trust-evaluation logic: the AGGREGATOR delegates per-workspace evaluation to the GATE and only aggregates results.

A research workspace whose GATE invocation emits any ERROR-tier diagnostic MUST NOT be flipped to `research_phase: complete`. The maintenance bypass mode in [§4.1](#41-maintenance-bypass-mode) MUST NOT be used to evade this check; trust-audit failures are evidence that the synthesis is not yet trustworthy, not that the linter is misconfigured. The acceptance contract for this rule is anchor [`M.B.5`](#6-acceptance-criteria-gherkin-scenarios) below.

**Run-log baseline recovery.** The fall-forward awk recovers the most-recent reachable `end_commit:` even when intermediate records are malformed. If no `end_commit:` is reachable anywhere in the file (the run-log is corrupt or has been truncated), the agent MUST fail loudly per [`research/governance-specs-update-research/output/SPEC.md` §2](./research/governance-specs-update-research/output/SPEC.md) (recommended amendments). The agent MUST NOT silently fall back to the repo's initial commit when the file is non-empty but corrupt; the only sanctioned reseed is a human-confirmed `coherence-reseed` annotation appended to `maintenance/run-log.md`. The acceptance contract for this rule is anchor [`M.B.1`](#6-acceptance-criteria-gherkin-scenarios) below.

---

## 3. Nightly Maintenance Run (Secondary Routine)

The Nightly Maintenance Run is a broader sweep executed less frequently (e.g. weekly or after large batches of work).

### 3.1 Scope

- **DO:** Update the dynamic sections of `readme.md` files (State, Learnings, Blockers) across the repository.
- **DO:** Aggregate unstructured insights from `friction-log.md` files into formal Tasks in `/tasks/`.
- **DO:** Verify that every open Task in `/tasks/` has a corresponding prompt in `/prompts/`.
- **DON'T:** Apply T3 or T4 changes directly. Write Tasks for them.
- **DON'T:** Re-execute or modify completed research workspaces.

### 3.2 Dynamic Readme Updates

`readme.md` files MUST act as executable state machines, not static indices, per [`research/repo-maintenance-protocol-spec/output/SPEC.md` §3](./research/repo-maintenance-protocol-spec/output/SPEC.md) ("Dynamic Readme Schema"). Every operational `readme.md` MUST be partitioned into a *static* region above an HTML-comment boundary marker and a *dynamic* region below it.

**Static section (preserve unless files move):**
- Purpose — why this folder exists in this location.
- Linked Navigation — relative Markdown links to every file and subfolder.
- Assumptions Log — `## Assumptions Log` heading; either substantive entries or the literal `(none)` line.

**Dynamic section (actively rewrite):**
- Current State — operational status of the folder.
- Latest Synthesised Learnings — bullet points from nested `synthesis/` or `reflection/` folders.
- Open Blockers — any outstanding issues preventing further progress.

**Boundary markers.** The static and dynamic regions MUST be separated by the HTML comments `<!-- BEGIN DYNAMIC -->` and `<!-- END DYNAMIC -->`. Maintenance routines MUST NOT rewrite content above the `BEGIN DYNAMIC` marker (except to repair broken relative links); they MUST rewrite the content between the markers from the latest synthesis/reflection sources during every Nightly Maintenance Run.

**Mechanical enforcement.** [`tools/maintenance/dynamic-readme-partition.py`](./tools/maintenance/dynamic-readme-partition.py) (Task 039 ST-4) is the partition linter. It walks operational `readme.md` files under `tasks/`, `research/`, and `prompts/`, verifies the marker pair is present, and emits a diagnostic when the static/dynamic boundary is violated. The linter is advisory-tier today; promotion to gating requires the corpus to be clean (per the [Toolchain Flip SPEC §3.2](./research/toolchain-flip-criteria/output/SPEC.md) WARN→ERROR sequencing rule).

**Aggregator integration with the trust-audit nightly roll-up.** The dynamic section's "Latest Synthesised Learnings" bullets for any operational folder under `research/` MUST be sourced from the per-workspace trust-audit GATE output (§2.3). The cross-workspace AGGREGATOR ([`tools/maintenance/trust-audit.py`](./tools/maintenance/trust-audit.py), Task 039 ST-5) is the nightly roll-up surface; its output is the canonical input to the dynamic-readme rewrite step. The acceptance contract for this rule is anchor [`M.B.6`](#6-acceptance-criteria-gherkin-scenarios) below.

### 3.3 Task Delegation Pipeline

The repository self-improves by converting friction into Tasks.

1. **Extract friction** — scan all `reflection/friction-log.md` files. Identify FL1–FL3 entries and unresolved contradictions.
2. **Package as Tasks** — for each FL1+ issue, create a Task in `/tasks/<NNN>-<slug>/task.md` per `TASK.md`. The Task MUST link to a prompt in `/prompts/<slug>/prompt.md` that a future agent can execute. The agent MUST NOT fix the complex issues directly during the maintenance run.

### 3.4 Stale-Task Audit and the `updated` Lifecycle

The Coherence Check and the Nightly Maintenance Run MUST audit the freshness of every open Task whose `created` date precedes the most recent `done` Task by more than the staleness window (default: 7 days, configurable via `MAINT_STALE_DAYS`). For each candidate the agent MUST classify the Task into one of four buckets:

| Bucket | Symptom | Action |
|---|---|---|
| **Still accurate** | Plan, Todo, and `task_affects_paths` still describe work that needs doing in the form described. | No action. Optionally bump `updated:` to today (T1). |
| **Drifted (re-frame)** | Goal is still desirable, but Plan/Todo no longer reflect the current repo state — usually because a successor Task or a research SPEC shipped tooling that subsumes part of the original plan. | Apply the **`updated` lifecycle** per `TASK.md §4.7`: create a successor Task, set `task_supersedes`/`task_superseded_by` reciprocally, flip the predecessor's `task_status: updated`, write a `friction-log.md` with a Supersession Rationale paragraph. This is a **T3 action** (§1) — the agent MUST file the lifecycle transition itself as a Task only if the supersession spans more than the typical two-Task pair (e.g. when one predecessor splits into multiple successors with non-trivial scoping decisions). For ordinary 1→1 supersessions, the maintenance agent MAY perform the transition directly because every step is mechanical (frontmatter mutations + a one-paragraph friction log) and reversible. |
| **Completed by drift** | Every Todo item is satisfied by other commits (the artefacts now exist) but the Task was never closed. | Close as `task_status: done` with a `friction-log.md` noting "completed-by-drift" and pointing at the commits that satisfied each Todo. |
| **No longer desirable** | The Task's intent is not relevant any more (e.g. a feature was deleted). | Close as `task_status: abandoned` per `TASK.md §8.3`. Do NOT use `updated` for cancellation. |

**Decision algorithm (deterministic).** The classification reduces to the five-signal decision tree shipped by [`research/spec-staleness-decision-formalization/output/SPEC.md` §1](./research/spec-staleness-decision-formalization/output/SPEC.md). The algorithm consumes the five signals defined in §2 of that SPEC and emits exactly one of `still_accurate`, `drifted`, `completed_by_drift`, `no_longer_desirable`. The tree has 3 levels and 4 leaves, well inside the SPEC's falsification bound (≤5 levels, ≤12 leaves). The maintenance agent MUST treat the SPEC pseudocode as the contract; it MUST NOT introduce additional buckets or signals at audit time.

**Signal vector** (see SPEC §2 for extraction recipes):

| # | Signal | Type | Default under ambiguity |
|---|---|---|---|
| **S1** | `todo_satisfaction` | float in `[0.0, 1.0]` | `0.0` (refuses to fire `completed_by_drift` on an empty Todo). |
| **S2** | `affects_paths_present` | bool (AND-aggregate) | `False` if `task_affects_paths` is empty. |
| **S3** | `plan_anchors_live` | bool | `True` if `## Plan` has zero relative links. |
| **S4** | `goal_endorsed` | bool | `False` (refuses to claim endorsement absent evidence). |
| **S5** | `successor_present` | bool | `False`. |

**Decision tree** (paraphrased from SPEC §1; the SPEC pseudocode is authoritative):

1. **Gate.** If `(today - task.created).days ≤ MAINT_STALE_DAYS`, the Task is younger than the audit window; the agent MUST skip it (no bucket emitted).
2. **Level 1 — Goal endorsement.** If `not goal_endorsed` (S4=False) → `no_longer_desirable`.
3. **Level 2 — Completion-by-drift.** If `todo_satisfaction ≥ 1.0 AND affects_paths_present` (S1=1.0 AND S2=True) → `completed_by_drift`.
4. **Level 3 — Drift vs. still-accurate.** If `successor_present OR not plan_anchors_live` (S5=True OR S3=False) → `drifted`.
5. **Default.** Otherwise → `still_accurate`.

**`MAINT_STALE_DAYS` configuration.** The staleness window MUST be configured via the environment variable `MAINT_STALE_DAYS`, an integer ≥ 1, with default `7` (per SPEC §4). The maintenance agent reads it as `int(os.environ.get("MAINT_STALE_DAYS", "7"))`; non-integer values MUST be rejected with exit code 2 and message `MAINT_STALE_DAYS must be a positive integer; got '<value>'`. Values > 365 are rejected as a sanity bound. Per-routine overrides are permitted (e.g. `MAINT_STALE_DAYS=3` for daily coherence sweeps, `MAINT_STALE_DAYS=14` for weekly nightlies); the override is invocation-local and does not edit any repo file.

**Mechanical implementation.** [`tools/maintenance/staleness-audit.py`](./tools/maintenance/staleness-audit.py) (Task 039 ST-3) implements the decision tree above. It walks every Task whose `task_status` is `open` or `in_progress`, applies the SPEC §1 pseudocode, and emits one diagnostic per Task in the canonical `<path>::<level>:<code>:<msg>` format consumed by [`tools/check-maintenance-bypass.py`](./tools/check-maintenance-bypass.py) and the coherence run-log. Exit codes: `0` if every audited Task is `still_accurate` (or every Task is younger than the staleness window); `2` if at least one Task lands in `{drifted, completed_by_drift, no_longer_desirable}` (advisory-tier); `1` on usage error. The script excludes `decisions/` from its scan by construction so that `adr_status: Accepted` files are never proposed for mutation (mirrors the §1 T4-immutability rule).

The acceptance contract for the bucket-assignment determinism is anchor [`M.B.3`](#6-acceptance-criteria-gherkin-scenarios) below.

**Successor naming.** A successor Task uses the next free `<NNN>` and a slug that signals continuity with the predecessor (e.g. `<predecessor-slug>-v2` or a more specific re-framing such as `<predecessor-slug>-via-fm-edit`). The successor's `## Goal` MUST open with a one-line "Successor to Task NNN" pointer; the body re-frames the work against current repo state.

**Mechanical cross-check.** The audit's `tasks/readme.md`-vs-`task_status` drift signal is also produced mechanically by [TASK.md §7.0 row §7.11](./TASK.md) (`tools/fm/index_diff.py`, landed by [Task 067](./tasks/067-sync-tasks-index-status-drift/task.md) — renumbered from 031 per [Task 043](./tasks/043-renumber-duplicate-task-ids-v3/) — per Task 032 finding F11). An agent SHOULD run `tools/check-governance.sh` first to surface drift; the §3.4 audit then handles the classification/lifecycle decision the linter cannot make on its own.

**Drift-check inputs differentiate spec-bearing from review-bearing research.** When the staleness audit walks `task_spawns_research` to verify that the produced research workspace still matches the Task's premise, it MUST classify the workspace before flagging drift:

- **Spec-bearing research** (`research/<slug>/output/SPEC.md` exists with `research_phase: complete`): the audit treats the SPEC as the canonical successor artefact and SHOULD trigger the **drifted (re-frame)** bucket only when the SPEC explicitly supersedes the Task's plan.
- **Review-bearing research** (workspaces produced for PR review or critique runs whose deliverable is `notes.md` / `output/REVIEW.md` rather than a SPEC): the audit MUST NOT treat the absence of a SPEC as drift. Review research closes by being filed and referenced; it is not expected to mutate root specs.

This distinction prevents the false-positive observed during the Task 001 friction log, where review-bearing research was flagged as "incomplete" against an audit rule that assumed every research run produces a SPEC.

### 3.5 Duplicate `task_id` Governance (T3 Renumbering)

Duplicate `task_id` collisions (e.g. two `task_id: "006"` folders) are a known failure mode of the §8.1 "renumber on commit" protocol when two agents pick the next free slot on independent branches. Resolving such a collision is a **T3 (Structural) action** per §1, even though the per-file mutation is mechanical, because the resolution touches:

- The colliding Task's folder name (`tasks/<NNN>-<slug>/` rename).
- That Task's `task_id` frontmatter value.
- Every reciprocal reference: `task_blocked_by`, `task_supersedes`, `task_superseded_by` in sibling Tasks.
- The bullet for the Task in `tasks/readme.md` (per `TASK.md §4.8`).

Because the change spans multiple files and rewrites cross-references, the maintenance agent MUST NOT perform the renumber inline during a coherence run. Instead it MUST file a Task (e.g. the Task 013 / Task 024 lineage) whose Plan covers:

1. Identify all colliding `task_id` values via `ls tasks/ | sort` and `grep '^task_id:' tasks/*/task.md`.
2. Pick the next free `<NNN>` slot for the *later-created* colliding folder (the earlier folder retains its number).
3. Rename the folder and update the `task_id` frontmatter atomically in one commit.
4. Rewrite every `task_blocked_by` / `task_supersedes` / `task_superseded_by` entry that referenced the renumbered Task by its old `<NNN>`.
5. Update `tasks/readme.md` so the bullet path and number match the new folder.
6. Verify `tools/check-governance.sh` exits 0 against the post-renumber state before committing.

The slug MUST remain stable across renumbering; only `<NNN>` and `task_id` change. Renumbering by reusing an unrelated free slot (e.g. picking 030 to clear a 006 collision) is permitted when the Task naturally fits later in the sequence.

**Resolving the discovery loop.** Until [Task 033 ST-3](./tasks/033-task-spec-integration/subtasks/03-tooling-duplicate-task-id-linter.md) shipped [`tools/fm/check-duplicate-task-id.py`](./tools/fm/check-duplicate-task-id.py), the §3.5 prose acknowledged a circular dependency: a coherence run discovers a collision, files a T3 Task, but the colliding state remains in the working tree until the Task runs — so the *next* coherence run re-discovers the same collision and would file a *duplicate* dedup Task. The dup-id linter resolves the loop mechanically.

**When the coherence run files the Task itself vs. waits for a human.** The maintenance agent MUST file the dedup Task **automatically** when *all four* of the following predicates hold:

1. `tools/fm/check-duplicate-task-id.py` emits exactly one collision pair (or a small N-way collision; the linter's report is mechanical).
2. No open Task's `task_affects_paths` already covers the colliding folders (the agent MUST grep `tasks/*/task.md` for the colliding `<NNN>` strings before filing).
3. The colliding folders have at least one `task_status: open` member (closing collisions on `done` Tasks is lower-priority and SHOULD wait for human review).
4. The current run is a Coherence Check (`routine_type: coherence-check`), not a Nightly Maintenance Run. Nightlies SHOULD escalate to a human-confirmed annotation rather than file a Task autonomously.

If any predicate fails, the agent MUST log the collision in the run-log notes and MUST NOT file a Task on its own; the human reviewer takes the next step.

**Interaction with `tools/check-governance.sh` step `[5/6]` (ADR validator).** The dup-id linter operates on Task folders only (`tasks/<NNN>-<slug>/`); it does NOT scan `decisions/<NNNN>-<slug>.md`. The ADR validator at step `[5/6]` (PRE_COMMIT.md §7.C) owns the `adr_*` namespace and rejects `adr_status: Accepted` mutations independently. The maintenance run MUST NOT edit any `decisions/<NNNN>-<slug>.md` file at any tier — not to renumber, not to bump `updated:`, not to repair a relative link — even when the dup-id linter is the entry point that surfaced the cross-reference. Cross-references from a renumbered Task into the ADR ledger are amended by *re-running* `tools/adr/cli.py synthesize` (which rewrites the guarded section of `AGENTS.md`), never by hand-editing the ADR file.

**Mechanical surface.** The linter is wired into `tools/check-governance.sh` as the optional `[opt]` block guarded by `FM_DUPLICATE_TASK_ID_STRICT` (default `0`); promotion to gating is owned by Task 043 (renumber) per the [Toolchain Flip SPEC §3.2](./research/toolchain-flip-criteria/output/SPEC.md) WARN→ERROR ladder. After Task 043 lands and the corpus is dup-free, the env-var default flips to `1` and the toggle is removed in the next release window.

The acceptance contract for the discovery-loop closure is anchor [`M.B.4`](#6-acceptance-criteria-gherkin-scenarios) below.

### 3.6 ADR Falsifier-Trigger Audit (Nightly Cadence)

[ADR-0008](./decisions/0008-narrative-skills-status-quo.md) and [ADR-0009](./decisions/0009-root-spec-no-consolidation.md) each ratify *status quo* with a set of falsifier triggers that, when fired, mandate a successor ADR. The eight triggers are mechanical, semi-mechanical, or manual predicates. Without a recurring measurement cadence, the triggers are theoretical: a decision ratified at `adr_status: Proposed` would never collect the evidence required to flip to `Accepted` or to spawn a successor.

[`tools/maintenance/adr-trigger-audit.py`](./tools/maintenance/adr-trigger-audit.py) (Task 069) is the binding measurement mechanism for the eight triggers. It composes [`tools/maintenance/bundle-size-snapshot.py`](./tools/maintenance/bundle-size-snapshot.py) for the two bundle-token triggers (ADR-0008 F2 + ADR-0009 F1), reuses the snapshot's `--include-dependents` extension for ADR-0009 F2, walks `skills/` for ADR-0008 F1, aggregates `tasks/*/friction-log.md` for the two semi-mechanical sustained-friction triggers (ADR-0008 F3 + ADR-0009 F3), and scans `task_affects_paths:` blocks for ADR-0008 F4. The single manual trigger (ADR-0008 F5 — third-party-adopter blocker) MUST surface as `MANUAL` in the audit report rather than as a fire/no-fire predicate; the audit cannot synthesise a missing signal.

**Cadence.** The Nightly Maintenance Run (§3) MUST invoke `python3 tools/maintenance/adr-trigger-audit.py --format runlog` once per run and append the single-line projection to [`maintenance/run-log.md`](./maintenance/run-log.md) as a sibling of the run record. The Repo Coherence Check (§2) MAY invoke the audit but is NOT required to; the audit's data refreshes slowly (bundle size, skill counts, friction over a 14-day window) and the coherence-check cadence is per-session, which over-samples the predicate space.

**Runlog projection format.** One line per nightly run, appendable to `maintenance/run-log.md`:

```
YYYY-MM-DD | adr-trigger-audit | 8 triggers / window=14d / bundle~<N> tokens | <ok|FIRED:CODE,CODE...> | manual=<CODE,CODE...>
```

The projection is intentionally identical in shape to `bundle-size-snapshot.py --format runlog` so a maintenance agent can `grep` both lines from the same record window.

**Exit-code contract.** The audit exits `0` when no mechanical or semi-mechanical trigger fires (manual triggers are reported but never count as a fire), `2` when at least one trigger fires (advisory-tier — a maintainer decides whether to file an ADR-0008 / ADR-0009 successor), and `1` on usage error. The audit MUST NOT be wired into the default `tools/check-governance.sh` gate; it MAY run as an `[opt]`-tier WARN-only row if the maintainer chooses to surface fires in pre-commit output, but a fired trigger MUST NOT block a commit.

**Action on a fire.** When the audit reports `FIRED:<CODE>`, the maintenance agent MUST NOT mutate ADR-0008 or ADR-0009 in place (both files are `T4`-immutable once `Accepted`; while at `Proposed` they remain root-spec-tier per §1 and require a successor or amendment Task). Instead the agent MUST file a Task whose Plan covers the successor ADR per [`decisions/readme.md`](./decisions/readme.md), citing the audit's diagnostic line as the evidence anchor.

The acceptance contract for the audit cadence is anchor [`M.B.8`](#6-acceptance-criteria-gherkin-scenarios) below.

---

## 4. Finalising Any Run

Before committing the results of any maintenance run, verify:

1. All touched `readme.md` files comply with the static/dynamic partitioning schema (§3.2).
2. All T3 findings have a corresponding Task in `/tasks/`.
3. No T3 or T4 changes were made directly.
4. `maintenance/run-log.md` has been updated with the run record.
5. The commit message references the run-log entry date and the commit range scanned.

### 4.1 Maintenance Bypass Mode

The repository employs a **maintenance-bypass** mode in `.githooks/pre-commit`. By default, the pre-commit hook blocks any commit if a governance linter fails. However, if the repository has pre-existing errors, the hook will allow the commit **if and only if** every file causing an error has a corresponding `open` Task in `/tasks/` whose `task_affects_paths` array covers the offending file. If any error is not covered by an open Task, the commit MUST block.

`tools/check-maintenance-bypass.py` (re-pointed by Task 017 Batch 2c) harvests `<path>::<level>:<code>:<msg>` diagnostics from `tools/fm/validate.py` as the canonical source of error-bearing paths and folds the legacy `tools/legacy/lint-structure.py` / `lint-linkage.py` outputs in to cover structural and cross-reference rules fm-validate does not yet replace. A path is considered "covered" when it appears in some open Task's `task_affects_paths`.

---

## 5. Maintenance Folder Reference

The `/maintenance/` folder is the governance support centre for this repository. It holds content that root specs summarise but do not define:

| File | Purpose |
|---|---|
| [`maintenance/language-spec.md`](./maintenance/language-spec.md) | Canonical RFC 2119 keyword definitions, Gherkin syntax binding, full Frontmatter Ontology (L0–L3). |
| [`maintenance/run-log.md`](./maintenance/run-log.md) | Structured log of every Coherence Check and Nightly Maintenance run. The agent reads this to establish its starting-commit baseline. |

The `/maintenance/` folder MUST NOT be used to store Task orchestration, prompt drafts, or research workspaces. Those belong in `/tasks/`, `/prompts/`, and `/research/` respectively.

### 5.1 Tooling Prerequisites

`tools/check-governance.sh` runs five mandatory steps (`fm-validate --type-check`, `lint-structure`, `lint-runlog`, `adr/cli.py validate`, `fm/index_diff`) plus a `[trust]` audit and an OPTIONAL narrative-ontology pair gated on `maintenance/schemas/narrative-ontology/ontology.json` existing on disk. The mandatory steps require only PyYAML; the optional narrative-ontology validator additionally requires `jsonschema>=4.18`. Per Task 032 finding F8, when `jsonschema` is absent, `tools/dramatica-nav/validate.py` emits a `WARN` and exits 0 so the suite-level exit code is not poisoned by a missing optional dependency.

The supported install path is `./install.sh` (which pulls all of `tools/requirements.txt`); contributors who skip it MAY still invoke `tools/check-governance.sh` and will see the WARN above instead of a misleading FAIL.

---

## 6. Acceptance Criteria (Gherkin Scenarios)

The seven scenarios below are the executable acceptance contract for §1, §2.3, §3.2, §3.4, and §3.5. Each scenario is anchored with a stable identifier (`M.B.<n>`); the linters cited above are the mechanical hooks for scenarios where automation is feasible. The `Scenario:` line is preceded by a `# anchor: <id>` comment so downstream Gherkin parsers can address the scenario directly.

```gherkin
# anchor: M.B.1 — run-log baseline recovery
Feature: Coherence run recovers `end_commit` when the run-log is corrupt
Scenario: Last record is malformed but a prior record carries a valid end_commit
  Given `maintenance/run-log.md` has 12 records
  And the most recent record's `end_commit:` field is missing or malformed
  And the immediately-prior record's `end_commit:` is the SHA `4c5e7e4`
  When the coherence-run agent reads the file at Step 1a of `prompts/repo-coherence-check/prompt.md`
  Then the awk fall-forward MUST recover `4c5e7e4` as the baseline
  And the agent MUST proceed with `git log 4c5e7e4..HEAD --name-only` as the delta source
  And the agent MUST NOT silently fall back to the repo's initial commit
  And if no prior record carries a valid `end_commit:` the agent MUST fail loudly with a `coherence-reseed` request
```

```gherkin
# anchor: M.B.2 — T1 / T2 / T3 tier classification boundary
Feature: Maintenance agent classifies a proposed change before mutation
Scenario: Stale `updated:` date on a task.md is a T1 mechanical repair
  Given `tasks/099-example/task.md` has `updated: 2026-04-01`
  And the file's most-recent body-byte change in `git log` is dated `2026-05-07`
  When the maintenance agent identifies the staleness during a coherence run
  Then the agent MUST classify the repair as T1 (Mechanical, §1)
  And the agent MUST apply the repair via `tools/fm/edit.py --bump-updated tasks/099-example/task.md`
  And the agent MUST NOT use `sed` or `awk` to mutate frontmatter
  And the repair MUST land in the same atomic commit as the run-log record
Scenario: Adding a missing `type:` key to a task.md is T2 (Additive)
  Given `tasks/098-example/task.md` lacks a `type:` L1 frontmatter key
  And the file lives under `tasks/` (so the unambiguous value is `task`)
  When the maintenance agent observes the missing key
  Then the agent MUST classify the repair as T2 (Additive, §1)
  And the agent MUST apply the repair via `tools/fm/edit.py --set type=task tasks/098-example/task.md`
Scenario: Renaming a section heading in a root spec is T3 (Structural)
  Given `MAINTENANCE.md` carries a heading `## 3.4 Stale-Task Audit and the `updated` Lifecycle`
  And the maintenance agent considers renaming the heading to `## 3.4 Staleness Audit`
  When the agent classifies the proposed change
  Then the agent MUST classify the change as T3 (Structural, §1)
  And the agent MUST NOT edit `MAINTENANCE.md` directly during the coherence run
  And the agent MUST file a Task in `/tasks/<NNN>-<slug>/` whose Plan covers the rename
```

```gherkin
# anchor: M.B.3 — stale-task lifecycle bucket assignment
Feature: Staleness audit emits a deterministic bucket per the §3.4 decision tree
Scenario: Task older than `MAINT_STALE_DAYS` with every Todo satisfied lands in completed-by-drift
  Given a Task `tasks/050-example/task.md` whose `created:` is `2026-04-01`
  And today's date is `2026-05-08`
  And `MAINT_STALE_DAYS` resolves to `7` (the default)
  And every `## Todo` checkbox is `- [x]` (S1 = 1.0)
  And every path in `task_affects_paths` exists on disk (S2 = True)
  And at least one current root spec endorses the Task's Goal (S4 = True)
  When `tools/maintenance/staleness-audit.py` evaluates the Task per `research/spec-staleness-decision-formalization/output/SPEC.md` §1
  Then the script MUST classify the Task as `completed_by_drift`
  And the script MUST emit one diagnostic line in the form `tasks/050-example/task.md::WARN:MAINT.STALE.COMPLETED_BY_DRIFT:<msg>`
  And the script MUST exit `2` (advisory-tier — at least one Task is non-still_accurate)
  And the script MUST NOT mutate the Task file
Scenario: Two independent agents agree on the bucket for the same HEAD
  Given two maintenance agents A and B run `tools/maintenance/staleness-audit.py` against the same `HEAD`
  And both export `MAINT_STALE_DAYS=7`
  When each agent collects the per-Task bucket assignments
  Then the two agents MUST emit identical `(<NNN>, <bucket>)` pairs for every audited Task
  And any divergence MUST be filed as a classifier-implementation bug, NOT a SPEC ambiguity
```

```gherkin
# anchor: M.B.4 — dup-id discovery loop closure
Feature: Coherence run files exactly one dedup Task per collision, never a duplicate
Scenario: Coherence run discovers a 006 collision and files Task 044 once
  Given `tools/fm/check-duplicate-task-id.py` reports exactly one collision pair `(006-foo, 006-bar)`
  And no existing open Task's `task_affects_paths` covers `tasks/006-foo/` OR `tasks/006-bar/`
  And at least one of the colliding folders has `task_status: open`
  And the current run carries `routine_type: coherence-check`
  When the maintenance agent applies the §3.5 "When the coherence run files the Task itself" predicates
  Then the agent MUST file a single new Task at the next free `<NNN>` (e.g. `tasks/044-resolve-006-collision/`)
  And the agent MUST set the new Task's `task_affects_paths` to cover both colliding folders
  And `tasks/readme.md` MUST be updated in the same commit per TASK.md §4.8
  And on the *next* coherence run the linter MUST recognise the open dedup Task
        via `task_affects_paths` and MUST NOT file a duplicate Task
Scenario: Nightly maintenance escalates to a human rather than autofiling
  Given `tools/fm/check-duplicate-task-id.py` reports a collision pair
  And the current run carries `routine_type: nightly-maintenance` (NOT coherence-check)
  When the maintenance agent applies the §3.5 predicates
  Then the agent MUST log the collision in the run-log `notes:` field
  And the agent MUST NOT file a dedup Task autonomously
  And the human reviewer MUST take the next step
```

```gherkin
# anchor: M.B.5 — trust-audit gating before research closure
Feature: Research workspace cannot transition to complete while trust-audit fails
Scenario: GATE emits an ERROR; the workspace MUST NOT flip to research_phase: complete
  Given a research workspace at `research/example-spec/` whose `readme.md` carries `research_phase: in_progress`
  And the agent intends to flip the workspace to `research_phase: complete`
  When the agent invokes `python3 tools/check-trust-audit.py research/example-spec/`
  And the GATE emits at least one ERROR-tier diagnostic against the schema/behavioral/governance dimensions
  Then the agent MUST NOT mutate `research/example-spec/readme.md` to set `research_phase: complete`
  And the agent MUST NOT use the maintenance-bypass (§4.1) to evade the failure
  And the agent MUST repair the underlying defect (or file a Task that does) before retrying the transition
Scenario: AGGREGATOR rolls per-workspace GATE results into the nightly maintenance run-log
  Given three research workspaces have transitioned to `research_phase: complete` since the last nightly
  When `python3 tools/maintenance/trust-audit.py` runs as part of the nightly roll-up
  Then the AGGREGATOR MUST import `DIAGNOSTIC_SCHEMA` from `tools/check-trust-audit.py` (no duplicate logic)
  And the AGGREGATOR MUST emit one summary record per workspace into the maintenance run-log
  And any workspace whose GATE result regressed since the previous nightly MUST be flagged in the roll-up
```

```gherkin
# anchor: M.B.6 — dynamic-readme partition
Feature: Maintenance run rewrites the dynamic section but preserves the static section
Scenario: Operational readme has the BEGIN/END DYNAMIC markers; nightly rewrite respects them
  Given `tasks/051-example/readme.md` carries `<!-- BEGIN DYNAMIC -->` and `<!-- END DYNAMIC -->` markers
  And the section above `BEGIN DYNAMIC` lists Purpose, Linked Navigation, and Assumptions Log (static)
  And the section between markers lists Current State, Latest Synthesised Learnings, Open Blockers (dynamic)
  When the Nightly Maintenance Run rewrites the file from the latest synthesis sources
  Then the agent MUST NOT mutate any byte above `<!-- BEGIN DYNAMIC -->`
  And the agent MUST overwrite the content between the markers with the freshly-aggregated state
  And `tools/maintenance/dynamic-readme-partition.py` MUST exit 0 against the rewritten file
Scenario: Partition violation is reported as a diagnostic
  Given `tasks/052-example/readme.md` is missing the `<!-- BEGIN DYNAMIC -->` marker
  When `python3 tools/maintenance/dynamic-readme-partition.py tasks/052-example/readme.md` runs
  Then the linter MUST emit a diagnostic naming the missing marker
  And the linter MUST NOT mutate the file (it is a verifier, not a mutator)
```

```gherkin
# anchor: M.B.7 — ADR T4-immutability
Feature: Coherence run refuses to mutate any `adr_status: Accepted` file at any tier
Scenario: Coherence run refuses to mutate Accepted ADR
  Given a `decisions/0042-storage-path.md` with frontmatter `adr_status: Accepted`
  And a coherence-run agent identifies a missing `updated:` date as a T1 repair
  When the agent attempts to apply the T1 repair via `tools/fm/edit.py`
  Then `tools/fm/edit.py` MUST refuse with diagnostic
        `M.B.7:adr-accepted-immutable:cannot apply T1 to adr_status=Accepted`
  And the agent MUST file a Task at the next free `<NNN>` instead of mutating
  And `tasks/readme.md` MUST be updated in the same commit per TASK.md §4.8
Scenario: Maintenance run MUST NOT mutate `decisions/<NNNN>-<slug>.md` at any tier
  Given any file under `decisions/` with frontmatter `adr_status: Accepted`
  And a maintenance routine (Coherence Check or Nightly Maintenance Run) is active
  When the routine considers a T1, T2, or T3 mutation against the file
  Then the routine MUST refuse to mutate the file in place at every tier
  And the routine MUST NOT bump `updated:`, MUST NOT repair relative links, MUST NOT renumber the slot
  And the routine MUST author a successor ADR per `decisions/readme.md` instead
  And `tools/maintenance/staleness-audit.py` MUST exclude `decisions/` from its scan by construction
```

The seven anchors above (M.B.1 through M.B.7) close the (a)–(f) Goal of [Task 039](./tasks/039-maintenance-spec-integration/task.md). Future Tasks that promote any advisory linter to gating MUST add a paired Gherkin scenario under the next free anchor (M.B.8 onward) so the acceptance contract grows with the toolchain.

```gherkin
# anchor: M.B.8 — ADR falsifier-trigger audit cadence
Feature: Nightly maintenance run invokes the ADR-0008 / ADR-0009 trigger audit and records the result
Scenario: Audit runs once per nightly cadence and emits a runlog projection
  Given the Nightly Maintenance Run (§3) is active
  And `tools/maintenance/adr-trigger-audit.py` is executable
  When the maintenance agent invokes `python3 tools/maintenance/adr-trigger-audit.py --format runlog`
  Then the audit MUST emit exactly one line in the form
        `<date> | adr-trigger-audit | 8 triggers / window=<N>d / bundle~<N> tokens | <ok|FIRED:...> | manual=...`
  And the agent MUST append the line to `maintenance/run-log.md` in the same atomic commit as the run record
  And the audit MUST exit `0` when no mechanical or semi-mechanical trigger fires
  And the audit MUST exit `2` when at least one such trigger fires (advisory)
  And manual triggers (ADR-0008 F5) MUST be reported as `MANUAL` and MUST NOT count as a fire
Scenario: Audit fire spawns a successor-ADR Task rather than an in-place edit
  Given the audit emits `FIRED:ADR-0008.F1` (narrative-skill count exceeds threshold)
  When the maintenance agent processes the diagnostic
  Then the agent MUST NOT mutate `decisions/0008-narrative-skills-status-quo.md` in place
  And the agent MUST file a Task whose Plan covers the ADR successor per `decisions/readme.md`
  And the Task's `task_affects_paths` MUST include the ADR file
  And the Task body MUST cite the audit's diagnostic line as evidence
```
