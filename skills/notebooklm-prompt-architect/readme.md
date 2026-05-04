# notebooklm-prompt-architect

## What
>- Use when designing custom-instruction prompts, source-pack governance, or full production specs for NotebookLM Audio Overviews / Deep Dive podcasts — especially "pitch podcast" use cases that demand narrative arc, dramatic tension (Spannung), adversarial host dynamics, and long-form duration. Produces 10,000-character persona prompts, Markdown governance source files (_rules.md, _governance.md, _dosanddonts.md, _phonetic-glossary.md), Hero's-Journey pitch scripts, and German variants. Triggers on: NotebookLM, Audio Overview, Deep Dive, pitch podcast, podcast persona, custom instructions, 10000 character prompt, Spannung, Hörbuch generieren, Investorenpitch als Podcast, suspense audio, adversarial hosts, Hero's Journey podcast, source pack governance, _rules.md injection, Murf, ElevenLabs export. Also use to override NotebookLM's default banter, force long-form output beyond the ~15-minute cap, eliminate pronunciation artifacts, or stage research documents into a coherent narrative pitch.

## Why here
Snapshot of the user-skill `/mnt/skills/user/notebooklm-prompt-architect/` from a Claude.ai
session (taken 2026-05-04). Version-controlled here so that other agents
(Claude Code, Jules, gemini-cli) can read, audit, and propose changes via PR.
The session-side copy under `/mnt/skills/user/` remains the live runtime
"upstream" until a sync-back protocol is defined.

## Top-level navigation
- [SKILL.md](./SKILL.md)
- [artifact-mitigation.md](./artifact-mitigation.md)
- [assets/](./assets/)
- [duration-control.md](./duration-control.md)
- [german-localization.md](./german-localization.md)
- [narrative-frameworks.md](./narrative-frameworks.md)
- [persona-architecture.md](./persona-architecture.md)
- [persona-templates.md](./persona-templates.md)
- [source-architecture.md](./source-architecture.md)
- [spannung-engineering.md](./spannung-engineering.md)

## Assumptions Log
- Skill-internal subfolders (e.g. `references/`, `scripts/`, `agents/`) are
  NOT given their own `readme.md`. Rationale: skills are governed by `SKILL.md`
  and Anthropic's skill-creator conventions; adding per-subfolder readmes would
  trigger "Structural Bloat" per `FRUSTRATED.md` (FL2 special-trigger). This
  drift is logged once here and once globally in the PR Frustration Log.
- The `name` and `description` shown above are extracted verbatim from
  `SKILL.md` YAML frontmatter; if the skill is updated in `/mnt/skills/user/`,
  this readme drifts until the next snapshot run.
