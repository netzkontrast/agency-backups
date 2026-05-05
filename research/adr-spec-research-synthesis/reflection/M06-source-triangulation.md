---
type: note
status: active
slug: adr-spec-research-synthesis-m06
summary: "M06 Source Triangulation matrix: every analysis finding cited in ≥ 2 source files."
created: 2026-05-05
updated: 2026-05-05
---

# [M06] Source Triangulation

Per the originating Gemini research prompt, every factual claim used to seed `workspace/analysis.md` and `output/SPEC.md` MUST be confirmed in ≥ 2 independent source files.

## Triangulation Matrix

| Claim (analysis ID) | Source 1 | Source 2 | Source 3 (optional) | Triangulated |
|---|---|---|---|---|
| I1 — Layered frontmatter (L0–L3), depth ≤ 1 | `TASK.md §3` | `AGENTS.md` "Frontmatter Ontology" | `maintenance/schemas/header-ontology.json` | yes |
| I2 — Audit graph via frontmatter only | `FOLDERS.md §6` | `TASK.md §3.3` | `RESEARCH.md §3` | yes |
| I3 — `/research/` is canonical for synthesis (no `docs/`) | `FOLDERS.md §1` (only 3 operational folders) | `FOLDERS.md §8` (exemption table excludes `docs/`) | filesystem absence of `docs/` | yes |
| I4 — Operational folders are exactly three | `FOLDERS.md §1` | `FOLDERS.md §7 anti-pattern` | `AGENTS.md "Task Type Routing"` | yes |
| I5 — RFC 2119 + Gherkin are the spec language | `AGENTS.md §"Spec Language Reference"` | every existing root spec uses both | `header-ontology.json` `body_schema.gherkin_block` | yes |
| I6 — `claude/<topic>-<date>` branch + `/sc:createPR` closure | `AGENTS.md §"Closing Run Procedure"` | current branch matches the pattern | Gemini draft §0 cites it | yes |
| I7 — Repair tiers T1/T2/T3/T4 | `MAINTENANCE.md §1` | `MAINTENANCE.md §3.5` | references throughout `tasks/` | yes |
| I8 — Research workspaces immutable post-`complete` | `MAINTENANCE.md §1` (T4) | `RESEARCH.md §7` | `PROMPT.md §7` | yes |
| I9 — `tools/check-governance.sh` is the gate | `PRE_COMMIT.md §7` | `tools/check-governance.sh` | `MAINTENANCE.md §1.1` | yes |
| I10 — `AGENTS.md` mixes hand-authored + accreted content | `AGENTS.md` body inspection | `AGENTS.md` LOOP_LOG section explicitly says "Jules appends one record per iteration. Do not edit manually." | — | yes |
| I11 — `header-ontology.json` is the binding source for tooling | `header-ontology.json` `$schema-note` | `TASK.md §3` ("the JSON wins for `tools/fm/validate.py`") | `tools/fm/validate.py` reads it | yes |
| I12 — Friction-log mandatory at every closure | `FRUSTRATED.md` | `RESEARCH.md §5.9` | `TASK.md §7.7` | yes |
| I13 — Supersession reciprocity required | `TASK.md §4.7` | `TASK.md §6 (Reciprocity audit scenario)` | `tasks/readme.md` lineage annotations | yes |
| I14 — External research routes via `/research/<provider>/<slug>/` + Task | `RESEARCH.md §6` | `tasks/003-analyze-skillmd-novel-authoring/` precedent | `research/gemini/...` directory exists | yes |
| C1 — Gemini's `docs/decisions/` does not match `FOLDERS.md` | `FOLDERS.md §1` | filesystem check | Gemini §2 makes the conflicting claim | resolved |
| C3 — `AGENTS.md` is not safe to overwrite wholesale | `AGENTS.md` body | LOOP_LOG accretion pattern | `AGENTS.md` "Closing Run Procedure" hand-authored normative prose | resolved |
| C4 — No `agency-adr` CLI exists | `tools/` directory listing | `tools/check-governance.sh` does not invoke it | — | resolved |
| C7 — `AGENTS.md` already exceeds 2,000 tokens | `wc -w AGENTS.md` ≈ 3,600 words ≈ 4,800 tokens | the file's own "Frontmatter Ontology" + "Narrative Ontology" sections are each substantial | — | resolved |

## Single-Source Claims (Flagged for Caution)

| Claim | Single source | Justification |
|---|---|---|
| The `bcp14-keyword` fidelity-mode is "deterministic enough" for the v0 metric. | this synthesis run only | This is a *design proposal*, not an empirical claim. It is explicitly routed to Task 029 / Task 028 for falsification. |
| Token-limit 2,000 is "aspirational" rather than achievable for the current `AGENTS.md`. | `wc -w` heuristic only | The empirical token count requires a tokeniser; the heuristic is a lower bound. The `[OPEN]` item in §8 of `output/SPEC.md` makes this falsifiable. |

## Method Audit

[M06] was applied at every claim-introduction point in `analysis.md`. No factual claim survived without a triangulating second source except for the design proposals above, which are flagged in §8 of `output/SPEC.md` as `[OPEN]` items.
