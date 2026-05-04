# dramatica-vocabulary

## What
Aktive Dramatica-Theorie für Storyform-Aufbau, Encoding und Storyweaving — kein passives Dictionary, sondern Werkzeug. Trigger explizit bei Dramatica, Storyform, Throughline, Class, Type, Variation, Element, Archetype, Dynamic Pair, MC, IC, Goal, Consequence, Cost, Dividend, Driver, Outcome, Judgment, Limit, sowie bei Archetypen-Namen Protagonist, Antagonist, Guardian, Contagonist, Sidekick, Skeptic, Reason, Emotion. Trigger proaktiv in Narrativ-Kontexten — bei novel-architect-Arbeit (Kohärenz Protokoll), Agency System Triptychon-Tracks (Album 1/2/3), Suno-Lyric-Arbeit mit klarem Charakterbogen, oder Diskussionen über Resolve (Steadfast/Change), Approach (Be-er/Do-er), Mental Sex (Linear/Holistic), Growth (Stop/Start). Liefert präzise Definitionen mit Dynamic Pairs, strukturelle Verortung in der Dramatica-Hierarchie, Encoding-Vorschläge und Konsistenz-Checks gegen die 75 Dynamic Pairs. Nicht greifen bei Hero's Journey, Save the Cat, Beat Sheets oder anderen explizit benannten Story-Modellen.

## Why here
Snapshot of the user-skill `/mnt/skills/user/dramatica-vocabulary/` from a Claude.ai
session (taken 2026-05-04). Version-controlled here so that other agents
(Claude Code, Jules, gemini-cli) can read, audit, and propose changes via PR.
The session-side copy under `/mnt/skills/user/` remains the live runtime
"upstream" until a sync-back protocol is defined.

## Top-level navigation
- [SKILL.md](./SKILL.md)
- [references/](./references/)

## Assumptions Log
- Skill-internal subfolders (e.g. `references/`, `scripts/`, `agents/`) are
  NOT given their own `readme.md`. Rationale: skills are governed by `SKILL.md`
  and Anthropic's skill-creator conventions; adding per-subfolder readmes would
  trigger "Structural Bloat" per `FRUSTRATED.md` (FL2 special-trigger). This
  drift is logged once here and once globally in the PR Frustration Log.
- The `name` and `description` shown above are extracted verbatim from
  `SKILL.md` YAML frontmatter; if the skill is updated in `/mnt/skills/user/`,
  this readme drifts until the next snapshot run.
