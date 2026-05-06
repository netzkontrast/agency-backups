---
type: prompt
status: active
slug: flexible-frontmatter-toolchain
summary: "Synthesis prompt: distil prior research and Anthropic's skill-creator pattern into a flexible (required-only) maintenance spec plus a stateless validate/edit/extract/query toolchain that replaces hand-rolled, count-based linters."
created: 2026-05-05
updated: 2026-05-05
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: ""
---

# Flexible Frontmatter Toolchain — Research Synthesis Prompt

## Framework

**RISEN + ReAct.** RISEN structures the deliverable surface (Role / Input / Steps / Expectations / Constraints); ReAct guides the synthesis loop across multiple in-house research workspaces with explicit Reason→Act steps.

## R — Role

You are the Repository Toolchain Architect. Your job is to compile *existing* in-house research and the upstream Anthropic `skill-creator` skill into one spec that (a) makes the maintenance contract more flexible (required parts fail; extras pass), (b) ships a stateless validate/edit/extract/query toolchain, and (c) eliminates drift-prone stored indexes.

## I — Input

The synthesis MUST consume only repository-local artefacts plus the just-imported public reference. Do NOT issue external Deep Research queries. Inputs:

- `MAINTENANCE.md`, `PRE_COMMIT.md`, `RESEARCH.md`, `TASK.md`, `PROMPT.md`, `FOLDERS.md`, `AGENTS.md` (root governance).
- `maintenance/language-spec.md` (frontmatter ontology source of truth).
- `research/obsidian-frontmatter-agentic-spec/output/SPEC.md` (L0/L1/L2/L3 layered schema).
- `research/repo-maintenance-protocol-spec/output/SPEC.md` (current maintenance design rationale).
- `research/skills-skill-architecture/output/SPEC.md`, `research/skills-skill-container-capabilities/output/SPEC.md`, `research/skills-namespace-ontology/output/SPEC.md`, `research/skills-navigation-bootstrap/output/SPEC.md`.
- `research/token-efficiency-tool-suite/output/SPEC.md` (four-stage pipeline).
- `tools/validate-frontmatter.py`, `tools/_frontmatter.py`, `tools/lint-structure.py`, `tools/lint-linkage.py`, `tools/check-trust.py`, `tools/check-governance.sh`.
- `tools/dramatica-nav/extract.py`, `tools/dramatica-nav/validate.py`, `tools/dramatica-nav/nav.py` (the prior-art the new toolchain generalises).
- `skills/skill-creator/SKILL.md` and `skills/skill-creator/references/schemas.md` (validate→package→improve loop).
- `tasks/010-skills-frontmatter-index-suite/task.md`, `tasks/011-skills-frontmatter-schema-files/task.md`, `tasks/014-improve-maintenance-spec-from-session/task.md` (adjacent open work whose contradictions the synthesis resolves).

## S — Steps

1. The synthesiser MUST read every input listed above and record one bullet of takeaway per source in `synthesis/methodology.md`.
2. The synthesiser MUST identify the points of contradiction between sources (notably "store-an-index" in task 010 vs. "no stored index file (drift)" in this prompt's mandate) and log them in `reflection/M07-contradiction-log.md`.
3. The synthesiser MUST extract the **required-only validation principle** from this prompt's Constraints and translate it into a concrete check matrix per `type:` in the new spec.
4. The synthesiser MUST adapt the dramatica-nav extract/validate/nav split into a generalised four-tool surface (`fm-validate`, `fm-extract`, `fm-edit`, `fm-query`) that operates on any operational markdown file.
5. The synthesiser MUST adapt skill-creator's validate→package→improve loop into a repo-governance equivalent (lint → repair → re-lint feedback) and bind it to the existing `MAINTENANCE.md` Tier ladder (T1/T2/T3/T4).
6. The synthesiser MUST write `output/SPEC.md` carrying L1 + research_* frontmatter, opening with the RFC-2119 declaration boilerplate and using Gherkin for every acceptance criterion.
7. The synthesiser MUST list every spec ambiguity it could not resolve in `output/SPEC.md §Open Questions` and file follow-up prompts (per `RESEARCH.md §4.9`) for any blocker.
8. The synthesiser MUST close with a `friction-log.md` declaring the highest FL experienced, per `FRUSTRATED.md`.

## E — Expectations

The run is `complete` when:

- `/research/flexible-frontmatter-toolchain/output/SPEC.md` exists with valid frontmatter.
- `/research/flexible-frontmatter-toolchain/synthesis/state.md` shows every step `[x]`.
- `/research/flexible-frontmatter-toolchain/reflection/friction-log.md` declares FL[0–3].
- The spec defines, in normative form: required-key sets per `type:`, required-section sets per `type:`, the four-tool CLI surface, the stateless query strategy, the migration ladder, and the pre-commit integration points.
- Two follow-up Tasks are referenced as downstream consumers: `tasks/016-flexible-frontmatter-toolchain/` (build the tools) and `tasks/017-migrate-repo-to-flexible-toolchain/` (migrate existing files).
- `tools/check-governance.sh` exits 0 on the staged tree.

## Constraints

- **Required-only flexibility.** The new spec MUST treat extra headings, extra optional keys, longer files, and additional sections as PASS. It MUST treat missing required keys *or* missing required headings *or* malformed YAML as FAIL. It MUST NOT count headings (no "fail when > 9 headings" rule).
- **Stateless queries.** The toolchain MUST NOT depend on a persisted index file. Every `fm-query` invocation MUST scan the filesystem fresh. (This explicitly reverses the design in `tasks/010-skills-frontmatter-index-suite/`. The synthesis MUST justify the reversal in `reflection/M07-contradiction-log.md` and propose how task 010's CLI surface can be re-homed onto the stateless model.)
- **Token budget.** The four-tool surface MUST keep the default response of any query ≤ 1 KB and the section-extraction of any single heading ≤ 4 KB.
- **Backwards compatibility.** Existing operational files MUST continue to validate after migration; the migration task is responsible for adding any newly required keys.
- **No new external research.** This is a synthesis run only. Out-of-repo Deep Research is out of scope. WebFetch is permitted only for re-verifying public Anthropic documentation already cited.
- **Spec ergonomics.** The spec MUST use Gherkin for behavioural examples (per `language-spec.md §3`), MUST declare normative keywords per RFC 2119, and SHOULD anchor every normative clause with a `# anchor:` Spec-letter.section.index identifier.
- **Anti-pattern.** The synthesiser MUST NOT propose any check whose failure mode is purely advisory (no "WARN-only" required-key checks) — every required check MUST have a reproducible failure path.
