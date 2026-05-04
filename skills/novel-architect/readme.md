# novel-architect

## What
>- Orchestrator für den deutschsprachigen Roman „Kohärenz Protokoll" (Hard-SF / Philosophical Horror, Dual-Storyform, 39 Kapitel, 13 Alters). State-Management läuft über NCP (Narrative Context Protocol v1.3.0) via ncp-author — Storyform A + B als zwei narratives, dynamics/storypoints/storybeats/moments als NCP-Entitäten. Nicht-strukturelle Canon-Daten (DKT, Prosa-Regeln, Mandate) in canon-meta.md. Lädt Workspace bei Session-Start, routet Skill-Pipeline (dramatica-theory, dramatica-vocabulary, ncp-author, memory-sync, research-prompt-optimizer, doc-coauthoring, drive-markdown-converter), packt sich nach signifikanten Schritten via skill-creator. Trigger — novel-architect, Kohärenz Protokoll, Roman Encoding, Storyweaving, Vortex, Throughline, Storyform A, Storyform B, NCP, ncp.json, Kanon, Kael, AEGIS, Juna, DKT, Kapitel-Entwurf, /analyze, /interview, /synthesize, /draft. Implizit bei Alters, Klimax, Dual-POV, Riss-Mandat, 39-Kapitel-Plan. NICHT bei Agency-System.

## Why here
Snapshot of the user-skill `/mnt/skills/user/novel-architect/` from a Claude.ai
session (taken 2026-05-04). Version-controlled here so that other agents
(Claude Code, Jules, gemini-cli) can read, audit, and propose changes via PR.
The session-side copy under `/mnt/skills/user/` remains the live runtime
"upstream" until a sync-back protocol is defined.

## Top-level navigation
- [SKILL.md](./SKILL.md)
- [commands/](./commands/)
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
