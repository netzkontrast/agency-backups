---
type: index
status: active
slug: 011-skills-frontmatter-schema-files
summary: "Index for Task 011 — author JSON Schemas for L1/L2 frontmatter and the canonical header ontology."
created: 2026-05-04
updated: 2026-05-04
---

# Task 011 — Skill & Frontmatter Schema Files

## What and Why

This folder coordinates extracting the frontmatter contract out of prose specs and Python source into a portable JSON Schema bundle. The bundle is what makes the Task 010 index verifiable, and what makes Jules/Gemini compatibility a contract instead of an aspiration.

## Linked Navigation

- [`task.md`](./task.md) — Goal, Plan, Todo, Links.
- Executing prompt: [`/prompts/skills-frontmatter-schema-files/prompt.md`](../../prompts/skills-frontmatter-schema-files/prompt.md).
- Sibling tasks: [`../009-author-skills-root-spec/`](../009-author-skills-root-spec/), [`../010-skills-frontmatter-index-suite/`](../010-skills-frontmatter-index-suite/).
- Predecessor flagging the schema gap: [`../008-harden-coherence-baseline-protocol/`](../008-harden-coherence-baseline-protocol/) §5.

## Assumptions Log

- We assume JSON Schema (Draft 2020-12) is the right format. Alternatives considered: Pydantic, Zod, hand-rolled YAML. JSON Schema wins because (a) language-neutral so Jules and Gemini can validate without Python, (b) already familiar to the target audience, (c) round-trips through `tools/validate-frontmatter.py` with one library import.
- We assume the schemas live under `maintenance/schemas/` rather than `tools/schemas/` because they are *governance artifacts*, not implementation tools — `MAINTENANCE.md` is the spec that already groups validators and contract artifacts under `/maintenance/`.
- We assume the prose specs continue to carry human-readable tables alongside the canonical schema link. Replacing the prose with a bare link harms readability for human maintainers; the schema link is the source of truth for tools, the table is the source of truth for humans, and a `tools/lint-schema-prose-parity.py` follow-up may later check they match.
