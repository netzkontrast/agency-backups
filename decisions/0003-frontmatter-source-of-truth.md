---
type: adr
status: draft
slug: 0003-frontmatter-source-of-truth
summary: "Cross-directory edges in the audit graph (Task↔Prompt↔Research↔Skill) MUST live in frontmatter, not body Markdown links. Body links are encouraged for navigation but never consumed by tooling."
created: 2026-05-07
updated: 2026-05-07
adr_id: ADR-0003
adr_status: Proposed
adr_owner: agency-maintainer
adr_tags:
  - frontmatter
  - audit-graph
  - linkage
---

# ADR-0003 — Frontmatter as the Single Source of Truth for the Audit Graph

## Context and Problem Statement

Body-level Markdown links between Tasks, Prompts, Research, and Skills are convenient for human navigation but unparseable by tooling without a full Markdown AST and link-resolution pass. The repo's audit graph (Task → Prompt → Research → Prompt → …) MUST be queryable mechanically, so reciprocity, orphan-detection, and supersession-DAG validation can run as cheap pre-commit checks.

The rule is declared at [`FOLDERS.md:86-99`](../FOLDERS.md) (linkage keys + reciprocity check) and [`TASK.md:42-46`](../TASK.md) (Layered Schema with Namespacing). It has never been ratified as an ADR; this ADR formalises it so future expansions of the linkage namespace (new edge types) land via supersession.

## Decision Drivers

- **Mechanical reciprocity.** `tools/lint-linkage.py` rejects asymmetric edges; that check needs a closed list of declarative linkage keys.
- **Two reading audiences.** Humans benefit from body-Markdown links; tooling benefits from frontmatter. The two surfaces co-exist without ambiguity only if one is declared authoritative.
- **Future graph render.** A future graph CLI (`tools/fm/query.py` evolution) or static-site renderer depends on the structured edge being authoritative.

## Considered Options

1. **Body Markdown link as ground truth.** Rejected: requires AST parsing for every check; relative-link resolution is brittle; reciprocity is essentially undecidable without keying every link to a back-reference convention.
2. **Separate edge-list file (e.g. `audit-graph.json`).** Rejected: duplicates state; introduces a sync surface that drifts on every move/rename.
3. **Frontmatter-as-ground-truth + body links for navigation (chosen).** A closed list of L2-namespaced keys (`task_uses_prompts`, `prompt_relates_to_task`, `research_executes_prompt`, …) carries the audit graph; body links are encouraged and unconstrained.

## Decision Outcome

Every cross-directory edge in the audit graph MUST be expressed in frontmatter via the linkage keys listed in [`FOLDERS.md`](../FOLDERS.md) §6; body-level Markdown links are encouraged for human navigation but MUST NOT be relied on by any validator, lint, or graph tool.

## Consequences

- **Positive.** `tools/lint-linkage.py` walks the tree without parsing prose. Reciprocity is a CI-checkable invariant. Future graph tooling has a declarative source.
- **Negative.** Humans MUST update frontmatter (not just body links) when re-routing a Task or Prompt; the two surfaces drift if the discipline lapses.
- **Neutral.** This is the graph backbone every audit and synthesis tool reuses; ADR-0005 (T4 immutability) and the ratified SPEC §6 (ADR supersession DAG) inherit the reciprocity model directly.
