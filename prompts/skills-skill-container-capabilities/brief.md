# Brief: claude.ai Container Capabilities

## Source

Follow-up question from `research/skills-skill-architecture/`. Resolves UNCERTAIN markers U1 (is `git` available in the claude.ai container?) and U2 (does the filesystem persist across sessions?).

## Question

What tools, runtimes, and filesystem behaviour does the claude.ai session container expose to a `SKILL.md` stub trying to bootstrap a git-backed skill loader?

## Why it's blocked

The `skills-skill` architecture spec at `research/skills-skill-architecture/output/SPEC.md` cannot be finalised without empirical answers to U1 and U2.
