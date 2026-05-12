---
name: superpowers-writing-skills
description: >-
  TDD-for-skills — apply Red-Green-Refactor to SKILL.md authoring. Use when creating or revising any skill in /skills/; complements skill-creator + spec-skill.
skill_kind: meta
skill_target_agents: [claude-code]
skill_references_skills: [skill-creator, skills-skill-bootstrap, spec-skill, superpowers-tdd]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superpowers@v4.0.3"
---

# superpowers-writing-skills (imported from Superpowers v4.0.3)

## What

Imported skill-authoring discipline from the Superpowers corpus. Applies TDD's **Red-Green-Refactor** cycle to **skill documentation** itself — every SKILL.md gets a failing-test phase, a minimal-implementation phase, and a refactor pass.

## When to use

Fire when authoring or substantively revising any skill in `/skills/`. Complements Agency's existing skill-authoring substrate:

- `skill-creator` — bootstrap a new SKILL.md skeleton.
- `skills-skill-bootstrap` — orchestrate skill-authoring sessions.
- `spec-skill` — author the Gherkin spec the skill must satisfy.
- `superpowers-writing-skills` (this skill) — **the TDD discipline** that ties them together.

## How to use

Three phases per skill — strictly ordered:

1. **RED.** Write a Gherkin scenario that the future SKILL.md MUST satisfy. The scenario should fail when read against an empty `SKILL.md`. (Run a dry-read or have a subagent attempt the scenario; it should be unable.)
2. **GREEN.** Write the **minimum** SKILL.md body that lets a fresh agent execute the scenario correctly. Resist adding unrelated guidance.
3. **REFACTOR.** Restructure for clarity, extract bulky examples to `references/`, tighten language. The scenario stays green throughout.

Full per-phase guidance + worked examples at `references/upstream-superpowers-writing-skills.md` (22 KB upstream body).

## Relation to Agency native skills

- **`skill-creator`** — bootstrap layer (file scaffolding).
- **`spec-skill`** — Gherkin specification layer (what the skill must satisfy).
- **`superpowers-writing-skills`** — discipline that drives the bootstrap + spec layers iteratively.
- **`superpowers-tdd`** — sibling discipline; same R/G/R cycle applied to code.

## References

- Upstream verbatim mirror: [`references/upstream-superpowers-writing-skills.md`](./references/upstream-superpowers-writing-skills.md) (Superpowers `skills/writing-skills/SKILL.md` @ SHA `b9e16498`, v4.0.3 — 22 KB body lives entirely in references/ per ADR-0011 D.3+D.6).
- Triage rationale: [`tasks/092-…/references/triage-notes/superpowers-writing-skills.md`](../../tasks/092-port-skill-corpora-phase-2/references/triage-notes/superpowers-writing-skills.md).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native Skill tool + Read/Write/Edit.
- Known limitation: one-shot snapshot at Superpowers `v4.0.3` — re-syncs require a new Task per ADR-0011 D.9.
