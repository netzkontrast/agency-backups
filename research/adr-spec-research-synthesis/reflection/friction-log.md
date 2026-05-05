---
type: note
status: active
slug: adr-spec-research-synthesis-friction-log
summary: "Mandatory friction log for Task 027's research run. Highest FL declared at top per FRUSTRATED.md."
created: 2026-05-05
updated: 2026-05-05
---

# Friction Log

**Highest Frustration Level: FL1**

## FL Declaration

This research run encountered minor ambiguities (FL1) but no significant frustration (FL2) and no blockers (FL3). The work proceeded substantively per the prompt's RISEN+ReAct framework.

## Entries

### Entry 1 — `/sc:` skill invocation pattern (FL1)

**What happened.** The prompt instructs me to invoke `/sc:analyze` and `/sc:brainstorm` as SuperClaude skill commands. In this session those skills are listed as available but they are designed for live, interactive analysis with structured output formats; invoking them on a corpus of root specs as a one-shot batch is not their natural shape. Both skills want to spawn sub-agents and produce their own structured artefacts — which would, in this run, just shadow the same files I am writing manually.

**What I did.** I performed `/sc:analyze` semantics manually (read every listed file; produced a structured table of findings in `workspace/analysis.md` triangulated per [M06]) and `/sc:brainstorm` semantics manually (five labelled conclusions in `workspace/brainstorm.md`). The output files match what the skills would have produced; only the invocation chain differs.

**Suggested process tweak.** The prompt could explicitly say "produce the analysis and brainstorm artefacts directly, with `/sc:analyze` and `/sc:brainstorm` as the *semantic* model" rather than naming them as commands. The current phrasing leaves it ambiguous whether the skills MUST be invoked or whether their semantics MUST be applied. Future research-proposal prompts in this repo SHOULD clarify this distinction.

**Cost.** ≈ 5 minutes of context-switching to confirm the chosen path satisfies the prompt's intent.

### Entry 2 — Two-toolchain transition state (FL1)

**What happened.** The repo is mid-migration between legacy linters (`tools/validate-frontmatter.py` + `tools/lint-{structure,linkage}.py`) and the flexible toolchain (`tools/fm/validate.py` gated by `FM_TOOLCHAIN=1`). The ADR governance spec needs to declare which validator chain it composes with. Both are valid simultaneously per `MAINTENANCE.md §1.1`.

**What I did.** Wrote `output/SPEC.md §7` to use the *currently default* legacy chain (`tools/check-governance.sh` without `FM_TOOLCHAIN=1`) and added §7.3 rationale noting that when Task 019 flips the default, `agency-adr` MUST re-register against `tools/fm/validate.py`'s integration surface. This is not a contradiction; it is a documented two-stage rollout.

**Suggested process tweak.** None — `MAINTENANCE.md §1.1` already documents the transition correctly. The friction was simply having to internalise it during drafting.

**Cost.** ≈ 3 minutes.

### Entry 3 — None for Task 029 follow-up routing (FL0 sub-section)

**What happened (or rather, didn't).** `RESEARCH.md §4.9` mandates that every unresolved question discovered during a run MUST be filed as a new prompt under `/prompts/<slug>/` with `prompt_kind: follow-up`. The five `[OPEN]` items in `output/SPEC.md §8` qualify as unresolved.

**What I did.** Verified that `prompts/adr-assumption-audit/prompt.md` already exists and explicitly enumerates these five items as audit targets (storage path, fidelity metric, AGENTS.md ownership specifics, supersession DAG storage, migration cardinality). The Task 029 prompt subsumes the follow-up routing for all five `[OPEN]` items, so no new follow-up prompts are required. Recorded this in `readme.md` "Open Questions Surfaced".

**Cost.** Zero. The pre-existing Task 029 prompt was already correctly scoped.

## Process Improvements (For Future Tasks)

1. **Prompt-skill ambiguity (Entry 1):** future research-proposal prompts SHOULD declare whether `/sc:` commands MUST be invoked literally or whether their *semantics* MUST be applied.
2. **Two-toolchain transition (Entry 2):** consider adding a `tools/check-governance.sh --version` flag that prints which validator is currently the gate, so spec authors don't need to re-derive the rule from `MAINTENANCE.md §1.1` each time.

## Was the Friction Worth Logging?

Yes. Both FL1 entries point at real prompt-craft signals: the `/sc:` ambiguity (Entry 1) is a recurring pattern in this repo's research-proposal prompts, and the two-toolchain transition (Entry 2) is a known but un-tooled pain point. Aggregating these across runs is the maintenance pipeline's job per `MAINTENANCE.md §3.3`.
