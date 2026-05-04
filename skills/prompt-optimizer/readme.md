# prompt-optimizer

## What
>- Use at the START of EVERY conversation, before processing any user request. ALWAYS activates on the first message in any conversation — no exceptions. Intercepts the user's initial prompt, selects the optimal framework from the 27-framework catalog, optimizes the prompt with full analysis, then executes. Triggers on: every initial prompt, first message, conversation start, improve prompt, optimize prompt, better prompt, rewrite prompt.

## Why here
Snapshot of the user-skill `/mnt/skills/user/prompt-optimizer/` from a Claude.ai
session (taken 2026-05-04). Version-controlled here so that other agents
(Claude Code, Jules, gemini-cli) can read, audit, and propose changes via PR.
The session-side copy under `/mnt/skills/user/` remains the live runtime
"upstream" until a sync-back protocol is defined.

## Top-level navigation
- [SKILL.md](./SKILL.md)
- [anti-patterns.md](./anti-patterns.md)
- [clarification-questions.md](./clarification-questions.md)
- [examples.md](./examples.md)
- [framework-components.md](./framework-components.md)
- [intent-framework-map.md](./intent-framework-map.md)
- [output-format.md](./output-format.md)
- [selection.md](./selection.md)
- [templates.md](./templates.md)

## Assumptions Log
- Skill-internal subfolders (e.g. `references/`, `scripts/`, `agents/`) are
  NOT given their own `readme.md`. Rationale: skills are governed by `SKILL.md`
  and Anthropic's skill-creator conventions; adding per-subfolder readmes would
  trigger "Structural Bloat" per `FRUSTRATED.md` (FL2 special-trigger). This
  drift is logged once here and once globally in the PR Frustration Log.
- The `name` and `description` shown above are extracted verbatim from
  `SKILL.md` YAML frontmatter; if the skill is updated in `/mnt/skills/user/`,
  this readme drifts until the next snapshot run.
