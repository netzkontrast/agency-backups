---
name: superpowers-verification-before-completion
description: >-
  Require evidence before claiming work is done. Use at the closing edge of any implementation wave to prevent false-positive "complete" reports — every claim must be backed by a verifiable artefact.
skill_kind: discipline
skill_target_agents: [claude-code]
skill_references_skills: [sc-self-review, sc-test]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superpowers@v4.0.3"
---

# superpowers-verification-before-completion (imported from Superpowers v4.0.3)

## What

Imported discipline gate from the Superpowers corpus. Forbids claiming work "complete" without an evidence artefact: a green test run, a successful `Bash` invocation, a `Read` confirming the expected output, etc. Counterpart to `sc-self-review` — verification is the **evidence** step; self-review is the **reflexion** step.

## When to use

Fire **before** every claim of completion: PR opening, `task_status: done` flip, "the bug is fixed" statement, "tests pass" claim. The discipline is the gate; the gate is mandatory.

## How to use

1. Identify the claim about to be made (e.g. "the lint error is fixed").
2. Pick the smallest verifiable artefact that proves it (e.g. `ruff check path/` exit code).
3. Run it; capture the result.
4. Only after the artefact lands as evidence, make the claim.
5. If the artefact contradicts the intended claim, **revise the claim** — never massage the evidence.

Full behavioural specification at `references/upstream-superpowers-verification-before-completion.md`.

## References

- Upstream verbatim mirror: [`references/upstream-superpowers-verification-before-completion.md`](./references/upstream-superpowers-verification-before-completion.md) (Superpowers `skills/verification-before-completion/SKILL.md` @ SHA `b9e16498`, v4.0.3).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).
- Triage rationale: [`tasks/092-…/references/triage-notes/superpowers-discipline-cluster.md`](../../tasks/092-port-skill-corpora-phase-2/references/triage-notes/superpowers-discipline-cluster.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native tools only.
- Known limitation: one-shot snapshot at Superpowers `v4.0.3` — re-syncs require a new Task per ADR-0011 D.9.
