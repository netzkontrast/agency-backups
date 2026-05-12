---
type: note
status: active
slug: adr-corpus-extraction-friction-log
summary: "Mandatory friction log for the ADR corpus extraction run. Highest FL declared at top per FRUSTRATED.md."
created: 2026-05-07
updated: 2026-05-07
---

# Friction Log

**Highest Frustration Level: FL1**

## FL Declaration

The extraction completed substantively per the ST-1 contract. One FL1 entry; no FL2 or FL3.

## Entries

### Entry 1 — Condensed-mirror vs full-prose round-trip ambiguity (FL1)

**What happened.** The ST-1 contract requires `output/SPEC.md` to render each candidate "MADR-shaped" but allows the SPEC to "be condensed table-style for the SPEC, full prose only for the 5 ratified files". This produces two surfaces (condensed mirror in SPEC §3, full MADR prose in `/decisions/0001…0005`) that must agree forever. There is no mechanical check today that detects drift between the SPEC mirror and the ratified file. I documented the round-trip obligation explicitly in the SPEC §1.3 and in the workspace `readme.md` Workflow Assumptions, but the rule is honour-system until a successor Task adds a validator.

**Suggested process tweak.** A future Task SHOULD add a `tools/adr/cli.py` sub-check that diffs the ratified `Decision Outcome` and `Consequences` body sections against the SPEC §3 condensed mirror; ERROR on substantive divergence. This composes naturally with the existing `agency-adr validate` flow.

**Cost.** ≈ 5 minutes deciding how to phrase the round-trip obligation in a way that did not weaken the SPEC's authoritativeness.

## Boundaries Honoured

- ✓ The eight root specs were not modified.
- ✓ The ratified ADR files use `adr_status: Proposed` so they do not enter the synthesised AGENTS.md guarded section.
- ✓ Every IADR cites a `file:line` evidence anchor; no synthesised clauses.
- ✓ Three predecessor IADRs from `research/adr-assumption-audit/output/REPORT.md` §2 are cited explicitly.
- ✓ Four candidates documented as rejected in SPEC §6 for false-positive control (target was ≥3).
- ✓ `python3 tools/adr/cli.py validate` and `python3 tools/adr/cli.py synthesize --dry-run --token-limit 6000` both exit 0 against the new corpus.

## Aggregate FL Pattern (For Maintenance)

The recurring research-proposal-prompt friction recorded in Task 027 and Task 029 friction logs ("ambiguity about literal sub-agent invocation") did not surface this run; ST-1 is single-agent execution by construction. The new friction surfaced here (round-trip obligation between SPEC mirror and ratified file) is *novel* but follows the same pattern as the SPEC §8 OQ.5 deferral — a process gap in the lifecycle of a Proposed ADR that a successor Task SHOULD pick up after the third occurrence.
