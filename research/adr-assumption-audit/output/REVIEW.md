---
type: note
status: active
slug: adr-assumption-audit-review
summary: "External peer review of PR #64 (Tasks 027–029: ADR governance spec, tooling plan, assumption audit). Identifies 2 critical errors in REPORT.md, 1 confirmed process deviation, and 1 structural ambiguity in the subagent execution model. Merge-conditional."
created: 2026-05-05
updated: 2026-05-05
---

# PR #64 — Peer Review: ADR Governance Spec, Tooling Plan, and Assumption Audit

**Reviewer:** Claude Code (`claude/stoic-mendel-cFCdt`)
**Target PR:** [#64](https://github.com/netzkontrast/agency/pull/64)
**Branch:** `claude/adr-spec-research-NPwuc → main`
**Head SHA:** `44759efd`
**Tasks Reviewed:** 027 (ADR spec), 028 (tooling plan), 029 (assumption audit)
**Reviewed against:** `AGENTS.md`, `RESEARCH.md`, `PROMPT.md`, `TASK.md`, `FRUSTRATED.md`

---

## §0 Verdict

**Merge-conditional.** The research is substantively sound and methodologically rigorous. Two numeric errors in `REPORT.md` must be corrected before merge (§1.1 and §1.2); they corrupt the token-cheap summary that agents rely on instead of reading the full body. The process deviations (§2) are self-documented in the friction log and do not block merge but should inform future prompt revisions.

---

## §1 Critical Issues (Must Fix Before Merge)

### §1.1 Frontmatter Summary Miscounts High-Blast Assumptions

**File:** `research/adr-assumption-audit/output/REPORT.md` — frontmatter `summary` field, line 6.

**What is wrong:** The `summary` field reads:

> "9 hidden assumptions (3 high-blast) …"

But §1 of the body enumerates:
- **4** high-blast technical: ASM-001, ASM-004, ASM-005, ASM-009 (the section header correctly states "(4)")
- **1** high-blast cultural: ASM-007 (header states "(1)")
- Total high-blast: **5**, not 3.

The claim of "3 high-blast" does not match any sensible reading of the body — it is neither 4 (technical only) nor 5 (technical + cultural).

**Why this matters:** Per `AGENTS.md` §Frontmatter Ontology, `summary` is "the primary token-saving lever." Future agents routing triage decisions — e.g., "how many high-blast risks are unresolved?" — will read the summary first and receive a wrong count. In an ADR governance workflow where blast radius drives action priority, this is a meaningful error.

**Required fix:** Update `summary` to read "9 hidden assumptions (5 high-blast: 4 technical + 1 cultural, 4 medium)" or equivalent accurate form.

---

### §1.2 Medium-Blast Section Header Mismatch

**File:** `research/adr-assumption-audit/output/REPORT.md` — §1 "Medium-Blast Assumptions" section header.

**What is wrong:** The section header reads:

> `### Medium-Blast Assumptions (3)`

But the table under it contains **4** rows: ASM-002, ASM-003, ASM-006, ASM-008.

The commit message correctly states "4 medium" but the REPORT.md header says "(3)". This is an internal inconsistency within the same document.

**Why this matters:** The number in the header is machine-readable in the same sense as the frontmatter `summary` — it is the first datum a reviewer sees before scanning rows. A wrong count erodes confidence in the entire findings list.

**Required fix:** Change header to `### Medium-Blast Assumptions (4)`.

---

## §2 Process Deviations (Documented; No Merge Block)

### §2.1 Subagent Execution: Serial, Not Parallel

**File:** `research/adr-assumption-audit/reflection/friction-log.md` — Entry 1.

**What happened:** The prompt (`prompts/adr-assumption-audit/prompt.md`) explicitly states: "You operate by deploying three subagents … Subagents are parallel workers." The friction log transparently admits:

> "In practice I executed the three subagent passes serially within this session, producing the three workspace files (M13 / M07 / M06+M08) as if each were authored by a distinct sub-agent. The artefact shape matches the prompt's expectation; only the execution model differs."

The commit message calls it a "Three-subagent critical-thinking audit" without noting the serial execution. This is technically accurate (three methods were applied) but obscures the deviation for a reader who does not open the friction log.

**Assessment:** The friction log satisfies FRUSTRATED.md's disclosure requirement. The output artefacts (three separate workspace files with distinct methods) are formally correct. The substantive risk — that serial execution might produce cross-contaminated conclusions — is real but not evidenced in this run.

**Recommendation for future prompts:** Add the explicit fork the friction log suggests: "MUST apply each method's semantics in sequence (single-agent execution)" vs. "MUST spawn parallel sub-agents." This is a recurring FL1 across Tasks 027 and 029 — `MAINTENANCE.md §3.3` trigger threshold is one more occurrence.

---

### §2.2 Cross-Task Amendment Target File Mismatch

**File:** `research/adr-assumption-audit/reflection/friction-log.md` — Entry 2.

**What happened:** Task 029's prompt §Step 7.3 instructs: "Update `tasks/028-adr-tooling-impl-plan/task.md` §Open Decisions with any PD-NNN items found in Step 4." The agent instead appended the PD↔OD cross-reference to `tasks/028-adr-tooling-impl-plan/implementation-plan.md` (a new §A appendix).

**Justification given:** `task.md` lacks a `§Open Decisions` section — the open decisions live in `implementation-plan.md §6`. The amendment was purely additive and classified as T1 (mechanical) per `MAINTENANCE.md §1`.

**Assessment:** The reasoning is sound. A strict reading of the prompt is impossible because the referenced section does not exist. The additive-only constraint was honoured (§1–§7 unmodified). Post-closure mutation of a done Task's plan is a documented concern but the agent's analogy to T1 repair is defensible.

**Recommendation for future prompts:** The prompt should reference the correct file (`implementation-plan.md`) and scope (append §A appendix), as the friction log suggests.

---

## §3 Observations (Quality; Not Blocking)

### §3.1 Worst-Case Composition Analysis Is Incomplete

**File:** `research/adr-assumption-audit/output/REPORT.md` §1 "Worst-Case Composition."

The composition analysis covers ASM-001 ∘ ASM-009 (polarity inversion + extraction blind spot → claimed 2× under-reported compression ratio). A second high-risk composition is not analysed: **ASM-005 ∘ ASM-001** — where the pre-commit gate is bypassed (GitHub web edit, force-push) AND the polarity inversion is undetectable by the BCP14 keyword extractor. This composition allows a corrupted normative to reach `AGENTS.md` without any automated gate catching it. ASM-005's HIGH blast radius rating is specifically premised on the CI workflow not yet existing; combined with ASM-001, the "no automated mitigation in any pipeline" scenario materialises.

This does not require a REPORT.md rewrite — it could be addressed as a Task-030 scoping note.

### §3.2 PD-006 and PD-007 Lack Subagent Attribution

**File:** `research/adr-assumption-audit/output/REPORT.md` §3.

PD-006 and PD-007 are identified as "novel findings" (not pre-specified in the prompt) but their audit trail is missing: which subagent surfaced them, via which axis or method step? Per the REPORT.md §0 quality bar ("every finding cites a `file:line` or `file §section` evidence anchor"), these PDs should trace back to a workspace file line.

They are traceable in spirit (PD-006 relates to the spec's missing human-review lifecycle, PD-007 to the missing stale-`Proposed` audit) but the formal evidence anchor is absent.

### §3.3 Action 2 Circular Sequencing Not Flagged

**File:** `research/adr-assumption-audit/output/REPORT.md` §4 Action 2.

The implementation hint states: "This Task SHOULD be authored *after* the implementing-agent Task ships `agency-adr validate`, so the ADRs themselves can be validated as they land." But the implementing-agent Task's schema validation (`tools/adr/validate.py`) depends on knowing the P1 IADR set to define the first-batch ADR shape. This creates an implicit dependency cycle:

> Task-030 (ADR authoring) waits for `agency-adr validate` → `agency-adr validate` is shaped by which IADRs it must validate → shaping the IADR list is Task-030's job.

This is resolvable (start with ADR schema validation against the MADR shape, then bootstrap the first-batch ADRs) but should be flagged as PD-008 rather than left as an implicit sequencing risk in the Action 2 hint.

---

## §4 Compliance Checklist

| Gate | Status | Note |
|---|---|---|
| `tools/check-governance.sh` exits 0 | ✅ | Confirmed in commit message |
| L1 + L2 frontmatter on all operational files | ✅ | Spot-checked; all research files have `research_*` namespace |
| `prompt.md` snapshot in `research/adr-assumption-audit/` | ✅ | Authorised by `RESEARCH.md §2` directory spec |
| Task 029 marked `task_status: done` | ✅ | Confirmed in `tasks/029-adr-assumption-audit/task.md` |
| T4-immutable spec not modified | ✅ | `research/adr-spec-research-synthesis/output/SPEC.md` untouched |
| RISEN+ReAct framework applied | ✅ | Role, Input, Steps, Expectations, Narrowing all present in prompt |
| Three distinct methods applied | ✅ | M13, M07, M06+M08 each produce separate workspace files |
| Quality bar (file:line citations) | ✅ (partial) | PD-006, PD-007 missing attribution (§3.2) |
| Friction log FL1 with entries | ✅ | Two FL1 entries; both documented with cause and cost |
| Frontmatter summary accurate | ❌ | Wrong high-blast count (§1.1) |
| REPORT.md section headers accurate | ❌ | Medium-blast header says "(3)", body has 4 rows (§1.2) |

---

## §5 Required Changes Summary

| # | File | Change | Blocking? |
|---|---|---|---|
| R1 | `research/adr-assumption-audit/output/REPORT.md` line 6 (frontmatter `summary`) | Correct "(3 high-blast)" → "(5 high-blast: 4 technical + 1 cultural)" | YES |
| R2 | `research/adr-assumption-audit/output/REPORT.md` §1 "Medium-Blast Assumptions" header | Correct "(3)" → "(4)" | YES |
| R3 | Future: `prompts/adr-assumption-audit/prompt.md` or template | Add explicit subagent-invocation-mode clause | NO (future) |
| R4 | Future: file PD-008 (Task-030 / agency-adr sequencing cycle) | Flag as pending decision | NO (future) |
