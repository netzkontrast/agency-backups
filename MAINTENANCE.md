---
type: spec
status: active
slug: maintenance-spec
summary: "Governs the Nightly Maintenance Run and the Repo Coherence Check routine. Defines scope, repair permissions, run-log protocol, and Task delegation rules for all automated maintenance agents."
created: 2026-05-02
updated: 2026-05-08
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

**Mutation surface stability.** `tools/fm/edit.py` is the canonical T1/T2 mutator for frontmatter; coherence-check agents SHOULD prefer it over `sed`/`awk` because it preserves body bytes and quoting, takes a file lock, and rejects T3/T4 operations by construction (per [SPEC.md §7.2](./research/flexible-frontmatter-toolchain/output/SPEC.md)). Body-section mutations are deferred to `tools/fm/section.py` (Task 018).

### 1.1 Toolchain Surface (Post-Migration)

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

`readme.md` files MUST act as executable state machines, not static indices. Enforce this partition:

**Static section (preserve unless files move):**
- Purpose and why this folder exists.
- Linked navigation (relative Markdown links to all files and subfolders).

**Dynamic section (actively rewrite):**
- Current State — operational status of the folder.
- Latest Synthesised Learnings — bullet points from nested `synthesis/` or `reflection/` folders.
- Open Blockers — any outstanding issues preventing further progress.

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

**Decision algorithm.** For a candidate Task:

1. Read `task.md` and every artefact path in `task_affects_paths`.
2. For each Todo item, attempt to verify whether it has been satisfied (artefact exists and matches the Todo's intent).
3. If 100% satisfied → **completed-by-drift**.
4. Else if the Task references mechanisms that have been retired or superseded (legacy linters, persistent indexes when `tools/fm/` is the canonical surface, etc.) → **drifted (re-frame)**.
5. Else if the Task's Goal is no longer endorsed by any current spec → **no longer desirable**.
6. Else → **still accurate**.

**Successor naming.** A successor Task uses the next free `<NNN>` and a slug that signals continuity with the predecessor (e.g. `<predecessor-slug>-v2` or a more specific re-framing such as `<predecessor-slug>-via-fm-edit`). The successor's `## Goal` MUST open with a one-line "Successor to Task NNN" pointer; the body re-frames the work against current repo state.

**Mechanical cross-check.** The audit's `tasks/readme.md`-vs-`task_status` drift signal is also produced mechanically by [TASK.md §7.0 row §7.11](./TASK.md) (`tools/fm/index_diff.py`, landed by [Task 031](./tasks/031-sync-tasks-index-status-drift/task.md) per Task 032 finding F11). An agent SHOULD run `tools/check-governance.sh` first to surface drift; the §3.4 audit then handles the classification/lifecycle decision the linter cannot make on its own.

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
