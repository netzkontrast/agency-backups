# M07 — Contradiction Log

**File:** `modules/methods/m07-contradiction-log.md`
**Type:** method
**Mandatory:** no (default for Cat-B and Cat-C)
**Self-applied in Phase 2:** yes (sub-phase 4.1 — scan intent for internal inconsistencies)

## Purpose

Maintain a structured log of every contradiction encountered during
research — not silent resolution, not premature dismissal. Counters
the failure mode where the agent picks one side of a disagreement
without telling the reader, leaving the reader unable to assess
confidence. The log becomes part of the final output.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `claim_x` | `agent_runtime_fill` | agent at runtime | yes | One side of the contradiction (claim X) |
| `claim_not_x` | `agent_runtime_fill` | agent at runtime | yes | The opposing claim (not X, or X with materially different specifics) |

**Structural markers:** none. Body is pure prose.

## Body composition

- **Section anchor:** `### Method: Contradiction Log`
- **Order constraint:** standalone — placed in methods sequence per
  category default order
- **Composition partner:** pairs with M06 Source Triangulation
  (triangulation surfaces contradictions; the log captures them) and
  M09 Red Team (red team adversarially seeks contradictions; the log
  is the structured output)

## Self-applied hook detail (sub-phase 4.1)

When Phase 2 loads `intent.yaml` and validates it, M07 fires as a
silent scan for internal inconsistencies. Examples:
- `depth=surface` + `output_format=exhaustive matrix` (cheap research
  + expensive output)
- `temporal_scope=last 3 months` + `priors=well-established theory
  pre-2020` (recent vs. settled)
- `output_language=de` + `source_priority=English-only journals`

Findings land in `meta-prompt.self_reflection.contradictions[]` and
surface in the plan view so the user sees them before approval.

## Split decision

**Currently:** single file
**Should it split?** No — log mechanism is one cohesive structure.

## Future extension points

1. **World-Change Log distinction.** For Cat-C lifecycle research,
   contradictions can mean "sources disagree about state of the world"
   OR "the world changed". Cat-C body of c-lifecycle.md mentions a
   World-Change Log; could become a sibling module
   `m7b-world-change-log.md` with cross-reference, OR an enum slot
   `{{contradiction_type}}: source_disagreement | world_change`.
2. **Severity-tier slot.** Currently all contradictions are equal in
   the log. Add `{{severity}}: low | medium | high` (matches
   `meta-prompt.self_reflection.contradictions[].severity` from
   self-applied hook) and use it to drive output prioritization.
3. **Resolution-status flag.** Some contradictions are resolved during
   research (one side debunked). Add `{{resolution_status}}: open |
   resolved | unresolvable` to mark which need reader attention.

## Open questions

- [ ] The self-applied hook detects intent-level contradictions; the
      runtime use detects research-level contradictions. Should these
      land in the same `contradictions[]` field with a `source: phase2 |
      runtime` discriminator, or in separate fields?
- [ ] `escape_criterion` says "If log >10 entries, consider the
      research question may be ill-posed". Should this become a
      structural alert (`if len(contradictions) > 10 → warn user`) or
      stay as guidance?

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.M07`
- Triggered by signals: `conflicting reports`, `contradictions`,
  `disagreement`
- Default for category: B, C
- Pairs well with: M06, M09
- Self-applied hook (catalog): `sub_phase: 4.1`,
  `depth_active: [standard, exhaustive]`

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
