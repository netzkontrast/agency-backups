---
type: note
status: active
slug: adr-spec-research-synthesis-state
summary: "Step-by-step checklist for Task 027's research run. Every step MUST be [x] before commit per RESEARCH.md §5.7."
created: 2026-05-05
updated: 2026-05-05
---

# State

## Synthesis Steps

- [x] 1. Bootstrap: `./install.sh` exit 0, `tools/check-governance.sh` baseline exit 0.
- [x] 2. Read all root specs and tooling per the prompt's Input list.
- [x] 3. Initialise workspace per `RESEARCH.md §2`: `readme.md`, `prompt.md`, `workspace/`, `synthesis/`, `reflection/`, `output/`.
- [x] 4. Snapshot prompt body into `prompt.md`.
- [x] 5. Step 1 — produce `workspace/analysis.md` with `/sc:analyze` semantics.
- [x] 6. Step 2 — produce `workspace/brainstorm.md` with five integration questions answered.
- [x] 7. Step 3 — apply [M13] across four axes; produce `reflection/M13-query-expansion.md`.
- [x] 8. Apply [M06] Source Triangulation; produce `reflection/M06-source-triangulation.md`.
- [x] 9. Apply [M07] Contradiction Log; produce `reflection/M07-contradictions.md`.
- [x] 10. Apply [M08] What Would Change My Mind for high-stakes claims; produce `reflection/M08-what-would-change-my-mind.md`.
- [x] 11. Step 4 — draft `output/SPEC.md` with §0–§9 re-derived from Steps 1–3.
- [x] 12. Step 5 — populate `reflection/friction-log.md` with FL declaration at top.
- [x] 13. Synthesis files: `methodology.md`, `tracks.md`, `post-synthesis-log.md`, `readme.md`, `state.md`.
- [x] 14. Run `tools/check-governance.sh`; verify exit 0 against new files.
- [x] 15. Step 6 — set Task 027 `task_status: done`; verify Tasks 028 + 029 remain `open`.
- [x] 16. Update `tasks/readme.md` and `research/readme.md` to reflect new state.

## Open-Question Routing

Every `[OPEN]` item from `workspace/brainstorm.md` appears in `output/SPEC.md §8` with an explicit owner and unblock condition. Items routed to Task 029 are referenced in that task's prompt (`prompts/adr-assumption-audit/prompt.md` already enumerates these as audit targets), so no new follow-up prompts are required (`RESEARCH.md §4.9` open-question outward-routing is satisfied via Task 029's existing prompt).
