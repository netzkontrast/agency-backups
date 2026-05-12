---
name: superpowers-using-superpowers
description: >-
  Meta-skill — when to invoke which Superpowers skill, ordering, and avoiding rationalisation. Rewritten for Agency's Skill-tool semantics; no SessionStart-injection (D.7).
skill_kind: meta
skill_target_agents: [claude-code]
skill_references_skills: [superpowers-tdd, superpowers-systematic-debugging, superpowers-verification-before-completion]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superpowers@v4.0.3"
---

# superpowers-using-superpowers (imported from Superpowers v4.0.3, adapted per ADR-0011 D.7)

## What

Imported meta-skill from the Superpowers corpus, rewritten for Agency. The upstream framework injected its meta-discipline at SessionStart (via `hooks/session-start.sh`). ADR-0011 D.7 prohibits SessionStart injection; **Agency surfaces this discipline via the Skill tool** (`/superpowers-using-superpowers`) — user-invocable only, never auto-loaded.

## When to use

Fire when about to start a substantial development task and you want to confirm you have the right discipline gates loaded. Especially useful before: a complex debug session (→ load `superpowers-systematic-debugging`), a bug fix (→ load `superpowers-tdd`), or a "complete" claim (→ load `superpowers-verification-before-completion`).

## How to use

1. Restate the task you're about to start in one sentence.
2. Identify which discipline gate applies. Use the table below:

   | Task shape | Discipline to fire |
   |---|---|
   | Implementing a feature / fix | `superpowers-tdd` |
   | Debugging an unclear failure | `superpowers-systematic-debugging` |
   | About to claim "done" | `superpowers-verification-before-completion` |
   | Receiving review feedback | `superpowers-receiving-code-review` |
   | Closing a branch | `superpowers-finishing-a-branch` |
   | Long-horizon multi-step work | `superpowers-executing-plans` + `superpowers-writing-plans` |
   | Parallel independent subtasks | `superpowers-dispatching-parallel-agents` |

3. **Resist rationalisation.** "It's a small change so TDD doesn't apply" is the classic failure mode — the discipline gates exist for the cases where the agent feels they don't.
4. Cite the chosen discipline in the friction-log so future audits can trace decisions.

## Adaptations from upstream

- **D.7 strip:** removed all "loaded at SessionStart" framing. Skill is user-invocable via the Skill tool.
- **Skill-tool wiring:** replaced upstream "read SUPERPOWERS.md first" instruction with Agency's Skill tool lookup.

Full upstream specification at `references/upstream-superpowers-using-superpowers.md`.

## References

- Upstream verbatim mirror: [`references/upstream-superpowers-using-superpowers.md`](./references/upstream-superpowers-using-superpowers.md) (Superpowers `skills/using-superpowers/SKILL.md` @ SHA `b9e16498`, v4.0.3).
- Triage rationale: [`tasks/092-…/references/triage-notes/superpowers-using-superpowers.md`](../../tasks/092-port-skill-corpora-phase-2/references/triage-notes/superpowers-using-superpowers.md).
- D.7 enforcement context: [`tasks/092-…/references/triage-notes/superpowers-hooks-skip.md`](../../tasks/092-port-skill-corpora-phase-2/references/triage-notes/superpowers-hooks-skip.md).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native Skill tool only.
- Known limitation: one-shot snapshot at Superpowers `v4.0.3` — re-syncs require a new Task per ADR-0011 D.9.
