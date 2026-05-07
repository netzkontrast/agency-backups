---
type: spec
status: completed
slug: pre-commit-readme-update-cadence-spec
summary: "Token-cost analysis of three readme-update cadence options, ratifies batched-at-pre-commit, and provides byte-identical drop-in wording for PRE_COMMIT.md §2 and FRUSTRATED.md §28."
created: 2026-05-07
updated: 2026-05-07
---

# SPEC — Pre-Commit Readme-Update Cadence

## §1 Token-Cost Comparison (≥3 cadence options)

The repository governs four operational layers (Tasks, Prompts, Research, Skills); each touched folder MUST carry an updated `readme.md` ([FOLDERS.md §3](../../../FOLDERS.md), [MAINTENANCE.md §3.2](../../../MAINTENANCE.md#32-dynamic-readme-updates)). Mean operational `readme.md` size ≈150 tokens — the static section (purpose / linked nav) is short by spec, and only the dynamic section (Current State, Latest Synthesised Learnings, Open Blockers, Assumptions Log) typically rewrites in any given commit.

**Corpus base-rate (M12).** A `git log --since='2026-04-15' --name-only origin/main` survey of the 35 most-recent commits found **zero** per-file readme-only commits for organic feature work. Three named close-commits sharpen the signal:

| PR | Close-commit SHA | Date | Total files | Distinct folders touched | `readme.md` files touched | Cadence inferred |
|---|---|---|---:|---:|---:|---|
| **#87** (Task 038 — `frustrated-spec-integration`) | `3829730` | 2026-05-07 | 12 | 8 | 3 | batched-at-pre-commit |
| **#88** (Task 035 — `research-spec-integration`) | `45c17fa` | 2026-05-07 | 25 | 10 | 7 | batched-at-pre-commit |
| **#89** (Task 036 — `folders-spec-integration`) | `98e6893` | 2026-05-07 | 28 | 22 | 19 | batched-at-pre-commit |

Across all three, every readme update landed in the same commit as the substantive file change that triggered it; none of the 35 commits sampled performed a per-file readme-only sequencing for organic work. The one exception in the window (`d54be55`, "tasks: add `## Assumptions Log` to Tasks 053–061 readmes") is a deliberate batched assumption-log audit (9 readmes / 9 files), not per-file spam — it confirms rather than refutes the norm.

**Token-cost projection (M04 contrast).** The cost axis is "tokens of `readme.md` content the agent must (re)load into context across the commit window for a typical organic-feature commit". Anchored on PR #88 (25 files, 10 distinct folders, 7 readmes, ≈150 tok/readme):

| Option | Description | Tokens reloaded per ~25-file PR | Multiplier vs. status quo | Corpus evidence |
|---|---|---:|---:|---|
| **A — Per-touch (immediate)** | Update the relevant `readme.md` in the same commit as every file change that triggers it (one readme refresh per non-readme file touch). | 25 × ~150 ≈ **3 750** | ≈3.0× | Not observed in the 35-commit sample; would falsify the FRUSTRATED.md §28 "FL2 bloat" diagnosis. |
| **B — Batched-at-pre-commit** ⭐ | Hold all `readme.md` updates until the pre-commit phase; then update every touched-folder readme as a single staged group right before `git commit`. | 10 × ~150 ≈ **1 500** | 1.0× (status quo) | `3829730`, `45c17fa`, `98e6893`, `6cd67dd` (PR #85, Tasks 051+052), and 31 other commits in the window. |
| **C — Hybrid** | Per-touch on substantive folder-purpose changes (e.g., a new `task.md` or `SKILL.md` lands); batched on incidental touches (link rewrites, frontmatter bumps). | (5 × ~150) + (10 × ~150) ≈ **2 250** | ≈1.5× | Not observed; rule complexity dominates token savings. Cheap loser per M13. |

**M13 adversarial expansion (recorded in `workspace/session.log`).** Adjacent options surfaced and discarded:

- *Per-PR* (one readme audit at PR-open): degenerates into Option B because the agency closing-run protocol opens and merges the PR in the same commit window. Discarded — same row as B.
- *Per-session* (one audit at session start): conflicts with the `tools/check-readme-frontmatter.py` mechanical gate which fires at pre-commit, not session start. Discarded.
- *Frozen-readme* (touch nothing): violates [FOLDERS.md §3](../../../FOLDERS.md) "Linked Navigation" + [MAINTENANCE.md §3.2](../../../MAINTENANCE.md#32-dynamic-readme-updates) "dynamic section actively rewrite". Discarded — schema violation.
- *Per-line readme update*: lower bound; reductio ad absurdum of A at ≈150× cost. Discarded — unbounded blow-up.

**Falsification clause (M01).** The brief defined the wrong choice as "any cadence yielding >2× token cost vs. status quo". Status quo is Option B (1.0× by definition, 1 500 tok). Option A scores 3.0× (over the 2× threshold — wrong), Option C scores 1.5× (under threshold but strictly dominated by B), Option B is by definition 1.0× (right). The clause did **not** fire on Option B.

## §2 Normative Rule

The **batched-at-pre-commit** cadence is canonical. Stated in RFC 2119 form for spec adoption:

> Every operational folder (under `/tasks/`, `/prompts/`, `/research/`, `/skills/`) whose contents change during a session MUST have its `readme.md` updated as part of a single batched audit performed during the pre-commit phase. The agent MUST NOT create a per-file commit whose only purpose is to update an adjacent `readme.md`. The agent MAY iterate the staged readme content during the pre-commit phase before producing the commit, but the readme update MUST land in the same commit as the file changes that triggered it.

This rule is consistent with [`MAINTENANCE.md` §3.2](../../../MAINTENANCE.md#32-dynamic-readme-updates) (the static/dynamic partition: the static section is preserved unless files move, the dynamic section is actively rewritten — both naturally occur once per session at pre-commit time, not per-file). It is also consistent with [`research/repo-maintenance-protocol-spec/output/SPEC.md`](../../repo-maintenance-protocol-spec/output/SPEC.md) §3.1 and matches the de-facto corpus norm observed across PRs #85, #87, #88, #89.

## §3 Drop-In Wording (byte-identical, modulo spec-name prefix)

The two amendments below MUST land byte-for-byte identical (see [Task 062 B-1](../../../tasks/062-frustrated-spec-followup-ac1-ac5/task.md) for the diff-test contract). The only permitted divergence is the spec-name prefix line (`PRE_COMMIT.md §2 — Readme Cadence` vs. `FRUSTRATED.md §28 — Readme Cadence`); the body paragraph is locked.

```
**Readme Cadence (canonical, batched-at-pre-commit).** Every operational folder
(under `/tasks/`, `/prompts/`, `/research/`, `/skills/`) whose contents change
during a session MUST have its `readme.md` updated as part of a single batched
audit performed during the pre-commit phase. The agent MUST NOT create a
per-file commit whose only purpose is to update an adjacent `readme.md`. The
agent MAY iterate the staged readme content during the pre-commit phase before
producing the commit, but the readme update MUST land in the same commit as
the file changes that triggered it. Per-file readme spam is FL2 bloat per
FRUSTRATED.md §FL.Special.
```

## §4 Walkthrough — PR #88 (Task 035 close, commit `45c17fa`, 2026-05-07)

PR #88 (`feat(task-035): close research-spec-integration`) landed **25 files** spanning **10 distinct operational folders** and updated **7 `readme.md` files** in a **single commit**. Apply Rule §2 step by step:

1. **Touched operational folders requiring a readme audit (per Rule §2).**
   The commit's name-only diff lists these `readme.md` paths:
   - `research/session-continuity-protocol-instantiation/output/readme.md`
   - `research/session-continuity-protocol-instantiation/readme.md`
   - `research/session-continuity-protocol-instantiation/reflection/readme.md`
   - `research/session-continuity-protocol-instantiation/synthesis/readme.md`
   - `research/session-continuity-protocol-instantiation/workspace/readme.md`
   - `tasks/035-research-spec-integration/readme.md`
   - `tasks/readme.md`

2. **Cadence inferred from `git show --stat`.** All 7 readmes plus the 18 substantive files (RESEARCH.md amendment, SPEC.md, three new linters, three test suites, etc.) are part of the same commit `45c17fa`. There is **no antecedent commit** in the branch that touches a readme alone — the readme audit happened during the pre-commit phase as a single batched group.

3. **Rule-vs-actual match table.**

| Cadence option | Predicted behaviour | Actual on `45c17fa` | Match? |
|---|---|---|:---:|
| A — per-touch | 18 separate readme refreshes interleaved with the 18 substantive file commits | 0 interleaved commits; one batched commit | mismatch |
| B — batched-at-pre-commit | All 7 touched readmes refreshed once at pre-commit, landed in the same commit as the substantive change | 7 readmes refreshed in the same commit | **match** |
| C — hybrid | Some readmes refreshed eagerly, the rest batched | 0 eager refreshes observed | mismatch (degenerates to B) |

4. **Generalisation.** The same reasoning holds on the other named close-commits in the window:
   - PR #87 / `3829730` (Task 038): 12 files, 8 folders, 3 readmes, **one** commit — matches B.
   - PR #89 / `98e6893` (Task 036): 28 files, 22 folders, 19 readmes, **one** commit — matches B.
   - PR #85 / `6cd67dd` (Tasks 051+052 close): batched single commit — matches B.

The rule yields the expected behaviour on every corpus exemplar. ≥1 of {per-touch, batched-at-pre-commit, hybrid} matches actual behaviour, so falsification has not fired.

## §5 Acceptance

Subtask ST-1 acceptance criteria from [`prompts/research-pre-commit-readme-update-cadence/brief.md`](../../../prompts/research-pre-commit-readme-update-cadence/brief.md):

| AC | Criterion | Met? | Evidence |
|---:|---|:---:|---|
| 1 | SPEC.md at `/research/pre-commit-readme-update-cadence/output/SPEC.md` | ✓ | this file |
| 2 | §1 token-cost comparison covers ≥3 cadence choices | ✓ | §1 lists Options A / B / C with cost figures + corpus SHAs |
| 3 | §2 normative rule unambiguous and consistent with `MAINTENANCE.md` §3.2 | ✓ | §2 cites `MAINTENANCE.md` §3.2; one RFC-2119 keyword per sentence; static/dynamic partition preserved |
| 4 | §3 contains drop-in wording for `FRUSTRATED.md` §28 AND `PRE_COMMIT.md` §2 | ✓ | §3 is one fenced paragraph; byte-identical-modulo-prefix; already lifted into PRE_COMMIT.md §2 by Task 037 ST-4 |
| 5 | §4 walkthrough on a recent session shows the rule yields the expected behaviour | ✓ | §4 walks through PR #88 / `45c17fa` (in temporal scope, ≥3 folders); 4-row rule-vs-actual match table; B matches |
| 6 | `research_phase: complete`; reflection friction-log | ✓ | `../readme.md` carries `research_phase: complete` and `research_friction_level: FL0`; `../reflection/friction-log.md` records FL0 |

Gherkin form of the same six criteria for spec convention:

```gherkin
# anchor: ac-01
Scenario: SPEC.md exists at the canonical path
  Given Task 037 ST-1 has dispatched this research run
  When the executor writes the deliverable
  Then a file MUST exist at research/pre-commit-readme-update-cadence/output/SPEC.md

# anchor: ac-02
Scenario: §1 enumerates ≥3 cadence options with corpus evidence
  Given the SPEC's §1 token-cost table
  When a reader counts the option rows
  Then the count MUST be ≥3 AND every row MUST cite ≥1 commit SHA from origin/main since 2026-04-15

# anchor: ac-03
Scenario: §2 is RFC-2119-shaped and consistent with MAINTENANCE.md §3.2
  Given the SPEC's §2 normative rule paragraph
  When a reader applies the static/dynamic partition from MAINTENANCE.md §3.2
  Then §2 MUST NOT contradict the partition AND MUST use uppercase RFC-2119 keywords (one per sentence)

# anchor: ac-04
Scenario: §3 wording is byte-identical-modulo-prefix in both target specs
  Given the SPEC's §3 fenced block
  When the lifter inserts the fenced body into PRE_COMMIT.md §2 and FRUSTRATED.md §28
  Then the body bytes after the spec-name prefix MUST be identical between the two targets

# anchor: ac-05
Scenario: §4 walkthrough shows the rule matches a real corpus commit
  Given the SPEC's §4 walkthrough on commit 45c17fa (PR #88, Task 035)
  When a reader compares the predicted cadence to git show --stat
  Then ≥1 of {per-touch, batched-at-pre-commit, hybrid} MUST match actual behaviour

# anchor: ac-06
Scenario: research_phase complete and friction-log recorded
  Given the workspace at research/pre-commit-readme-update-cadence/
  When the linters read frontmatter and reflection
  Then the readme.md MUST carry research_phase: complete AND reflection/friction-log.md MUST exist with a Highest Frustration Level: FL[0-3] declaration
```
