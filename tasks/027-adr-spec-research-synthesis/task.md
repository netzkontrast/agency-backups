---
type: task
status: active
slug: adr-spec-research-synthesis
summary: "Analyze root specs and tooling via /sc:analyze + /sc:brainstorm, then execute a Research run that produces the repo-native ADR governance specification integrating the Gemini draft with existing governance conventions."
created: 2026-05-05
updated: 2026-05-05
task_id: "027"
task_status: open
task_owner: "unassigned"
task_priority: P1
task_uses_prompts:
  - adr-spec-research-synthesis
task_spawns_research:
  - adr-spec-research-synthesis
task_spawns_prompts:
  - adr-tooling-impl-plan
  - adr-assumption-audit
task_supersedes: []
task_blocked_by: []
task_affects_paths:
  - research/adr-spec-research-synthesis/
  - prompts/adr-spec-research-synthesis/
  - AGENTS.md
  - RESEARCH.md
  - TASK.md
---

# Task 027 — ADR Spec Research Synthesis

## Goal

Produce the **repo-native ADR governance specification** for `netzkontrast/agency` — the canonical, enforceable document that defines how Architecture Decision Records are authored, stored, superseded, synthesized into `AGENTS.md`, and validated. The Gemini-generated draft (`research/gemini/agency-adr-governance-spec/adr-governance-spec.md`) is the theoretical foundation; this task grounds it against the actual repo structure and governance conventions, resolving every mismatch.

The task is **done** when `research/adr-spec-research-synthesis/output/SPEC.md` exists, passes `tools/check-governance.sh`, and is acknowledged by the maintainer as the authoritative ADR governance document for this repository.

Spawns Task 028 (tooling implementation plan) and Task 029 (assumption audit) upon completion.

## Context

The Gemini research (`research/gemini/agency-adr-governance-spec/adr-governance-spec.md`) established a rigorous §0–§9 ADR governance specification using MDL compression, DAG supersession, Gherkin acceptance criteria, and JSON-Schema frontmatter contracts. However, it was produced without full read access to the repo's internal files. Key gaps exist:

- The existing tooling (`tools/fm/`, `tools/check-governance.sh`) already implements some overlapping concerns.
- The Frontmatter Ontology (`maintenance/schemas/header-ontology.json`) partially defines the structural metadata that the ADR spec independently proposes.
- The branching convention (`claude/<topic>-<date>`) is already established but not formally referenced in the ADR spec.
- Root files `FRUSTRATED.md`, `MAINTENANCE.md`, and `PRE_COMMIT.md` are referenced in the Gemini spec by name but their actual content may diverge from assumptions.

## Plan

### Phase 1 — `/sc:analyze` Root Specs and Tooling

Run `/sc:analyze` across the following to extract the current governance surface:

1. Root specs: `AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `MAINTENANCE.md`, `FRUSTRATED.md`, `README.md`
2. Tooling: `tools/check-governance.sh`, `tools/fm/validate.py`, `tools/fm/edit.py`, `tools/fm/query.py`, `tools/fm/extract.py`
3. Existing schemas: `maintenance/schemas/header-ontology.json` (if present)
4. Gemini ADR draft: `research/gemini/agency-adr-governance-spec/adr-governance-spec.md`

Produce an analysis report identifying: (a) existing architectural decisions that are already implicitly in effect, (b) structural conventions the ADR spec must honour, (c) tooling hooks the synthesis pipeline can attach to.

### Phase 2 — `/sc:brainstorm` Integration Points

Run `/sc:brainstorm` with the analysis report as input. Brainstorm:

1. Where does `docs/decisions/` fit relative to `research/` and `tasks/`?
2. How does the `agency-adr synthesize` pipeline attach to `PRE_COMMIT.md` hooks without conflicting with `tools/check-governance.sh`?
3. How does the ADR frontmatter schema (`id`, `title`, `status`, `date`, `supersedes`) compose with the existing L1/L2 Vault Core Frontmatter Ontology?
4. What is the migration path for decisions already implicitly embedded in root specs (e.g., MADR-style structural choices baked into `TASK.md`)?
5. How does `AGENTS.md` synthesis interact with the existing manual `AGENTS.md` content?

### Phase 3 — Execute Research Run

Execute the `adr-spec-research-synthesis` prompt as a full Research run. The research workspace (`research/adr-spec-research-synthesis/`) MUST follow `RESEARCH.md` structure. The output deliverable is `research/adr-spec-research-synthesis/output/SPEC.md`.

The SPEC.md MUST:
- Follow the §0–§9 schema from the Gemini draft, adjusted for repo-specific reality
- Declare the canonical `docs/decisions/` path (or a justified alternative)
- Define the complete JSON-Schema for ADR frontmatter, composing with the L1/L2 ontology
- Specify the CLI shape for `agency-adr validate` and `agency-adr synthesize`
- Include Gherkin acceptance criteria for every MUST statement
- Resolve all mismatches identified in Phase 1 and integration points from Phase 2

### Phase 4 — Governance Verification and Spawn

1. Run `tools/check-governance.sh` against all new files; resolve any failures.
2. Mark this task `done`.
3. Spawn Task 028 (`028-adr-tooling-impl-plan`) for implementation planning.
4. Spawn Task 029 (`029-adr-assumption-audit`) for the critical-thinking assumption audit.

## Todo

- [ ] 1. Run `/sc:analyze` across all root specs and tooling listed in Phase 1.
- [ ] 2. Produce analysis report in `research/adr-spec-research-synthesis/workspace/analysis.md`.
- [ ] 3. Run `/sc:brainstorm` on the five integration questions in Phase 2.
- [ ] 4. Record brainstorm output in `research/adr-spec-research-synthesis/workspace/brainstorm.md`.
- [ ] 5. Execute `adr-spec-research-synthesis` prompt as a Research run.
- [ ] 6. Produce `research/adr-spec-research-synthesis/output/SPEC.md`.
- [ ] 7. Run `tools/check-governance.sh`; fix any failures.
- [ ] 8. Set `task_status: done`.
- [ ] 9. Confirm Task 028 and Task 029 are created and set to `open`.

## Links

- ADR Governance draft: [`research/gemini/agency-adr-governance-spec/adr-governance-spec.md`](../../research/gemini/agency-adr-governance-spec/adr-governance-spec.md)
- Originating research prompt: [`research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md`](../../research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md)
- Executing prompt: [`prompts/adr-spec-research-synthesis/prompt.md`](../../prompts/adr-spec-research-synthesis/prompt.md)
- Spawns: [`028-adr-tooling-impl-plan/task.md`](../028-adr-tooling-impl-plan/task.md), [`029-adr-assumption-audit/task.md`](../029-adr-assumption-audit/task.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`RESEARCH.md`](../../RESEARCH.md), [`PROMPT.md`](../../PROMPT.md), [`AGENTS.md`](../../AGENTS.md)
