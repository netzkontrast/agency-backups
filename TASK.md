---
type: spec
status: active
slug: task-spec
summary: "Root specification governing the /tasks/ orchestration directory, the Task lifecycle, and the Frontmatter Ontology that links Tasks to Prompts and Research."
created: 2026-05-04
updated: 2026-05-04
---

# Task Orchestration Specification

> **Mechanical Enforcement Notice:** This spec is mechanically enforced by `tools/check-governance.sh`. Before editing any file under `/tasks/`, install the pre-commit hook once with `tools/install-hooks.sh`. See [§7 Mandatory Pre-Commit Checks](#7-mandatory-pre-commit-checks-for-task-tasks) for the per-clause linter mapping.

When the agent is asked to perform a unit of work that is neither a pure prompt-craft nor a pure research execution, the agent MUST treat it as a **Task** and apply the rules in this document. A Task is the orchestration layer that links *what should be done* (Task) to *the instruction set* (Prompt) and *the produced evidence* (Research, code, or specs).

## 1. Definitions (RFC 2119)

The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this document are to be interpreted as described in RFC 2119.

- **Task** — A bounded, named unit of work owned by an agent or human, with an explicit goal, a plan, a todo list, and explicit links (via frontmatter) to the prompts it executes and the artifacts it affects.
- **Prompt** — An executable instruction set stored in `/prompts/<slug>/`. A Task MUST NOT inline a prompt; it MUST link to one.
- **Research** — An executed knowledge-gathering workspace stored in `/research/<slug>/`. Research is the *output* of running a research-flavored Prompt; it is never the source of an instruction.
- **Artifact** — Any file produced by executing a Task (code, spec, doc, research output).

A Task is **distinct from** a Prompt: creating a Task is an internal coordination action, not an externally-facing instruction set.

## 2. Directory Structure

Every Task MUST live in a dedicated subfolder under `/tasks/`. The folder name MUST be `<NNN>-<slug>` where `NNN` is a zero-padded sequence number (e.g. `001`, `017`) and `<slug>` is kebab-case (max 5 tokens).

```text
/tasks
└── /<NNN>-<slug>
    ├── readme.md        # Directory index (per FOLDERS.md).
    ├── task.md          # The Task spec: frontmatter + Goal + Plan + Todo. MUST exist.
    ├── notes.md         # OPTIONAL running notes captured during execution.
    └── friction-log.md  # OPTIONAL friction log per FRUSTRATED.md.
```

Subfolders inside a Task directory MUST NOT be created unless 4+ files of the same category accumulate (per `FOLDERS.md`).

## 3. Frontmatter Ontology (Layered Schema with Namespacing)

This repository adopts the **Layered Schema with Namespacing** model from `research/obsidian-frontmatter-agentic-spec/output/SPEC.md`. Every markdown file in this repository SHOULD carry frontmatter conforming to L0+L1; files in operational directories (`/tasks/`, `/prompts/`, `/research/`) MUST additionally carry the L2 namespace appropriate to their directory. YAML MUST NOT nest deeper than one level.

### 3.1 L0 — Obsidian Reserved (optional)

| Key | Type | Purpose |
|---|---|---|
| `tags` | list | Native Obsidian graph/search. |
| `aliases` | list | Alternate wikilink targets. |
| `cssclasses` | list | UI rendering modifier. |

### 3.2 L1 — Vault Core (mandatory for operational files)

| Key | Type | Purpose |
|---|---|---|
| `type` | string | One of: `task`, `prompt`, `research`, `spec`, `readme`, `note`, `index`. Drives parser routing. |
| `status` | string | One of: `draft`, `active`, `blocked`, `completed`, `archived`. |
| `slug` | string | Kebab-case identifier; MUST match folder name where applicable. |
| `summary` | string | Token-cheap tl;dr. The agent SHOULD prefer reading `summary` before opening the body. |
| `created` | date | ISO-8601 (`YYYY-MM-DD`). |
| `updated` | date | ISO-8601 (`YYYY-MM-DD`). |

### 3.3 L2 — Domain Namespaces (mandatory inside their directory)

Convention: `<domain>_<key>`. Keys MUST be flat (no nested objects). Lists are permitted but MUST contain scalars or short strings only.

**Task namespace** (mandatory in `/tasks/<NNN>-<slug>/task.md`):

| Key | Type | Purpose |
|---|---|---|
| `task_id` | string | Zero-padded sequence (e.g. `"001"`). |
| `task_status` | string | One of: `open`, `in_progress`, `blocked`, `done`, `abandoned`. |
| `task_owner` | string | Agent name or human identifier. |
| `task_priority` | string | One of: `P0`, `P1`, `P2`, `P3`. |
| `task_uses_prompts` | list | Slugs of prompts this Task executes. MAY be empty. |
| `task_spawns_research` | list | Slugs of research workspaces produced by this Task. MAY be empty. |
| `task_affects_paths` | list | Relative paths the Task is allowed to modify. |

**Prompt namespace** (mandatory in `/prompts/<slug>/prompt.md`):

| Key | Type | Purpose |
|---|---|---|
| `prompt_kind` | string | One of: `research-proposal`, `follow-up`, `tool-instruction`, `task-spec`, `general`. |
| `prompt_framework` | string | One of: `RISEN`, `RISE-DX`, `ReAct`, `RISEN+ReAct`, `CoT`. |
| `prompt_target_agent` | string | E.g. `Claude Code`, `Gemini`, `any`. |
| `prompt_relates_to_task` | string | Task slug, or empty if standalone. |
| `prompt_spawned_from_research` | string | Research slug that motivated this prompt, or empty. |

**Research namespace** (mandatory in `/research/<slug>/output/SPEC.md` and `readme.md`):

| Key | Type | Purpose |
|---|---|---|
| `research_phase` | string | One of: `kickoff`, `synthesis`, `reflection`, `complete`. |
| `research_executes_prompt` | string | Slug of the prompt that triggered this run. |
| `research_friction_level` | string | One of: `FL0`, `FL1`, `FL2`, `FL3`. |

### 3.4 L3 — Agent-Only (sidecar, not in markdown)

L3 metadata (vector embeddings, graph scores, token matrices) MUST NOT appear in YAML frontmatter. It MUST live in a sidecar file (e.g. `/.agent_cache/<filename>.meta.json`) per the obsidian-frontmatter spec.

### 3.5 Worked Example — Task Frontmatter

```yaml
---
type: task
status: active
slug: refactor-governance-from-specs
summary: "Encode rules from Spec A/B/C, G/H/I, J/K/L into linters, hooks, and templates."
created: 2026-05-04
updated: 2026-05-04
task_id: "001"
task_status: open
task_owner: "claude-code"
task_priority: P1
task_uses_prompts:
  - refactor-governance-from-specs
task_spawns_research: []
task_affects_paths:
  - PRE_COMMIT.md
  - .githooks/
  - tools/
---
```

## 4. Workflow (Task Lifecycle)

1. **Initialize** — Create `/tasks/<NNN>-<slug>/` and `task.md` with the L1 + Task-namespace frontmatter. Set `task_status: open`.
2. **Plan** — Inside `task.md`, write the Goal, the Plan, and a checklist Todo.
3. **Link Prompts** — If the Task requires an instruction set, ensure a prompt exists under `/prompts/<slug>/` and reference its slug in `task_uses_prompts`. If no suitable prompt exists, the agent MUST first create one as a Prompt Task per `PROMPT.md`.
4. **Execute** — Set `task_status: in_progress`. The agent works on the listed paths; new artifacts are created in their proper home (`/research/`, source code, `/prompts/`, etc.). Notes accumulate in `notes.md` if useful.
5. **Block** — If blocked, set `task_status: blocked` and append a dated entry to `notes.md` describing the blocker.
6. **Close** — When all Todo items are checked, set `task_status: done`, update `updated`, and (if friction was non-trivial) commit a `friction-log.md`.

## 5. `task.md` Required Sections

Every `task.md` MUST contain, in order:

1. YAML frontmatter (L1 + Task namespace).
2. `# <Title>` — Human-readable title.
3. `## Goal` — One paragraph. The single, falsifiable outcome.
4. `## Plan` — Numbered steps. Each step SHOULD reference the artifact it produces.
5. `## Todo` — GitHub-style checklist (`- [ ]` / `- [x]`). The Task is `done` only when every box is checked.
6. `## Links` — Relative Markdown links to: linked prompts (`/prompts/<slug>/prompt.md`), spawned research (`/research/<slug>/`), and any other key artifacts.

## 6. Gherkin Scenarios (Normative)

```gherkin
Feature: Task pickup and linkage

  Scenario: Agent picks up an open Task
    Given a file "/tasks/<NNN>-<slug>/task.md" exists
    And its frontmatter has "task_status: open"
    When an agent claims the task
    Then the agent MUST set "task_status: in_progress" before any other write
    And the agent MUST set "task_owner" to its identifier
    And the agent MUST update the "updated" field to today's ISO date

  Scenario: Task requires an instruction set
    Given a Task references prompts in "task_uses_prompts"
    When the agent begins execution
    Then for each referenced slug, "/prompts/<slug>/prompt.md" MUST exist
    And if any referenced prompt is missing, the agent MUST first create it per PROMPT.md
    And the agent MUST NOT inline the prompt body inside task.md

  Scenario: Task closure
    Given every checkbox in the "## Todo" section is "[x]"
    When the agent finalizes the task
    Then "task_status" MUST be set to "done"
    And the "updated" field MUST be set to today's ISO date
    And a friction-log entry MUST be produced per FRUSTRATED.md (FL0 inclusive)

  Scenario: Spawning research from a Task
    Given a Task creates a new research workspace
    When the agent finishes the research run
    Then the research slug MUST appear in "task_spawns_research"
    And the research SPEC frontmatter MUST set "research_executes_prompt"
       to the slug of the prompt under "task_uses_prompts"
```

## 7. Mandatory Pre-Commit Checks for Task Tasks

The agent MUST run `tools/check-governance.sh` before committing any change to `/tasks/`. The agent MUST NOT commit if that script exits non-zero. The seven checks below are mechanically enforced by the linters mapped in §7.0.

### 7.0 Mechanical Enforcement Mapping

| Check | Tool | Failure mode |
|---|---|---|
| §7.1 Frontmatter Integrity | [`tools/validate-frontmatter.py`](./tools/validate-frontmatter.py) | Missing L1/L2 keys, YAML depth > 1, non-kebab slug |
| §7.2 Prompt Linkage | [`tools/lint-linkage.py`](./tools/lint-linkage.py) | `task_uses_prompts` slug doesn't resolve |
| §7.3 Research Linkage | [`tools/lint-linkage.py`](./tools/lint-linkage.py) | `task_spawns_research` slug doesn't resolve (closed tasks only) |
| §7.4 Path Containment | human review | No mechanical check — human responsibility |
| §7.5 Todo Completion | [`tools/lint-linkage.py`](./tools/lint-linkage.py) | `task_status: done` with unchecked `- [ ]` items |
| §7.6 Readme Audit | [`tools/lint-structure.py`](./tools/lint-structure.py) | Missing `readme.md` in task folder |
| §7.7 Friction Log | [`tools/lint-linkage.py`](./tools/lint-linkage.py) + [`tools/check-trust.py`](./tools/check-trust.py) | `task_status: done` without `friction-log.md` containing an FL[0-3] declaration |

Before committing a Task that is being closed, the agent MUST verify:

1. **Frontmatter Integrity** — `task.md` carries every required L1 and Task-namespace key. YAML nesting depth is ≤ 1.
2. **Prompt Linkage** — Every slug in `task_uses_prompts` resolves to an existing `/prompts/<slug>/prompt.md`.
3. **Research Linkage** — Every slug in `task_spawns_research` resolves to an existing `/research/<slug>/` folder.
4. **Path Containment** — Files modified by the Task fall within `task_affects_paths` (or the agent has updated that list to reflect reality).
5. **Todo Completion** — Either every `- [ ]` is checked, or `task_status` is `blocked`/`abandoned` with a reason in `notes.md`.
6. **Readme Audit** — `/tasks/<NNN>-<slug>/readme.md` exists and links to every other file in the folder (per `FOLDERS.md`).
7. **Friction Log** — `friction-log.md` exists if `FL > FL0`; an FL0 declaration MAY be inlined in the closing commit message instead.

## 8. Edge Cases & Open Questions

### 8.1 Concurrent Task Numbering

Two agents may simultaneously claim the next sequence number. The agent MUST resolve this on commit by:

1. Running `ls tasks/ | sort` immediately before staging.
2. If the chosen `<NNN>` already exists on disk or on the target branch, the agent MUST renumber to the next free `<NNN>` and update `task_id` accordingly.
3. The Task slug MUST remain stable across renumbering; only `<NNN>` changes.

### 8.2 Multi-Prompt Tasks

A Task MAY list multiple prompts in `task_uses_prompts`. Semantics:

- The prompts are executed in declaration order unless the Plan section explicitly states otherwise.
- Each executed prompt produces its own research workspace; all such slugs MUST appear in `task_spawns_research` on closure.
- A Task MUST NOT list the same prompt slug twice; if a prompt is executed multiple times with different inputs, those are separate prompts (separate slugs).

### 8.3 Abandonment

A Task MAY end without closure. The agent MUST:

1. Set `task_status: abandoned`.
2. Append a dated entry to `notes.md` stating the reason and the last reproducible state.
3. List any partial artifacts under a `## Partial Artifacts` section in `task.md` so a future agent can resume or salvage.

The pre-commit checks in §7 are relaxed for `abandoned` tasks (todo completion is not required) but `notes.md` MUST exist and contain the abandonment reason.

### 8.4 Resumption

When a Task in `task_status: blocked` is unblocked, the agent MUST:

1. Set `task_status: in_progress`.
2. Update `updated` to today.
3. Append a "## Resumption Checklist" section to `notes.md` listing what was assumed about the prior state (per Spec-G/H/I session-continuity rules).

### 8.5 Tasks That Spawn Tasks

A Task MAY discover that it requires sub-coordination. It MUST NOT nest sub-tasks inside `/tasks/<NNN>-<slug>/`; instead, it creates a sibling `/tasks/<MMM>-<sub-slug>/` and adds the parent slug to that child's `notes.md` under "## Parent Task". The graph is intentionally flat.

### 8.6 Research-Only Sessions Without a Task

A research run MAY proceed without a `/tasks/` entry when it is a one-shot extraction triggered directly by a prompt. The Task layer is for *coordinated* work; ad-hoc research does not require it. The judgement test: would a future agent need to know this work happened? If yes, file a Task; if no, the research workspace alone is sufficient.

## 9. Anti-Patterns

- **MUST NOT** inline an executable prompt body inside `task.md`. Link to `/prompts/<slug>/prompt.md` instead.
- **MUST NOT** store research synthesis or outputs inside `/tasks/`. Those belong in `/research/<slug>/`.
- **MUST NOT** nest YAML frontmatter beyond one level.
- **MUST NOT** create a Task folder without a `task.md`.
- **SHOULD NOT** create a Task for trivial single-edit work that is fully described by a commit message.
