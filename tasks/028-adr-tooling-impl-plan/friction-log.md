---
type: note
status: active
slug: 028-adr-tooling-impl-plan-friction-log
summary: "Mandatory closure friction log for Task 028 (TASK.md §7.7). Plan-only task; no working code authored."
created: 2026-05-05
updated: 2026-05-05
---

# Task 028 Friction Log

**Highest Frustration Level: FL1**

## Outcome

`tasks/028-adr-tooling-impl-plan/implementation-plan.md` is in force as the build contract for `agency-adr`. Module decomposition (§2), test map (§3), CI workflow spec (§4), `PRE_COMMIT.md` hook spec (§5), and a 10-row open-decisions list (§6) are populated. Total estimated build effort: ≈ 3–5 working weeks (§7.4).

## FL Declaration

This task closed cleanly. The two FL1 frictions encountered during the plan draft:

### Entry 1 — Phase ordering of `fidelity.py` (FL1)

**What happened.** SPEC §5.1 ADR.A.3.4 mandates a fidelity floor with three selectable algorithms (`bcp14-keyword`, `adr-id-anchor`, `llm-pass`). Two of the three modes need data the synthesis pipeline only produces *after* compression, but the third (`llm-pass`) introduces an Anthropic SDK runtime dep that the repo's `tools/requirements.txt` deliberately avoids. Resolution: `fidelity.py` lives in build phase 3 alongside `extract` and `compress`; v0 ships only `bcp14-keyword`; `llm-pass` is OD.2 (deferred).

**Suggested process tweak.** The SPEC could have included a "minimum deliverable per algorithm mode" hint. Not a blocker — the plan documents the deferral explicitly.

**Cost.** ≈ 5 minutes deciding whether `fidelity` is a phase-3 or phase-4 module.

### Entry 2 — `prompts/adr-tooling-impl-plan/prompt.md` already complete (FL0–FL1)

**What happened.** Todo step 8 instructed me to "flesh out" the prompt as a ready-to-execute task-spec prompt. On inspection the prompt is already complete: it carries the L1 + Prompt-namespace frontmatter, a RISEN body (R-I-S-E-N), seven steps, a Constraints/Narrowing section, and explicit non-goals. The "flesh out" verb suggested unfinished content. Resolution: re-checked the prompt against `header-ontology.json` `types.prompt` (required keys + required headings), confirmed conformance, and re-worded the todo to "verify ... is a ready-to-execute task-spec prompt".

**Suggested process tweak.** Future Task plans SHOULD avoid prescriptive verbs ("flesh out", "polish") for artefacts that the spawning Task already authored to completion. A plain "verify" is more honest.

**Cost.** ≈ 2 minutes confirming the prompt was indeed conformant.

## Boundaries Honoured

- No code written under `tools/adr/` (per the prompt's Non-goals).
- No `.github/workflows/adr-validate.yml` written (spec only).
- No edits to the immutable [`research/adr-spec-research-synthesis/output/SPEC.md`](../../research/adr-spec-research-synthesis/output/SPEC.md) (T4 immutability per `MAINTENANCE.md §1`).
- No `PRE_COMMIT.md` edit. The §5.1 text in `implementation-plan.md` is the *specification* of the future edit; landing it is the implementation Task's job.

## Outstanding Items

OD.1 / OD.2 / OD.4 / OD.10 (§6 of `implementation-plan.md`) are routed to Task 029's assumption audit. Task 029 unblocks with this commit (its `task_blocked_by: ["027"]` is satisfied by Task 027's `done` status; Task 028 was not a blocker).
