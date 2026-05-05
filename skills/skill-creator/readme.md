---
type: index
status: active
slug: skill-creator
summary: "Mirror of Anthropic's public skill-creator skill (github.com/anthropics/skills/skills/skill-creator). Used as a reference pattern for the validate → package → improve loop adapted by tasks 016/017."
created: 2026-05-05
updated: 2026-05-05
---

# /skills/skill-creator/ (mirror)

**What is this folder?** A verbatim mirror of [anthropics/skills · skills/skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) at the time of import (2026-05-05). Source of truth remains upstream; this mirror exists so in-house tooling can adapt the pattern without round-tripping the network.

**Why is it here?** The `flexible-frontmatter-toolchain` research synthesises the **validate → package → improve** loop expressed by skill-creator into a generalised toolchain for repo governance. Keeping a local copy lets us reference exact line numbers from the spec and from tasks 016/017.

## Contents

- [`SKILL.md`](./SKILL.md) — Authoring + iteration loop spec.
- [`LICENSE.txt`](./LICENSE.txt) — Upstream licence; preserved verbatim.
- [`references/schemas.md`](./references/schemas.md) — JSON shapes for evals / grading / benchmarks.
- [`scripts/`](./scripts/) — Nine Python scripts: `quick_validate.py`, `package_skill.py`, `aggregate_benchmark.py`, `generate_report.py`, `improve_description.py`, `run_eval.py`, `run_loop.py`, `utils.py`, `__init__.py`.
- [`agents/`](./agents/) — Three sub-agent prompts: `analyzer.md`, `comparator.md`, `grader.md`.
- [`assets/eval_review.html`](./assets/eval_review.html) — HTML eval-set reviewer.

## Reuse Notes

- The pattern we adopt: `quick_validate.py` is a good model for our `tools/validate-frontmatter.py` refactor — short, schema-driven, and emits one diagnostic per problem.
- `package_skill.py` informs the migration tooling in task 017 (idempotent re-pack of governance metadata).
- The grader/analyzer agents are *not* reused directly; they inform the friction-log + run-log feedback loop in `MAINTENANCE.md`.

## Sync Discipline

This mirror MUST NOT be hand-edited. To refresh, rerun the import (URLs in the parent task's `friction-log.md`) or set up an upstream sync in [`/skills/skills-skill-bootstrap/`](../skills-skill-bootstrap/).
