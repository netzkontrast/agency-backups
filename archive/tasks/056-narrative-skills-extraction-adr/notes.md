---
type: note
status: active
slug: 056-narrative-skills-extraction-adr-notes
summary: "Implementation notes for Task 056 — inventory of the narrative footprint, option tradeoffs, and the ADR-0008 status-quo decision with five falsifier triggers."
created: 2026-05-11
updated: 2026-05-11
---

# Task 056 — Implementation Notes

## 1. Narrative-skill footprint inventory

Measured 2026-05-11 on `claude/complete-three-tasks-n3fZR`.

### Skill folders

| Folder | Files | Markdown | Size |
|---|---:|---:|---:|
| `skills/dramatica-theory/` | 18 | 17 | 962 KB |
| `skills/dramatica-vocabulary/` | 26 | 26 | 442 KB |
| `skills/ncp-author/` | 49 | 25 | 567 KB |
| `skills/novel-architect/` | 16 | 14 | 132 KB |
| `skills/the-agency-system-architect/` | 12 | 8 | 66 KB |
| `skills/suno-lyric-writer/` | 7 | 7 | 47 KB |
| **Total** | **128** | **97** | **~2.2 MB** |

### Supporting infrastructure

| Path | Files | Size |
|---|---:|---:|
| `maintenance/schemas/narrative-ontology/` | 19 | ~520 KB |
| `tools/dramatica-nav/` | 34 | ~250 KB |
| **Combined narrative footprint** | **181** | **~3.0 MB** |

### Cross-references into the four root specs

| Spec | Narrative-related lines | Surface |
|---|---:|---|
| `AGENTS.md` | ~70 (lines 290–356) | `## Narrative Ontology` section + NO.1–NO.6 rules |
| `SKILLS.md` | 3 lines | Type-enum example + ladder language at line 235 |
| `PRE_COMMIT.md` | 7 lines | Linter table entries for `dramatica-nav/validate.py` + `cleanup.py` |
| `MAINTENANCE.md` | 2 lines | Step `[opt]` narrative-ontology pair (gated on `ontology.json`) |

The AGENTS.md `## Narrative Ontology` section is **8.6 KB / ~2150 tokens** (4 chars/token estimate). The 9-spec bootstrap bundle (per README §10) is ~50 K tokens; the narrative section is **~4 % of session boot**.

### Tasks / prompts / research workspaces touching narrative paths

A `find . -maxdepth 3 -type d -iname "*narrative*|*dramatica*|*ncp*|*novel*"` returns 17 directories beyond the root specs:

- `tasks/003-analyze-skillmd-novel-authoring/`
- `tasks/015-integrate-dramatica-ncp-skills/`
- `tasks/030-cleanup-dramatica-skills-corpus/`
- `tasks/042-dramatica-nav-followups/` (**open**)
- `tasks/056-narrative-skills-extraction-adr/` (this task)
- `prompts/github-skillmd-novel-authoring-de-en/`
- `prompts/integrate-dramatica-ncp-skills/`
- `prompts/tooling-narrative-ontology-load-discipline/`
- `research/gemini/github-skillmd-novel-authoring-de-en/`
- `research/integrate-dramatica-ncp-skills/`
- `research/ncp-novel-co-authoring-spec/`
- `skills/{dramatica-theory,dramatica-vocabulary,ncp-author,novel-architect,the-agency-system-architect,suno-lyric-writer}/`
- `tools/dramatica-nav/`
- `maintenance/schemas/narrative-ontology/`

Any extraction or namespace migration ripples through all of these.

## 2. Option tradeoff matrix

| Axis | O1 Extract | O2 Isolate (`skills/narrative/`) | O3 Status quo |
|---|---|---|---|
| Session-boot token saving | ~4 % | ~4 % (offset by new root spec) | 0 % |
| Migration cost | High | Medium | Zero |
| Audit-graph integrity | Cross-repo coordination | Preserved | Preserved |
| In-flight Task disruption | Tasks 030/042/015 break | Tasks 030/042 retarget | None |
| Future-narrative-skill cost | Trivial (no negotiation) | Low (under new namespace) | Low (same `/skills/<name>/`) |
| Contributor onboarding | Two-repo discipline | New `NARRATIVE.md` to read | NO.5 workaround to learn |

The decisive factor: **migration cost is non-trivial and the workaround is mechanically enforced**. Until friction-pattern data justifies the spend, status quo is the rational choice.

## 3. The ADR

Authored at [`decisions/0008-narrative-skills-status-quo.md`](../../decisions/0008-narrative-skills-status-quo.md), `adr_status: Proposed`. Validates clean against `python3 tools/adr/cli.py validate` (1 → 0 diagnostics after summary trimmed to ≤ 240 chars).

The ADR records **five falsifier triggers** (F1–F5) that, when any fires, mandate a successor ADR re-evaluating Options 1 and 2 against then-current evidence:

- **F1** Narrative-skill count > 10 (today: 6).
- **F2** Bootstrap-bundle token cost > 60 K (today: ~50 K).
- **F3** Sustained FL1+ friction citing NO.5 across ≥ 3 sessions in a 14-day window.
- **F4** Narrative-skill change requires T3 amendment to a root spec *other than* `SKILLS.md` or AGENTS.md `## Narrative Ontology`.
- **F5** Third-party adopter requires narrative-content exclusion as a hard prerequisite.

The ADR ships at `Proposed` rather than `Accepted` because the triggers have not yet been observed; ratification to `Accepted` would prematurely lock the topology against the evidence the triggers are designed to surface.

## 4. Why no successor implementation Task is opened

The status-quo decision requires no migration; future migration (if a trigger fires) is the responsibility of the successor ADR's implementation Task, not this one. Opening a pre-emptive migration Task today would invert the falsifier logic (commit to the migration before observing the friction that justifies it).

## 5. Falsifiability check

The Goal's falsifiable outcome was: "a new ADR under `decisions/<NNNN>-narrative-skills-extraction.md` is ratified (`adr_status: Accepted` or `Proposed` with a follow-up implementation Task), recording one of {extract-to-sibling-repo, isolate-as-`skills/narrative/` namespace with own root spec, status-quo with rationale}."

Satisfied:

1. ADR landed at `decisions/0008-narrative-skills-status-quo.md` (`narrative-skills-status-quo` slug chosen over `narrative-skills-extraction` because the decision is *non*-extraction — the slug should reflect the choice, not the rejected option).
2. `adr_status: Proposed` per the task's permitted set.
3. The three options are all evaluated in §"Considered Options"; the chosen one (status quo) is named in §"Decision Outcome".
4. No follow-up implementation Task is opened — justified in §4 above and in the ADR's §"Consequences".
