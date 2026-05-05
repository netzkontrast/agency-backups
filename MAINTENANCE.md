---
type: spec
status: active
slug: maintenance-spec
summary: "Governs the Nightly Maintenance Run and the Repo Coherence Check routine. Defines scope, repair permissions, run-log protocol, and Task delegation rules for all automated maintenance agents."
created: 2026-05-02
updated: 2026-05-05
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
| **T4 — Research-touching** | Any modification to a `/research/<slug>/` workspace that is `research_phase: complete`. | MUST NOT touch. Research is immutable after closure. | — |

**Root governance specs** (`AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `FRUSTRATED.md`, `PRE_COMMIT.md`, `MAINTENANCE.md`) are subject to T1/T2 repairs only. Structural changes to these files MUST be written as Tasks.

**Mutation surface stability.** `tools/fm/edit.py` is the canonical T1/T2 mutator for frontmatter; coherence-check agents SHOULD prefer it over `sed`/`awk` because it preserves body bytes and quoting, takes a file lock, and rejects T3/T4 operations by construction (per [SPEC.md §7.2](./research/flexible-frontmatter-toolchain/output/SPEC.md)). Body-section mutations are deferred to `tools/fm/section.py` (Task 018).

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

---

## 5. Maintenance Folder Reference

The `/maintenance/` folder is the governance support centre for this repository. It holds content that root specs summarise but do not define:

| File | Purpose |
|---|---|
| [`maintenance/language-spec.md`](./maintenance/language-spec.md) | Canonical RFC 2119 keyword definitions, Gherkin syntax binding, full Frontmatter Ontology (L0–L3). |
| [`maintenance/run-log.md`](./maintenance/run-log.md) | Structured log of every Coherence Check and Nightly Maintenance run. The agent reads this to establish its starting-commit baseline. |

The `/maintenance/` folder MUST NOT be used to store Task orchestration, prompt drafts, or research workspaces. Those belong in `/tasks/`, `/prompts/`, and `/research/` respectively.
