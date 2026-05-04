# Brief: Research and Spec the `skills-skill`

## Source

This brief was provided by Michael Schimmer as part of the three-stage bootstrap-skills-sync mission, taken over from a claude.ai session by Claude Code agent `claude/bootstrap-skills-sync-Zadie`. The brief was embedded verbatim in the mission prompt delivered on 2026-05-04.

## Target Agent

Claude Code (claude-sonnet-4-6 or later), acting as a research agent executing a Research Task per `RESEARCH.md`.

## Intended Model

claude-sonnet-4-6 (or later). The brief is within context window; no chunking needed.

## Use-Case Context

Stage C of the bootstrap-skills-sync mission. Stage A (skills import PR) and Stage B (sync mechanism) are companion stages. This prompt is the instruction set for Stage C — the research that must precede any implementation of `skills-skill`.

## User Request (Unedited)

See [prompt.md](./prompt.md) for the complete, formatted prompt. The brief below is the verbatim text as delivered.

The brief asks for:
1. A preliminary architecture spec covering R1–R7 (bootstrap, sync, routing, progressive disclosure, trust, cross-agent portability, offline behavior).
2. A self-contained Google Gemini Deep Research prompt to be run externally by Michael.
3. An integration plan for folding the Gemini PDF back into the spec.

## Constraints Noted by Agent

- The research task cannot implement `skills-skill`; it can only specify it.
- Root governance specs must not be edited.
- Uncertain sections must be explicitly marked, not papered over.
- Open questions must be filed as follow-up prompts per `RESEARCH.md §4.9`.
