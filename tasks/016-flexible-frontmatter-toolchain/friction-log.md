---
type: note
status: active
slug: task-016-friction-log
summary: "FL declaration for Task 016 (flexible-frontmatter-toolchain). FL1 — task scope was clear and the SPEC was actionable; one small inconsistency between SPEC §3.4 prose and §6.1 example was caught and documented."
created: 2026-05-05
updated: 2026-05-05
---

# Friction Log — Task 016

## Frustration Level: FL1

**Reasoning.** The work was well-scoped (the SPEC at
`/research/flexible-frontmatter-toolchain/output/SPEC.md` enumerated
exactly what to build) and the existing `tools/_frontmatter.py` plus
`tools/dramatica-nav/` provided strong prior art for the diagnostic
shape. The implementation, tests, and CI wiring fit a single session.

The single FL1-grade friction was an internal inconsistency in the
SPEC: §3.4 says "Levenshtein-distance 1" but the §6.1 acceptance
example (`tpye` → `type`) is *Damerau*-Levenshtein 1, not standard
Levenshtein 1. Resolved in the implementation by using OSA distance
(transposition-aware); documented in `notes.md` for Task 017 to fold
into a SPEC amendment.

## Specific frictions encountered

1. **SPEC vs. live tree mismatch on skills.** §3.2 lists
   `skill_kind, skill_target_agents` as required for `type=skill`,
   but no live SKILL.md carries those keys (Anthropic's format uses
   `name` + `description`). §6.1 expects `name` to be the required
   key. The header-ontology JSON encodes `name`/`description` as
   REQUIRED and the skill_* keys as RECOMMENDED. Task 017 needs to
   pick one canonical interpretation in a SPEC amendment.

2. **Heading normalisation under-specified.** §4.2 only commits to
   "stripping em-dashes and surrounding whitespace". The §4.2 example
   (`## Goal:` ↔ `## Goal`) implies trailing colons strip too. The
   implementation strips trailing `:`, `—`, `–`, `-`, and whitespace.
   This is a reasonable extension but should be locked into the SPEC
   wording.

3. **fnmatch vs. regex in the path-classification table.** First
   draft of `header-ontology.json` used `[0-9]{3}` (regex character
   class) which `fnmatch` doesn't understand — patterns silently
   matched nothing. Replaced with `[0-9][0-9][0-9]`. Worth noting
   for future authors of similar JSON-driven matchers.

## Suggested follow-ups (Task 017 territory)

- Migrate prompt.md files to drop parenthetical heading hints
  (`## I — Input (to flesh out)` → `## I — Input`).
- Add frontmatter to `research/<slug>/{workspace,reflection,
  synthesis,output}/readme.md` files, OR narrow the scope of files
  fm-validate considers operational.
- Resolve the `skill_kind/skill_target_agents` vs `name/description`
  question in a SPEC amendment.
- Flip `FM_TOOLCHAIN=1` as the default in `tools/check-governance.sh`
  once the migration backlog is empty.
