# Brief: `tools/skills-index.py emit` — Contract & JSON Schema

## Source

Follow-up question from the `skills-navigation-bootstrap` research run (2026-05-04). Corresponds to Q2 in `research/skills-navigation-bootstrap/output/SPEC.md` §7.

## Question

The `skills-navigation-bootstrap` SPEC.md proposes a single emitter `tools/skills-index.py` exposing three verbs: `emit`, `get`, `verify`. The proposal specifies the verbs and a sketch of the manifest output but does not nail down:

1. The **complete JSON Schema** for the manifest (`<runtime-skills-dir>/.index.json`).
2. The exit codes, error messages, and partial-failure semantics for each verb.
3. The integration points: how `skills/skills-skill-bootstrap/sync.sh` calls `emit` after a sync; how `verify.sh` calls `verify`; how `tools/check-governance.sh` adds it to the pre-commit gate.
4. The behaviour of `get --section <name>` when section headings have minor textual drift (e.g., `## When to use` vs `## When To Use`).

## Why it's blocked

Task 010 cannot start implementation without an agreed contract. Task 011 cannot finalise its schema files without §1 above.
