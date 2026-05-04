---
type: spec
status: active
slug: maintenance-spec
summary: "Governs the Nightly Maintenance Run and the Repo Coherence Check routine. Defines scope, repair permissions, run-log protocol, and Task delegation rules for all automated maintenance agents."
created: 2026-05-02
updated: 2026-05-04
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

| Tier | Description | Permitted action |
|---|---|---|
| **T1 — Mechanical** | Missing or stale `updated:` date; missing `slug:` that can be derived from folder name; broken relative Markdown link where target exists; missing `readme.md` stub (per FOLDERS.md). | Fix immediately, in-place. |
| **T2 — Additive** | Adding a missing L1 or L2 frontmatter key whose value is unambiguous from context (e.g. adding `type: task` to a `task.md`). | Fix immediately, in-place. |
| **T3 — Structural** | Changing section headings, rewriting content, altering schema definitions, adding new L2 keys to the ontology, modifying root governance specs beyond T1/T2. | MUST NOT fix directly. Write a Task in `/tasks/` instead. |
| **T4 — Research-touching** | Any modification to a `/research/<slug>/` workspace that is `research_phase: complete`. | MUST NOT touch. Research is immutable after closure. |

**Root governance specs** (`AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `FRUSTRATED.md`, `PRE_COMMIT.md`, `MAINTENANCE.md`) are subject to T1/T2 repairs only. Structural changes to these files MUST be written as Tasks.

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

Every run MUST append one record to `maintenance/run-log.md` before the run's commit. The record format is defined in that file's header. The agent MUST read the last record's `end_commit` field before beginning; if the field is absent (first run), the agent MUST use the repository's initial commit as the baseline.

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

---

## 4. Finalising Any Run

Before committing the results of any maintenance run, verify:

1. All touched `readme.md` files comply with the static/dynamic partitioning schema (§3.2).
2. All T3 findings have a corresponding Task in `/tasks/`.
3. No T3 or T4 changes were made directly.
4. `maintenance/run-log.md` has been updated with the run record.
5. The commit message references the run-log entry date and the commit range scanned.

---

## 5. Maintenance Folder Reference

The `/maintenance/` folder is the governance support centre for this repository. It holds content that root specs summarise but do not define:

| File | Purpose |
|---|---|
| [`maintenance/language-spec.md`](./maintenance/language-spec.md) | Canonical RFC 2119 keyword definitions, Gherkin syntax binding, full Frontmatter Ontology (L0–L3). |
| [`maintenance/run-log.md`](./maintenance/run-log.md) | Structured log of every Coherence Check and Nightly Maintenance run. The agent reads this to establish its starting-commit baseline. |

The `/maintenance/` folder MUST NOT be used to store Task orchestration, prompt drafts, or research workspaces. Those belong in `/tasks/`, `/prompts/`, and `/research/` respectively.
