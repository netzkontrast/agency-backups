---
name: superpowers-systematic-debugging
description: >-
  Four-phase root-cause investigation methodology. Use when /sc:troubleshoot triage cannot identify a failure in one pass — escalates to evidence-gather → hypothesise → test → fix.
skill_kind: discipline
skill_target_agents: [claude-code]
skill_references_skills: [sc-troubleshoot, sc-root-cause-analyst]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superpowers@v4.0.3"
---

# superpowers-systematic-debugging (imported from Superpowers v4.0.3)

## What

Imported four-phase debugging discipline from the Superpowers corpus. Forces evidence-before-hypothesis ordering on complex bugs. Counterpart to `sc-troubleshoot` (lightweight triage); escalate here when triage fails.

## When to use

Fire when:
- `sc-troubleshoot` triage did not identify the failure in one pass.
- The bug is recurring, intermittent, or spans multiple components.
- A "fix" already shipped but the symptom returned — that's a sign the previous fix was a guess.

## How to use

Run the four phases in order — **do not skip ahead**:

1. **Gather evidence.** Read logs, diffs, reproduction steps, recent changes. Do not hypothesise yet.
2. **Hypothesise.** Generate **≥ 2** candidate causes. A single hypothesis is a guess.
3. **Test.** For each hypothesis, design a falsifying observation (not a confirming one). Run it.
4. **Fix.** Only after one hypothesis survives the falsifying test, implement the fix. Verify by re-running the failing reproduction.

Full per-phase guidance + worked examples at `references/upstream-superpowers-systematic-debugging.md`.

## References

- Upstream verbatim mirror: [`references/upstream-superpowers-systematic-debugging.md`](./references/upstream-superpowers-systematic-debugging.md) (Superpowers `skills/systematic-debugging/SKILL.md` @ SHA `b9e16498`, v4.0.3).
- Escalation source: [`skills/sc-troubleshoot/SKILL.md`](../sc-troubleshoot/SKILL.md).
- Triage rationale: [`tasks/092-…/triage-notes/superpowers-discipline-cluster.md`](../../tasks/092-port-skill-corpora-phase-2/references/triage-notes/superpowers-discipline-cluster.md).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native tools only.
- Known limitation: one-shot snapshot at Superpowers `v4.0.3` — re-syncs require a new Task per ADR-0011 D.9.
