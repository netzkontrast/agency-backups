---
name: superpowers-finishing-a-branch
description: >-
  Structured branch-completion workflow. Use at the closing edge of a development branch to verify tests pass, then explicitly pick one of {merge, PR, discard} — never let a branch drift into limbo.
skill_kind: discipline
skill_target_agents: [claude-code]
skill_references_skills: [sc-createPR, superpowers-verification-before-completion]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superpowers@v4.0.3"
---

# superpowers-finishing-a-branch (imported from Superpowers v4.0.3)

## What

Imported branch-completion discipline from the Superpowers corpus. Three-option decision tree: **merge** (fast-forward to main), **PR** (open a review), or **discard** (delete the branch). Overlaps Agency's [AGENTS.md Closing Run Procedure](../../AGENTS.md#closing-run-procedure) (CR.1–CR.7) but adds the explicit **discard** option for branches that should not ship.

## When to use

Fire when a development branch is "done" — tests green, governance clean — and a decision is needed about its fate. Pairs with `superpowers-verification-before-completion` (verify before deciding) and `sc-createPR` (the "PR" branch of the decision tree).

## How to use

1. Confirm verification gates: tests pass, governance exits 0, no uncommitted changes.
2. Pick exactly one of:
   - **merge** — fast-forward to `main` (only when CR.1–CR.7 hold and the user authorised it).
   - **PR** — invoke `sc-createPR` to open a review.
   - **discard** — `git branch -D <name>` after confirming no unique work would be lost.
3. Record the chosen option in the friction log and any related Task's `task.md`.
4. **Never** leave a branch in limbo (no merge, no PR, no discard).

Full behavioural specification at `references/upstream-superpowers-finishing-a-branch.md`.

## References

- Upstream verbatim mirror: [`references/upstream-superpowers-finishing-a-branch.md`](./references/upstream-superpowers-finishing-a-branch.md) (Superpowers `skills/finishing-a-development-branch/SKILL.md` @ SHA `b9e16498`, v4.0.3).
- Agency anchor: [AGENTS.md § Closing Run Procedure](../../AGENTS.md#closing-run-procedure) (CR.1–CR.7).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native tools only.
- Known limitation: one-shot snapshot at Superpowers `v4.0.3` — re-syncs require a new Task per ADR-0011 D.9.
