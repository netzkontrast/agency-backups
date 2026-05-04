# the-agency-system-architect

## What
>- Orchestrates the full concept-album production pipeline for "The Agency System" (Michael Schimmer's darkwave/industrial triptych — Album 1 "Together We Confide", Album 2 "Moment der Klarheit", Album 3 "Gegenüber"). Use this skill whenever the user mentions The Agency System, Manifest Protocol, a new track for the triptych, Suno generation for an Agency-album song, or asks to draft/review/prompt-engineer lyrics that must match the project's specific DNA (corporate mimicry, IFS-informed polyphony, cybernetic metaphors, 120 BPM industrial-darkwave grid). Triggers on: "Agency System", "Manifest Protocol", "new track for the album", "nächster Song Agency", "Suno prompt Agency", "Track X der Trilogie". Delegates lyric craft to the suno-lyric-writer skill; owns the project-specific conceptual, narrative, and aesthetic gate.

## Why here
Snapshot of the user-skill `/mnt/skills/user/the-agency-system-architect/` from a Claude.ai
session (taken 2026-05-04). Version-controlled here so that other agents
(Claude Code, Jules, gemini-cli) can read, audit, and propose changes via PR.
The session-side copy under `/mnt/skills/user/` remains the live runtime
"upstream" until a sync-back protocol is defined.

## Top-level navigation
- [ALBUM_STATE.example.json](./ALBUM_STATE.example.json)
- [SKILL.md](./SKILL.md)
- [master_prompt_sheet.md](./master_prompt_sheet.md)
- [narrative_bible.md](./narrative_bible.md)
- [quality_gate_audit.md](./quality_gate_audit.md)
- [sonic_branding.md](./sonic_branding.md)
- [sprachliche_abbildung.md](./sprachliche_abbildung.md)
- [state_manager.py](./state_manager.py)
- [suno_prompt_engineering.md](./suno_prompt_engineering.md)
- [the-agency-system-architect.skill](./the-agency-system-architect.skill)
- [validate_prosody.py](./validate_prosody.py)

## Assumptions Log
- Skill-internal subfolders (e.g. `references/`, `scripts/`, `agents/`) are
  NOT given their own `readme.md`. Rationale: skills are governed by `SKILL.md`
  and Anthropic's skill-creator conventions; adding per-subfolder readmes would
  trigger "Structural Bloat" per `FRUSTRATED.md` (FL2 special-trigger). This
  drift is logged once here and once globally in the PR Frustration Log.
- The `name` and `description` shown above are extracted verbatim from
  `SKILL.md` YAML frontmatter; if the skill is updated in `/mnt/skills/user/`,
  this readme drifts until the next snapshot run.
