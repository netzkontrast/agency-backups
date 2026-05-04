---
type: task
status: active
slug: skills-frontmatter-schema-files
summary: "Author machine-readable JSON Schemas for L1 / L2 frontmatter (task, prompt, research, skill) and the canonical header ontology, so tools can extract precision data from any operational markdown file."
created: 2026-05-04
updated: 2026-05-04
task_id: "011"
task_owner: "unassigned"
task_status: open
task_priority: P2
task_uses_prompts:
  - skills-frontmatter-schema-files
task_spawns_research: []
task_affects_paths:
  - maintenance/schemas/l1-vault-core.schema.json
  - maintenance/schemas/l2-task.schema.json
  - maintenance/schemas/l2-prompt.schema.json
  - maintenance/schemas/l2-research.schema.json
  - maintenance/schemas/l2-skill.schema.json
  - maintenance/schemas/header-ontology.json
  - maintenance/schemas/readme.md
  - tools/validate-frontmatter.py
  - tools/check-governance.sh
  - SKILLS.md
  - TASK.md
  - PROMPT.md
  - RESEARCH.md
---

# Task 011 — Skill & Frontmatter Schema Files

## Goal

Today the L1 + L2 frontmatter contract is enforced by a hand-rolled Python parser (`tools/validate-frontmatter.py`) whose rules are duplicated across the prose of `TASK.md §3`, `PROMPT.md §3`, `RESEARCH.md §3`, and the proposed `SKILLS.md`. There is no machine-readable definition that tools (or external agents) can consume. This task is `done` when:

1. A `maintenance/schemas/` directory exists with one JSON Schema per L2 namespace and one schema for L1 Vault Core. The schemas are the **canonical** definition; the prose specs reference them by relative link.
2. `tools/validate-frontmatter.py` is refactored to load and apply the JSON Schemas (via `jsonschema` or a vendored validator) instead of carrying the constraints inline. The behavior is identical; the code is shorter and the data is reusable.
3. A `header-ontology.json` schema describes every canonical `##` and `###` header expected in tasks, prompts, research SPECs, and skills (e.g. `## Goal`, `## Plan`, `## Todo`, `## What`, `## How to use`, `## References`). Each header carries a name, a one-line meaning, the type that owns it, and whether it is REQUIRED / RECOMMENDED / OPTIONAL.
4. The frontmatter index from Task 010 validates each entry against the appropriate schema and records `schema_valid: true|false` per entry, so consumers can skip invalid entries instead of silently mis-routing.
5. Cross-agent agents (Jules, Gemini) can fetch the schema files alone (a small JSON bundle) and validate any document the user pastes into them, without cloning the whole repo.

## Background — Why This Task Exists

1. **Constraints duplicated in prose.** The "L1 keys MUST be `type, status, slug, summary, created, updated`" rule appears in `TASK.md §3.2`, `AGENTS.md § Frontmatter Ontology Summary`, and `tools/validate-frontmatter.py` lines 37–38. A drift in one is a drift in all.
2. **Lossy header awareness.** Tools that want to extract just the `## Goal` of a task today rely on regex or full-file reads. The `query header <slug> <header>` command in Task 010 needs an ontology to know that `## Goal` exists in `task.md` but `## What` exists in `SKILL.md` — different types have different canonical headers.
3. **External agents need a portable contract.** Jules's cloud sandbox cannot run repo-local Python. A JSON Schema bundle is a portable contract Jules can validate against using a vendored library; it makes "Jules MUST conform to the same frontmatter rules" enforceable without porting code.
4. **Schema gap surfaced by Task 008.** Task 008 §5 already proposes adding `task_spawns_prompts` to the L2 namespace; a hand-rolled validator forces every such extension to be a code edit. A schema file makes it a one-line JSON change that the test suite immediately picks up.
5. **The header ontology is the missing key for precision extraction.** When an agent asks "what's the Goal of Task 008?", the index from Task 010 should return ~250 chars from the `## Goal` block, not 4 KB of `task.md`. Without a headers schema, the index cannot guarantee the section it slices is the section the agent meant.

## Plan

1. **Inventory the existing constraints.** Read `tools/validate-frontmatter.py` line by line and produce `notes.md` with a table of every constraint (key, owner-type, requirement, source-spec section).
2. **Author L1 Vault Core schema.** `maintenance/schemas/l1-vault-core.schema.json` — required keys, value-shape constraints (kebab-case slug, ISO-8601 dates, enums for `type` and `status`).
3. **Author L2 schemas.**
   - `l2-task.schema.json` — `task_id`, `task_status`, `task_owner`, `task_priority`, `task_uses_prompts`, `task_spawns_research`, `task_affects_paths`. Adds `task_spawns_prompts` (per Task 008 §5) marked OPTIONAL.
   - `l2-prompt.schema.json` — `prompt_kind`, `prompt_framework`, `prompt_target_agent`, `prompt_relates_to_task`, `prompt_spawned_from_research`, plus an OPTIONAL `prompt_relates_to_skill`.
   - `l2-research.schema.json` — `research_phase`, `research_executes_prompt`, `research_friction_level`, plus an OPTIONAL `research_documents_skill`.
   - `l2-skill.schema.json` — the proposed `skill_*` namespace from Task 009 (`skill_kind`, `skill_target_agents`, `skill_references_skills`, `skill_references_research`, `skill_references_prompts`, `skill_bootstrap_required`).
4. **Author the header ontology.** `maintenance/schemas/header-ontology.json` shape:
   ```json
   {
     "schema_version": "1",
     "headers": [
       {
         "header": "Goal",
         "level": 2,
         "owner_types": ["task"],
         "requirement": "REQUIRED",
         "meaning": "Single-paragraph falsifiable outcome. The Task is done only when this paragraph's claim is true."
       },
       {
         "header": "Plan",
         "level": 2,
         "owner_types": ["task"],
         "requirement": "REQUIRED",
         "meaning": "Numbered steps; each step SHOULD reference the artifact it produces."
       },
       {
         "header": "What",
         "level": 2,
         "owner_types": ["skill"],
         "requirement": "REQUIRED",
         "meaning": "What this skill is for. The first thing the agent reads after frontmatter."
       },
       ...
     ]
   }
   ```
   Initial coverage: every `##` header used in `templates/task.md`, `templates/prompt.md`, the `RESEARCH.md` directory shape, and the proposed `templates/skill.md`.
5. **Refactor `tools/validate-frontmatter.py`.** Replace inline constants with a small loader that reads the schema files; apply per-namespace validation by file path. Behavior parity test: the script's output on the current tree before and after the refactor MUST be byte-identical (modulo error-message wording). Record any wording delta in `notes.md`.
6. **Wire schemas into the Task 010 index.** When `build-frontmatter-index.py` writes an entry, it MUST also record `schema_valid: true|false`. Invalid entries MUST be visible in the `query orphans` command.
7. **Update prose specs to reference the schemas by link.** In `TASK.md §3.2`, `PROMPT.md §3`, `RESEARCH.md §3`, and `SKILLS.md` (delegated to Task 009), replace the inline tables of required keys with a one-line "Canonical schema: [`maintenance/schemas/l1-vault-core.schema.json`](./maintenance/schemas/l1-vault-core.schema.json)" plus a worked example. Tables stay in the spec for human readers, but the schema link is declared canonical.
8. **Document Jules/Gemini consumption pattern.** A `maintenance/schemas/readme.md` file describes how an external agent should fetch the schema bundle (URL or `git archive` of `maintenance/schemas/`) and validate a document it received from a user.
9. **Pre-commit verification.** `tools/check-governance.sh` exits 0; the index from Task 010 reports zero schema-invalid entries on the tracked tree (or, if any are found, they are pre-existing issues handed to Task 005 / Task 007).

## Todo

- [ ] 1. Inventory existing constraints; record in `notes.md`.
- [ ] 2. Author L1 Vault Core schema.
- [ ] 3. Author L2 task / prompt / research / skill schemas.
- [ ] 4. Author header ontology JSON.
- [ ] 5. Refactor `tools/validate-frontmatter.py` to load schemas; verify behavior parity.
- [ ] 6. Wire schema validation into the index from Task 010 (coordinate via the linked task).
- [ ] 7. Update `TASK.md` / `PROMPT.md` / `RESEARCH.md` to reference the schema files.
- [ ] 8. Author `maintenance/schemas/readme.md` with the cross-agent consumption pattern.
- [ ] 9. Confirm `tools/check-governance.sh` exits 0; close the task.

## Links

- Executing prompt: [`/prompts/skills-frontmatter-schema-files/prompt.md`](../../prompts/skills-frontmatter-schema-files/prompt.md)
- Depends on Task 009 for the `skill_*` namespace it codifies: [`../009-author-skills-root-spec/`](../009-author-skills-root-spec/)
- Sister of Task 010 (provides the schemas Task 010's index validates against): [`../010-skills-frontmatter-index-suite/`](../010-skills-frontmatter-index-suite/)
- Schema-gap predecessor: [`../008-harden-coherence-baseline-protocol/`](../008-harden-coherence-baseline-protocol/) §5 already proposes `task_spawns_prompts`; this Task delivers the schema change.
- Governing specs: [`TASK.md`](../../TASK.md) §3, [`PROMPT.md`](../../PROMPT.md) §3, [`RESEARCH.md`](../../RESEARCH.md) §3
