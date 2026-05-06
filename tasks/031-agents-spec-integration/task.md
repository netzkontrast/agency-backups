---
type: task
status: active
slug: agents-spec-integration
summary: "Integrate underused research findings (adr-assumption-audit ASM-001/004/005/009, skills-skill-container-capabilities U1-U2, gemini theoretical-foundation, ncp-novel-co-authoring) into AGENTS.md, mechanically enforce NO.5 narrative-ontology load discipline, and close the §60-65 assumption-log substance gap."
created: 2026-05-06
updated: 2026-05-06
task_id: "031"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - AGENTS.md
  - tools/check-narrative-ontology-load.py
  - tools/check-rfc2119-polarity.py
  - tools/check-assumption-log.py
---

# Task 031 — AGENTS.md Spec Integration

## Goal

Bring AGENTS.md into alignment with three completed-but-under-cited research outputs and close one acknowledged enforcement gap. The Task is `done` when (a) AGENTS.md carries a `§0 Theoretical Foundations` cross-reference to `research/gemini/agency-adr-governance-spec/`, (b) §3.3 RFC-2119 declaration carries a polarity-inversion footnote citing `research/adr-assumption-audit/output/REPORT.md §1`, (c) §6 (Skills Architecture) documents the `git unavailable / filesystem stateless` operational constraints from `research/skills-skill-container-capabilities/output/SPEC.md`, (d) NO.5 narrative-ontology load discipline is enforced by a new linter, and (e) §60–65 assumption-log substance is mechanically validated.

## Context

Per the spec-corpus audit produced in this branch, AGENTS.md has four under-utilized integration points:

1. **adr-assumption-audit** (`research/adr-assumption-audit/output/REPORT.md §1`) surfaces 4 HIGH-blast hidden assumptions affecting any future ADR-style synthesis into AGENTS.md (ASM-001 polarity-inversion, ASM-004 marker-check insufficiency, ASM-005 pre-commit bypassability, ASM-009 silent MADR-body truncation). None are currently footnoted in AGENTS.md.
2. **skills-skill-container-capabilities** (`research/skills-skill-container-capabilities/output/SPEC.md`) resolved U1 (no `git` binary in claude.ai container) and U2 (no filesystem persistence). AGENTS.md §6 still describes the skill loader as if `git clone` is available.
3. **gemini agency-adr-governance-spec** is the theoretical foundation for the MDL-compression / supersession-DAG paradigm but is uncited in AGENTS.md §0.
4. **ncp-novel-co-authoring-spec** defines the citation-reproducibility protocol (`path/to/file.ext:Lstart-Lend@<sha>`) used during novel co-authoring; AGENTS.md §6 does not reference it.

Plus two enforcement gaps:

- NO.5 (§251) — "An agent doing non-narrative work MUST NOT load the Narrative Ontology" — no linter enforces this; agents waste tokens loading the 215-entry ontology.
- §60–65 — assumption-log requirement is normative but readme.md `## Assumptions Log` substance is never mechanically validated.

## Plan

1. **Phase 1 — Research head.** Spawn the `adr-corpus-extraction-from-governance-specs` research run (subtask `01`) so the §0 cross-reference and ADR backbone in §3.3 land on a tested corpus, not a stub.
2. **Phase 2 — Tooling.** Author three linters in parallel (subtasks `02`, `03`, `04`) that mechanically gate the new clauses.
3. **Phase 3 — Spec amendment.** Apply the AGENTS.md edits (subtask `05`) referencing both the research output and the new tooling. Edits are T2-Additive per `MAINTENANCE.md §1`.
4. **Phase 4 — README + index sync.** Update `README.md §10` if the new linters introduce a new pre-commit check (per `README.md §11.3 R.7`). Update `tasks/readme.md` per `TASK.md §4.8`.

## Todo

- [ ] 1. Dispatch subtask `01-research-adr-corpus-extraction` (research head); produces `research/adr-corpus-extraction-from-governance-specs/output/SPEC.md`.
- [ ] 2. Dispatch subtask `02-tooling-narrative-ontology-load-discipline` (Phase A — independent).
- [ ] 3. Dispatch subtask `03-tooling-rfc2119-polarity-audit` (Phase A — independent).
- [ ] 4. Dispatch subtask `04-tooling-assumption-log-substance` (Phase A — independent).
- [ ] 5. Dispatch subtask `05-spec-amendment-agents-md` (Phase B — depends on 01–04 producing artefacts).
- [ ] 6. Run `tools/check-governance.sh`; fix every ERROR.
- [ ] 7. Update `README.md §6` if a new linter joins the pre-commit pipeline (R.7 trigger).
- [ ] 8. Update `tasks/readme.md` to reflect this task's `task_status` transition.
- [ ] 9. Author `friction-log.md` with FL[0-3] declaration per FRUSTRATED.md.
- [ ] 10. Set `task_status: done`.

## Links

- Subtask index: [`subtasks/readme.md`](./subtasks/readme.md)
- Source research (under-cited, to be back-ported):
  - [`research/adr-assumption-audit/output/REPORT.md`](../../research/adr-assumption-audit/output/REPORT.md) §1 High-Blast Assumptions
  - [`research/skills-skill-container-capabilities/output/SPEC.md`](../../research/skills-skill-container-capabilities/output/SPEC.md)
  - [`research/gemini/agency-adr-governance-spec/`](../../research/gemini/agency-adr-governance-spec/)
  - [`research/ncp-novel-co-authoring-spec/output/SPEC.md`](../../research/ncp-novel-co-authoring-spec/output/SPEC.md)
- Governing specs: [`AGENTS.md`](../../AGENTS.md), [`MAINTENANCE.md`](../../MAINTENANCE.md) §1 (T1/T2/T3 tier), [`TASK.md`](../../TASK.md), [`FOLDERS.md`](../../FOLDERS.md), [`README.md`](../../README.md) §11.3
- Sibling tasks: [Task 027](../027-adr-spec-research-synthesis/task.md), [Task 029](../029-adr-assumption-audit/task.md)
