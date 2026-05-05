---
type: task
status: active
slug: header-ontology-and-schema-mirror
summary: "Successor to Task 011. The canonical machine-readable contract is now maintenance/schemas/header-ontology.json (shipped by Task 016, consumed by tools/fm/validate.py). Add an OPTIONAL per-type JSON Schema mirror so Jules and Gemini can validate documents without cloning the repo, and round out the ontology's docs."
created: 2026-05-05
updated: 2026-05-05
task_id: "023"
task_status: open
task_owner: "unassigned"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_supersedes:
  - "011"
task_blocked_by: []
task_affects_paths:
  - maintenance/schemas/
  - maintenance/schemas/readme.md
  - tools/fm/validate.py
---

# Task 023 — Header Ontology + Per-Type JSON Schema Mirror

Successor to [Task 011](../011-skills-frontmatter-schema-files/task.md). The original plan asked for one JSON Schema per L2 namespace plus a header ontology. Task 016 consolidated this into a single canonical file: [`maintenance/schemas/header-ontology.json`](../../maintenance/schemas/header-ontology.json) — that file now binds `tools/fm/validate.py`. The remaining 011 deliverables are:

1. Per-type JSON Schema files (`l1-vault-core.schema.json`, `l2-task.schema.json`, etc.) — useful for *external* agents (Jules, Gemini) that vendor `jsonschema` and cannot import the repo's Python.
2. A `maintenance/schemas/readme.md` index documenting which file is canonical (the ontology JSON), which are mirrors, and how they stay in sync.

This Task is *additive* — it MUST NOT introduce a second source of truth. The ontology JSON wins; the schemas are generated mirrors regenerated on every change to the ontology.

## Goal

`maintenance/schemas/` contains:

1. The canonical [`header-ontology.json`](../../maintenance/schemas/header-ontology.json) (already exists).
2. A `readme.md` index file documenting the canonical-vs-mirror partition and the regeneration command.
3. Generated mirrors at `l1-vault-core.schema.json`, `l2-task.schema.json`, `l2-prompt.schema.json`, `l2-research.schema.json`, `l2-skill.schema.json` — produced by a small generator script.
4. A pre-commit gate that fails if the mirrors disagree with the ontology.

## Plan

1. **Author the schemas readme.** Document canonicality, list every file, point to the ontology as the single source of truth.
2. **Write the generator.** A short Python script (`tools/fm/gen_schema_mirror.py`) that reads `header-ontology.json` and emits one JSON Schema per L2 type to `maintenance/schemas/l2-<type>.schema.json`. Generate L1 the same way.
3. **Wire the pre-commit check.** Extend `tools/check-governance.sh` to re-run the generator and `git diff --exit-code` over `maintenance/schemas/`. Mirror divergence MUST fail the commit.
4. **Smoke-test cross-agent use.** Validate one operational file (a task.md and a prompt.md) against the generated L1 + L2 schemas using a vendored `jsonschema` CLI to prove the mirrors are usable in isolation.

## Todo

- [ ] 1. Write `maintenance/schemas/readme.md` with the canonical/mirror partition.
- [ ] 2. Implement the generator script.
- [ ] 3. Generate the five mirror files; commit them as build artefacts.
- [ ] 4. Wire the divergence gate into `tools/check-governance.sh`.
- [ ] 5. Cross-agent smoke test (jsonschema CLI on a sample file).
- [ ] 6. Append `friction-log.md` (FL[0-3]).

## Links

- Predecessor: [`../011-skills-frontmatter-schema-files/task.md`](../011-skills-frontmatter-schema-files/task.md)
- Canonical ontology: [`maintenance/schemas/header-ontology.json`](../../maintenance/schemas/header-ontology.json)
- Source spec: [`research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) §3, §4
- Governing specs: [`TASK.md`](../../TASK.md), [`MAINTENANCE.md`](../../MAINTENANCE.md)
