---
type: note
status: active
slug: triage-note-writing-skills
summary: "Triage note for superpowers/skills/writing-skills/SKILL.md. Decision adapt: 22 KB body applies TDD to skill authoring; valuable but requires heavy references/ extraction to fit D.6."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — `superpowers/skills/writing-skills/SKILL.md`

## What it is

A 22.4 KB meta-skill: "apply Red-Green-Refactor TDD to **skill documentation**." Drives an iterative author-test-revise loop for authoring SKILL.md bodies, with worked examples and a deep checklist.

## Why `adapt` (not `port`)

The body is 4.4× over the D.6 5 KB cap. Naive `port` violates the cap immediately. ST-3 MUST:

1. Preserve the **methodology** prose (TDD-for-skills, RED/GREEN/REFACTOR phases) in the main SKILL.md body — target ≤ 4 KB.
2. Move worked examples, the checklist, and reference-material into `skills/superpowers-writing-skills/references/`:
   - `references/red-phase-worked-example.md`
   - `references/green-phase-worked-example.md`
   - `references/refactor-checklist.md`
3. Cross-reference Agency's `skill-creator`, `skills-skill-bootstrap`, and `spec-skill` skills via `skill_references_skills` frontmatter (do NOT inline-link in body).

## Conflict with Agency's existing skill-authoring tooling

Agency already ships:

- `skills/skill-creator/` — bootstrap a new SKILL.md.
- `skills/skills-skill-bootstrap/` — orchestrate skill-authoring sessions.
- `skills/spec-skill/` — Gherkin-driven spec authoring.

The upstream `writing-skills` adds a **distinct** discipline (TDD-for-docs) that complements rather than duplicates. ST-3 MUST cite the relationship in the SKILL.md `## Relation to Agency native skills` section.

## Landing folder

`skills/superpowers-writing-skills/`. Tier L3 (depends on Agency's skill-authoring substrate).

## Audit-graph linkage

- `skill_source: "superpowers@v4.0.3"`
- `skill_references_skills: [skill-creator, skills-skill-bootstrap, spec-skill, superpowers-tdd]`
