# gdrive-notion-curator

## What
>- MCP-driven Drive-zu-Notion Curator. Vier Operations: setup (komplett-Listing Source-Folder paginated, alle Files verarbeiten, DBs initial anlegen), routine (incremental, filter createdTime gt newest_in_last_run, cap 50 ASC, Status-Report bei Backlog), review-inbox (askuser-driven, on-demand), repair (komplett-Listing /curated/ paginated, diff gegen Notion). Kopiert Drive-Files EINMAL nach /Claude/curated/ flach, klassifiziert via Title plus Content gegen Topics-DB, indexiert klassifizierte Files als Sub-Pages mit Auszug, schickt unklare Klassifikationen in Inbox-DB. Notion ist State-Source. Sensitive Topics werden NICHT inhaltlich gelesen. Trigger bei drive aufräumen, drive sortieren, drive curate, kuratiere meine docs, neue docs einsortieren, drive cleanup, repair drive notion, drive scan, drive routine, drive sweep, files in topic einsortieren auch ohne explizites skill-Wort. v0.4.0 nutzt Drive-MCP plus Notion-MCP.

## Why here
Snapshot of the user-skill `/mnt/skills/user/gdrive-notion-curator/` from a Claude.ai
session (taken 2026-05-04). Version-controlled here so that other agents
(Claude Code, Jules, gemini-cli) can read, audit, and propose changes via PR.
The session-side copy under `/mnt/skills/user/` remains the live runtime
"upstream" until a sync-back protocol is defined.

## Top-level navigation
- [README.md](./README.md)
- [SKILL.md](./SKILL.md)
- [assets/](./assets/)
- [references/](./references/)
- [scripts/](./scripts/)

## Assumptions Log
- Skill-internal subfolders (e.g. `references/`, `scripts/`, `agents/`) are
  NOT given their own `readme.md`. Rationale: skills are governed by `SKILL.md`
  and Anthropic's skill-creator conventions; adding per-subfolder readmes would
  trigger "Structural Bloat" per `FRUSTRATED.md` (FL2 special-trigger). This
  drift is logged once here and once globally in the PR Frustration Log.
- The `name` and `description` shown above are extracted verbatim from
  `SKILL.md` YAML frontmatter; if the skill is updated in `/mnt/skills/user/`,
  this readme drifts until the next snapshot run.
