---
type: note
status: active
slug: pr27-governance-review
summary: "Methodology: diff-cluster cross-reference against governance specs."
created: 2026-05-04
updated: 2026-05-04
---

# Methodology

## Approach

**Diff-Cluster Cross-Reference (M-DCCR).**

1. The PR diff was grouped into the six change clusters named in the PR body:
   linkage fixes, spec drift reconciliation, DRY refactor, housekeeping, and friction-log retrofit.
2. Each cluster was evaluated against the specific governance spec clause it claims to address.
3. Additional checks were applied that the PR body does not name: audit-graph completeness,
   self-referential consistency, and run-log protocol compliance.

## Evidence Sources

| Source | Role |
|---|---|
| PR #27 diff (19 files, +251/−207) | Primary evidence |
| `prompts/repo-coherence-check/prompt.md` | Original driving prompt |
| AGENTS.md (CR.1–CR.6, L1 table, RFC 2119 rules) | Normative reference |
| TASK.md §2, §3, §7.7 | Normative reference |
| PROMPT.md §3, §6.5, §6.6 | Normative reference |
| RESEARCH.md §6 | Normative reference |
| `maintenance/run-log.md` | Audit-trail evidence |
