# drive-markdown-converter

## What
>- Use when the user wants to convert Google Docs or PDFs in a Google Drive folder to Markdown and upload the results to another Drive folder — without letting file contents land in the main context window. Supports two execution modes: Artifact-Generator (interactive React UI) and Subagent-Prompt (isolated API call for pipeline integration). Triggers on: drive to markdown, convert drive files, google docs to markdown, pdf to markdown drive, drive conversion, drive batch convert, context-safe drive, drive markdown pipeline.

## Why here
Snapshot of the user-skill `/mnt/skills/user/drive-markdown-converter/` from a Claude.ai
session (taken 2026-05-04). Version-controlled here so that other agents
(Claude Code, Jules, gemini-cli) can read, audit, and propose changes via PR.
The session-side copy under `/mnt/skills/user/` remains the live runtime
"upstream" until a sync-back protocol is defined.

## Top-level navigation
- [SKILL.md](./SKILL.md)

## Assumptions Log
- Skill-internal subfolders (e.g. `references/`, `scripts/`, `agents/`) are
  NOT given their own `readme.md`. Rationale: skills are governed by `SKILL.md`
  and Anthropic's skill-creator conventions; adding per-subfolder readmes would
  trigger "Structural Bloat" per `FRUSTRATED.md` (FL2 special-trigger). This
  drift is logged once here and once globally in the PR Frustration Log.
- The `name` and `description` shown above are extracted verbatim from
  `SKILL.md` YAML frontmatter; if the skill is updated in `/mnt/skills/user/`,
  this readme drifts until the next snapshot run.
