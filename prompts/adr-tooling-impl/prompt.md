---
type: prompt
status: active
slug: adr-tooling-impl
summary: "Drives Task 031: implement the agency-adr CLI suite end-to-end against the build contract in tasks/028-adr-tooling-impl-plan/implementation-plan.md. Successor to the plan-only prompt adr-tooling-impl-plan; lifts every Non-goal of that prompt into a Goal here."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN
prompt_target_agent: "Claude Code"
prompt_relates_to_task: adr-tooling-impl
---

# ADR Tooling Implementation — Task-Spec Prompt

## Framework

RISEN+ReAct. Framework declared at the top; this section restates it for fm-validate header conformance.

## R — Role

You are the **Implementing Agent** for `netzkontrast/agency`. You receive an unambiguous build contract — the [Task 028 implementation plan](../../tasks/028-adr-tooling-impl-plan/implementation-plan.md) — and translate every contract row into committed code, tests, configuration, and documentation. You write the working code that the predecessor prompt explicitly forbade.

## I — Input

1. **Build contract:** `tasks/028-adr-tooling-impl-plan/implementation-plan.md` (authoritative — read fully before any other file).
2. **Governance spec:** `research/adr-spec-research-synthesis/output/SPEC.md` (the ADR.A.* anchors cited by the plan).
3. **Audit report:** `research/adr-assumption-audit/output/REPORT.md` (PD-002 / PD-005 refinements that bind the implementation).
4. **Existing primitives:** `tools/fm/_core.py` (`parse_frontmatter`, `Diagnostic`, `find_section_body`, `detect_shape`, `FileLock`, `load_ontology`).
5. **Hook composer:** `tools/check-governance.sh`.
6. **Schema registry:** `maintenance/schemas/header-ontology.json`, `maintenance/schemas/diagnostic-explanations.json`.
7. **Repo conventions:** `TASK.md`, `PROMPT.md`, `PRE_COMMIT.md`, `MAINTENANCE.md`, `FOLDERS.md`.

## S — Steps

### Step 1 — Schema and folder registration

Add `types.adr` to `maintenance/schemas/header-ontology.json` with the §7.4 JSON-Schema embedded under `types.adr.json_schema`. Add the `decisions/[0-9][0-9][0-9][0-9]-*.md` rule to `path_classification.rules`. Append `/decisions/` to the `FOLDERS.md §8` non-operational table. Seed `decisions/readme.md`.

### Step 2 — Phase-1 modules

Author `tools/adr/__init__.py`, `tools/adr/schema.py` (JSON-Schema validator using `jsonschema`), and `tools/adr/body.py` (MADR heading presence + ADR.A.1.4 ≥ 2 considered options + ADR.A.2.3 / ADR.A.2.4 non-empty checks).

### Step 3 — Phase-2 modules

Author `tools/adr/corpus.py` (`AdrRecord` dataclass + `load_corpus`), `tools/adr/graph.py` (`AdrGraph` + Kahn's cycle detection + reciprocity + orphan checks; mark every cycle path as seen so siblings do not rediscover it), and `tools/adr/ids.py` (duplicate `adr_id` + filename↔frontmatter coupling).

### Step 4 — Phase-3 modules

Author `tools/adr/extract.py` (BCP-14 sentence extraction from "Decision Outcome" + "Consequences" of every live Accepted ADR), `tools/adr/compress.py` (MDL-style dedup that aggregates citations across duplicate sentences; emit `[ADR-0001, ADR-0002]` style multi-cite), and `tools/adr/fidelity.py` (ship `bcp14-keyword` + `adr-id-anchor`; raise `NotImplementedError` for `llm-pass` per OD.2).

### Step 5 — Phase-4 modules

Author `tools/adr/synthesize.py` (idempotent marker-bounded write; refuse on missing markers with `ADR.A.3.5`; declare `decisions_root: Path | None = None` and derive from `repo_root` inside the function) and `tools/adr/runlog.py` (append a record honouring `tools/lint-runlog.py`'s `REQUIRED_FIELDS` schema; ADR-specific metadata goes in `notes`).

### Step 6 — Phase-5 entry point

Author `tools/adr/cli.py` (`validate` + `synthesize` sub-commands, `--strict`, `--format=text|json`; emit JSON to stdout and text diagnostics to stderr — document this split in a comment) and `tools/adr/readme.md` (folder index per `FOLDERS.md §3`).

### Step 7 — Test suite

Under `tests/adr/`, author one pytest module per build phase (`conftest.py`, `test_schema.py`, `test_body.py`, `test_filename_coupling.py`, `test_ids.py`, `test_graph.py`, `test_extract.py`, `test_compress.py`, `test_fidelity.py`, `test_synthesize.py`, `test_runlog.py`, `test_cli.py`, `test_explore.py`). Every scenario MUST carry a `# anchor: ADR.A.<aspect>.<stmt>` comment and assert against the diagnostic codes the spec names.

### Step 8 — Pre-commit hook integration

Insert a numbered step (currently `[5/5]`) into `tools/check-governance.sh` that runs `python3 tools/adr/cli.py validate`; renumber downstream steps. Document the validator in a new `PRE_COMMIT.md §7.C` section, including the diagnostic-code remedy table.

### Step 9 — AGENTS.md guarded section

Insert a `## Synthesised ADR Constraints` section into `AGENTS.md` with the byte-exact `<!-- BEGIN AGENCY-ADR SYNTHESIS -->` and `<!-- END AGENCY-ADR SYNTHESIS -->` markers (OD.6 resolution: separate section near the bottom). Run `python3 tools/adr/cli.py synthesize` once on the empty corpus so the committed bytes match what dry-run produces — the GitHub Actions diff gate enforces this.

### Step 10 — GitHub Actions workflow

Author `.github/workflows/adr-validate.yml` per plan §4: trigger on `decisions/**`, `AGENTS.md`, `tools/adr/**`, `tests/adr/**`, the ontology JSON, and the workflow itself; run `tools/check-governance.sh --no-trust`, the ADR test suite, and `synthesize --dry-run`; diff the dry-run body against the committed `AGENTS.md` guarded section; upload the dry-run artefact for forensic review (≥ 7 day retention).

### Step 11 — Diagnostic-explanations registration

Add an entry per `ADR.A.*` code to `maintenance/schemas/diagnostic-explanations.json` (`severity_hint` / `what` / `why` / `fix`) so `--explain` annotates ADR diagnostics correctly.

### Step 12 — Verification + closure

Run `python3 -m pytest tests/` (MUST exit 0, ≥ 200 cases) and `tools/check-governance.sh` (MUST exit 0). Set `task_status: done` in `tasks/031-adr-tooling-impl/task.md`. Author `tasks/031-adr-tooling-impl/friction-log.md` with the FL declaration and any frictions encountered. Commit and push.

## E — Expectations

**Deliverable:** A merge-ready PR on a `claude/<topic>-<date>` branch carrying every artefact above. The PR's pre-commit gate MUST exit 0; the GitHub Actions `adr-validate` job MUST exit 0; the test suite MUST cover every Gherkin anchor with a deterministic assertion.

**Non-goals:**
- Authoring the first batch of ADRs (the corpus seed). That is sequenced as a separate Task per [`research/adr-assumption-audit/output/REPORT.md`](../../research/adr-assumption-audit/output/REPORT.md) §3 PD-005.
- Implementing the `llm-pass` fidelity mode (deferred per OD.2; v0 ships `bcp14-keyword` + `adr-id-anchor`).
- Editing `research/adr-spec-research-synthesis/output/SPEC.md` (T4-immutable per `MAINTENANCE.md §1`).
- Editing `.githooks/pre-commit` directly (the only gate edit is via `tools/check-governance.sh`, per ADR.A.5.8).

## N — Narrowing

- Scope: implementation only. Do not propose new spec changes; surface novel concerns in `friction-log.md` for a successor Task.
- Tool boundary: `agency-adr` MUST reuse `tools/fm/_core.py` for parsing, diagnostics, file locking, ontology loading. No reimplementation.
- Determinism: the synthesizer MUST be byte-stable across runs against an unchanged corpus (ADR.A.3.6).
- Cycle correctness: `graph.detect_cycles` MUST mark every cycle path as seen so duplicate diagnostics are not emitted from sibling start nodes.
- Spec citations: every diagnostic message and every test docstring MUST cite the ADR.A.* anchor it enforces.

## Constraints

- The agent MUST run `tools/check-governance.sh` before pushing each commit; a non-zero exit MUST block the push.
- The agent MUST NOT modify any file under `research/<slug>/output/` whose `research_phase` is `complete`.
- The agent MUST cite every assumption back to its source spec or implementation-plan §; silent intent inference is forbidden.
- The agent SHOULD treat any conflict between the spec and the implementation-plan as a T3 change requiring a sub-Task or a friction-log entry surfacing the divergence.
- The agent MUST NOT introduce new runtime dependencies beyond stdlib and the existing `jsonschema` requirement.
- The agent SHOULD NOT add `tools/__init__.py`; preserving the script-mode-only import idiom keeps the existing `tools/fm/` test suite green.
