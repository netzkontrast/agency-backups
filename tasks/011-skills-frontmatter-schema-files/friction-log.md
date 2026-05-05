---
type: note
status: active
slug: 011-friction-log
summary: "Friction log for Task 011 closing as 'updated' — predecessor of Task 023."
created: 2026-05-05
updated: 2026-05-05
---

# Friction Log — Task 011

## FL Declaration

**FL0** — plan obsolesced cleanly. Task 016 consolidated what Task 011 had decomposed into five separate JSON Schema files (`l1-vault-core.schema.json`, `l2-task.schema.json`, `l2-prompt.schema.json`, `l2-research.schema.json`, `l2-skill.schema.json`) into a single canonical [`maintenance/schemas/header-ontology.json`](../../maintenance/schemas/header-ontology.json). The unified ontology now binds `tools/fm/validate.py` directly; the per-type fragmentation is no longer the canonical surface.

## Supersession Rationale

The canonical machine-readable contract for L1 + L2 frontmatter and per-type required headings is now the single file `maintenance/schemas/header-ontology.json`, encoding the matrices from `research/flexible-frontmatter-toolchain/output/SPEC.md` §3 and §4. `tools/fm/validate.py` loads this file directly (per its `_expected_required_keys` helper). Per-type JSON Schemas are still useful for *external* agents (Jules, Gemini) that vendor `jsonschema` and cannot import the repo's Python — but they MUST be regenerated mirrors, not parallel sources of truth.

The continuation lives at [`/tasks/023-header-ontology-and-schema-mirror/`](../023-header-ontology-and-schema-mirror/) and is scoped to producing those mirrors plus the divergence gate.

## Pointers

- Successor: [`../023-header-ontology-and-schema-mirror/task.md`](../023-header-ontology-and-schema-mirror/task.md)
- Canonical ontology shipped: [`maintenance/schemas/header-ontology.json`](../../maintenance/schemas/header-ontology.json)
- Lineage governance: [`TASK.md §4.7`](../../TASK.md), [`MAINTENANCE.md §3.4`](../../MAINTENANCE.md).
