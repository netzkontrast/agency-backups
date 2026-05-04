# Scenario-Tag Survey

First-pass mapping of the eleven personas-scenarios from [`/tasks/013-integrate-dramatica-ncp-skills/task.md § Personas and Working Scenarios`](../../../tasks/013-integrate-dramatica-ncp-skills/task.md) to candidate term files. **Confidence: medium.** This is a starting heuristic for Task 013 plan step 6 ("tag the top-≥40 terms"); the final per-term tagging happens during that step by reading individual term sections, not whole files.

The schema's `scenarios: ≤8` per-term cap is enforced in the schema; the per-scenario candidate counts below are *first-pass*, expected to be filtered down to 8 or fewer per term by the downstream tagger.

## Persona A — Novel Author Anna

### `novel.storyform-slot-fill`

> Filling a Storypoint slot for a Throughline.

| File | Candidate term count | Why |
|---|---:|---|
| `elements.md` | ~25 | Every MC/OS/IC/RS Problem / Solution / Symptom / Response candidate is an Element. |
| `variations.md` | ~25 | Every Issue slot resolves to a Variation. |
| `types.md` | ~16 | Every Concern slot resolves to a Type. |
| `overview-appreciations.md` | ~10 | Story-level Goal / Outcome / Limit slots. |
| `dynamic-pairs-index.md` | reference-only | Used by the slot-fill validator, not tagged per term. |
| **Estimated terms tagged** | **~20** (top-shelf only) | The full ~76 cap is too noisy; tag only the ~20 most-loaded slots. |

### `novel.act-pivot`

> Designing the Act-2/Act-3 hinge.

| File | Candidate term count | Why |
|---|---:|---|
| `types.md` | ~16 | The 16 Types are the act-level signposts. |
| `structural-terms.md` | ~6 | Act, Signpost, Journey, Sequence definitions. |
| `plot-dynamics.md` | ~4 | Driver pivot semantics. |
| **Estimated terms tagged** | **~10** | |

### `novel.crucial-element-audit`

> Auditing whether a draft really pivots on its declared Crucial Element.

| File | Candidate term count | Why |
|---|---:|---|
| `elements.md` | ~64 | Every Element is a candidate Crucial Element host. |
| `dynamic-pairs-index.md` | reference-only | Crucial-Element ↔ partner pair detection. |
| `dramatica-fundamentals.md` | ~3 | Resolve + Crucial-Element pairing rules. |
| **Estimated terms tagged** | **~25** | Tag the most common Crucial-Element hosts (Trust/Test, Logic/Feeling, Pursue/Avoid, Pursuit/Reconsider, Control/Uncontrolled, etc.). |

### `novel.character-arc`

> Designing or diagnosing a character arc.

| File | Candidate term count | Why |
|---|---:|---|
| `archetypes.md` | 8 | One tag per archetype. |
| `character-dynamics.md` | ~4 | Resolve, Growth, Approach, Problem-solving Style. |
| `elements.md` | ~16 | The eight motivation pairs (one Element per archetype-half). |
| **Estimated terms tagged** | **~12** | |

### `novel.diagnose-flat-draft`

> Diagnosing why a draft feels flat.

| File | Candidate term count | Why |
|---|---:|---|
| `essential-questions.md` | 8 | The diagnostic question set. |
| `storyform-mechanics.md` | 5 | Consistency rules. |
| **Estimated terms tagged** | **~6** | These are mostly *concept* entries; pointers to anti-patterns / heuristics chapters via `term_file`. |

### `novel.dual-storyform`

> Encoding two parallel Storyforms (A + B) for an interference-style novel.

| File | Candidate term count | Why |
|---|---:|---|
| `storyform-mechanics.md` | ~3 | Throughline distribution + diametrality rules apply per storyform. |
| `dramatica-fundamentals.md` | ~2 | Class-distribution constraints. |
| **Estimated terms tagged** | **~3** | Highly specific; few candidates. |

## Persona B — Organist / Lyric Architect Otto

### `lyric.verse-chorus-pair`

> Choosing the Element-pair that drives Verse↔Chorus tension.

| File | Candidate term count | Why |
|---|---:|---|
| `elements.md` | ~32 | The 32 Element-pairs (16 dynamic pairs at Element level). |
| `dynamic-pairs-index.md` | reference-only | The pair index. |
| **Estimated terms tagged** | **~16** | One tag per Element half of a high-frequency pair (Control/Uncontrolled, Logic/Feeling, Trust/Test, etc.). |

### `lyric.bridge-pivot`

> Designing a track bridge that flips the pair.

| File | Candidate term count | Why |
|---|---:|---|
| `element-quads.md` | 16 | The Quad geometry tells you which pair flips at the Bridge. |
| `dynamic-terms.md` | ~7 | Dynamic / companion / dependent pair semantics. |
| **Estimated terms tagged** | **~10** | |

### `lyric.album-arc-mapping`

> Mapping an album to a Story Driver / Outcome / Judgment.

| File | Candidate term count | Why |
|---|---:|---|
| `plot-dynamics.md` | ~13 | Driver, Limit, Outcome, Judgment plus the four ending categories. |
| `overview-appreciations.md` | ~6 | Story-wide appreciations. |
| **Estimated terms tagged** | **~8** | |

### `lyric.archetype-as-system-part`

> Mapping system architecture parts onto archetypes.

| File | Candidate term count | Why |
|---|---:|---|
| `archetypes.md` | 8 | One tag per archetype. |
| `elements.md` | ~16 | The motivation pairs each archetype carries. |
| **Estimated terms tagged** | **~10** | |

### `lyric.refrain-as-restatement`

> Refrain as the structural restatement of the same Element.

| File | Candidate term count | Why |
|---|---:|---|
| `dynamic-terms.md` | ~7 | Companion-pair vs. dynamic-pair distinction. |
| `element-quads.md` | 16 | Quad geometry primer. |
| **Estimated terms tagged** | **~6** | |

## Aggregate

| | Estimated tags emitted | Median per scenario |
|---|---:|---:|
| Novel Author scenarios (6) | ~76 | ~12 |
| Lyric Architect scenarios (5) | ~50 | ~10 |
| **Combined** | **~126 tags across ~80 terms** | **~2.4 scenarios per term (well below cap)** |

**Hot terms** likely to carry the most scenario tags (≥3 each):
- Element halves of the high-frequency pairs: Trust/Test, Logic/Feeling, Pursuit/Avoid, Control/Uncontrolled, Cause/Effect.
- The 8 Archetypes (each carries an arc-design tag + a system-part tag).
- The 4 Plot Dynamics (Driver, Limit, Outcome, Judgment).
- Crucial Element (concept) — tagged across `novel.storyform-slot-fill`, `novel.crucial-element-audit`, `novel.character-arc`, `novel.diagnose-flat-draft`.

## Falsification check (M01 self-applied)

The `task.md` design hypothesis was *"per-term frontmatter is sufficient to power scenario-keyed lookup without a separate scenario index."* This survey's median of ~2.4 scenarios per tagged term, and the 8-cap holding for every hot term, **leaves the hypothesis intact** for the kickoff phase. Re-test after Task 013 plan step 6 produces real per-term tags; if the median drifts above 5, the navigator MUST also build `scenario-index.json` per the M01 contingency in `methodology.md`.

## What this survey does not do

- Does not authoritatively tag any term. The actual `scenarios: [...]` list per term is produced in Task 013 plan step 6.
- Does not stretch beyond the 11 scenarios defined in `task.md`. New scenarios go through the proposal procedure declared in `task.md § Scenario Taxonomy Rules`.
