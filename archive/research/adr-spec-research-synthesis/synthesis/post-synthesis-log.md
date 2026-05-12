---
type: note
status: active
slug: adr-spec-research-synthesis-post-synthesis-log
summary: "Chronological merge log: how /workspace and /reflection findings were folded into output/SPEC.md §0–§9."
created: 2026-05-05
updated: 2026-05-05
---

# Post-Synthesis Log

Per-section merge log for [`../output/SPEC.md`](../output/SPEC.md). Each row records the section, the upstream artefacts that were merged in, and any open loops left behind.

| Section | Source artefacts | Open loops surfaced |
|---|---|---|
| §0 Status & Provenance | `analysis.md §A` (implicit decisions), `prompt.md` (run-start snapshot), Gemini §0 (world-change) | none |
| §1 Normative Conventions | `AGENTS.md "Spec Language Reference"` (RFC 2119), `header-ontology.json` (BCP-14 keyword density), `M07-contradictions.md` row C5 (exit-code convention) | none |
| §2 System-Level Conventions | `analysis.md §B` (B1–B11), `brainstorm.md Q1, Q2, Q4` (path, CLI, AGENTS.md ownership), `M07 row C1, C3, C4, C10` | guarded-section marker placement → `[DEFERRED to Task 028]` |
| §3 Aspect 1 — Explore | `analysis.md §A` (implicit decisions seed), `RESEARCH.md §1, §2` (research run convention), `brainstorm.md Q5` (migration corpus) | migration cardinality → `[OPEN]` |
| §4 Aspect 2 — Plan | `TASK.md §3.3 Prompt namespace` (frontmatter shape), MADR template (Gemini §4), `brainstorm.md Q3` (frontmatter composition) | none |
| §5 Aspect 3 — Implement | `M13-query-expansion.md §3 (orthogonal MDL)` (token budget), Gemini §5 (MDL framing), `brainstorm.md Q4` (guarded-section), `M07 row C7, C8` (token-limit, fidelity) | fidelity-metric algorithm → `[OPEN]`; token-limit empirical floor → `[OPEN]` |
| §6 Aspect 4 — Review | `TASK.md §4.7, §8.7` (supersession reciprocity, blocker chain), `MAINTENANCE.md §1` (T4 immutability), `M07 row C9` (ADR immutability) | none |
| §7 Aspect 5 — Validate | `header-ontology.json` (composition target), `tools/fm/validate.py` (Diag shape), `tools/check-governance.sh` (gate composition), `brainstorm.md Q2` (CLI co-location) | none |
| §8 Known Limitations & Open Questions | five `[OPEN]` items + two `[DEFERRED]` items rolled up from `brainstorm.md` "Open Items Roll-Up" | every `[OPEN]` and `[DEFERRED]` lives here with owner + unblock condition |
| §9 Knowledge Base Index | `M06-source-triangulation.md` matrix (sources used), `M07-contradictions.md` table (resolved tensions), `M13-query-expansion.md` (axis log) | none |

## Merge Order

1. §1 first — locks the normative vocabulary the rest of the spec uses.
2. §0 second — references §1's vocabulary for the world-change annotation.
3. §2 third — declares the system invariants every aspect inherits.
4. §3–§7 in MADR-aspect order (Explore → Plan → Implement → Review → Validate).
5. §8 last among normative sections — a parking lot for `[OPEN]` items requires the rest of the spec to be drafted so each item can cite its blocking section.
6. §9 finalises the audit (sources, contradictions, axis log).

## Bytes-Equivalence Check

The Gemini draft was used as a *structural template* (§0–§9 ordering, table schemas) but no §X.1 row, §X.2 Gherkin scenario, or §X.3 paragraph is a verbatim copy. The repo-native §2 introduces conventions absent from Gemini (guarded-section markers, `decisions/` path); the repo-native §7 inverts the schema from `id/title/status/date` to `slug/adr_id/adr_status` (per `M07-contradictions.md row C2`).

## Idempotency

A second run of this synthesis under unchanged inputs produces a byte-identical `output/SPEC.md`. This is asserted (not yet verified by tooling) per the deterministic-merge convention; once Task 028 ships `agency-adr synthesize`, the assertion becomes a Gherkin acceptance test.
