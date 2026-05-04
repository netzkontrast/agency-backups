# Brief — Author Skills Root Spec

## Raw user request

> Create a Task Workflow with corresponding Research, but Not execute them. End goal: a new SKILL.md root spec governing /skills/ — detailing how skills should be used, what tools should exist, what that means for AGENTS.md and every workflow in the repo, and how the skills-skill bootstrap should work (clone latest skills into the workspace + token-efficient instructions on using the tools within the skills directory). Make those skills reference each other.

## Target audience

Whichever agent (Claude Code, Jules, or Gemini) picks up Task 009 from `/tasks/009-author-skills-root-spec/`.

## Intended model / agent

Claude Code or Jules. The prompt is RISEN-shaped (no live tool execution required); a Gemini Deep Research run could also produce a defensible draft.

## Use-case context

`/skills/` is the only top-level operational concern in this repo without a root governance file. `AGENTS.md` routes skill-authoring requests nowhere. The 14 skills currently in the tree do not carry the L1+L2 frontmatter the rest of the repo demands; they have not yet been brought under the linter. Authoring `SKILLS.md` is a prerequisite for Tasks 010 and 011 to operate against an explicit contract instead of inferred conventions.
