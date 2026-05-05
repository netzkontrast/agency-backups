# Snapshot — flexible-frontmatter-toolchain prompt (run-start)

This file is an immutable snapshot of `/prompts/flexible-frontmatter-toolchain/prompt.md` at the moment the run started, per `RESEARCH.md §4 step 3`. The canonical, evolving prompt is the `/prompts/` copy.

---

(See [`../../../prompts/flexible-frontmatter-toolchain/prompt.md`](../../prompts/flexible-frontmatter-toolchain/prompt.md). Frontmatter is intentionally omitted from this snapshot to avoid implying a second authoritative file under `/research/`. The body below mirrors the run-start contents.)

## Framework

RISEN + ReAct.

## R — Role

Repository Toolchain Architect.

## I — Input

Repository-local artefacts only: root governance specs, prior-research SPECs (obsidian-frontmatter, repo-maintenance, skills-skill-architecture, skills-namespace-ontology, skills-navigation-bootstrap, token-efficiency-tool-suite), the `tools/` linter set, `tools/dramatica-nav/`, and the just-mirrored `skills/skill-creator/`. Plus adjacent tasks 010, 011, 014.

## S — Steps

1. Read every input and record one bullet per source in `synthesis/methodology.md`.
2. Log contradictions (most importantly: stored-index vs stateless) in `reflection/M07-contradiction-log.md`.
3. Translate the **required-only** flexibility principle into a per-`type:` check matrix.
4. Generalise dramatica-nav's split into `fm-validate / fm-extract / fm-edit / fm-query`.
5. Adapt skill-creator's validate→package→improve loop into a lint→repair→re-lint feedback for repo governance, bound to T1/T2/T3/T4.
6. Write `output/SPEC.md` with RFC-2119 boilerplate and Gherkin acceptance criteria.
7. List unresolved questions and file follow-ups per `RESEARCH.md §4.9`.
8. Close with `friction-log.md` declaring FL[0–3].

## E — Expectations

`output/SPEC.md` exists; `synthesis/state.md` is fully checked; `reflection/friction-log.md` declares an FL; tasks 016 and 017 are linked downstream; `tools/check-governance.sh` exits 0.

## Constraints

- Required-only flexibility (extras pass; missing required keys/headings fail).
- No persistent index; queries are stateless.
- Default query response ≤ 1 KB; section extraction ≤ 4 KB.
- Backwards-compatible migration.
- No new external research.
- Spec uses Gherkin + RFC-2119 + `# anchor:` IDs.
- No advisory-only required checks.
