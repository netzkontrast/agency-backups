---
type: index
status: active
slug: dramatica-scenarios-epic
summary: "Directory index for Task 078 — the dramatica-scenarios Epic umbrella. Spawns 12-18 child Tasks across 4 cohorts (Foundation, Discovery, Authoring, Integration) per the SPEC.md the foundational research prompt will produce."
created: 2026-05-11
updated: 2026-05-11
---

# Task 078 — `dramatica-scenarios` Epic

**What:** An Epic Task that replaces `tools/dramatica-nav/nav.py`'s filename-
pointer indirection (the `term_file` field) with a theory-grounded scenario-
content corpus. Every `novel.*` scenario gets a populated
`skills/dramatica-theory/scenarios/<id>.md`; `nav.py` gets a new `instruct`
subcommand that returns embedded content with file:line citations rather
than a path the caller must dereference.

**Why here:** Matches the Task 070 Epic pattern. The umbrella Task tracks
overall progress; the actual work happens in child Tasks (079..08N) spawned
from the foundational research SPEC.md.

## Navigation

- [`task.md`](./task.md) — Epic spec, plan, todo (10 items).

## Spawns

- **Research workspace:** `research/dramatica-scenarios-foundation/`
  (slug-equality with the prompt that drives it).
- **Foundational prompt:**
  [`prompts/dramatica-scenarios-foundation/prompt.md`](../../prompts/dramatica-scenarios-foundation/prompt.md)
  — already drafted and reader-test-audited; awaiting dispatch to an
  external deep-research agent.
- **Child Tasks:** `tasks/079-…/` through `tasks/08N-…/` per cohort.
  Exact list materializes after SPEC.md §3.4 (FINAL scenario taxonomy)
  and §4 (Epic decomposition recommendation) land.

## Cohort summary (planning placeholder)

| Cohort | Tasks | Status | Blocked by |
|---|---|---|---|
| Research (Phase A) | This Epic body + 1 research run | in_progress (prompt drafted, dispatch pending) | — |
| Cohort 1 — Foundation | ≥ 3 child Tasks (content-template, line-index, nav.py instruct) | not-spawned | SPEC.md §4.1 |
| Cohort 2 — Discovery confirmation | 1 child Task (ontology.json taxonomy update) | not-spawned | SPEC.md §3.4 + §4.2 |
| Cohort 3 — Authoring | `N` child Tasks (`N ≥ 9` per prompt acceptance signal #6) | not-spawned | Cohorts 1 + 2 |
| Cohort 4 — Integration | ≥ 2 child Tasks (novel-architect wire-up, integration tests) | not-spawned | Cohort 3 |

## Audit graph

```text
tasks/078-dramatica-scenarios-epic/task.md
        │ task_uses_prompts ──► prompts/dramatica-scenarios-foundation/prompt.md
                                        │ executed by agent ──► research/dramatica-scenarios-foundation/output/SPEC.md
                                                                        │ SPEC drives ──► tasks/079..08N/ (child Tasks)
                                                                                                                │ child Tasks affect ──► skills/dramatica-theory/scenarios/*.md
                                                                                                                                                  │ + tools/dramatica-nav/nav.py (instruct subcommand)
                                                                                                                                                  │ + ontology.json (line-index + scenario tags)
```

## Assumptions Log

- The foundational research prompt's Phase-4 reader-test surfaced 5 P0/P1/P2
  fixes (counts, vocab enumeration, citation-rule relaxation, cohort-count
  hard-coding, cross-corpus balance, reader-test reception protocol) — all
  applied to `prompts/dramatica-scenarios-foundation/prompt.md` before the
  Epic spawned. If the research run surfaces additional ambiguities, file
  them as follow-up prompts (`prompt_kind: follow-up`, `prompt_spawned_from_
  research: dramatica-scenarios-foundation`), do NOT edit the prompt in-place
  after dispatch.
- Exact child-Task count (`N` in Cohort 3) depends on §3.4's gap analysis.
  Acceptance floor is 9 scenarios (6 keepers + 3 ADDs) per the prompt's
  acceptance signal #6.
- Per the user's directive, `lyric.*` scenarios are out-of-scope for THIS
  Epic. A future Epic spawned by `suno-lyric-writer` may build the lyric.*
  corpus following this Epic's template + tooling.
