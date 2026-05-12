---
name: superpowers-receiving-code-review
description: >-
  Technical verification discipline before implementing review feedback. Use when responding to PR review comments — do not "fix" feedback without first verifying the reviewer's claim is correct.
skill_kind: discipline
skill_target_agents: [claude-code]
skill_references_skills: [superpowers-requesting-code-review, sc-self-review]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superpowers@v4.0.3"
---

# superpowers-receiving-code-review (imported from Superpowers v4.0.3)

## What

Imported discipline from the Superpowers corpus. Counterweight to the impulse to "just fix" every review comment without thinking. The skill forces a technical-verification step: is the reviewer's claim actually correct? Sometimes it isn't.

## When to use

Fire when a reviewer leaves a comment that suggests a change. Especially: comments that propose architectural changes, comments that claim a bug exists, comments that suggest a "better" idiom. Do not skip this for "obvious" comments — performative agreement is the failure mode this skill prevents.

## How to use

1. Read the comment carefully. Restate it in your own words.
2. Ask: **is the reviewer's claim verifiably correct?** Reach for evidence: re-read the code, run the failing test the reviewer cited, check the docs.
3. Three outcomes:
   - **Correct + agreed:** make the change; thank the reviewer.
   - **Correct + disagreed:** explain the trade-off in a reply; ask the reviewer if they still want the change after your context.
   - **Incorrect:** reply with the counter-evidence; close the thread without the change.
4. **Never** make a change just to close a thread — that creates technical debt and trains reviewers to leave low-quality comments.

Full behavioural specification at `references/upstream-superpowers-receiving-code-review.md`.

## References

- Upstream verbatim mirror: [`references/upstream-superpowers-receiving-code-review.md`](./references/upstream-superpowers-receiving-code-review.md) (Superpowers `skills/receiving-code-review/SKILL.md` @ SHA `b9e16498`, v4.0.3).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native tools only.
- Known limitation: one-shot snapshot at Superpowers `v4.0.3` — re-syncs require a new Task per ADR-0011 D.9.
