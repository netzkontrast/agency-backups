---
name: superpowers-tdd
description: >-
  Red-Green-Refactor test-driven development discipline. Use before implementing any behavioural change — write the failing test first, watch it fail, then write the minimal code to make it pass.
skill_kind: discipline
skill_target_agents: [claude-code]
skill_references_skills: [sc-test, superpowers-verification-before-completion]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superpowers@v4.0.3"
---

# superpowers-tdd (imported from Superpowers v4.0.3)

## What

Imported Red-Green-Refactor TDD discipline from the Superpowers corpus. Differs from `sc-test` (which **runs** tests) — `superpowers-tdd` is the upstream discipline gate that says *write the test first*.

## When to use

Fire before implementing any behavioural change in code. Especially: bug fixes (the test that should have caught it), new features (the test that demonstrates the contract), refactors (the test that pins the existing behaviour before you change the implementation).

## How to use

Three phases — strictly ordered:

1. **RED.** Write the failing test. Run it. **Watch it fail** — a test that doesn't fail when expected is a bug in the test, not a passing implementation.
2. **GREEN.** Write the **minimum** code to make the test pass. Resist the urge to add structure, abstractions, or related fixes.
3. **REFACTOR.** With the test passing, restructure the code for clarity / reuse / performance. The test stays green throughout. If the test breaks during refactor, you broke the implementation, not the test.

Full per-phase guidance + worked examples at `references/upstream-superpowers-tdd.md`.

## References

- Upstream verbatim mirror: [`references/upstream-superpowers-tdd.md`](./references/upstream-superpowers-tdd.md) (Superpowers `skills/test-driven-development/SKILL.md` @ SHA `b9e16498`, v4.0.3).
- Test-execution counterpart: [`skills/sc-test/SKILL.md`](../sc-test/SKILL.md).
- Triage rationale: [`tasks/092-…/triage-notes/superpowers-discipline-cluster.md`](../../tasks/092-port-skill-corpora-phase-2/references/triage-notes/superpowers-discipline-cluster.md).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native tools only.
- Known limitation: one-shot snapshot at Superpowers `v4.0.3` — re-syncs require a new Task per ADR-0011 D.9.
