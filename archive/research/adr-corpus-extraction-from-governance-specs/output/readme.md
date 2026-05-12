---
type: index
status: active
slug: adr-corpus-extraction-output
summary: "Output directory for the ADR corpus extraction run. Holds SPEC.md — the authoritative IADR catalogue."
created: 2026-05-07
updated: 2026-05-07
---

# Output

- [`SPEC.md`](./SPEC.md) — Authoritative IADR catalogue. 18 candidates total; 5 ratified to `/decisions/` as `adr_status: Proposed`; 4 rejected in §6 for false-positive control.

`research_phase: complete`. The SPEC is the source of truth for the IADR inventory; ratified ADR files in `/decisions/` are MADR full-prose round-trips of the §3 condensed entries.
