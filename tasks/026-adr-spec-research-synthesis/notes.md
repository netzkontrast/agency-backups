---
type: note
status: active
slug: adr-spec-research-synthesis-pr-review
summary: "PR review critique of #52 (claude/save-architecture-governance-research-gy1dB → main): structural violations, governance failures, and protocol gaps found during pre-execution audit."
created: 2026-05-05
updated: 2026-05-05
---

# Notes — Task 026: PR #52 Pre-Execution Review

Authored by: `claude/stoic-mendel-Ifs5Y`
PR under review: [#52 — Add ADR governance specification and implementation tasks](https://github.com/netzkontrast/agency/pull/52)
Branch: `claude/save-architecture-governance-research-gy1dB` → `main`
Head SHA: `a7799503c203dbd7e89fb6c24d8826269c245aca`
Review date: 2026-05-05

---

## Review Summary

PR #52 establishes the scaffolding for a three-phase ADR governance pipeline (Tasks 026–028), ingests a Gemini-generated ADR governance spec, adds a bootstrap script (`install.sh`), and extends `AGENTS.md` with mandatory session-setup rules. The high-level architecture is sound and the task decomposition is well-structured. However, several structural violations and protocol breaches must be resolved before this PR can be merged without leaving the repository in a broken state.

---

## Critical Issues

### C1 — Folder named literally "slug" instead of the research slug

**File:** `research/gemini/slug/` (entire folder)
**Spec:** `RESEARCH.md §6.1` — the folder name MUST be the kebab-case slug derived from the research topic.

The `result.md` inside correctly declares `slug: agency-adr-governance-spec`. The folder containing it is named `slug` — a placeholder word, not the actual slug. This means:

1. Any linkage tool resolving `research_executes_prompt: agency-adr-governance-spec` looks for `/research/gemini/agency-adr-governance-spec/result.md` and finds nothing.
2. The path reference in `tasks/026-adr-spec-research-synthesis/task.md` under `## Links` points to `../../research/gemini/slug/adr-governance-spec.md` — a path that is technically reachable today but will break if the folder is ever renamed to its correct value without a link update.
3. Any future agent attempting to resolve `prompt_spawned_from_research: agency-adr-governance-spec` against the path-namespaced resolution rule (`RESEARCH.md §6`, second paragraph) will not find a match.

**Required fix:** Rename `research/gemini/slug/` → `research/gemini/agency-adr-governance-spec/` and update all relative links in `task.md`, `result.md`, and the two additional files inside.

---

### C2 — Governance check exits non-zero at commit time (SS.2 violation)

**File:** `AGENTS.md` (newly added SS.1–SS.3 rules), commit `a7799503`
**Spec:** `AGENTS.md §Session Setup` rule SS.2 — "An agent MUST run `tools/check-governance.sh` immediately after `install.sh` completes and MUST NOT proceed if it exits non-zero."

Running `tools/check-governance.sh` on the merged state of this PR yields:

```
--- [opt] Narrative-ontology validator ---
ERROR: jsonschema is required. Install with: pip install jsonschema
=== FAIL: one or more checks failed. ===
```

The PR adds `install.sh` precisely to ensure `jsonschema` is available — but the commits in this PR were made in an environment where `jsonschema` was not installed. The agent therefore committed in violation of the very rule it added to `AGENTS.md`. This is a self-referential governance failure: the PR that mandates SS.2 compliance was itself non-compliant with SS.2 at commit time.

**Required fix:** Before merge, the submitting agent (or a human operator) must run `./install.sh && tools/check-governance.sh` and confirm exit 0. The `jsonschema` package must be present in the CI/hook environment before the SS.1–SS.3 rules become enforceable.

---

## Significant Issues

### S1 — OPTIONAL frontmatter fields set to empty strings instead of being omitted

**Files:**
- `prompts/adr-spec-research-synthesis/prompt.md` — `prompt_spawned_from_research: ""`
- `prompts/agency-adr-governance-spec/prompt.md` — `prompt_relates_to_task: ""` and `prompt_spawned_from_research: ""`

**Spec:** `PROMPT.md §3` — both fields are declared OPTIONAL. `AGENTS.md §Frontmatter Ontology` — "YAML MUST NOT nest beyond one level. Lists MUST contain scalars or short strings only." The YAML Depth Rule does not directly govern empty-string OPTIONAL fields, but setting an OPTIONAL field to `""` rather than omitting it creates false linkage surface: a linter that does `if frontmatter.get("prompt_spawned_from_research")` resolves to falsy on `""`, but a linter doing `"prompt_spawned_from_research" in frontmatter` finds a key and may attempt resolution, failing with a spurious error.

**Required fix:** Remove the `prompt_spawned_from_research: ""` and `prompt_relates_to_task: ""` lines from both files. OPTIONAL fields with no value MUST be omitted.

---

### S2 — `research/gemini/slug/` lacks a `readme.md` directory index

**File:** `research/gemini/slug/` (folder)
**Spec:** `FOLDERS.md` (directory index requirement), `RESEARCH.md §5.5` — "Missing `readme.md` in research folder" is a lint failure mode.

The external research folder contains only `adr-governance-spec.md`, `research-prompt_agency-adr-governance-spec.md`, and `result.md`. No `readme.md` is present. The structural linter (`tools/lint-structure.py`) currently passes because the check is keyed on the `/research/<slug>/` pattern for standard research runs, and the provider-namespaced path may evade the check. However, the requirement is still normative.

**Required fix:** Add `research/gemini/agency-adr-governance-spec/readme.md` (or `slug/` while the rename from C1 is pending) with L1 frontmatter (`type: readme`, `status: active`, etc.) and relative links to all files in the folder.

---

### S3 — Task 026 `task_spawns_research` pre-declares a research slug that does not yet exist

**File:** `tasks/026-adr-spec-research-synthesis/task.md`
**Field:** `task_spawns_research: [adr-spec-research-synthesis]`
**Spec:** `TASK.md §7.4` — "Every slug in `task_spawns_research` resolves to an existing `/research/<slug>/` folder" — **checked only for closed tasks.**

Technically this is allowed for open tasks. However, it creates a misleading state: a reader of `tasks/readme.md` scanning the index may assume the research workspace already exists. This is a convention concern rather than a hard violation.

**Recommendation:** Add a note in `task.md` under `## Goal` or `## Plan` clarifying that `task_spawns_research` is a pre-declaration of the *intended* output slug, not a confirmation that the workspace exists.

---

## Minor Issues

### M1 — `AGENTS.md` "Session Setup" section ordering

The new "Session Setup" section (SS.1–SS.3) was inserted as the second paragraph after the opening welcome, appearing *after* the "Before committing any work: You MUST review PRE_COMMIT.md" inline notice. An agent reading linearly may execute the PRE_COMMIT check before running `install.sh`, which is the wrong order if the pre-commit hooks depend on the installed packages. The intent is correct but the positioning creates an ambiguous priority ordering.

**Recommendation:** Either move the "Session Setup" section before the "Before committing" inline notice, or add an explicit ordering note ("Session Setup MUST precede the PRE_COMMIT check").

### M2 — `adr-governance-spec.md` references `docs/decisions/` with no reconciliation

The Gemini spec (`research/gemini/slug/adr-governance-spec.md §2`) mandates `docs/decisions/` as the canonical ADR storage path. The repo currently has no `docs/` directory, and `FOLDERS.md` does not define one. Task 026 explicitly lists resolution of this conflict as a goal (§ Context, point about storage path), but the Gemini spec is marked `Status: IN-FORCE` in its own frontmatter — which is incorrect given it has not yet been reconciled with the repo structure. The `IN-FORCE` claim is premature.

**Recommendation:** Change the status header in `adr-governance-spec.md §0` from `IN-FORCE` to `DRAFT — PENDING SYNTHESIS (Task 026)` to prevent downstream agents from treating it as authoritative before Task 026 reconciles it.

---

## Positive Observations

1. **Task sequencing is correct.** Tasks 027 and 028 both declare `task_blocked_by: ["026"]`, correctly enforcing execution order. The linter will gate them until Task 026 is done.
2. **Task index sync is correct.** `tasks/readme.md` was updated in the same commit as Task 026–028 creation, satisfying `TASK.md §4.8`.
3. **Stub prompt for external research is correctly structured.** `/prompts/agency-adr-governance-spec/` contains `brief.md`, `prompt.md`, and `readme.md`, matching `RESEARCH.md §6.3`.
4. **The three-phase pipeline (research → implementation plan → assumption audit) is architecturally sound.** The separation of concerns between Tasks 026, 027, and 028 avoids the anti-pattern of inlining all concerns in a single task.
5. **The install.sh bootstrap script is well-written.** Idempotent, handles PEP 668 externally-managed environments via `--break-system-packages` fallback, and verifies each dependency with an import check after install.

---

## Action Items for Task 026 Executor

Before beginning Phase 1 of Task 026, the executing agent MUST resolve the following against this task's preconditions:

- [ ] Confirm `research/gemini/slug/` is renamed to `research/gemini/agency-adr-governance-spec/` (C1)
- [ ] Confirm `./install.sh && tools/check-governance.sh` exits 0 (C2)
- [ ] Remove empty-string OPTIONAL frontmatter fields (S1)
- [ ] Verify `readme.md` exists in the corrected gemini research folder (S2)
- [ ] Downgrade Gemini spec status from `IN-FORCE` to `DRAFT — PENDING SYNTHESIS` (M2, recommended)
