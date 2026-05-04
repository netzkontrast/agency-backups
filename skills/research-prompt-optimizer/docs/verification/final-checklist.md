# Verification — Self-Verification Checklist for the Executing AI

**File:** `modules/verification/final-checklist.md`
**Type:** verification
**Mandatory:** yes (always rendered into every prompt as the final
section, after Synthesis)
**Self-applied in Phase 2:** no (this checklist is for the executing
agent at the END of execution; Phase 2 has its own integrity check
via M4 self-applied variant)

## Purpose

Final 11-item self-audit the executing agent runs **after Synthesis
is complete** and **before delivering output to the user**. Each
item is a yes/no check tied to a specific module's contract: did
M01 fire on every hypothesis, did M07 log every contradiction, did
M13 expand on at least K axes, etc. The checklist is the agent's
own structural integrity gate — output is not delivered until all
11 pass (or failed items are explicitly flagged with reason).

## Slot inventory (no agent-runtime slots; checklist items are fixed)

This module has **no parameterized slots**. The 11 items are fixed
text. Agent fills the answers (✓ / ✗ / N/A with reason) inline at
runtime.

**Structural markers (NOT slots — agent-runtime counters):**

- `[K]`, `[M]`, `[N]` — counter placeholders the agent fills with
  actual numbers from their run (e.g., "queries expanded along K
  axes", "M independent sources cited per claim")
- `[enumerate]` — agent-runtime instruction for items requiring lists

## Body composition

- **Section anchor:** `## Self-Verification Checklist`
- **Order constraint:** very last section of every rendered prompt,
  AFTER `partials/synthesis-schema.md`. Output delivery is gated on
  passing this checklist.
- **Composition partner:** validates outputs of EVERY active module —
  M01..M13 methods, M0..M4 replication, all cross-pollination
  modules, the structural framework's section coverage. The single
  most cross-cutting verification artifact.

## Split decision

**Currently:** single file
**Should it split?** No — the checklist is one gate; splitting
defeats the all-or-nothing semantics. Like M4, the value comes from
treating it as a single hard pass/fail.

## Future extension points

1. **Per-item severity tags.** Currently all 11 items are equal
   gates. Some (e.g., "all CBs honored") are hard; others (e.g.,
   "M13 expansion at minimum cadence") could be soft. Add
   `severity` per item.
2. **Domain-specific checklist extensions.** Cat-B compliance
   research could add item 12: "every Don't from TIDD-EC verified
   not violated". Cat-C could add: "Resumption Protocol fired at
   session start". A `{{domain_extra_items}}` slot driven by
   category + framework + active modules could append.
3. **Failure-handling protocol slot.** Current behavior on failed
   item is "flag with reason". A `{{failure_handling_protocol}}`
   slot could enable `flag_only` | `block_delivery` |
   `request_user_review` per item.
4. **Checklist-result archive.** For Cat-C lifecycle research, the
   per-session checklist results should accumulate. A future slot
   `{{checklist_result_log}}` tied to the persistent knowledge
   store would enable cross-session integrity audits.

## Open questions

- [ ] The 11 items are listed but not formally numbered/named
      against module contracts in the body. Should there be a
      mapping table (item N → module M's contract item C) for
      auditability?
- [ ] When the checklist fails on item K, current behavior is
      "flag with reason and continue to next item". Should item K's
      failure block subsequent items (gating)? Currently
      independent.
- [ ] The 11-item count is hard-coded. As new mandatory modules
      are added (future v3.1, v3.2), the count grows. Should the
      checklist auto-derive items from active mandatory modules
      rather than enumerate inline?

## Catalog cross-reference

- Catalog: `modules.final-checklist` (declared in catalog as the
  single verification module)
- Mandatory: yes (universal in every rendered prompt)
- Self-applied hook: no
- Consumes: outputs of every active module (cross-cutting)
- Gates: output delivery to user

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
