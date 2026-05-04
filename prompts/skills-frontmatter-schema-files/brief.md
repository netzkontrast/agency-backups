# Brief — Skill & Frontmatter Schema Files

## Raw user request

> Maybe also add some Schema files - for which Headers means what, so the Tools can extract with precision what they need to give back to an Agent.

## Target audience

Whichever agent (Claude Code, Jules, or Gemini) picks up Task 011 from `/tasks/011-skills-frontmatter-schema-files/`.

## Intended model / agent

Claude Code is a natural fit (refactoring + JSON authoring + Python edits). Jules is also viable since the work is filesystem-local and bounded.

## Use-case context

Frontmatter rules currently live in three places: prose specs (TASK.md / PROMPT.md / RESEARCH.md / proposed SKILLS.md), the hand-rolled validator (`tools/validate-frontmatter.py`), and the tribal knowledge of past task authors. A drift in any one is a silent drift across all. Equally, Markdown header semantics (e.g. "what does `## Goal` mean? Is it required?") are not formalized anywhere a machine can read. This prompt turns both contracts into JSON Schemas that tools and external agents can consume.
