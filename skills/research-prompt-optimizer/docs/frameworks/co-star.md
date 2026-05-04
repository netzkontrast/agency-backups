# CO-STAR — Context · Objective · Style · Tone · Audience · Response

**File:** `modules/frameworks/co-star.md`
**Type:** framework
**Role:** structural_layer
**Override trigger:** `audience tone is decisive AND output is for external/non-expert reader`
**Override priority:** 1 (highest priority — fires first when conditions match)
**Self-applied in Phase 2:** no

## Purpose

Specialized framework for research where the **output recipient
shapes the form** as much as the content. Public-facing reports,
non-expert briefings, executive summaries, marketing intelligence
deliverables. The Style + Tone + Audience axes are what RISEN
under-specifies. CO-STAR forces explicit calibration of voice.

## Slot inventory

This module has **no frontmatter slots** — body is paste-ready
template with 6 fixed sections.

**Structural markers:** none.

## Body composition

- **Section anchors:** 6 fixed sections — `## Context`,
  `## Objective`, `## Style`, `## Tone`, `## Audience`, `## Response`
- **Order constraint:** Audience comes near the end intentionally —
  it's the *constraint* that filters the otherwise-free Style + Tone
  choices upstream
- **Composition partner:** sits above ReAct. Pairs well with
  M04 Contrast Classes (audience-sensitive evaluative claims need
  explicit contrast classes) and `categories/a-exploration.md` when
  exploration outcomes need to land for non-expert audiences

## Split decision

**Currently:** single file
**Should it split?** No — the 6 sections cohere as one voice-
calibration framework.

## Future extension points

1. **Audience-tier vocabulary.** Currently free-text. Add
   `{{audience_tier}}` enum (`expert` | `informed_general` |
   `lay_public` | `child`) to make tier choices systematic and
   surface-able for review.
2. **Style + Tone partial.** A future
   `partials/style-tone-calibration.md` could provide canonical
   style/tone matrices (e.g., "executive briefing" → terse +
   neutral + numerate) that CO-STAR pulls from rather than
   regenerating per intent.
3. **Multi-audience output.** When the same research must produce
   variants for different audiences (Cat-B with multiple
   stakeholders), CO-STAR currently produces one calibration.
   Future: `{{audience_variants}}` (list) to drive multi-output.

## Open questions

- [ ] Override priority 1 (highest) means CO-STAR wins when
      audience-tone is decisive AND another framework also matches.
      Is "audience-tone is decisive" the right tiebreaker, or should
      it be intent-explicit (`intent.output_calibration_priority`)?
- [ ] When CO-STAR fires alongside Cat-B (extraction with audience),
      RISEN's Expectations and CO-STAR's Response overlap. Pure
      bespoke synthesis territory? Currently CO-STAR replaces RISEN
      wholesale.

## Catalog cross-reference

- Catalog: `modules.co-star`
- Override trigger: `audience tone is decisive AND output is for
  external/non-expert reader`
- Override priority: 1
- Default for: (none — selected by override)
- Pairs well with: M04, Cat-A (when exploration → public output)
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
