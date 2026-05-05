---
type: index
status: active
slug: flexible-frontmatter-toolchain
summary: "Prompt folder for the synthesis run that produces /research/flexible-frontmatter-toolchain/. The prompt is research-proposal kind; downstream tasks 016 and 017 consume the SPEC."
created: 2026-05-05
updated: 2026-05-05
---

# /prompts/flexible-frontmatter-toolchain/

**What is this folder?** Holds the synthesis prompt that produces a new Maintenance + Frontmatter Toolchain SPEC.

**Why is it here?** Per `PROMPT.md`, every research workspace has a corresponding `/prompts/<slug>/`. The same slug names the workspace at `/research/flexible-frontmatter-toolchain/`.

## Contents

- [`prompt.md`](./prompt.md) — RISEN+ReAct synthesis prompt with full RISEN structure, RFC-2119-normative steps, and a no-external-research constraint.

## Downstream Consumers

- Implementation: [`/tasks/016-flexible-frontmatter-toolchain/`](../../tasks/016-flexible-frontmatter-toolchain/) — build the four-tool CLI surface.
- Migration: [`/tasks/017-migrate-repo-to-flexible-toolchain/`](../../tasks/017-migrate-repo-to-flexible-toolchain/) — migrate existing files.
