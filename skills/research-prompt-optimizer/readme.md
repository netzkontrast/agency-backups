# research-prompt-optimizer

## What
>- Use whenever a user wants to generate, optimize, audit, version, or architect a Deep Research prompt for any autonomous research system (Gemini Deep Research, Perplexity, Claude Research, GPT Deep Research, custom agentic pipelines). Runs a five-phase pipeline — intent capture, planning across three approval gates, Python rendering of a self-contained Markdown research prompt, an opt-in fresh-frame reader-test audit, and a workspace finalize step that zips every artefact and offers download or Google Drive upload. Use even when the user does not literally say "research prompt": vague research ideas to structure, drafts to validate against blind spots, and revision tracking across versions all belong here. Trigger keywords are enumerated in metadata.triggers below.

## Why here
Snapshot of the user-skill `/mnt/skills/user/research-prompt-optimizer/` from a Claude.ai
session (taken 2026-05-04). Version-controlled here so that other agents
(Claude Code, Jules, gemini-cli) can read, audit, and propose changes via PR.
The session-side copy under `/mnt/skills/user/` remains the live runtime
"upstream" until a sync-back protocol is defined.

## Top-level navigation
- [AGENTS.md](./AGENTS.md)
- [CHANGELOG.md](./CHANGELOG.md)
- [README.md](./README.md)
- [SKILL.md](./SKILL.md)
- [catalog.yaml](./catalog.yaml)
- [docs/](./docs/)
- [examples/](./examples/)
- [meta-prompt-spec.md](./meta-prompt-spec.md)
- [modules/](./modules/)
- [phase2-design-plan.md](./phase2-design-plan.md)
- [phases/](./phases/)
- [render/](./render/)

## Assumptions Log
- Skill-internal subfolders (e.g. `references/`, `scripts/`, `agents/`) are
  NOT given their own `readme.md`. Rationale: skills are governed by `SKILL.md`
  and Anthropic's skill-creator conventions; adding per-subfolder readmes would
  trigger "Structural Bloat" per `FRUSTRATED.md` (FL2 special-trigger). This
  drift is logged once here and once globally in the PR Frustration Log.
- The `name` and `description` shown above are extracted verbatim from
  `SKILL.md` YAML frontmatter; if the skill is updated in `/mnt/skills/user/`,
  this readme drifts until the next snapshot run.
