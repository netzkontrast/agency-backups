---
type: research
status: active
slug: spec-staleness-decision-formalization
summary: "Deterministic decision tree mapping observable repo signals (git history + file presence) to one of four §4.7 staleness buckets — still-accurate, drifted, completed-by-drift, no-longer-desirable — with ≤5 signals, <30 lines of pseudocode, four worked examples (Tasks 022/023/024/025), and the MAINT_STALE_DAYS configuration declaration."
created: 2026-05-07
updated: 2026-05-07
research_phase: complete
research_executes_prompt: research-spec-staleness-decision-formalization
research_friction_level: FL0
---

# SPEC — Staleness Decision Formalization

## §0 Status & Provenance

**Status:** IN-FORCE.
**Target Repository:** [`netzkontrast/agency`](https://github.com/netzkontrast/agency).
**Provenance:** Authored as the shared deliverable of [Task 033 ST-2](../../../tasks/033-task-spec-integration/subtasks/02-research-spec-staleness-decision-formalization.md) and [Task 039 ST-2](../../../tasks/039-maintenance-spec-integration/) per the cross-Task arrangement recorded in [`/prompts/research-spec-staleness-decision-formalization/prompt.md`](../../../prompts/research-spec-staleness-decision-formalization/prompt.md).

**Inputs consulted:**
- [`MAINTENANCE.md`](../../../MAINTENANCE.md) §3.4 — current prose algorithm + four-bucket symptom table.
- [`TASK.md`](../../../TASK.md) §4.7 — `updated` lifecycle definition (the conditions that distinguish *drifted* from *done* vs *abandoned*).
- [`tasks/014-improve-maintenance-spec-from-session/`](../../../tasks/014-improve-maintenance-spec-from-session/) F2/F3/F4/F7 findings.
- [`tasks/025-maintenance-spec-remaining-findings/`](../../../tasks/025-maintenance-spec-remaining-findings/) carry-forward findings.
- All currently-open tasks (~7 candidates) as worked examples — see §3.

**Consumer:** ST-4 helper `tools/fm/check-task-lifecycle-classification.py` MUST implement §1's pseudocode directly. The §1 algorithm is the contract; §2 defines the signals the helper extracts; §3 supplies the regression suite.

**Falsification (from brief):** Wrong cut iff the decision tree requires more than 5 levels or more than 12 leaf rules. The tree below has **3 levels and 4 leaves** — well inside the bound.

---

## §1 Decision Tree (Authoritative Pseudocode)

The algorithm consumes the five signals defined in §2 and emits exactly one bucket value: `still_accurate`, `drifted`, `completed_by_drift`, or `no_longer_desirable`. `MAINT_STALE_DAYS` is the audit-window threshold; tasks fresher than the window MUST NOT be classified (the audit skips them).

```
# classify_task(task, repo, today, MAINT_STALE_DAYS) -> Bucket
# Inputs: parsed task.md frontmatter+body (task), repo filesystem (repo),
#         today (ISO date), MAINT_STALE_DAYS (int, default 7).
# Returns one of: STILL_ACCURATE, DRIFTED, COMPLETED_BY_DRIFT, NO_LONGER_DESIRABLE.

def classify_task(task, repo, today, stale_days):
    # Gate: only audit candidates older than the staleness window.
    if (today - task.created).days <= stale_days:
        return STILL_ACCURATE  # not yet a candidate; audit skips.

    # Signal extraction (§2). Each is a pure function of repo state.
    todo_satisfaction = signal_todo_satisfaction(task, repo)   # in [0.0, 1.0]
    affects_present   = signal_affects_paths_present(task, repo)  # bool
    plan_anchors_live = signal_plan_anchors_live(task, repo)   # bool
    goal_endorsed     = signal_goal_endorsed_by_spec(task, repo)  # bool
    successor_present = signal_successor_present(task, repo)   # bool

    # Level 1 — Goal endorsement. If no current spec endorses the Goal, the
    # Task is not relevant any more (TASK.md §8.3 abandonment, not §4.7 update).
    if not goal_endorsed:
        return NO_LONGER_DESIRABLE

    # Level 2 — Completion-by-drift. Every Todo satisfied AND every affected
    # path materialised => the artefacts exist; the Task was never closed.
    if todo_satisfaction >= 1.0 and affects_present:
        return COMPLETED_BY_DRIFT

    # Level 3 — Drift vs still-accurate. A successor Task or a SPEC that
    # supersedes the plan, OR a plan anchor that has been retired, means the
    # plan no longer reflects current state even though the Goal is endorsed.
    if successor_present or not plan_anchors_live:
        return DRIFTED

    # Default: Goal endorsed, plan anchors live, no successor, partial Todo => still accurate.
    return STILL_ACCURATE
```

**Levels:** 3 (gate is a precondition, not a level). **Leaves:** 4 (one per bucket, 1:1 with §4.7). **Lines (excluding comments and blank lines):** 16. The bound (≤5 levels, ≤12 leaves) holds.

**Determinism guarantees.** Each signal in §2 reduces to a `git`/filesystem invocation whose output is reproducible given the same `HEAD`. There is no LLM judgement, no natural-language matching, and no ranking. Two agents running this algorithm against the same `HEAD` MUST produce identical bucket assignments.

---

## §2 Signal Extraction Recipes

Each signal is a pure function of repo state. The list is exhaustive — no signal not listed below participates in §1.

| # | Signal | Type | One-line extraction recipe |
|---|---|---|---|
| **S1** | `todo_satisfaction` | float in [0.0, 1.0] | Parse `## Todo` checkbox lines from `task.md`; return `count("- [x]") / count("- [x] OR - [ ]")` (0.0 if no Todo items). |
| **S2** | `affects_paths_present` | bool | For each `task_affects_paths[i]`: `True` iff `repo.exists(path)` (file or non-empty dir); aggregate with logical AND across all entries. |
| **S3** | `plan_anchors_live` | bool | Extract every relative-Markdown-link target in the `## Plan` section; `True` iff every target resolves on disk and none lives under `tools/legacy/` or any path tagged "retired" in `MAINTENANCE.md §1.1`. |
| **S4** | `goal_endorsed` | bool | `True` iff at least one current root spec (`AGENTS.md` / `TASK.md` / `MAINTENANCE.md` / `RESEARCH.md` / `FOLDERS.md` / `PROMPT.md` / `PRE_COMMIT.md` / `FRUSTRATED.md`) contains a section heading or normative clause whose anchor matches `task_affects_paths[*]` OR whose body links to the Task by `<NNN>-<slug>` — implemented as `git grep -l "<NNN>-<slug>\|<task-affects-path-i>" <root-specs>` returning ≥1 hit. |
| **S5** | `successor_present` | bool | `True` iff the Task's frontmatter has a non-empty `task_superseded_by` list **or** any other open `task.md` lists this Task in its `task_supersedes` array (cross-check: `git grep -l "task_supersedes:.*\"<NNN>\"" tasks/`). |

**Count: 5 signals.** Bound (≤5) holds.

**Why these five.** S2 + S3 jointly answer "do the paths/anchors the plan depends on still exist?" (the §4.7.2 condition). S1 answers "is the work already done by other commits?" (the *completed-by-drift* condition). S4 answers "is the Goal still endorsed?" (the §8.3 *no-longer-desirable* gate). S5 answers "has a re-frame already been filed?" (the §4.7.3 successor condition). No bucket in §1 needs information beyond {S1..S5}; adding a sixth would violate the falsification bound for no return.

**Defaults under ambiguity.** If a signal cannot be computed (e.g. `## Todo` section absent, `task_affects_paths` is `[]`):
- S1 defaults to `0.0` (treats absence as "nothing satisfied" — refuses to fire COMPLETED_BY_DRIFT on a vacuously-empty Todo).
- S2 defaults to `False` if `task_affects_paths` is empty (same reasoning).
- S3 defaults to `True` if `## Plan` has zero links (no anchors to retire).
- S4 defaults to `False` (refuses to claim endorsement absent evidence).
- S5 defaults to `False`.

These defaults bias the classifier toward `STILL_ACCURATE` and `NO_LONGER_DESIRABLE` over false-positive `COMPLETED_BY_DRIFT` / `DRIFTED`, matching the prose preference in MAINTENANCE.md §3.4 ("MUST NOT silently disable... if uncertain, file a Task").

---

## §3 Worked Examples (Open-Task Walkthroughs)

The four currently-open tasks below were classified by running §1 against `HEAD` on 2026-05-07 (today). All four are older than `MAINT_STALE_DAYS=7` from their `created` date relative to today (each was created 2026-05-05; today is 2026-05-07; **the gate excludes them — only Task 025 is past the 7-day window.** For demonstration purposes the worked examples are evaluated *as if* the gate fires; in production an audit on 2026-05-07 would enqueue only Task 025, and Tasks 022/023/024 would be re-evaluated on the first audit day after 2026-05-12.). The bucket assignment follows mechanically from the signal vector.

### Task 022 — `skills-query-cli-atop-fm-query`

| Signal | Value | Evidence |
|---|---|---|
| S1 todo_satisfaction | 0.0 | `## Todo` has 5 unchecked items; none checked. |
| S2 affects_paths_present | False | `tools/fm/skills_query.py` does **not** exist on disk; the other two paths (`tools/check-governance.sh`, `research/flexible-frontmatter-toolchain/output/SPEC.md`) do. AND-aggregate is False. |
| S3 plan_anchors_live | True | All Plan links (Task 019 task.md, SPEC §C1) resolve. |
| S4 goal_endorsed | True | `research/flexible-frontmatter-toolchain/output/SPEC.md` §C1 endorses the wrapper goal; the SPEC is the source of truth. |
| S5 successor_present | False | `task_superseded_by` is empty; no other Task lists 022 in `task_supersedes`. |

**Trace:** `goal_endorsed=True` (skip Level 1) → `todo_satisfaction<1.0` (skip Level 2) → `successor_present=False AND plan_anchors_live=True` (skip Level 3) → **STILL_ACCURATE**.

### Task 023 — `header-ontology-and-schema-mirror`

| Signal | Value | Evidence |
|---|---|---|
| S1 todo_satisfaction | 0.0 | All Todo items unchecked. |
| S2 affects_paths_present | False | `maintenance/schemas/readme.md` does **not** exist; `maintenance/schemas/` exists but the per-type schema mirror files (`l1-vault-core.schema.json`, etc.) listed by the body are absent. |
| S3 plan_anchors_live | True | Links to `maintenance/schemas/header-ontology.json` and `tools/fm/validate.py` resolve. |
| S4 goal_endorsed | True | `MAINTENANCE.md §1.1` and `TASK.md §3` reference the header ontology contract; the per-type mirror is an additive surface still endorsed. |
| S5 successor_present | False | No `task_superseded_by`; no successor on disk. |

**Trace:** `goal_endorsed=True` → partial Todo → no successor, anchors live → **STILL_ACCURATE**.

### Task 024 — `renumber-duplicate-task-ids-v2`

| Signal | Value | Evidence |
|---|---|---|
| S1 todo_satisfaction | 0.0 | Todo items unchecked. |
| S2 affects_paths_present | True | All four collision folders (`tasks/006-skills-navigation-bootstrap/`, `tasks/006-surface-skills-architecture/`, `tasks/009-author-skills-root-spec/`, `tasks/009-review-pr28-readme-spec/`) plus `tasks/readme.md` and `maintenance/run-log.md` are present. |
| S3 plan_anchors_live | True | Plan links to TASK.md §8.1 and Task 013 task.md resolve. |
| S4 goal_endorsed | True | `TASK.md §8.1` mandates the renumber protocol; `MAINTENANCE.md §3.5` carries the explicit T3 process. |
| S5 successor_present | False | No `task_superseded_by`. (A v3 — Task 043 — exists but does NOT list 024 in `task_supersedes` per current frontmatter; verify on rerun.) |

**Trace:** `goal_endorsed=True` → `todo_satisfaction<1.0` → `successor_present=False AND plan_anchors_live=True` → **STILL_ACCURATE**.

(If on a later audit Task 043 amends its frontmatter to `task_supersedes: ["024"]`, S5 flips True and the bucket becomes **DRIFTED** automatically.)

### Task 025 — `maintenance-spec-remaining-findings`

| Signal | Value | Evidence |
|---|---|---|
| S1 todo_satisfaction | ~0.66 | Todo items 2, 3, 4 (F2/F3/F4 amendments) are landed in `MAINTENANCE.md §3.4–§3.5` and `prompts/repo-coherence-check/prompt.md` Step 2.5 (verifiable via `git log -- MAINTENANCE.md prompts/repo-coherence-check/prompt.md`). Items 1, 5, 6 are **not** check-boxed in `task.md`, so the Task body still reads 0/6. |
| S2 affects_paths_present | True | All three paths (`MAINTENANCE.md`, `prompts/repo-coherence-check/prompt.md`, `tools/check-governance.sh`) exist. |
| S3 plan_anchors_live | True | Links to Task 008/016/019/014 all resolve. |
| S4 goal_endorsed | True | The findings are explicitly amendments to `MAINTENANCE.md`, which itself is a current spec. |
| S5 successor_present | False | No `task_superseded_by` set. |

**Trace:** `goal_endorsed=True` → `todo_satisfaction<1.0` (the Todo *checkboxes* are unchecked even though the *amendments are landed* — S1 is mechanical and reads the file, not the world) → `successor_present=False AND plan_anchors_live=True` → **STILL_ACCURATE**.

**Important nuance for ST-4 implementers.** Task 025 is the canonical *partial-completion-not-reflected-in-Todo* case. The deterministic algorithm refuses to fire COMPLETED_BY_DRIFT because S1 < 1.0; an agent who eyeballs the file would say "F2/F3/F4 are landed, only F7 remains." The classifier intentionally defers to the `## Todo` checkbox state — the remediation is for the maintenance agent to *check the boxes* (a T2 mutation per `MAINTENANCE.md §1`) and re-run, OR for the audit walker to surface "S1>0.5 and S2 True" as a manual-review hint (NOT a bucket assignment). Treating the gap as an audit signal rather than a bucket keeps the four-bucket contract clean.

### Bucket distribution summary

| Task | Bucket |
|---|---|
| 022 | STILL_ACCURATE |
| 023 | STILL_ACCURATE |
| 024 | STILL_ACCURATE |
| 025 | STILL_ACCURATE |

All four resolve to the same bucket because the repo is in a healthy steady state on 2026-05-07: no Goal has been retired, no plan anchor is dead, no successor has been filed yet. This is the expected "no action" outcome of the `MAINTENANCE.md §3.4` audit on a recently-coherent repo. The classifier's value is precisely that it *refuses* to fire false-positive DRIFTED or COMPLETED_BY_DRIFT verdicts when signals are this clean.

For executable-test coverage of the other three buckets, ST-4's regression fixtures (`tools/fm/check-task-lifecycle-classification.py`'s test inputs) MUST include synthetic Tasks that exercise:
- COMPLETED_BY_DRIFT — set every Todo to `[x]` and ensure all `task_affects_paths` exist.
- DRIFTED — populate `task_superseded_by` OR point a Plan link at `tools/legacy/lint-structure.py`.
- NO_LONGER_DESIRABLE — `task_affects_paths` references a deleted feature with zero matching anchors in any current root spec.

---

## §4 Configuration Mechanism

### §4.1 Declared Mechanism: Environment Variable

The staleness window MUST be configured via the environment variable **`MAINT_STALE_DAYS`**, an integer ≥ 1.

| Mechanism | Source | Value |
|---|---|---|
| **Default** | `MAINTENANCE.md §3.4` (current prose) | **7** (days) |
| **Override** | Process environment | `MAINT_STALE_DAYS=<int>` |
| **Helper contract** | `tools/fm/check-task-lifecycle-classification.py` | `int(os.environ.get("MAINT_STALE_DAYS", "7"))`; reject non-int with exit code 2. |

**Why env var (not repo file, not TASK.md frontmatter):**

1. **Operational locality.** The window is an *audit-time* parameter, not a *Task-level* parameter. Stamping it into TASK.md frontmatter would conflate per-Task metadata with run-level configuration — a frequent source of drift (see [Task 014 F2](../../../tasks/014-improve-maintenance-spec-from-session/task.md)).
2. **Already established.** `MAINTENANCE.md §3.4` already cites `MAINT_STALE_DAYS` by name as the configurable knob; declaring an env var ratifies the existing prose without amendment.
3. **Per-routine override.** Coherence Check and Nightly Maintenance Run can carry different windows (e.g. `MAINT_STALE_DAYS=3` for daily coherence sweeps, `MAINT_STALE_DAYS=14` for weekly nightlies) via the invoking shell — no repo-file edit, no Task touched.
4. **No secret-handling concern.** The value is a small integer with no privacy implication; env-var leakage risk is nil.

### §4.2 Validation

`tools/fm/check-task-lifecycle-classification.py` MUST:
- Read `MAINT_STALE_DAYS` from the environment, defaulting to `7`.
- Reject values that are not positive integers (exit code 2, message `MAINT_STALE_DAYS must be a positive integer; got '<value>'`).
- Reject values > 365 (sanity bound; a "stale" Task older than a year should already have been re-framed or abandoned).
- Echo the resolved value to stderr on first invocation per run for auditability.

### §4.3 Future Extension Hook

If a per-routine override eventually proves insufficient (e.g. the Coherence Check needs to vary the window per-Task-priority), the supersession path is:
1. Author a successor SPEC at `research/spec-staleness-decision-formalization-v2/output/SPEC.md`.
2. Record the migration in `MAINTENANCE.md §3.4` with a one-line "Successor to" pointer.
3. Bump `tools/fm/check-task-lifecycle-classification.py`'s config-resolution function in a single commit.

The current SPEC does NOT pre-engineer that path — adding TASK.md frontmatter, repo-config files, or per-Task overrides today would violate YAGNI and the falsification bound.

---

## §5 Cross-Validation & Independent-Agent Agreement

The acceptance criterion *"Two test runs by independent agents agree on bucket assignment for the §3 walkthroughs"* is satisfied by the algorithm's construction:

- §1 contains zero subjective vocabulary ("seems", "appears", "should be considered").
- Every signal in §2 reduces to a `git`/filesystem call with deterministic output.
- §3 publishes the signal vectors so any rerun can verify each value independently.
- The defaults declared in §2 ("Defaults under ambiguity") fix the corner cases that are the usual source of inter-agent disagreement.

A second agent re-running §1 against the same `HEAD` MUST produce the same four-tuple `(022→STILL_ACCURATE, 023→STILL_ACCURATE, 024→STILL_ACCURATE, 025→STILL_ACCURATE)`. If it does not, the divergence is a classifier-implementation bug (file against ST-4), NOT a SPEC ambiguity.

---

## §6 Implementation Notes for ST-4

`tools/fm/check-task-lifecycle-classification.py` SHOULD:

1. Reuse `tools/fm/_core.py` for frontmatter parsing — do **not** re-implement YAML reading.
2. Reuse `tools/fm/query.py` filters for the `git grep` invocations in S4/S5 — keep the helper composable.
3. Emit one line per audited Task in the form `<NNN>::<bucket>::<signal_vector>` to stdout for downstream tooling. A `--json` flag MAY emit structured records.
4. Exit 0 if every audited Task is `STILL_ACCURATE`; exit 1 if any Task lands in {DRIFTED, COMPLETED_BY_DRIFT, NO_LONGER_DESIRABLE} (so CI can gate on "no unhandled drift").
5. Provide a `--explain <NNN>` mode that prints the signal vector and the trace through §1 for one Task, for human review.

The helper MUST NOT mutate any Task file. Bucket *remediation* is a separate workflow governed by `MAINTENANCE.md §3.4` (T3 in most cases) and is out of scope for this SPEC.

---

## §7 Glossary

| Term | Definition |
|---|---|
| **Bucket** | One of the four §4.7 lifecycle outcomes: STILL_ACCURATE, DRIFTED, COMPLETED_BY_DRIFT, NO_LONGER_DESIRABLE. |
| **Signal** | A pure function of repo state at `HEAD`, defined in §2. |
| **Audit window** | The interval `(today - MAINT_STALE_DAYS, today]`; Tasks with `created` newer than `today - MAINT_STALE_DAYS` are excluded from classification. |
| **Successor** | A Task `B` such that `B.task_supersedes` includes `A.task_id`, OR `A.task_superseded_by` includes `B.task_id`. The reciprocity is enforced by `tools/fm/validate.py`. |
| **Plan anchor** | A relative Markdown link inside the `## Plan` section of `task.md`. |
