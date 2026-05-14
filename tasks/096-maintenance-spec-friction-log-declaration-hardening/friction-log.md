---
type: friction-log
status: active
slug: task-096-coherence-run-friction-log
summary: "Session friction log for the 2026-05-14 Repo Coherence Check that filed Task 096. FL1: three ERROR-tier diagnostics cleared as T1 mechanical repairs; one structural observation (closed-Task T1 boundary not codified) ratified as Task 096 §Plan-1; the /sc:* command chain executed without surprises."
created: 2026-05-14
updated: 2026-05-14
---

# 2026-05-14 Coherence Run — Friction Log

**Highest Frustration Level: FL1** — minor friction. The Repo Coherence Check
executed mostly mechanically; one structural finding (the §1.0.1 closed-research
T1/T2 allowance has no symmetric clause for closed Tasks) was new but resolved
in-band by filing Task 096. The `/sc:*` chain (`analyze → reflect → improve →
Review`) is well-suited to maintenance closure and produced concrete artefacts
at each stage.

## What worked

- **Linter-first triage.** Drove the run from `tools/check-governance.sh`
  output, not from re-reading 756 changed files. The three blocking ERROR codes
  (`T.7.11`, `FR.B.4` × 2) pointed at exactly three files; the fix surface was
  small.
- **`tools/fm/edit.py --bump-updated`** behaved as documented per file. The
  preserved-body-bytes contract held for the three T1 surfaces.
- **Run-log baseline recovery** worked first-try: the most recent reachable
  `end_commit:` (`6e4859d`) was the `adr-synthesize` record from 2026-05-12.
  Per §2.3, `task-implementation` / `adr-synthesize` records remain valid
  baselines because they advance HEAD; the awk fall-forward keyed off them
  cleanly.
- **`/sc:*` chain telemetry.** Each `/sc:*` stage produced a concrete artefact:
  `/sc:analyze` → 4-finding table; `/sc:reflect` → CR.1–CR.7 adherence checklist;
  `/sc:improve` → 3 quality lifts (factual accuracy, flow precision, frontmatter
  completeness); `/sc:Review` → 4-question approval + 2 reflexion patterns.

## What surfaced as friction

### FE-1 (FL1) — `tools/fm/edit.py --bump-updated` does not accept multiple paths

**What happened.** I batched four `--bump-updated` calls into one shell command
with `&&` chaining (`tools/fm/edit.py --bump-updated A && tools/fm/edit.py
--bump-updated B && …`). The first one-shot call with all paths as args
returned `error: unrecognized arguments` because the argparse declaration only
takes a single positional `path`.

**Outcome.** Three sequential invocations succeeded. The chained syntax is
mechanically equivalent; the friction is purely UX.

**Pattern.** A coherence sweep typically touches 3–10 files; the single-path
constraint forces N shell invocations or one `xargs` per wave. Captured as
Task 096 §Plan-2.

### FE-2 (FL1) — §1.0.1 closed-research allowance has no closed-Task analogue

**What happened.** Two of the three ERRORs landed on `friction-log.md` files
inside `task_status: done` Tasks. §1.0.1 explicitly allows T1/T2 frontmatter
+ link repairs on closed *research*; for closed *Tasks* the rule is absent.
I applied the T1 repair anyway (declaration line is metadata-shaped, not
event-content-shaped) and named the implicit precedent in the run-log notes.

**Outcome.** Three T1 repairs landed. The boundary call was correct on first
principles but the spec did not back it up.

**Pattern.** Captured as Task 096 §Plan-1. A two-line §1.0.2 + one Gherkin
scenario (`M.B.9`) closes the gap permanently.

### FE-3 (FL1) — `FR.B.4` linter error message does not suggest the canonical line

**What happened.** Both `FR.B.4:malformed` diagnostics pointed at the offending
file but did not offer the line to paste. I had to manually derive the canonical
form from `summary:` (for Task 033) and from the highest inline `(FL3, …)`
event tag (for Task 030).

**Outcome.** Both files repaired correctly. The derivation rule is mechanical
(highest of: `summary:` FL token, body inline FL tokens) and the linter could
emit it as part of the error message.

**Pattern.** Captured as Task 096 §Plan-3. Linter remains a verifier; the
auto-derivation is suggestion-only.

### FE-4 (FL0) — `/sc:*` flow not codified

**What happened.** The user instruction "use /sc: skills helpful" + the explicit
chain "/sc:analyze → /sc:reflect → /sc:improve → /sc:Review → /sc:createPR" is
empirically a good close sequence for maintenance runs. MAINTENANCE.md §4 does
not document it; the agent inferred the flow from the user instruction.

**Outcome.** Chain executed cleanly. No fallback needed.

**Pattern.** Captured as Task 096 §Plan-4. Adding a §4.2 subsection that names
the canonical chain (one paragraph + one Gherkin) means the next coherence-run
agent can `/sc:load` MAINTENANCE.md and execute the chain without re-deriving.

## /sc:* invocation log

| When | Command | Outcome |
|---|---|---|
| After T1 fixes landed | `/sc:analyze` | 4-finding table; finding A.1 = §1.0.1 boundary precedent; FA.3 = 13 trust-audit items deferred to nightly cadence |
| Post-analyze | `/sc:reflect` | CR.1–CR.7 adherence checklist green; 3 patterns surfaced (P-1 linter-first triage = recurring; P-2 + P-3 new) |
| Pre-commit | `/sc:improve` | 3 quality lifts: run-log factual accuracy; Task 096 §Plan-4 flow precision; Task 096 frontmatter completeness |
| Pre-commit | `/sc:Review` (= `@self-review`) | 4-question approval; 2 reflexion patterns (R-1 two-track output; R-2 canonical close sequence); APPROVED |
| Closing | `/sc:createPR` | (this step) — opens draft PR per CR.7 (Claude Code path) |

## Closure summary

- **T1 repairs landed.** 3 of 3 ERRORs cleared in-place; no T3 inline mutations to root specs.
- **Task 096 filed.** P3 maintenance hardening with 4 §Plan items + 4 Gherkin acceptance anchors (M.B.9–M.B.12 reserved in MAINTENANCE.md §6 namespace).
- **Run-log record appended.** `routine_type: coherence-check`, `routine_id` = the session SHA at commit time, `issues_skipped: 13` with cadence justification.
- **Governance gate green** on the pre-commit working tree.
- **CR.1–CR.7 checklist** in progress: steps 1 (this file), 2 (tasks/readme.md
  index sync via Task 093 bullet flip + Task 096 bullet add), 3 (gate green
  verified), 4 (PR via `/sc:createPR`).
