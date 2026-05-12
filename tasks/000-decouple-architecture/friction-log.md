# Friction Log — Task 000

**Highest Frustration Level:** FL1

## What went well (FL0 portion)

- The obsidian-frontmatter spec gave a ready-made ontology to anchor namespaces. Zero re-derivation cost.
- RFC-2119 + Gherkin scaffolding from the existing `RESEARCH.md` and `PROMPT.md` was directly portable to `TASK.md`.
- The `Explore` and `Plan` agents were not needed; the working set fit in main context.

## FL1 — Minor friction surfaced on second pass

1. **Spec written without a validator.** First commit shipped four governance specs but no enforcement script. The user's framing (*"perfekt auf ein CLI-Tool oder einen Graphen vor"*) was a hint I underweighted on pass one. Mitigation: added `tools/validate-frontmatter.py` on the second pass after re-reading the prompt.

2. **Templates not shipped.** First commit mandated frontmatter shapes but provided no copy-and-edit starter. A future agent would have authored from memory and drifted. Mitigation: added `/templates/` on the second pass.

3. **Pre-commit routing inconsistency.** First commit added `TASK.md` but did not update `PRE_COMMIT.md` to mention it. The master pre-commit checklist still routed only to `RESEARCH.md`. Mitigation: rewrote `PRE_COMMIT.md` §6 with the three-row routing table.

4. **Reflection methods named in the prompt's frontmatter were not produced as artifacts.** The prompt explicitly listed M10, M07, M13 under "critical_thinking_methods". On pass one these were applied implicitly (in commit message + PR-style summary) but no artifact existed. Mitigation: created `/tasks/000-decouple-architecture/` retroactively with three reflection files, dogfooding the new spec.

5. **Validator first draft had blanket scope.** Initial implementation walked every `.md` file and demanded frontmatter, generating 80+ false positives on legacy research workspaces. Mitigation: narrowed to spec-mandated files only (`task.md`, `prompt.md`, `output/SPEC.md`, root `readme.md`s) and added a waivers file for grandfathered artifacts.

## Recommendations for Future Architectural Refactors

- When the originating prompt lists critical-thinking methods in frontmatter, treat that as a required deliverable list, not an optional rhetoric flourish.
- Spec-without-validator is a sign of incomplete work. If the spec mandates a shape, ship the script that checks the shape in the same commit.
- Templates are not optional ergonomics; they are the *defense against drift* between architecture authoring and architecture adoption.
