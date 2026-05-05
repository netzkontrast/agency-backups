---
type: index
status: active
slug: adr-spec-research-synthesis-output
summary: "Output directory for Task 027's research run. Holds the canonical ADR governance specification for netzkontrast/agency."
created: 2026-05-05
updated: 2026-05-05
---

# Output

The final deliverable of this research run.

## Files

- [`SPEC.md`](./SPEC.md) — **The repo-native ADR Governance Specification** (§0–§9). Authoritative. Status `IN-FORCE` once `tools/check-governance.sh` exits 0 against this folder.

## Status

`research_phase: complete`. The SPEC is the binding contract for any ADR work in this repo from this commit forward. Implementation lives in [Task 028](../../../tasks/028-adr-tooling-impl-plan/task.md); assumption audit lives in [Task 029](../../../tasks/029-adr-assumption-audit/task.md).
