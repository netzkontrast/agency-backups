# agency

Decoupling Machine, Actor, and Space for Long-Horizon AI Agency.

This repository is a governance + research workspace, not an application. It hosts:

- **Top-level governance specs** that bind every agent operating here:
  [`AGENTS.md`](./AGENTS.md) (entry point, frontmatter ontology, RFC 2119
  + Gherkin language binding), [`TASK.md`](./TASK.md), [`PROMPT.md`](./PROMPT.md),
  [`RESEARCH.md`](./RESEARCH.md), [`FOLDERS.md`](./FOLDERS.md),
  [`FRUSTRATED.md`](./FRUSTRATED.md), [`PRE_COMMIT.md`](./PRE_COMMIT.md),
  [`MAINTENANCE.md`](./MAINTENANCE.md).
- **Operational directories** under [`/tasks/`](./tasks/),
  [`/prompts/`](./prompts/), [`/research/`](./research/) — the audit graph
  defined by FOLDERS.md.
- **Mechanical enforcement** in [`/tools/`](./tools/): governance linters
  invoked by [`tools/check-governance.sh`](./tools/check-governance.sh) and
  the pre-commit hook.

**Start here:** [`AGENTS.md`](./AGENTS.md). Every agent MUST read it before
writing any file.
