---
type: note
status: active
slug: 045-readme-coherence-refresh-friction
summary: "Friction log for Task 045 closure. Highest Frustration Level: FL1."
created: 2026-05-08
updated: 2026-05-08
---

# Task 045 — Friction Log

Highest Frustration Level: FL1

## Summary

Goal conditions met with one slot-collision adaptation.

## Entries

- **FL1 — ADR slot 0001 was already taken.** The Task plan named the
  new ADR `decisions/0001-agency-system-prototype-exemption.md` but
  `0001-mandatory-session-bootstrap.md` already owns that slot in the
  current ledger. Filed the ADR as `0006-agency-system-prototype-exemption.md`
  (next free slot). The body still records the carve-out the Task
  asked for; the slug differs from the Task plan only in its
  numeric prefix.
- **FL0 — Reframe edits were straightforward.** §1 grew from three
  rows to four (Capability / Skill row added); §3 gained §3.4
  Capability — `/skills/`; the strapline at the top swapped
  "Machine, Actor, and Space" for "Machine, Actor, Space, and
  Capability"; the §1 "Pending reframe" callout was removed.
  R.3 / R.14 references to the framing were updated in lockstep.
  R.21 was appended to §11.6 anti-patterns to mandate that any new
  schema corpus added under `maintenance/schemas/<name>/` MUST be
  mentioned in §12 in the same commit. Existing R.1–R.20 retained
  their numeric values (R.10 spec ↔ §11.5 RM.1.4 anchor).
- **FL0 — §12 added.** New top-level §12 *Narrative Ontology
  (load-gated)* points at AGENTS.md NO.1–NO.6,
  `maintenance/schemas/narrative-ontology/`, and
  `tools/dramatica-nav/nav.py`. Matches the §11.5 RM.1.1 / RM.1.2
  Gherkin scenarios (no broken cross-refs, no contradiction with a
  root spec).
- **FL0 — ADR governance closed cleanly.** ADR-0006 `Accepted`
  immediately (one author, narrow carve-out, FOLDERS.md §8 already
  reserved the slot). `tools/adr/cli.py synthesize` rewrote the
  AGENTS.md guarded block. Governance gate green.

## Goal Condition Sweep

1. ✅ §1 + §3 frame four concerns (Machine / Actor / Space /
   Capability).
2. ✅ §12 exists, describes the load-gated narrative ontology, links
   to AGENTS.md NO.1–NO.6.
3. ✅ R.1–R.20 numeric values preserved; R.21 appended at next free
   identifier per R.10.
4. ✅ ADR 0006 (renumbered from the planned 0001 due to slot
   collision) is `adr_status: Accepted`; synthesize rewrote AGENTS.md
   guarded block.
5. ✅ `tools/check-governance.sh` exits 0.
