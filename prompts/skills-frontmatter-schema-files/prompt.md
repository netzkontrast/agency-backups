---
type: prompt
status: active
slug: skills-frontmatter-schema-files
summary: "Author JSON Schemas for L1 / L2 frontmatter (task, prompt, research, skill) and a header ontology so tools can extract precise sections from any operational markdown file."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: task-spec
prompt_framework: RISEN
prompt_target_agent: "Claude Code"
prompt_relates_to_task: skills-frontmatter-schema-files
---

# Author Schema Files for Frontmatter & Headers

## Framework

**RISEN.** This is a structured authoring task with a well-defined target shape (JSON Schema Draft 2020-12) and a pre-existing parser to refactor against. ReAct loops are unnecessary; all evidence is in-repo.

---

## § RFC 2119

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals as shown here.

---

## R — Role

You are a schema author writing the canonical machine-readable definition of the repository's frontmatter and header conventions. Your output is the source of truth that tools (`validate-frontmatter.py`, the index from Task 010) and external agents (Jules, Gemini) consume.

## I — Input

The executor MUST read:

1. `/tasks/011-skills-frontmatter-schema-files/task.md` — the binding plan.
2. `/tools/validate-frontmatter.py` — the existing constraints to lift.
3. `/TASK.md §3`, `/PROMPT.md §3`, `/RESEARCH.md §3` — the prose canon.
4. `/SKILLS.md §3` once Task 009 lands — the `skill_*` namespace authority.
5. `/templates/task.md`, `/templates/prompt.md`, the proposed `/templates/skill.md` — the canonical body shapes that ground the headers ontology.
6. `/maintenance/language-spec.md` — the RFC-2119 + Gherkin grammar the schemas reference.

## S — Steps

### Step 1 — Constraint inventory

Open `tools/validate-frontmatter.py`. For every constant, regex, or branch that encodes a rule, write a row to `notes.md`:

| Source line | Constraint | Owner schema |
|---|---|---|
| L37 `L1_REQUIRED = {...}` | `type, status, slug, summary, created, updated` are required | l1-vault-core |
| L38–39 `L2_TASK = {...}` | task_id, ... required for tasks | l2-task |
| ... | ... | ... |

The inventory MUST be exhaustive: every diagnostic the validator can emit MUST trace to a row.

### Step 2 — Author L1 schema

`maintenance/schemas/l1-vault-core.schema.json`. Required keys, types, enums, regex constraints (kebab-case slug, ISO-8601 dates). Use Draft 2020-12. The schema MUST also forbid extra properties at L1 (additional keys live in L2 namespaces, not in L1).

### Step 3 — Author L2 schemas

One file each:

- `l2-task.schema.json` — All keys in §3.3 of TASK.md, plus `task_spawns_prompts` (OPTIONAL list), per Task 008 §5.
- `l2-prompt.schema.json` — All keys in §3.3 of TASK.md (prompt namespace), plus OPTIONAL `prompt_relates_to_skill` (string slug).
- `l2-research.schema.json` — All keys in §3.3 of TASK.md (research namespace), plus OPTIONAL `research_documents_skill` (string slug).
- `l2-skill.schema.json` — `skill_kind` (enum), `skill_target_agents` (list, enum members), `skill_references_skills` (list, slug), `skill_references_research` (list, slug), `skill_references_prompts` (list, slug), `skill_bootstrap_required` (boolean).

Each schema MUST define `additionalProperties: false` to fail closed on typos (a frequent silent bug today).

### Step 4 — Author header ontology

`maintenance/schemas/header-ontology.json`. Shape exactly as in `tasks/011-skills-frontmatter-schema-files/task.md` §Plan step 4. Initial coverage:

- Task headers: `Goal`, `Plan`, `Todo`, `Links`, `Background`, `Frustration Log`, `Resumption Checklist`, `Partial Artifacts`.
- Prompt headers: `Framework`, `R — Role`, `I — Input`, `S — Steps`, `E — Expectations`, `Constraints`.
- Research SPEC headers: `§1 Normative Conventions`, `Executive Summary`, `Landscape Map`, `Design Hypotheses`, `Surviving Architecture`, `Normative Specification`, `Gherkin Acceptance Criteria`, `Open Questions`.
- Skill headers (per the proposed `templates/skill.md`): `What`, `When to use`, `How to use`, `References`, `Compatibility`.

Each entry MUST carry: `header`, `level` (2 or 3), `owner_types`, `requirement` (REQUIRED / RECOMMENDED / OPTIONAL), `meaning` (one sentence).

### Step 5 — Refactor `tools/validate-frontmatter.py`

Replace the inline constants with a small loader that reads the schemas. Use `jsonschema` if it can be added without bloating the existing dependency set; otherwise vendor a minimal validator (the spec only needs `required`, `enum`, `type`, `pattern`, `additionalProperties`, `items`).

Behavior parity test: `tools/validate-frontmatter.py` output MUST be byte-identical (modulo error-message wording) on the current tree. Record any wording change in `notes.md`.

### Step 6 — Wire schemas into the Task 010 index

Coordinate with the agent executing Task 010 (or amend the build script if Task 010 has already shipped) so each entry in `.agent_cache/frontmatter-index.json` carries `schema_valid: true|false`. Invalid entries MUST appear in `query orphans`.

### Step 7 — Update prose specs

In `TASK.md §3.2`, `PROMPT.md §3`, `RESEARCH.md §3`, and `SKILLS.md §3` (if Task 009 has landed), add a one-line "Canonical schema: [`maintenance/schemas/<file>`](./maintenance/schemas/<file>)" reference after the existing tables. Tables remain for human readers; the schema link is declared canonical for tools.

### Step 8 — Author cross-agent consumption README

`maintenance/schemas/readme.md` MUST describe how an external agent (Jules or Gemini) fetches and uses the schemas without cloning the whole repo. Two patterns:

1. `git archive` of `maintenance/schemas/` produces a self-contained tarball.
2. Direct raw-content fetch via the platform's GitHub MCP tool.

The readme MUST include a worked example: Jules receives a Markdown file from a user, fetches the schema bundle, validates the frontmatter, and rejects with a precise error if invalid.

### Step 9 — Lint sweep

`tools/check-governance.sh` MUST exit 0. The Task 010 index MUST report 0 schema-invalid entries on the tracked tree (or, where invalid entries are pre-existing, they MUST be itemized in `notes.md` and routed to Tasks 005 / 007 for remediation).

## E — Expectations

The following files MUST exist and be staged on completion:

| Path | Purpose |
|---|---|
| `/maintenance/schemas/l1-vault-core.schema.json` | L1 contract. |
| `/maintenance/schemas/l2-task.schema.json` | Task L2 contract. |
| `/maintenance/schemas/l2-prompt.schema.json` | Prompt L2 contract. |
| `/maintenance/schemas/l2-research.schema.json` | Research L2 contract. |
| `/maintenance/schemas/l2-skill.schema.json` | Skill L2 contract. |
| `/maintenance/schemas/header-ontology.json` | Header semantics. |
| `/maintenance/schemas/readme.md` | Cross-agent consumption guide. |
| `/tools/validate-frontmatter.py` | Refactored to load schemas. |
| `/TASK.md`, `/PROMPT.md`, `/RESEARCH.md`, `/SKILLS.md` | Schema link added in §3. |
| `/tasks/011-skills-frontmatter-schema-files/notes.md` | Constraint inventory + behavior-parity report. |
| `/tasks/011-skills-frontmatter-schema-files/friction-log.md` | FL declaration. |

## Constraints

1. **MUST** target JSON Schema Draft 2020-12 unless a hard incompatibility with the chosen validator forces an older draft (record the decision in `notes.md`).
2. **MUST NOT** introduce dependencies outside `pyproject.toml` without flagging in `notes.md`.
3. **MUST** keep schemas under 200 lines each; if a schema exceeds, factor into `<name>.schema.json` + `<name>.partials.json`.
4. **MUST** preserve behavior parity in `tools/validate-frontmatter.py`. Refactor is a no-functional-change commit.
5. **MUST** declare an FL value in the friction log.
