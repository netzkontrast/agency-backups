---
type: spec
status: active
slug: prompt-spec
summary: "Root specification for /prompts/. Prompts are the only place where executable instruction sets live; research proposals and follow-up questions are deposited here, never in /research/ or /tasks/."
created: 2026-05-02
updated: 2026-05-04
---

# Prompt Task Specification

> **Mechanical Enforcement Notice:** This spec is mechanically enforced by `tools/check-governance.sh`. Before editing any file under `/prompts/`, install the pre-commit hook once with `tools/install-hooks.sh`. See [§6 Mandatory Pre-Commit Checks](#6-mandatory-pre-commit-checks-for-prompt-tasks) for the per-clause linter mapping.

A **Prompt Task** produces an *instruction set* — a self-contained, executable artifact intended to be run by an agent. Prompts are the single source of truth for "what the agent is told to do". Tasks (`/tasks/`) coordinate work; Research (`/research/`) records what running a prompt produced. This file governs the `/prompts/` directory only.

## 1. Scope (What Belongs in `/prompts/`)

Every artifact whose primary purpose is to instruct an agent MUST be stored under `/prompts/<slug>/`. This explicitly includes:

1. **Research proposals** — Prompts that, when executed, will spawn a research workspace under `/research/`.
2. **Follow-up questions** — Open questions surfaced by a prior research run. These MUST be filed as new prompts in `/prompts/`, not appended to the original `/research/<slug>/`.
3. **Tool instructions** — Prompts that drive a one-shot or recurring tool action.
4. **Task-specs** — Prompts referenced by a Task in `/tasks/<NNN>-<slug>/task.md` via `task_uses_prompts`.

Prompts MUST NOT be inlined inside `task.md` files, and MUST NOT live inside `/research/<slug>/`.

## 2. Directory Structure

```text
/prompts
└── /<slug>
    ├── readme.md     # Directory index (per FOLDERS.md).
    ├── brief.md      # Raw user request, target audience, intended model/agent, use-case context.
    └── prompt.md     # The deliverable: the final, self-contained crafted prompt with frontmatter.
```

Subfolders MUST NOT be created unless 4+ same-category files (e.g., iteration drafts) accumulate, per `FOLDERS.md`.

## 3. Mandatory Frontmatter (Layered Schema with Namespacing)

`prompt.md` MUST carry the L1 Vault Core keys plus the L2 `prompt_*` namespace defined in `TASK.md` §3. Example:

```yaml
---
type: prompt
status: active
slug: <prompt-slug>
summary: "One-line tl;dr the agent reads instead of opening the body."
created: YYYY-MM-DD
updated: YYYY-MM-DD
prompt_kind: research-proposal | follow-up | tool-instruction | task-spec | general
prompt_framework: RISEN | RISE-DX | ReAct | RISEN+ReAct | CoT
prompt_target_agent: "Claude Code"
prompt_relates_to_task: <task-slug>      # OPTIONAL: only when a Task already lists this prompt in task_uses_prompts.
prompt_spawned_from_research: <slug>     # OPTIONAL: research that produced this prompt as a follow-up.
---
```

YAML MUST NOT nest deeper than one level. Lists MUST contain only scalars.

## 4. Workflow Requirements

1. **Initialize Directory** — Create `/prompts/<slug>/` immediately. Derive the slug from the brief's core intent (kebab-case, max 5 tokens).
2. **Store Brief** — Save the unedited user request and contextual metadata into `brief.md`. This is the immutable record of what was asked.
3. **Select Framework** — Choose a prompt engineering framework based on task type:
   - `RISEN + ReAct` — multi-step research and extraction tasks where the agent must iterate.
   - `RISE-DX` — for the agentic-spine prompts that demand reflection-driven execution.
   - `RISEN` — structured one-shot output tasks (spec generation, code scaffolding).
   - `Chain-of-Thought` — open-ended reasoning, analysis, or evaluation.
   Declare the framework in the frontmatter (`prompt_framework`) AND at the top of the body.
4. **Draft the Prompt** — Write `prompt.md` per the Engineering Principles (§5).
5. **Link Backward** — If the prompt was spawned by an open question from a prior research run, set `prompt_spawned_from_research: <research-slug>`. This forms the audit trail.
6. **Pre-Commit** — Run the checks in §6.

## 5. Prompt Engineering Principles

Every prompt produced MUST satisfy:

1. **Self-Containedness** — Works without external context, prior conversation history, or out-of-band documentation. Every method, framework, constraint, and term MUST be defined inline.
2. **Framework Declaration** — Frontmatter `prompt_framework` and a body header naming the framework.
3. **RFC 2119 Normativity** — Use `MUST`, `SHOULD`, `MAY` for normative requirements. No "please" or "try to" in mandatory clauses. Exactly one normative keyword per sentence.
4. **Deliverable Lock** — Specify output format precisely: file names, section headings, data types, encoding.
5. **Anti-Ambiguity** — If a term has two readings, define it inline.
6. **Constraint Isolation** — Group exclusions and hard constraints into a dedicated `Constraints` section.
7. **Failure Handling** — Specify what the agent MUST do when a step fails or a source is unavailable.

## 6. Mandatory Pre-Commit Checks for Prompt Tasks

The agent MUST run `tools/check-governance.sh` before committing any change to `/prompts/`. The agent MUST NOT commit if that script exits non-zero. The eight checks below are mechanically enforced by the linters mapped in §6.0.

### 6.0 Mechanical Enforcement Mapping

| Check | Tool | Failure mode |
|---|---|---|
| §6.1 Brief Integrity | [`tools/lint-structure.py`](./tools/lint-structure.py) | Missing `brief.md` in prompt folder |
| §6.2 Frontmatter Integrity | [`tools/validate-frontmatter.py`](./tools/validate-frontmatter.py) | Missing L1/L2 keys, YAML depth > 1, non-kebab slug |
| §6.3 Prompt Non-Empty | [`tools/lint-structure.py`](./tools/lint-structure.py) | Missing `prompt.md` in prompt folder |
| §6.4 Self-Containedness Test | human review | No mechanical check — human responsibility |
| §6.5 Backward Link Resolves | [`tools/lint-linkage.py`](./tools/lint-linkage.py) | `prompt_spawned_from_research` doesn't resolve |
| §6.6 Forward Link Reciprocity | [`tools/lint-linkage.py`](./tools/lint-linkage.py) | `prompt_relates_to_task` set but task does not list this prompt |
| §6.7 Readme Audit | [`tools/lint-structure.py`](./tools/lint-structure.py) | Missing `readme.md` in prompt folder |
| §6.8 Friction Log | human review (commit message) | No mechanical check at commit time |

Before committing the deliverables of a Prompt Task, the agent MUST verify:

1. **Brief Integrity** — `brief.md` exists and contains the exact, unedited user request.
2. **Frontmatter Integrity** — `prompt.md` carries every required L1 and `prompt_*` key. YAML nesting ≤ 1.
3. **Prompt Non-Empty** — `prompt.md` is non-empty and constitutes a complete, executable prompt.
4. **Self-Containedness Test** — Read `prompt.md` in isolation; no section requires external context.
5. **Backward Link Resolves** — If `prompt_spawned_from_research` is set, that research slug resolves to either `/research/<slug>/` or any `/research/<provider>/<slug>/` (provider subfolders per RESEARCH.md §6 are valid spawn sources).
6. **Forward Link Reciprocity** — `prompt_relates_to_task` encodes a *uses* relationship, not a "spawned by" relationship. If set, the named Task MUST list this prompt's slug in `task_uses_prompts`. Follow-up prompts not yet adopted by any Task MUST omit this field; their lineage is preserved via `prompt_spawned_from_research`.
7. **Readme Audit** — `/prompts/<slug>/readme.md` exists and links to `brief.md` and `prompt.md` per `FOLDERS.md`.
8. **Friction Log** — A `## Frustration Log` section in the PR/commit message (or a `friction-log.md` adjacent for standalone runs), per `FRUSTRATED.md`. FL0 declarations are still mandatory.

## 7. Anti-Patterns

- **MUST NOT** store prompt drafts inside `/research/<slug>/`. Research is execution-only.
- **MUST NOT** inline a prompt body inside a Task's `task.md`. Link via `task_uses_prompts`.
- **MUST NOT** modify a published research run to append "follow-up questions". Create a new prompt under `/prompts/` with `prompt_kind: follow-up` and `prompt_spawned_from_research` set.
