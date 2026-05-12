---
type: spec
status: active
slug: task-spec
summary: "Root specification governing the /tasks/ orchestration directory, the Task lifecycle, and the Frontmatter Ontology that links Tasks to Prompts and Research."
created: 2026-05-04
updated: 2026-05-11
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

A Task is **distinct from** a Prompt: creating a Task is an internal coordination action, not an externally-facing instruction set. **Planner / Tech-Lead framing.** A Task is the *Planner-layer* artefact — it decomposes work, sequences subtasks, and coordinates dependencies across the prompt, research, and code surfaces. A Prompt is the *Tech-Lead-layer* artefact — it instructs the executor that performs one slice of the plan. The two layers are deliberately separate so a single Task may delegate to multiple Prompts (and vice-versa), and so plan-level changes do not require rewriting executable instructions.

## 2. Directory Structure

Every Task MUST live in a dedicated subfolder under `/tasks/`. The folder name MUST be `<NNN>-<slug>` where `NNN` is a zero-padded sequence number (e.g. `001`, `017`) and `<slug>` is kebab-case (max 5 tokens).

```text
/tasks
└── /<NNN>-<slug>
    ├── readme.md        # Directory index (per FOLDERS.md).
    ├── task.md          # The Task spec: frontmatter + Goal + Plan + Todo. MUST exist.
    ├── notes.md         # OPTIONAL running notes captured during execution.
    └── friction-log.md  # MANDATORY when task_status reaches "done" or "abandoned", per FRUSTRATED.md.
```

Subfolders inside a Task directory MUST NOT be created unless 4+ files of the same category accumulate (per `FOLDERS.md`).

## 3. Frontmatter Ontology (Layered Schema with Namespacing)

This repository adopts the **Layered Schema with Namespacing** model from `research/obsidian-frontmatter-agentic-spec/output/SPEC.md`. Every markdown file in this repository SHOULD carry frontmatter conforming to L0+L1; files in operational directories (`/tasks/`, `/prompts/`, `/research/`) MUST additionally carry the L2 namespace appropriate to their directory. YAML MUST NOT nest deeper than one level.

**Canonical machine-readable encoding.** The required-key matrix and per-type body-schema (per [`research/flexible-frontmatter-toolchain/output/SPEC.md`](./research/flexible-frontmatter-toolchain/output/SPEC.md) §3, §4, §12) live in [`maintenance/schemas/header-ontology.json`](./maintenance/schemas/header-ontology.json). The prose tables in §3.1–§3.3 are the human-readable mirror; the JSON is the source for tooling. When the JSON and prose drift, the JSON wins for `tools/fm/validate.py` and the prose is amended in the next coherence run.

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

**Authoritative L2-namespace source.** The full required-key matrix and the per-type body schema for every operational namespace (`task_*`, `prompt_*`, `research_*`, `skill_*`, `adr_*`) live in [`research/flexible-frontmatter-toolchain/output/SPEC.md`](./research/flexible-frontmatter-toolchain/output/SPEC.md) §3–§4 (and its §12 body-schema appendix), encoded mechanically in [`maintenance/schemas/header-ontology.json`](./maintenance/schemas/header-ontology.json) — including the `types.adr` registration at `header-ontology.json:208` (pattern `decisions/[0-9][0-9][0-9][0-9]-*.md`). The tables below are the human-readable mirror; the JSON is the source for `tools/fm/validate.py`. Each namespace inline lists ≤ 3 quickref keys; for the full set, follow the link.

**Task namespace** (mandatory in `/tasks/<NNN>-<slug>/task.md`):

| Key | Type | Purpose |
|---|---|---|
| `task_id` | string | Zero-padded sequence (e.g. `"001"`). |
| `task_status` | string | One of: `open`, `in_progress`, `blocked`, `done`, `updated`, `abandoned`. See §4 for `updated` semantics. |
| `task_owner` | string | Agent name or human identifier. |
| `task_priority` | string | One of: `P0`, `P1`, `P2`, `P3`. |
| `task_uses_prompts` | list | Slugs of prompts this Task executes. MAY be empty. |
| `task_spawns_research` | list | Slugs of research workspaces produced by this Task. MAY be empty. |
| `task_spawns_prompts` | list | Slugs of follow-up prompts generated by this Task. MAY be empty. |
| `task_affects_paths` | list | Relative paths the Task is allowed to modify. |
| `task_blocked_by` | list | OPTIONAL. Zero or more `task_id` strings (or slugs) whose `task_status` MUST be `done` before this Task may transition `open` → `in_progress`. See §8.7 and the Gherkin scenarios in §6. MAY be empty. |
| `task_supersedes` | list | OPTIONAL. Set on a successor Task created via the `updated` lifecycle (§4.7). Each entry is the `task_id` (or slug) of the predecessor Task that this Task replaces. Reciprocal with `task_superseded_by`. MAY be empty. |
| `task_superseded_by` | list | OPTIONAL. Set on a predecessor Task at the moment its `task_status` is flipped to `updated`. Each entry is the `task_id` (or slug) of the successor that re-frames the work in light of current repo state. Reciprocal with `task_supersedes`. MAY be empty. |

**Prompt namespace** (mandatory in `/prompts/<slug>/prompt.md`):

| Key | Type | Purpose |
|---|---|---|
| `prompt_kind` | string | One of: `research-proposal`, `follow-up`, `tool-instruction`, `task-spec`, `general`. |
| `prompt_framework` | string | One of: `RISEN`, `RISE-DX`, `ReAct`, `RISEN+ReAct`, `CoT`. |
| `prompt_target_agent` | string | E.g. `Claude Code`, `Gemini`, `any`. |
| `prompt_relates_to_task` | string | OPTIONAL. Slug of the Task whose `task_uses_prompts` already lists this prompt (reciprocity required). Omit for follow-up prompts not yet adopted by a Task. |
| `prompt_spawned_from_research` | string | OPTIONAL. Slug of the research run that produced this prompt as a follow-up. Resolves under `/research/<slug>/` or `/research/<provider>/<slug>/`. |

**Research namespace** (mandatory in `/research/<slug>/output/SPEC.md` and `readme.md`):

| Key | Type | Purpose |
|---|---|---|
| `research_phase` | string | One of: `kickoff`, `synthesis`, `reflection`, `complete`. |
| `research_executes_prompt` | string | Slug of the prompt that triggered this run. |
| `research_friction_level` | string | One of: `FL0`, `FL1`, `FL2`, `FL3`. |

**Skill namespace** (mandatory in `/skills/<slug>/SKILL.md`; ratified by [`research/skills-namespace-ontology/output/SPEC.md`](./research/skills-namespace-ontology/output/SPEC.md)):

| Key | Type | Purpose |
|---|---|---|
| `skill_kind` | string | Closed vocabulary: one of `meta`, `domain`, `tool`, `bootstrap`, `adapter`. Determines activation precedence and host routing. |
| `skill_tier` | string | Closed vocabulary: one of `T1` (always-on, pre-loaded), `T2` (on-trigger, default), `T3` (reference-heavy, lazy-loaded sections). Drives manifest behaviour. |
| `skill_uses` | list | Slugs of skills this one operationally depends on. Broken target = ERROR (linter blocks commit per the §4 reciprocity rule of the ratifying SPEC). |

The full matrix (`skill_complements`, `skill_triggers`, `skill_supersedes`, the 14-skill mapping table, the two-case reciprocity rule, and the `metadata.*` deprecation map) lives in `research/skills-namespace-ontology/output/SPEC.md`. SKILLS.md and `tools/skills-index.py` consume that SPEC directly; `task.md` files do NOT inline `skill_*` keys.

**ADR namespace** (mandatory in `/decisions/<NNNN>-<slug>.md`; registered in [`maintenance/schemas/header-ontology.json:208`](./maintenance/schemas/header-ontology.json) as the fourth operational L2 namespace alongside `task_*` / `prompt_*` / `research_*` / `skill_*`):

| Key | Type | Purpose |
|---|---|---|
| `adr_id` | string | Pattern `ADR-NNNN` (zero-padded four-digit sequence). Distinct from L1 `slug`. |
| `adr_status` | string | Closed vocabulary: one of `Proposed`, `Accepted`, `Superseded`, `Deprecated`. Distinct from L1 `status` (which uses the operational vocabulary `draft`/`active`/etc). |
| `adr_supersedes` / `adr_superseded_by` | list | Reciprocal pair pointing to predecessor / successor `adr_id` values. Linter enforces both directions. |

The full ADR governance spec lives at [`research/adr-spec-research-synthesis/output/SPEC.md`](./research/adr-spec-research-synthesis/output/SPEC.md); `tools/adr/cli.py validate` is the binding linter (Task 028 / Task 031).

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
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - PRE_COMMIT.md
  - .githooks/
  - tools/
---
```

## 4. Workflow (Task Lifecycle)

The lifecycle states are: `open` → (`blocked` ↔) `in_progress` → (`done` | `updated` | `abandoned`). The `updated` state is a **closure with continuity**: the Task is closed (no further work happens against this folder), but a successor Task carries its intent forward in a re-framed shape. See §4.7 for the full rule.

1. **Initialize** — Create `/tasks/<NNN>-<slug>/` and `task.md` with the L1 + Task-namespace frontmatter. Set `task_status: open`.
2. **Plan** — Inside `task.md`, write the Goal, the Plan, and a checklist Todo.
3. **Link Prompts** — If the Task requires an instruction set, ensure a prompt exists under `/prompts/<slug>/` and reference its slug in `task_uses_prompts`. If no suitable prompt exists, the agent MUST first create one as a Prompt Task per `PROMPT.md`.
4. **Execute** — Set `task_status: in_progress`. *Precondition*: every entry in `task_blocked_by` MUST already have `task_status: done` (see §8.7). The agent works on the listed paths; new artifacts are created in their proper home (`/research/`, source code, `/prompts/`, etc.). Notes accumulate in `notes.md` if useful.
5. **Block** — If blocked by an *external* condition (a missing tool, a third-party review, a runtime constraint), set `task_status: blocked` and append a dated entry to `notes.md` describing the blocker. *Distinction*: Tasks blocked by **another Task in this repo** SHOULD use `task_blocked_by` instead of the `blocked` status — `blocked` is reserved for conditions outside the Task graph.
6. **Close (done)** — When all Todo items are checked, set `task_status: done`, update `updated`, and commit a `friction-log.md` containing an FL[0-3] declaration. The log is mandatory even when the run was frictionless (FRUSTRATED.md FL0).
7. **Close (updated)** — When the Task's *intent* is still relevant but its *plan or premise no longer reflects the current repo state* (e.g. an upstream Task shipped tooling that re-frames the work), the agent MUST follow §4.7 instead of §4.6.

### 4.7 The `updated` Lifecycle (Closure with Continuity)

A Task is set to `task_status: updated` when **all four** conditions below hold:

1. The Task's Goal is still desirable (the work has not been abandoned, deprioritised, or invalidated).
2. The Task's *Plan, Todo, or affected-paths* no longer reflect the current state of the repository — typically because:
   - Successor work in another Task has shipped tooling or specs that subsume part of the original plan;
   - Artefacts referenced by the original plan have been renamed, retired, or supersededby a newer mechanism (e.g. legacy linters → `tools/fm/`); or
   - A research synthesis (e.g. an output `SPEC.md`) explicitly supersedes the Task's premise (per `RESEARCH.md`).
3. A **successor Task** has been created at a new `<NNN>` slot whose `task.md` re-frames the original intent against the current repo state. The successor's frontmatter MUST set `task_supersedes: ["<old-task_id>"]`.
4. The predecessor's frontmatter MUST set `task_superseded_by: ["<new-task_id>"]` and the `updated` field MUST be set to today's ISO date.

Closing as `updated` MUST produce a `friction-log.md` in the predecessor folder containing:
- An `FL[0-3]` declaration (per FRUSTRATED.md), even if the friction is FL0 ("plan obsolesced cleanly").
- A one-paragraph **Supersession Rationale** explaining *why* the plan no longer reflects current state and pointing at the successor by relative path.

The `updated` state is **not** an excuse to skip work. If the Task's intent is no longer relevant, use `abandoned` (§8.3) instead. If the Task's plan executed cleanly to completion, use `done` (§4.6) instead. The `updated` state is reserved for *re-framing*, not *cancellation* and not *completion-by-drift*.

**Mechanical decision helper.** Before flipping `task_status` to `updated` or `abandoned`, the agent SHOULD invoke `tools/fm/check-task-lifecycle-classification.py --task <path> --target-status {updated,abandoned}`. The helper consumes the five-signal `classify_task` decision tree ratified in [`research/spec-staleness-decision-formalization/output/SPEC.md`](./research/spec-staleness-decision-formalization/output/SPEC.md) §1 — the algorithm extracts five pure-function signals from repo state (`todo_satisfaction`, `affects_paths_present`, `plan_anchors_live`, `goal_endorsed`, `successor_present`; see SPEC §2) and emits exactly one of four §4.7 buckets (`STILL_ACCURATE`, `DRIFTED`, `COMPLETED_BY_DRIFT`, `NO_LONGER_DESIRABLE`) without any agent attestation. The helper PASSes when the computed bucket matches the target (`updated` ⇒ {`DRIFTED`, `COMPLETED_BY_DRIFT`}; `abandoned` ⇒ `NO_LONGER_DESIRABLE`); on mismatch it FAILs with the signal vector and bucket trace cited. Example: `--target-status updated` against a Task with `task_superseded_by: ["043"]` reports PASS with `bucket=DRIFTED`. The `abandoned` branch additionally enforces TASK.md §8.3 (notes.md exists with an abandonment rationale). The original four-condition attestation-flag fallback (Task 033 ST-4) was retired by Task 049; the `--goal-still-desirable` / `--plan-drifted` flags are no longer accepted because S1/S4 mechanise both predicates. The helper is a manual maintenance tool; it is NOT wired into `tools/check-governance.sh`. The audit-window is configured via `MAINT_STALE_DAYS` (default 7) or `--stale-days`.

### 4.8 Mandatory Tasks-Index Update (`tasks/readme.md`)

Every change that affects the membership or `task_status` of any Task — namely:

- creating a new `tasks/<NNN>-<slug>/` folder,
- renaming a Task folder per §8.1,
- transitioning `task_status` (e.g. `open` → `in_progress`, `in_progress` → `done`/`updated`/`abandoned`/`blocked`), or
- setting/changing `task_blocked_by`, `task_supersedes`, or `task_superseded_by`,

MUST be accompanied **in the same commit** by an update to [`tasks/readme.md`](./tasks/readme.md) that brings the index into sync with the new state. The index is the single human-readable surface every agent (Claude Code, Jules, Gemini) consults before opening a Task body; a stale index is a session-continuity failure.

The agent MUST verify, before staging the commit:

1. **Membership** — every `tasks/<NNN>-<slug>/` folder on disk has exactly one bullet under `## Contents` in `tasks/readme.md`. No folder is missing; no bullet is orphaned.
2. **Status fidelity** — each bullet ends with `Status: \`<task_status>\`` matching the `task_status` value in that Task's `task.md` frontmatter.
3. **Lineage annotation** — any bullet whose Task is `task_status: updated` MUST carry a `→ superseded by [<NNN>](./<NNN>-<slug>/)` suffix; any Task with non-empty `task_blocked_by` SHOULD carry a `(blocked on Task <NNN>)` suffix.
4. **Index frontmatter freshness** — `tasks/readme.md`'s own `updated:` field MUST be bumped to today's ISO date on every such change (T1 mutation per `MAINTENANCE.md §1`).

The maintenance and coherence-check agents enforce this rule on every run; per-session agents enforce it at commit time. A commit that touches `task.md` or creates/renames a `tasks/<NNN>-<slug>/` folder without a corresponding edit to `tasks/readme.md` MUST be rejected by the linter mapping in §7.0 row §7.11.

### 4.9 Planning Pipeline for T3-Structural Tasks (`/sc:*` Ladder)

When a Task's scope crosses the T3 (Structural) repair tier defined in [`MAINTENANCE.md §1`](./MAINTENANCE.md#1-repair-permission-tiers) — section heading rewrites, schema changes, root-spec edits beyond T1/T2, slug renames, sub-module refactors, or cross-cutting prose rewrites across more than three files — the agent SHOULD execute the four-stage SuperClaude planning ladder before authoring `task.md`'s `## Plan` section:

```
/sc:analyze  →  /sc:brainstorm  →  /sc:design  →  /sc:workflow
```

Each stage produces a discoverable artifact and feeds the next:

| Stage | Purpose | Output | Canonical home |
|---|---|---|---|
| `/sc:analyze` | Audit current state vs. claims; surface findings with severity | H/M/L findings list | Chat or commit message; cited in `task.md` `## Context` |
| `/sc:brainstorm` | Socratic discovery of open design questions; lock decisions | Decision matrix (D1, D2, …) | `task.md` `## Context` or `readme.md` `## Assumptions Log` |
| `/sc:design` | Synthesize architectural artifacts; spawn parallel Explore subagents for evidence | 5 design artifacts (contracts, manifests, specs) | Chat; key artifacts may persist in `tasks/<NNN>-<slug>/design.md` |
| `/sc:workflow` | Decompose design into commit-sized atomic steps with DAG + verification | `workflow.md` (clusters, ACs, risks, FL pre-brief) | `tasks/<NNN>-<slug>/workflow.md` |

The `workflow.md` SHOULD be committed alongside `task.md` and `readme.md` so the executable plan is discoverable from the Task folder. Future agents reading the Task SHOULD be able to reconstruct the planning provenance from these files alone, without re-running the ladder.

**Worked example.** [Task 083 — novel-architect-v111-hardening](./tasks/083-novel-architect-v111-hardening/) executes the full ladder in-session, producing 6 locked decisions, 5 design artifacts, and a 19-commit workflow saved to [`workflow.md`](./tasks/083-novel-architect-v111-hardening/workflow.md). The Task's `readme.md` `## Assumptions Log` records the brainstorm decisions; `task.md` `## Context` cites the analysis findings.

#### Normative Rules

- **T.4.9.1** An agent considering a Task whose scope crosses the T3 boundary (per `MAINTENANCE.md §1`) SHOULD execute the `/sc:analyze → /sc:brainstorm → /sc:design → /sc:workflow` ladder before authoring `task.md`'s `## Plan` section. Skipping the ladder is permitted for trivially-decomposable Tasks (e.g., a single-file linter rule addition, a one-line frontmatter fix); the threshold is operator judgment, not mechanically enforced.
- **T.4.9.2** When the ladder is executed, the `/sc:workflow` output MUST be saved as `tasks/<NNN>-<slug>/workflow.md` carrying L1 Vault Core frontmatter (`type: note`, `status: active`, `slug`, `summary`, `created`, `updated`). The workflow document is the executable contract; `task.md`'s `## Plan` section MUST reference it by relative Markdown link.
- **T.4.9.3** `/sc:design` SHOULD use parallel Explore subagents for evidence gathering when the design requires reading reference patterns from sibling skills, design-source documents, or producing line-level manifests across more than three files. Subagent fan-out is the canonical pattern; sequential synthesis-only mode is permitted for trivially-scoped designs.
- **T.4.9.4** Decisions locked in `/sc:brainstorm` MUST be recoverable from the Task's `readme.md` `## Assumptions Log` or `task.md` `## Context`. An agent re-entering the Task in a later session MUST NOT have to re-run the brainstorm to recover the decision premises.
- **T.4.9.5** The ladder is **advisory-tier**: governance gate `tools/check-governance.sh` does NOT mechanically check for ladder execution. Compliance is a social contract between the Task author and reviewers; absence of `workflow.md` on a clearly-T3 Task is a code-review finding, not a pre-commit error.

```gherkin
Feature: Planning ladder for T3-structural Tasks

  # anchor: T.4.9.1
  Scenario: T3-structural Task scopes the planning ladder before writing
    Given an agent is about to file a new Task
    And the Task touches more than three files OR a root governance spec OR a sub-module refactor
    When the agent decides on the Task's `## Plan` section
    Then the agent SHOULD execute /sc:analyze → /sc:brainstorm → /sc:design → /sc:workflow first
    And the Task's task.md `## Plan` section SHOULD reference the workflow.md artifact

  # anchor: T.4.9.2
  Scenario: Workflow document is discoverable from the Task folder
    Given /sc:workflow has produced an implementation plan
    When the agent commits the plan
    Then the plan MUST live at tasks/<NNN>-<slug>/workflow.md
    And it MUST carry L1 frontmatter (type: note, status: active, slug, summary, created, updated)
    And task.md's `## Plan` section MUST reference it via relative Markdown link

  # anchor: T.4.9.4
  Scenario: Brainstorm decisions are recoverable from Task artefacts
    Given a Task that executed /sc:brainstorm in a prior session
    When a future agent re-enters the Task
    Then the locked decisions MUST be readable from `readme.md` `## Assumptions Log` OR `task.md` `## Context`
    And the agent MUST NOT need to re-run /sc:brainstorm to recover the decision premises
```

## 5. `task.md` Required Sections

Every `task.md` MUST contain, in order:

1. YAML frontmatter (L1 + Task namespace).
2. `# <Title>` — Human-readable title.
3. `## Goal` — One paragraph. The single, falsifiable outcome.
4. `## Plan` — Numbered steps. Each step SHOULD reference the artifact it produces.
5. `## Todo` — GitHub-style checklist (`- [ ]` / `- [x]`). The Task is `done` only when every box is checked.
6. `## Links` — Relative Markdown links to: linked prompts (`/prompts/<slug>/prompt.md`), spawned research (`/research/<slug>/`), and any other key artifacts.

## 6. Gherkin Scenarios (Normative)

> **Aspirational-scenario note.** A subset of the scenarios below — specifically the "Task with an unmet blocker MUST NOT start" scenario in this section, the `T.B.SUP.1` supersession-blocker scenario at the foot of this section, and the three §8.7 blocker-acceptance scenarios — assert behaviour that the current `tools/fm/validate.py --type-check` does NOT implement. As of this writing the validator implements `F.T.1` (dangling reference) and `F.T.2` (reciprocity) only; the blocker-satisfaction family (§7.0 row §7.9) is pending a future Task-049-class implementation. These scenarios document the desired behaviour and remain normative for the implementing Task; treating them as "currently executable" is the wrong reading. The `T.B.SUP.1` scenario carries an inline `(aspirational — implementing-task: pending …)` label as the canonical convention; the older scenarios pre-date the convention but share its status.

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

  Scenario: Task with an unmet blocker MUST NOT start
    Given a Task's frontmatter declares "task_blocked_by: ['017']"
    And task 017's "task_status" is one of "open", "in_progress", "blocked", or "updated"
    When an agent attempts to set "task_status: in_progress"
    Then the transition MUST be rejected
    And the agent MUST leave "task_status: open" (or "blocked" if the blocker condition is external)
    And the linter (tools/fm/validate.py --type-check, per Task 019) MUST emit an ERROR

  Scenario: Task with all blockers satisfied MAY start
    Given a Task's frontmatter declares "task_blocked_by: ['017']"
    And task 017's "task_status" is "done"
    When an agent claims the Task
    Then the agent MAY set "task_status: in_progress"
    And the agent MUST update "updated" to today's ISO date
    And the agent MUST set "task_owner" to its identifier

  Scenario: Closing a Task as "updated" with continuity
    Given a Task's Goal is still relevant
    And the Task's Plan no longer reflects the current repo state
    When the agent closes the Task with continuity
    Then the agent MUST create a successor Task at the next free <NNN>
    And the successor's frontmatter MUST set "task_supersedes" to a list containing the predecessor's task_id
    And the predecessor's frontmatter MUST set "task_superseded_by" to a list containing the successor's task_id
    And the predecessor's "task_status" MUST be set to "updated"
    And the predecessor's "updated" field MUST be set to today's ISO date
    And the predecessor MUST contain a "friction-log.md" with a Supersession Rationale paragraph
    And the successor's Goal MUST re-frame the predecessor's intent against the current repo state

  Scenario: Reciprocity audit on supersession
    Given a Task A has "task_superseded_by: ['B']"
    When the linter runs
    Then Task B MUST exist
    And Task B's frontmatter MUST contain A's task_id in "task_supersedes"
    And the linter MUST emit an ERROR if reciprocity is broken in either direction

  Scenario: Tasks-index stays in sync with task_status changes
    Given a Task's "task_status" is changed in "tasks/<NNN>-<slug>/task.md"
    When the agent stages the commit
    Then "tasks/readme.md" MUST be modified in the same commit
    And the bullet for that Task MUST cite the new "task_status"
    And "tasks/readme.md" frontmatter "updated" MUST be set to today's ISO date
    And the linter (§7.11) MUST emit an ERROR if any of these conditions fails

  Scenario: New Task folder appears in the index immediately
    Given a new "tasks/<NNN>-<slug>/" folder is created
    When the agent stages the commit that introduces it
    Then "tasks/readme.md" MUST contain a bullet for the new folder in the same commit
    And the linter MUST emit an ERROR if the index lacks a bullet for any tasks/<NNN>-<slug>/ on disk
    And the linter MUST emit an ERROR if the index contains a bullet whose tasks/<NNN>-<slug>/ folder does not exist

  # anchor: T.B.SUP.1 (aspirational — implementing-task: pending Task 049-class blocker-satisfaction follow-up)
  # supersession-blocker inheritance — sibling of the §8.7 "Blocker chain through 'updated'" scenario.
  # The current `tools/fm/validate.py --type-check` implements F.T.1 (dangling) and F.T.2
  # (reciprocity) only; the blocker-satisfaction family (§7.0 row §7.9) remains aspirational.
  # This scenario documents the desired behaviour for the future implementation.
  Scenario: Blocker auto-redirect through `updated` lifecycle
    Given Task X carries `task_blocked_by: ["Y"]`
    And Task Y transitions to `task_status: updated` with `task_superseded_by: ["Z"]`
    And Task Z carries `task_supersedes: ["Y"]`
    And Task Z is `task_status: open` (not yet done)
    When `tools/fm/validate.py --type-check` validates Task X at pre-commit
    Then the validator MUST treat Task X as still blocked
    And the diagnostic MUST cite both Y (superseded) and Z (live successor)
    And Task X MUST NOT transition open → in_progress until Z reaches `done`
```

## 7. Mandatory Pre-Commit Checks for Task Tasks

The agent MUST run `tools/check-governance.sh` before committing any change to `/tasks/`. The agent MUST NOT commit if that script exits non-zero. The seven checks below are mechanically enforced by the linters mapped in §7.0.

### 7.0 Mechanical Enforcement Mapping

The legacy column lists the historical linter set; the flexible-toolchain column lists the successor that supersedes it once `FM_TOOLCHAIN=1` is the default (per [SPEC.md §12.6](./research/flexible-frontmatter-toolchain/output/SPEC.md), Phase 3, owned by Task 019).

| Check | Legacy linter | Flexible-toolchain successor | Failure mode |
|---|---|---|---|
| §7.1 Frontmatter Integrity | [`tools/validate-frontmatter.py`](./tools/validate-frontmatter.py) | [`tools/fm/validate.py`](./tools/fm/validate.py) | Missing L1/L2 keys (F.3.1/F.3.2), YAML depth > 1 (F.3.3), non-kebab slug (F.3.3), did-you-mean typo (F.3.4) |
| §7.2 Body Schema (opt-in) | — | [`tools/fm/validate.py --check-body`](./tools/fm/validate.py) | Section shape mismatch (F.B.1), item-count (F.B.2), item_pattern miss (F.B.3) |
| §7.3 Prompt Linkage | [`tools/lint-linkage.py`](./tools/lint-linkage.py) | `tools/fm/validate.py --type-check` (Task 019) | `task_uses_prompts` slug doesn't resolve |
| §7.4 Research Linkage | [`tools/lint-linkage.py`](./tools/lint-linkage.py) | `tools/fm/validate.py --type-check` (Task 019) | `task_spawns_research` slug doesn't resolve (closed tasks only) |
| §7.5 Path Containment | human review | human review | No mechanical check — human responsibility |
| §7.6 Todo Completion | [`tools/lint-linkage.py`](./tools/lint-linkage.py) | `tools/fm/validate.py --check-body` (F.B.7) | `task_status: done` with unchecked `- [ ]` items |
| §7.7 Readme Audit | [`tools/lint-structure.py`](./tools/lint-structure.py) | `tools/fm/query.py missing-key=...` (Task 019) | Missing `readme.md` in task folder |
| §7.8 Friction Log | [`tools/lint-linkage.py`](./tools/lint-linkage.py) + [`tools/check-trust.py`](./tools/check-trust.py) | `tools/fm/query.py status=done,missing-file=friction-log.md` (Task 019) | `task_status` ∈ {`done`, `updated`, `abandoned`} without `friction-log.md` containing an FL[0-3] declaration |
| §7.9 Blocker Satisfaction | — (new) | `tools/fm/validate.py --type-check` (Task 019) | `task_status: in_progress` while any `task_blocked_by` entry resolves to a Task whose `task_status` ≠ `done` |
| §7.10 Supersession Reciprocity | — (new) | `tools/fm/validate.py --type-check` (Task 019) | `task_supersedes` / `task_superseded_by` are not reciprocal across the two referenced Task folders |
| §7.11 Tasks-Index Freshness | — (new) | `tools/fm/index_diff.py` (a.k.a. `python3 tools/fm/fm.py index-diff`) — see [Task 067](./tasks/067-sync-tasks-index-status-drift/) (renumbered from 031 per [Task 043](./tasks/043-renumber-duplicate-task-ids-v3/), TASK.md §8.1) | `tasks/readme.md` does not list every `tasks/<NNN>-<slug>/` folder, omits its current `task_status`, or fails to mark `updated`/`done`/`abandoned` rows with their supersession pointer |
| §8.1 Duplicate `task_id` | — (new) | [`tools/fm/check-duplicate-task-id.py`](./tools/fm/check-duplicate-task-id.py) (Task 033 ST-3) | Two active tasks share the same `task_id` without supersession reciprocity. Advisory by default during the migration window; set `FM_DUPLICATE_TASK_ID_STRICT=1` to gate. |

Before committing a Task that is being closed, the agent MUST verify:

1. **Frontmatter Integrity** — `task.md` carries every required L1 and Task-namespace key. YAML nesting depth is ≤ 1.
2. **Prompt Linkage** — Every slug in `task_uses_prompts` resolves to an existing `/prompts/<slug>/prompt.md`.
3. **Research Linkage** — Every slug in `task_spawns_research` resolves to an existing `/research/<slug>/` folder. **Enforcement scope:** [`tools/lint-linkage.py`](./tools/lint-linkage.py) only runs this check when `task_status` ∈ {`done`, `updated`, `abandoned`}. While the Task is `open`, `in_progress`, or `blocked`, `task_spawns_research` MAY pre-declare a slug whose `/research/<slug>/` folder does not yet exist — this is the intended pattern for a Task that will produce the research workspace as part of its execution. The closure-only enforcement was clarified after Task 001 surfaced false-positive ERROR diagnostics on open Tasks that legitimately listed a future research slug.
4. **Path Containment** — Files modified by the Task fall within `task_affects_paths` (or the agent has updated that list to reflect reality).
5. **Todo Completion** — Either every `- [ ]` is checked, or `task_status` is `blocked`/`abandoned` with a reason in `notes.md`.
6. **Readme Audit** — `/tasks/<NNN>-<slug>/readme.md` exists and links to every other file in the folder (per `FOLDERS.md`).
7. **Friction Log** — `friction-log.md` MUST exist for every closed task (`done`, `updated`, or `abandoned`) and MUST contain an `FL[0-3]` declaration, including for FL0 runs (FRUSTRATED.md). For `updated` closures the log MUST additionally carry a `## Supersession Rationale` paragraph (per §4.7). An inline declaration in the commit message is NOT a substitute.
8. **Blocker Satisfaction** — Every `task_id` in `task_blocked_by` MUST resolve to an existing Task whose `task_status` is `done`. A successor referenced in `task_superseded_by` does NOT itself satisfy a blocker; the *original* blocker Task must be `done` (or itself superseded by a chain that terminates in `done`).
9. **Supersession Reciprocity** — When `task_status: updated` is set, `task_superseded_by` MUST be non-empty AND every entry MUST resolve to an existing Task whose `task_supersedes` contains this Task's `task_id`.
10. **Tasks-Index Freshness** — `tasks/readme.md` MUST be updated in the **same commit** as any change that creates, renames, or transitions a Task. The index MUST contain one bullet per `tasks/<NNN>-<slug>/` folder on disk, MUST cite each Task's current `task_status`, AND MUST annotate any non-terminal closure with its lineage pointer:
   - `task_status: updated` → "→ superseded by [`<NNN>`](./NNN-<slug>/)" suffix.
   - `task_status: done`/`abandoned` → no suffix required, but the bullet's status MUST match the `task.md` frontmatter.
   - `task_status: blocked` → SHOULD note the blocker (`(blocked on Task NNN)`).
   This is a **mechanical, mandatory** sync — see §4.8 for the operational rule and §6 for the Gherkin scenario.

## 8. Edge Cases & Open Questions

### 8.1 Concurrent Task Numbering

Two agents may simultaneously claim the next sequence number. The agent MUST resolve this on commit by:

1. Running `ls tasks/ | sort` immediately before staging.
2. If the chosen `<NNN>` already exists on disk or on the target branch, the agent MUST renumber to the next free `<NNN>` and update `task_id` accordingly.
3. The Task slug MUST remain stable across renumbering; only `<NNN>` changes.

**Enforcement status — wired via `tools/fm/check-duplicate-task-id.py` (Task 033 ST-3).** Duplicate `task_id` detection is now mechanically performed by [`tools/fm/check-duplicate-task-id.py`](./tools/fm/check-duplicate-task-id.py). It scans every `tasks/<NNN>-<slug>/task.md`, builds a `{task_id: [paths]}` map across active tasks (`task_status` ∈ {open, in_progress, blocked, done, updated}), and flags every collision *except* those explained by reciprocal supersession (predecessor.task_superseded_by ↔ successor.task_supersedes per §3.3, §4.7, §7.10). It is wired into `tools/check-governance.sh` advisory-by-default during the migration window — set `FM_DUPLICATE_TASK_ID_STRICT=1` to gate the suite once Task 043 lands and the existing 006/006, 009/009, 031/031, 032/032 collisions are resolved. The agent obligations below remain in force (the linter is a backstop, not a substitute for the pre-creation check):

1. Before creating a new `tasks/<NNN>-<slug>/` folder, run `ls tasks/ | sort` and visually confirm the chosen `<NNN>` is unused on disk.
2. Run `git fetch origin main && git ls-tree -r --name-only origin/main tasks/ | grep '^tasks/<NNN>-' || true` to confirm the slot is unused on the target branch as well — a folder may have been merged on `main` after the agent started its branch.
3. If the slot is used, pick the next free `<NNN>` immediately; do not stage a colliding folder and rely on a future maintenance Task to fix it.
4. When the agent encounters an *existing* duplicate at session start, the agent MUST file a renumber Task per `MAINTENANCE.md §3.5` rather than attempting to resolve it inline as a T1/T2 mutation.

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

### 8.7 Blocker Tasks (`task_blocked_by`)

A Task MAY declare other Tasks as **blockers** by listing their `task_id` values in the `task_blocked_by` frontmatter list. Blocker semantics:

1. **Precondition for execution.** A Task with non-empty `task_blocked_by` MUST NOT transition `open` → `in_progress` until *every* listed blocker has `task_status: done`. The agent that attempts the transition MUST first read each blocker's `task.md` and verify the status.
2. **External vs. graph-internal blocks.** Use `task_blocked_by` for blocks that resolve when another Task in this repo finishes. Use `task_status: blocked` (per §4 Step 5) for blocks that depend on conditions outside the Task graph (e.g. an upstream library release, a third-party review). The two mechanisms are independent; a Task MAY be both `task_status: blocked` *and* carry `task_blocked_by` entries.
3. **Cycle prohibition.** The blocker graph MUST be acyclic. The linter (per §7.0 row §7.9) treats any cycle as an ERROR.
4. **Self-reference prohibition.** A Task MUST NOT list its own `task_id` in `task_blocked_by`.
5. **Successor inheritance.** When a blocked Task is closed as `updated` (§4.7), its successor inherits the blockers verbatim unless the successor's plan explicitly resolves them. The agent creating the successor MUST decide, per blocker, whether to copy it forward or drop it (with rationale in the successor's `notes.md`).
6. **Renumber stability.** If a blocker Task is renumbered per §8.1, every Task that references it via `task_blocked_by` MUST be updated in the same commit. The slug is the safer reference shape but `task_id` is permitted; mixing is allowed.

#### Acceptance Scenarios (Normative)

```gherkin
Feature: Blocker enforcement

  Scenario: Self-blocking is rejected
    Given a Task with task_id "020"
    When its frontmatter declares "task_blocked_by: ['020']"
    Then the linter MUST emit an ERROR
    And the agent MUST remove the self-reference before commit

  Scenario: Cyclic blockers are rejected
    Given Task 020 declares "task_blocked_by: ['021']"
    And Task 021 declares "task_blocked_by: ['020']"
    When the linter runs
    Then the linter MUST emit an ERROR for both Tasks
    And the cycle MUST be broken before commit

  Scenario: Blocker chain through "updated"
    Given Task 010 has "task_status: updated" and "task_superseded_by: ['022']"
    And Task 022 has "task_status: done"
    When Task X declares "task_blocked_by: ['010']"
    Then the linter MUST treat Task X's blocker as satisfied
       (an "updated" Task whose successor is "done" counts as satisfied)
    But the linter SHOULD emit a WARN that the reference SHOULD be updated to '022'
```

## 9. Anti-Patterns

- **MUST NOT** inline an executable prompt body inside `task.md`. Link to `/prompts/<slug>/prompt.md` instead.
- **MUST NOT** store research synthesis or outputs inside `/tasks/`. Those belong in `/research/<slug>/`.
- **MUST NOT** nest YAML frontmatter beyond one level.
- **MUST NOT** create a Task folder without a `task.md`.
- **SHOULD NOT** create a Task for trivial single-edit work that is fully described by a commit message.
