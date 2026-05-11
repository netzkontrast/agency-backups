---
type: note
status: active
slug: friction-log-023
summary: "Friction log for Task 023 — JSON-Schema mirror suite ships clean. FL0 with a single observation about PyYAML date coercion."
created: 2026-05-11
updated: 2026-05-11
---

# Friction Log — Task 023

Highest Frustration Level: FL0

## Summary

Additive Task. Shipped six Draft-07 mirror schemas (`l1-vault-core` + `l2-{task,prompt,research,skill,adr}`), a pure-stdlib generator (`tools/fm/gen_schema_mirror.py`), the `readme.md` partition document, a divergence gate (`tools/check-governance.sh` step `[5b]`), and a 9-test pytest suite that round-trips real `task.md` / `prompt.md` / ADR frontmatter through `jsonschema` Draft7. `tools/check-governance.sh` exits 0; the gate fires correctly when a mirror is mutated by hand.

## Observations

- **PyYAML date coercion.** `yaml.safe_load` returns `datetime.date` objects for ISO-8601 `created:` / `updated:` fields, which `jsonschema` rejects against `{"type": "string"}`. External agents MUST JSON-normalise frontmatter (e.g. `json.loads(json.dumps(fm, default=str))`) before validating. Documented in `maintenance/schemas/readme.md` and exercised in the smoke tests. No code change to the canonical ontology was needed.
- **ADR mirror is a verbatim lift.** `types.adr.json_schema` already existed inside `header-ontology.json` (anchor ADR.A.5.4). The generator delegates to it rather than re-deriving from `required_keys` — single source of truth preserved.

## Trust dimensions (Spec-J/K/L)

- **Schema integrity:** PASS — each mirror self-validates as Draft-07; full suite re-runs in `--check` mode at pre-commit.
- **Behavioural integrity:** PASS — 9/9 tests green; gate fires on intentional drift.
- **Governance integrity:** PASS — `tools/check-governance.sh` exits 0; no second source of truth introduced.

No follow-up Task warranted.
