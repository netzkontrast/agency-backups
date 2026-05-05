---
type: prompt
status: active
slug: adr-tooling-impl-plan
summary: "Drives Task 028: from the repo-native ADR governance spec (Task 027 output), produce a concrete, sequenced implementation plan for the agency-adr CLI tool suite — module decomposition, acceptance test map, CI/CD integration, and open-decisions list."
created: 2026-05-05
updated: 2026-05-05
prompt_kind: task-spec
prompt_framework: RISEN
prompt_target_agent: "Claude Code"
prompt_relates_to_task: adr-tooling-impl-plan
---

# ADR Tooling Implementation Plan — Task-Spec Prompt

## R — Role

You are the **Build Architect** for `netzkontrast/agency`. You receive a governance specification (`research/adr-spec-research-synthesis/output/SPEC.md`) and must translate its "interface contract yes, working code no" boundaries into a sequenced, unambiguous implementation plan. You write the plan, not the code.

## I — Input

1. **ADR governance spec:** `research/adr-spec-research-synthesis/output/SPEC.md` (authoritative — read fully before any other file)
2. **Gemini draft:** `research/gemini/agency-adr-governance-spec/adr-governance-spec.md` (background reference for CLI shape and JSON-Schema sketch)
3. **Existing tooling:** `tools/fm/validate.py`, `tools/fm/extract.py`, `tools/fm/edit.py`, `tools/fm/query.py`, `tools/check-governance.sh`
4. **Repo conventions:** `PRE_COMMIT.md`, `MAINTENANCE.md`, `TASK.md`

## S — Steps

### Step 1 — Audit Existing Tooling Primitives

Read all files under `tools/fm/` and `tools/check-governance.sh`. Produce a table:

| Primitive | File | Reusable by agency-adr? | Notes |
|-----------|------|------------------------|-------|
| YAML frontmatter parse | `tools/fm/validate.py` | … | … |
| File traversal | … | … | … |
| Schema validation | … | … | … |

Identify the repo's Python dependency management approach (requirements.txt / pyproject.toml). Record in `tasks/028-adr-tooling-impl-plan/implementation-plan.md §1`.

### Step 2 — Module Decomposition

Decompose `agency-adr` into independently testable modules. For each module, specify:
- Module name and file path under `tools/adr/`
- Single responsibility statement
- Public interface (function signatures, not implementations)
- Dependencies on other `agency-adr` modules and existing `tools/fm/` primitives
- Build phase (1 = no internal deps, 2 = depends on phase-1 modules, etc.)

Mandatory modules from the spec: `schema.py`, `graph.py`, `extract.py`, `compress.py`, `synthesize.py`, `cli.py`. Add additional modules only if justified by the spec.

### Step 3 — Acceptance Test Map

For every Gherkin scenario in the spec (anchored by `# anchor: A.<Aspect>.<Stmt>`), map to:
- `tests/adr/test_<aspect>.py` file
- Test function name
- Fixture requirements
- Build phase the test belongs to

Produce the test map table in `implementation-plan.md §3`.

### Step 4 — GitHub Actions Workflow Spec

Specify `.github/workflows/adr-validate.yml`:
- Trigger condition
- Job steps (pip install, validate, synthesize, diff check)
- Failure handling and exit-code contract
- AGENTS.md diff gate: what constitutes an acceptable diff vs a rejection condition

Do not write the YAML. Write the specification in `implementation-plan.md §4` as a structured list that a devops agent can follow unambiguously.

### Step 5 — PRE_COMMIT.md Hook Specification

Specify the hook entry for `PRE_COMMIT.md`:
- Trigger condition (which file paths trigger the hook)
- Command invoked
- Expected exit codes and their meanings
- Error message format (MUST reference spec statement IDs, e.g., `[A.4.5]`)

Write in `implementation-plan.md §5`.

### Step 6 — Open Decisions List

Enumerate every implementation decision the spec left open (flagged in §8 of the spec or inferred from the module decomposition). For each:
- Decision statement
- Options (A/B/C if applicable)
- Which Task 028 module is blocked until it is resolved
- Recommended owner (human architect / agent / defer to Task 029 report)

Write in `implementation-plan.md §6`.

### Step 7 — Complexity Estimation

For each module (Step 2) and test file (Step 3), assign a complexity estimate: S (< 1 day), M (1–3 days), L (> 3 days). Sum to a total implementation estimate. Record in `implementation-plan.md §7`.

### Step 8 — Verification and Closure

1. Run `tools/check-governance.sh` against all new files.
2. Mark `task_status: done` in `tasks/028-adr-tooling-impl-plan/task.md`.

## E — Expectations

**Deliverable:** `tasks/028-adr-tooling-impl-plan/implementation-plan.md` with §1–§7 fully populated.

The plan MUST be executable by a fresh agent with no prior context beyond this plan and the referenced input files. Ambiguity is a defect.

**Non-goals:**
- Writing any `tools/adr/*.py` code.
- Writing any test fixtures.
- Writing the GitHub Actions YAML.

## N — Narrowing

- Scope: implementation planning only. Do not modify the ADR governance spec produced by Task 027.
- Tool boundary: `agency-adr` MUST reuse existing `tools/fm/` parsing primitives; it MUST NOT duplicate them.
- No working code: interface contracts (type signatures, CLI shape, JSON-Schema) yes; implementations no.
- RFC 2119 normativity in the plan: one keyword per sentence; stable IDs from the spec MUST be cited.
