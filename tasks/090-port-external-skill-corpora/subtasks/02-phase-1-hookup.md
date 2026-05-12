---
type: note
status: active
slug: task-090-st2-phase-1-hookup
summary: "ST-2 (Task 090 Epic): rewrite AGENTS.md Closing Run Procedure to cite local skills/sc-createPR/, add RESEARCH.md §7 citing skills/sc-research/. Hookup only; corpus shipped by ST-1."
created: 2026-05-12
updated: 2026-05-12
---

# ST-2 — Phase 1 Hookup (was "Task B" in §10.5)

**Executor:** main-agent (Claude Code with `/sc:implement`).

**Parallelism:** Sequential — ST-2 MUST start **after** ST-1 closes `done` AND merges to `main`. Otherwise the AGENTS.md rewrite would cite a path that does not yet exist (broken-link state at HEAD).

**Depends on:** ST-1 ([`01-phase-1-corpus.md`](./01-phase-1-corpus.md)) at `task_status: done`; [ADR-0011](../../../decisions/0011-external-skill-corpora-import.md) at `adr_status: Accepted`.

**Spec:** [`../references/full-plan-part-4.md` §10.5 "Task B"](../references/full-plan-part-4.md) — the canonical 7-step plan, 3 Gherkin AC (`TB.1.1`–`TB.1.3`), and verbatim citation diffs (`../references/full-plan-part-4.md` §10.4 FR4 / FR5).

## Scope

- **AGENTS.md FR4.** Edit [`AGENTS.md`](../../../AGENTS.md) — Closing Run Procedure → Platform Implementation Notes → Claude Code subsection. Replace the prose paragraph citing `https://github.com/netzkontrast/SuperClaude_Framework/blob/main/src/superclaude/commands/createPR.md` with a local-path paragraph citing `[skills/sc-createPR/SKILL.md](./skills/sc-createPR/SKILL.md)`. Verbatim before/after diff in `../references/full-plan-part-4.md` §10.4 FR4.
- **RESEARCH.md FR5.** Append a new H2 section to [`RESEARCH.md`](../../../RESEARCH.md): `## 7. Skill-driven research runs` citing `[skills/sc-research/SKILL.md](./skills/sc-research/SKILL.md)` and ADR-0011. Verbatim section content in `../references/full-plan-part-4.md` §10.4 FR5.
- **Frontmatter bump.** Bump `updated:` to today on both modified files.

## Out of scope

- Modifying root specs other than `AGENTS.md` (CR.1.1 paragraph) and `RESEARCH.md` (new §7) — any other root-spec change is a separate Task per [`MAINTENANCE.md §1`](../../../MAINTENANCE.md#1-repair-permission-tiers).
- The `gh` CLI fallback paragraph in `AGENTS.md` MAY stay verbatim (BR.9.2 only requires the `src/superclaude/commands/createPR.md` URL to be removed; the `gh` paragraph is platform-independent prose).
- Any structural reflow of `AGENTS.md` or `RESEARCH.md` beyond the two cited edits.

## Acceptance Criteria

Verbatim from `../references/full-plan-part-4.md` §10.5 Task B — anchors `TB.1.1`–`TB.1.3`:

- **TB.1.1** — `grep -n "src/superclaude/commands/createPR.md" AGENTS.md` returns **zero matches** AND `grep -n "skills/sc-createPR/SKILL.md" AGENTS.md` returns **≥1 match**.
- **TB.1.2** — `RESEARCH.md` has `## 7. Skill-driven research runs` with Markdown links to `./skills/sc-research/SKILL.md` AND `./decisions/0011-external-skill-corpora-import.md`.
- **TB.1.3** — `python3 tools/check-rfc2119-polarity.py AGENTS.md RESEARCH.md` emits zero NEW WARN diagnostics over the pre-ST-2 baseline (the FR4 rewrite lives in a prose paragraph, NOT a MUST clause).

## Branch + PR shape

Author on a **fresh branch** derived from `main` after ST-1 merges. PR title MUST cite this subtask, e.g. `Task 090 ST-2: Phase 1 hookup (AGENTS.md cite + RESEARCH.md §7)`. PR body MUST include:

- The BR.9.2 grep output (`grep -n "src/superclaude/commands/createPR.md" AGENTS.md` exits with status 1 and zero matches).
- The TB.1.2 reader-visible confirmation: links resolve to the local files materialised by ST-1.
- Friction-log declaration (FL0-FL3) per `FRUSTRATED.md`.

## Closure check

When this PR merges, ST-1 and ST-2 both at `done`, the Epic ([`../task.md`](../task.md)) MAY flip to `task_status: done` and the `tasks/readme.md` entry MAY flip from `Status: open` → `Status: done`.
