# Tracks — toolchain-flip-criteria

Per-track work breakdown. The run had two tracks:

## Track A — Mechanical-flip checklist (§1 of SPEC.md)

- [x] A1. Identify gating-vs-advisory boundary in current `tools/check-governance.sh`.
- [x] A2. Enumerate criteria as git/grep-extractable predicates (no LLM judgment).
- [x] A3. Cap at ≤7 items per AC-2; collapse closely-related criteria where the same command verifies both.
- [x] A4. Account for the third toolchain (ADR Validator) per Task 039 §1.1.2.

## Track B — Procedure + cleanup + rollback (§2–§4 of SPEC.md)

- [x] B1. Author §2 as a single git-commit shape (file-change enumeration, atomic).
- [x] B2. Enumerate every retire/promote action in §3.
- [x] B3. Mentally execute `git revert <flip-sha>` against §2 to confirm rollback re-establishes the pre-flip working tree (§4).
- [x] B4. Confirm §3 cleanup is sequenced after the §2 flip, never bundled into the same atomic commit (rollback safety).
