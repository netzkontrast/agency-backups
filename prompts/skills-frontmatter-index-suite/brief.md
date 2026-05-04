# Brief — Skills Frontmatter Index & Tool Suite

## Raw user request

> Look for tools you can use to index all md files. Add another Task that describes an Overall Tool Suite for the repo and the skills-skill bootstrap, that maintains and uses an Index of all frontmatter data so the Tools can help Navigation better.

## Target audience

Whichever agent (Claude Code, Jules, or Gemini) picks up Task 010 from `/tasks/010-skills-frontmatter-index-suite/`.

## Intended model / agent

Claude Code is the natural executor (this is filesystem-heavy implementation work that benefits from the Edit/Bash toolset). Jules can run the same prompt in its sandbox.

## Use-case context

Today, an agent's only navigation surface for `/skills/` is the 5.7 KB `skills/readme.md` index plus full-file SKILL.md reads. The proposed `SKILLS.md §B.5` mandates a manifest-first read pattern, but no tool produces the manifest. This prompt drives the build of the indexer + query CLI + manifest generator that makes the rule operational.
