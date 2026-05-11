---
type: note
status: active
slug: friction-log-006
summary: "Friction log for Task 006 — surfaced skills-skill-architecture R4/R5/R7 invariants to SKILLS.md and cross-referenced from AGENTS.md. FL1 due to a scope-narrowing decision."
created: 2026-05-11
updated: 2026-05-11
---

# Friction Log — Task 006

Highest Frustration Level: FL1

## Summary

Ratified three blocks of [`research/skills-skill-architecture/output/SPEC.md`](../../research/skills-skill-architecture/output/SPEC.md) into root governance:

1. **R5 trust-boundary invariants → SKILLS.md §7.2** (anchors `B.6` repository lock, `B.7` version-reference declaration, `B.8` error surfacing, `B.9` scope containment).
2. **R4 progressive disclosure → SKILLS.md §7.3** (T1 200-char summary / T2 5 KB body / T3 unlimited references — the existing dramatica-corpus discipline, now repo-wide normative).
3. **R7 version-pinning + offline mode → SKILLS.md §7.4** (`SKILLS_SKILL_PIN`, `SKILLS_SKILL_OFFLINE` env-var vocabulary; interaction with the existing `AGENCY_SKILLS_ALLOW_STALE` documented).

`AGENTS.md "Skills Architecture"` gains a one-paragraph pointer linking the agent reading path to the new SKILLS.md subsections and listing the residual U3–U6 unresolved markers.

## FL1 — Scope-narrowing decision

The Task plan said *"Update `AGENTS.md` and/or `MAINTENANCE.md` with those findings."* The original `task_affects_paths` listed `AGENTS.md`, `MAINTENANCE.md`, `TASK.md` — but **not** `SKILLS.md`.

After reading the source SPEC and the existing root governance corpus, the right home for skill-loader operational invariants is **SKILLS.md** (the layer-specific spec, per the layer-routing table in [`CLAUDE.md §3`](../../CLAUDE.md#3-layer-routing--pick-the-right-spec-before-writing)). Surfacing them into `MAINTENANCE.md` or `TASK.md` would dilute those root specs' focus (T1–T4 ladder, Task lifecycle) with skill-specific concerns. The Task's `task_affects_paths` was updated at close to add `SKILLS.md`; the `MAINTENANCE.md` / `TASK.md` entries are retained but unmodified — the surfaced content reaches them through the existing AGENTS.md → SKILLS.md reading path.

The FL1 here is the *small re-think* required mid-Task to recognize that "and/or MAINTENANCE.md" was the wrong fit and to choose SKILLS.md instead. No work was wasted.

## Observations

- The source SPEC carries U1–U6 `UNCERTAIN` markers. U1/U2 (container capabilities) are already resolved upstream by `research/skills-skill-container-capabilities/output/SPEC.md` and surfaced in `AGENTS.md`. U3–U6 (host activation, Jules portability, raw-message availability, git signing) remain *un*-resolved; surfacing them as normative root-spec content would be wrong. The Task only ratifies the *resolved* portions of the SPEC.
- The R4 three-tier ladder formalises the existing dramatica-corpus discipline (small `SKILL.md` body, depth pushed to `references/`). It is therefore already-true for most of the existing 16 skills; the ratification is documentation, not a corpus migration.
- The R5 invariants were strongest argument for ratifying *now*. The skills-skill stub is the immutable security perimeter; auditing future bootstrap stubs against four explicit invariants beats auditing them against prose-only descriptions.

## Trust dimensions (Spec-J/K/L)

- **Schema integrity:** PASS — no frontmatter shape changes; `tools/check-governance.sh` exits 0; `tools/fm/validate.py --check-body` clean on SKILLS.md / AGENTS.md.
- **Behavioural integrity:** PASS — surfaced content is documentation, not new mechanical checks; existing R1/R7 bootstrap scenarios in §7.1 still validate.
- **Governance integrity:** PASS — surfaced content cites its source SPEC by repo-relative path; supersession claims preserved; U3–U6 deferred-to-Gemini status preserved verbatim.

No follow-up Task warranted in this scope. The natural follow-ups (resolving U3–U6) remain in the Gemini Deep Research queue per the source SPEC's §9 table.
