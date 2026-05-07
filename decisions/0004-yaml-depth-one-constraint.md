---
type: adr
status: draft
slug: 0004-yaml-depth-one-constraint
summary: "Frontmatter YAML MUST NOT nest beyond one level; lists MUST contain only scalars. Hand-rolled parser in tools/fm/_core.py enforces the constraint, defeating LLM nesting hallucinations."
created: 2026-05-07
updated: 2026-05-07
adr_id: ADR-0004
adr_status: Proposed
adr_owner: agency-maintainer
adr_tags:
  - frontmatter
  - yaml
  - llm-hallucination
  - parser
---

# ADR-0004 — YAML Depth-1 Constraint and Anti-Hallucination Rationale

## Context and Problem Statement

LLMs hallucinate nested YAML — silent indentation drift produces semantically wrong frontmatter that round-trips through `yaml.load` without error because PyYAML accepts ambiguous nesting permissively. The result is metadata that reads correctly to a human reviewer but evaluates incorrectly under tooling (e.g. a list of mappings becomes a single-key mapping with sibling keys on the wrong level).

The repo declares a depth-1 constraint at [`AGENTS.md:218-222`](../AGENTS.md) ("YAML frontmatter MUST NOT nest beyond one level. Lists MUST contain scalars or short strings only.") and the constraint is reified by the hand-rolled parser at [`tools/fm/_core.py:41-44`](../tools/fm/_core.py). This ADR formalises both the rule and its anti-hallucination rationale.

## Decision Drivers

- **Deterministic LLM authoring.** A constraint that is mechanically catchable defeats the most common LLM-frontmatter defect class.
- **Parser auditability.** A hand-rolled parser at ≈ 50 LoC is human-auditable; PyYAML is not.
- **Sufficiency.** Depth-1 with scalar lists covers every L1/L2 namespace currently in use (Task, Prompt, Research, Skill, ADR); structured nested metadata can live in body-level tables or separate schema files.

## Considered Options

1. **Full YAML 1.2.** Rejected: hallucination surface too wide; recovery from a malformed nested file is expensive in context-token cost.
2. **JSON-only frontmatter.** Rejected: breaks Obsidian's native rendering and graph view; contradicts the L0 Obsidian-reserved keys (`tags`, `aliases`, `cssclasses`).
3. **Depth-1 YAML with scalar lists (chosen).** A subset of YAML 1.2 that is parseable by ≈ 50 LoC, deterministic under LLM authoring, and round-trips via `tools/fm/edit.py`.

## Decision Outcome

All frontmatter in this repository MUST be YAML restricted to one level of nesting; lists MUST contain only scalars or short strings; nested mappings or lists-of-mappings MUST be rejected by the parser; the canonical parser is `tools/fm/_core.py:parse_frontmatter` and bypassing it (e.g. via PyYAML directly) is prohibited for governance-touching code.

## Consequences

- **Positive.** Parser is ≈ 50 LoC and audit-grade reliable. LLM-authored frontmatter is deterministically checkable. The constraint composes with ADR-0003 (frontmatter-as-truth) to keep the audit graph mechanically queryable.
- **Negative.** Complex structured metadata cannot live in frontmatter — it MUST be referenced from a body table or a separate schema file. Authors who reach for nested YAML must restructure.
- **Neutral.** This is the parsing baseline for the entire flexible toolchain (`tools/fm/`); the ADR validator (`tools/adr/cli.py`) reuses it per ratified SPEC §7.1 ADR.A.5.9.
