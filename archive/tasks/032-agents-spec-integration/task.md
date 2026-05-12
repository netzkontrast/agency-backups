---
type: task
status: archived
slug: agents-spec-integration
summary: "Integrate underused research findings (adr-assumption-audit ASM-001/004/005/009, skills-skill-container-capabilities U1-U2, gemini theoretical-foundation, ncp-novel-co-authoring) into AGENTS.md, mechanically enforce NO.5 narrative-ontology load discipline, and close the §60-65 assumption-log substance gap."
created: 2026-05-06
updated: 2026-05-12
task_id: "032"
task_status: archived
task_owner: "claude-opus-4-7"
task_priority: P2
task_uses_prompts:
  - research-adr-corpus-extraction
  - tooling-narrative-ontology-load-discipline
  - tooling-rfc2119-polarity-audit
  - tooling-assumption-log-substance
  - spec-amendment-agents-md
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - AGENTS.md
  - decisions/
  - tools/check-narrative-ontology-load.py
  - tools/check-rfc2119-polarity.py
  - tools/check-assumption-log.py
---

# Task 032 — AGENTS.md Spec Integration

## Goal

Bring AGENTS.md into alignment with three completed-but-under-cited research outputs and close one acknowledged enforcement gap, **while strictly respecting the `<!-- BEGIN AGENCY-ADR SYNTHESIS -->` / `<!-- END AGENCY-ADR SYNTHESIS -->` guarded section** introduced by Task 031 at `AGENTS.md:339-342`. All edits MUST land outside those markers, OR be authored as new ADR files in `/decisions/<NNNN>-<slug>.md` that the synthesizer (`tools/adr/cli.py synthesize`) auto-merges into the guarded block.

The Task is `done` when (a) AGENTS.md carries a `§0 Theoretical Foundations` cross-reference to `research/gemini/agency-adr-governance-spec/` (outside the guarded markers), (b) §3.3 RFC-2119 declaration carries a polarity-inversion footnote citing `research/adr-assumption-audit/output/REPORT.md §1`, (c) §6 (Skills Architecture) documents the `git unavailable / filesystem stateless` operational constraints from `research/skills-skill-container-capabilities/output/SPEC.md`, (d) NO.5 narrative-ontology load discipline is enforced by a new linter, (e) §60–65 assumption-log substance is mechanically validated, **and (f) `tools/adr/cli.py validate` exits 0 against the post-edit AGENTS.md (so the guarded markers stay intact and `ADR.A.3.5` does not fire)**.

## Context

Per the spec-corpus audit produced in this branch (and refreshed against `origin/main` after Task 031 landed), AGENTS.md has four under-utilized integration points:

1. **adr-assumption-audit** (`research/adr-assumption-audit/output/REPORT.md §1`) surfaces 4 HIGH-blast hidden assumptions affecting the now-LIVE ADR synthesis pipeline (ASM-001 polarity-inversion, ASM-004 marker-check insufficiency, ASM-005 pre-commit bypassability, ASM-009 silent MADR-body truncation). With Task 031 deployed, these are no longer theoretical — `tools/adr/synthesize.py` actively rewrites the guarded section, and an ASM-001 polarity inversion would silently invert governance. The ST-3 RFC-2119 polarity linter is now urgent rather than speculative.
2. **skills-skill-container-capabilities** (`research/skills-skill-container-capabilities/output/SPEC.md`) resolved U1 (no `git` binary in claude.ai container) and U2 (no filesystem persistence). AGENTS.md §6 still describes the skill loader as if `git clone` is available.
3. **gemini agency-adr-governance-spec** is the theoretical foundation for the MDL-compression / supersession-DAG paradigm but is uncited in AGENTS.md §0. With Task 031 implementing exactly that paradigm via `tools/adr/compress.py` + `tools/adr/graph.py`, citing the theoretical anchor closes a provenance gap.
4. **ncp-novel-co-authoring-spec** defines the citation-reproducibility protocol (`path/to/file.ext:Lstart-Lend@<sha>`) used during novel co-authoring; AGENTS.md §6 does not reference it.

Plus two enforcement gaps:

- NO.5 (§251) — "An agent doing non-narrative work MUST NOT load the Narrative Ontology" — no linter enforces this; agents waste tokens loading the 215-entry ontology.
- §60–65 — assumption-log requirement is normative but readme.md `## Assumptions Log` substance is never mechanically validated.

## Build-On Opportunity (post-Task-031)

ST-1 (ADR corpus extraction) becomes a **build-on**, not invent-from-scratch:

- Use `tools/adr/extract.py` to pull MUST/MUST NOT clauses from each root spec into MADR candidates.
- Use `tools/adr/synthesize.py --dry-run --token-limit 6000` to verify the candidate corpus would compress under the deployed budget.
- Land the ratified subset as actual `decisions/<NNNN>-<slug>.md` files with `adr_status: Proposed`; the synthesizer then routes them into AGENTS.md via the guarded section, satisfying part (a) of the Goal mechanically.

## Preconditions (satisfied at branch-time)

- **Task 027** (`adr-spec-research-synthesis`, done) — produced `research/adr-spec-research-synthesis/output/SPEC.md`, the canonical ADR format consumed by ST-1.
- **Task 028** (`adr-tooling-impl-plan`, done) — produced the build contract that Task 031 implemented.
- **Task 029** (`adr-assumption-audit`, done) — produced `research/adr-assumption-audit/output/REPORT.md` whose ASMs/IADRs/PDs feed ST-1's curated corpus.
- **Task 031** (`adr-tooling-impl`, in_progress on PR #67 → done on merge) — shipped `tools/adr/{extract,synthesize,validate}.py`, `decisions/`, the `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` markers in AGENTS.md, and `types.adr` in `header-ontology.json`. ST-1 builds atop this; without it, ST-1 falls back to invent-from-scratch.

## Plan

1. **Phase 1 — Research head.** Spawn the `adr-corpus-extraction-from-governance-specs` research run (subtask `01`) so the §0 cross-reference and ADR backbone in §3.3 land on a tested corpus, not a stub.
2. **Phase 2 — Tooling.** Author three linters in parallel (subtasks `02`, `03`, `04`) that mechanically gate the new clauses.
3. **Phase 3 — Spec amendment.** Apply the AGENTS.md edits (subtask `05`) referencing both the research output and the new tooling. Edits are T2-Additive per `MAINTENANCE.md §1`.
4. **Phase 4 — README + index sync.** Update `README.md §10` if the new linters introduce a new pre-commit check (per `README.md §11.3 R.7`). Update `tasks/readme.md` per `TASK.md §4.8`.

## Sample Gherkin (shape the maintainer authoring subtask 05 should produce)

```gherkin
# anchor: AG.NO5.1
Scenario: Non-narrative agent loads narrative ontology — WARN
  Given an agent runs a Task whose `task_affects_paths` does NOT include
        any of `skills/dramatica-*`, `skills/ncp-*`, `skills/novel-*`
  And the staged diff shows a read against `maintenance/schemas/narrative-ontology/ontology.json`
  When `tools/check-narrative-ontology-load.py` runs at pre-commit
  Then the linter MUST emit a WARN (exit 2) citing the offending file
  And `tools/check-governance.sh` MUST NOT block the commit (advisory only)
```

This sample fixes the *shape* (Given/When/Then anchored to a stable identifier `AG.NO5.1`); subtask 05 then authors the remaining scenarios for §60–§65 assumption-log substance, §3.3 polarity-inversion footnote behaviour, and §6 skills-container-capabilities citations.

## Todo

- [x] 1. Dispatch subtask `01-research-adr-corpus-extraction` (research head); produces `research/adr-corpus-extraction-from-governance-specs/output/SPEC.md` (18 IADRs catalogued; 5 P1 ratified into `decisions/0001-..0005-`).
- [x] 2. Dispatch subtask `02-tooling-narrative-ontology-load-discipline` (Phase A — independent). Shipped `tools/check-narrative-ontology-load.py` + 5 tests.
- [x] 3. Dispatch subtask `03-tooling-rfc2119-polarity-audit` (Phase A — independent). Shipped `tools/check-rfc2119-polarity.py` + 10 tests.
- [x] 4. Dispatch subtask `04-tooling-assumption-log-substance` (Phase A — independent). Shipped `tools/check-assumption-log.py` + 9 tests.
- [x] 5. Dispatch subtask `05-spec-amendment-agents-md` (Phase B). AGENTS.md gained §"Theoretical Foundations", RFC-2119 polarity advisory, §"Skills Architecture" (U1/U2 + citation protocol), §"Assumption-Log Substance", and the `AG.NO5.1` Gherkin scenario. Edits stay outside the `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` markers; `python3 tools/adr/cli.py validate AGENTS.md` exits 0.
- [x] 6. Ran `tools/check-governance.sh`. Pre-existing baseline ERRORs (`tasks/046-github-workflow-research/task.md` missing `## Todo`; `tasks/readme.md` missing 045/046 bullets) predate Task 032 and are out-of-scope drift tracked by `031-sync-tasks-index-status-drift`. No new ERRORs introduced.
- [x] 7. README §6 update — the three new linters run advisory-only (WARN-tier, never set FAIL=1) so they do NOT join the pre-commit gating pipeline; no R.7 trigger fires.
- [x] 8. Updated `tasks/readme.md` membership for this task's `done` transition.
- [x] 9. Authored `friction-log.md` with FL declaration.
- [x] 10. Set `task_status: done`.

## Links

- Subtask index: [`subtasks/readme.md`](./subtasks/readme.md)
- Source research (under-cited, to be back-ported):
  - [`research/adr-assumption-audit/output/REPORT.md`](../../research/adr-assumption-audit/output/REPORT.md) §1 High-Blast Assumptions
  - [`research/skills-skill-container-capabilities/output/SPEC.md`](../../research/skills-skill-container-capabilities/output/SPEC.md)
  - [`research/gemini/agency-adr-governance-spec/`](../../research/gemini/agency-adr-governance-spec/)
  - [`research/ncp-novel-co-authoring-spec/output/SPEC.md`](../../research/ncp-novel-co-authoring-spec/output/SPEC.md)
- Governing specs: [`AGENTS.md`](../../AGENTS.md), [`MAINTENANCE.md`](../../MAINTENANCE.md) §1 (T1/T2/T3 tier), [`TASK.md`](../../TASK.md), [`FOLDERS.md`](../../FOLDERS.md), [`README.md`](../../README.md) §11.3
- Sibling tasks: [Task 027](../027-adr-spec-research-synthesis/task.md), [Task 029](../029-adr-assumption-audit/task.md)
