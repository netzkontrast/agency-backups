# Brief — flexible-frontmatter-toolchain

## Raw user request

> Tool-Chain and governance Checks… we Need a new and Improved pre-Commit, and Maintenance Suite, Create a new Research Task, with help of the Research optimizer skill (Read the skill.md and follow instructions as good as possible) - then execute that Research across the repo… The goal of the Research is to Create a new Maintenance spec, that is more flexible - meaning… if a spec has more then 9 headings.. it does Not faul.. it fails if the needed Parts are Not there… then we Need a Complete Suite of frontmatter validation and Editing as well as Input extrqction Tools… Like the one we Build for dramatica… But more flexible.. The goal is to Create a spec, and a Tool, that allows to reduce Token across the Complete repo while also make things more flexible… additionally, there is no Need to Store an Index file (that can Drift)… Look at all the Research we have Done.. and compile a Synthesizer Research - then… Create a new Task, for implementing the newly defined toolchain, as well as a new Task to Migrate the repo to this Tools - Take a Look at the /skill-creator skill (copy it over into /skills Directory - from your skill-dir into the repo.. so we can work with this… and addept the Concept)

## Target audience / intended model

- Executor: Claude Code (Opus 4.7) running in this agency repository.
- Pipeline: synthesis-only research run consuming repo-local artefacts; no external Deep Research issued.

## Use-case context

- Branch: `claude/improve-precommit-suite-6KBSC`.
- Replaces the implicit "count > 9 headings = fail" pattern that would have grown into MAINTENANCE.md.
- Reverses the persisted-index strategy in `/tasks/010-skills-frontmatter-index-suite/` (see `reflection/M07-contradiction-log.md §C1`).
- Adapts the Anthropic public `skill-creator` validate→package→improve loop into repo-governance lint→repair→re-lint feedback.

## Decisions captured before drafting

- Lean synthesis only (no askuser pipeline gates).
- Required-keys-only flexibility (extras pass; missing required parts fail).
- Mirror Anthropic skill-creator into `/skills/skill-creator/` for reference.
- Produce: synthesis workspace + Task 016 (implementation) + Task 017 (migration). Do NOT build the tools in this session.
