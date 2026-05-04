# suno-lyric-writer

## What
>- Use when writing, reviewing, or revising song lyrics for Suno AI generation. Covers the full pipeline: lyric drafting with professional prosody and rhyme craft, Suno pronunciation scanning (homographs, tech terms, proper nouns, acronyms), 14-point quality review, and complete Suno v5/v5.5 prompt engineering including Section Tags, Metatags, Vocal-Delivery Tags, Persona/Voice/Custom-Model workflows, Creative Sliders, Extend/Cover/Remaster strategies and Negative Prompting. Triggers on: write lyrics, song text, Suno track, lyric review, let's work on a track, new song, revise lyrics, lyric QC, prosody check, pronunciation scan, review my lyrics, check lyrics for Suno, songwriting, write a song, Suno prompt, style prompt, suno tags, suno voice, persona, suno extend, suno cover, suno remaster, suno sliders.

## Why here
Snapshot of the user-skill `/mnt/skills/user/suno-lyric-writer/` from a Claude.ai
session (taken 2026-05-04). Version-controlled here so that other agents
(Claude Code, Jules, gemini-cli) can read, audit, and propose changes via PR.
The session-side copy under `/mnt/skills/user/` remains the live runtime
"upstream" until a sync-back protocol is defined.

## Top-level navigation
- [SKILL.md](./SKILL.md)
- [craft-reference.md](./craft-reference.md)
- [documentary-standards.md](./documentary-standards.md)
- [examples.md](./examples.md)
- [genre-practices.md](./genre-practices.md)
- [pronunciation-guide.md](./pronunciation-guide.md)

## Assumptions Log
- Skill-internal subfolders (e.g. `references/`, `scripts/`, `agents/`) are
  NOT given their own `readme.md`. Rationale: skills are governed by `SKILL.md`
  and Anthropic's skill-creator conventions; adding per-subfolder readmes would
  trigger "Structural Bloat" per `FRUSTRATED.md` (FL2 special-trigger). This
  drift is logged once here and once globally in the PR Frustration Log.
- The `name` and `description` shown above are extracted verbatim from
  `SKILL.md` YAML frontmatter; if the skill is updated in `/mnt/skills/user/`,
  this readme drifts until the next snapshot run.
