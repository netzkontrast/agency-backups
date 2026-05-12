---
type: adr
status: active
slug: 0010-novel-architect-error-tier-linter-policy
summary: "Permit ERROR-tier (gating) for novel-architect-family linters that mechanize prose specs from Tasks 072/073/075/076. Narrow scope: 4 planned linters + worksheet_audit body-check. 12-month sunset + 3 falsifier triggers force re-evaluation."
created: 2026-05-12
updated: 2026-05-12
adr_id: ADR-0010
adr_status: Proposed
adr_owner: agency-maintainer
adr_tags:
  - linter
  - error-tier
  - novel-architect
  - policy
  - skill-scoped-tooling
---

# ADR-0010 — Novel-Architect ERROR-Tier Linter Policy (Narrow)

## Context and Problem Statement

Tasks [072](../tasks/072-novel-architect-phase2-worksheet-loop/), [073](../tasks/073-novel-architect-hard-rules-validation/), [075](../tasks/075-novel-architect-scene-level-bridge/), and [076](../tasks/076-novel-architect-canon-status-schema/) (children of [Task 070](../tasks/070-novel-architect-v110-epic/) — the v1.1.0 Epic) shipped four prose specifications carrying Gherkin acceptance criteria with normative `MUST` / `MUST NOT` clauses:

| Source spec | Scope of MUST clauses | Current enforcement |
|---|---|---|
| [`methods/storyform/worksheet-loop.md`](../skills/novel-architect-structure/methods/storyform/worksheet-loop.md) | Phase 2 sub-phases MUST follow Worksheet Steps 0–8 ordering | Prose only — no linter |
| [`methods/validation/hard-rules.md`](../skills/novel-architect-structure/methods/validation/hard-rules.md) + [`assets/hard-rules-check.md`](../skills/novel-architect-structure/assets/hard-rules-check.md) | H1–H12 hard rules MUST pass before Gate 3 approval | Prose only — no linter |
| [`novel-architect-scene/methods/scene-level-bridge.md`](../skills/novel-architect-scene/methods/scene-level-bridge.md) | Every scene-matrix moment MUST carry Q1–Q5 fields populated | Prose only — no linter |
| [`assets/canon-meta-schema.md`](../skills/novel-architect-structure/assets/canon-meta-schema.md) | `canon_status: disputed` MUST NOT block active phase; `decanonized` MUST NOT be referenced | Prose only — no linter |

Without mechanical enforcement, these specifications degrade silently: storyform schema-drift goes undetected until manual archaeology against `dramatica-theory` reveals the violation, and the v1.1.0 Epic's Goal §3 (`tools/check-governance.sh` exits 0 after all sub-tasks land) was satisfied without protecting the post-merge state from regression.

The four planned linters that close this gap are scheduled in Epic 083 (Mini-Epic for v1.2.0):

| Planned linter | Source spec | Severity question |
|---|---|---|
| `tools/check-hard-rules.py` (+ folded `worksheet_audit` body-schema) | Task 073 hard-rules + Task 072 worksheet_audit | ERROR or WARN? |
| `tools/check-worksheet-order.py` | Task 072 worksheet-loop | ERROR or WARN? |
| `tools/check-scene-audit.py` | Task 075 scene-level-bridge | ERROR or WARN? |
| `tools/check-canon-status.py` | Task 076 canon-status-schema | ERROR or WARN? |

Existing repo precedent for *skill-scoped* (not repo-wide) linters is exclusively **WARN-tier**: `tools/check-rfc2119-polarity.py`, `tools/check-assumption-log.py`, `tools/check-narrative-ontology-load.py` all run advisory under `tools/check-governance.sh`. ERROR-tier slots are currently reserved for repo-wide schema/structural integrity (`tools/fm/validate.py --type-check`, `tools/lint-structure.py`, `tools/adr/cli.py validate`). Promoting four new linters to ERROR-tier on a single-skill-family path is a precedent shift versus this convention and therefore requires a recorded decision.

## Decision Drivers

### Binding prose-spec status is already T4-immutable

Tasks 072, 073, 075, 076 closed `done` on PR #102. Per [MAINTENANCE.md §1](../MAINTENANCE.md#1-repair-permission-tiers) the prose `MUST` clauses in their shipped specs are T3/T4 — they cannot be relaxed by in-place edit. The choice is therefore not "should we enforce them?" (they are already binding) but "how do we enforce them — by prose audit during Gate 3 review, or mechanically?"

### Silent storyform schema-drift is unrecoverable

H1–H12 violations (e.g. an `architecture.yaml` where two throughlines share a Class) propagate through Phase 3 character-architecture and Phase 4 research integration before becoming visible. By Phase 5 the drift is wedged into NCP moment frontmatter, and the recovery cost is a manual storyform reconstruction across 8 phases. Catching the violation at Gate 3 entry via mechanical check is the difference between a 30-second linter failure and a 2-hour archaeology session.

### Maintenance bypass already exists

[`tools/check-maintenance-bypass.py`](../tools/check-maintenance-bypass.py) (ratified via Task 037 and PRE_COMMIT.md §7.A) supports per-rule waivers covered by an open Task. A false-positive in a new ERROR-tier linter does not therefore force `--no-verify` (which [AGENTS.md](../AGENTS.md) and [CLAUDE.md §11](../CLAUDE.md#11-branch--commit-conventions) forbid) — it can be waived via the bypass mechanism while the linter is corrected. This safety net materially reduces the false-positive blast radius that would otherwise argue against day-1 ERROR-tier.

### Fixture corpus discipline mitigates novelty risk

Each linter in Epic 083 is required to ship with ≥3 known-clean + ≥3 known-bad fixtures (per `/sc:workflow` Phase 7 contract). The fixtures pin the linter's behaviour at landing time; subsequent edits run the suite. ERROR-tier promotion without a fixture corpus would be reckless, but with the corpus the linter's contract is mechanically auditable.

### Per-path scoping keeps cost local

Each linter is invoked by `tools/check-governance.sh` only when the staged diff or `task_affects_paths` includes `skills/novel-architect*/` or `novel-projects/`. Non-narrative commits pay zero CPU cost; the +<500ms-per-linter budget (and +<2s total per `/sc:workflow` Phase 7) materializes only on narrative work. ERROR-tier promotion does not penalize the rest of the repo.

### Precedent for skill-scoped tooling exists at ADR-0007

[ADR-0007 `skill-bundles-tools-frontmatter`](./0007-skill-bundles-tools-frontmatter.md) ratified that skill-scoped tooling declarations are first-class via the `skill_bundles_tools` allowlist. The present ADR extends the same per-skill-scoping principle from "skill declares the tools it ships" to "skill declares the linters that gate the tools it ships." The two ADRs together establish the per-skill-scoping pattern.

## Considered Options

### Option 1 — Keep WARN-tier (status quo)

Add the four new linters at WARN-tier alongside `check-rfc2119-polarity.py` et al. Violations surface as advisory diagnostics; `tools/check-governance.sh` exits 0 even when a hard-rule fails.

- **Positives.** Zero precedent shift; ERROR-tier remains reserved for repo-wide structural integrity. False-positives never block a commit. Linter authors face lower pressure to nail the fixture corpus on day 1.
- **Negatives.** The prose `MUST` clauses remain enforced only by reviewer attention. Silent drift returns the moment review is rushed. The four linters become a documentation artefact ("we have a linter for this") that is bypassable by anyone who chooses not to read the WARN output. Defeats the v1.2.0 enforcement Goal that Epic 083 is built around.
- **Cost.** Zero migration; ongoing cost is whatever WARN-tier already imposes (none, since pre-commit doesn't gate on WARN).

### Option 2 — ERROR-tier scoped to novel-architect family (chosen)

Permit the four planned linters (`check-hard-rules.py`, `check-worksheet-order.py`, `check-scene-audit.py`, `check-canon-status.py`, plus the `worksheet_audit` body-schema check folded into `check-hard-rules.py`) to ship at ERROR-tier under `tools/check-governance.sh`. The promotion is governed by three preconditions:

- **(i)** Each linter MUST ship with ≥3 known-clean + ≥3 known-bad fixtures under `tools/novel-architect-checks/tests/fixtures/`.
- **(ii)** Each linter MUST complete in <500ms on a reference `consciousness-novel` workspace; aggregate pre-commit budget +<2s.
- **(iii)** `tools/check-maintenance-bypass.py` MUST be wired to cover the new linters' rule-IDs (`HR.H1..H12`, `WS.STEP_ORDER`, `SC.Q1..Q5`, `CS.STATUS_VIOLATION`) so transition false-positives can be waived via an open Task rather than `--no-verify`.

- **Positives.** Mechanical enforcement of binding `MUST` clauses. Silent drift becomes impossible at the pre-commit boundary. The fixture corpus pins linter behaviour and is part of the change-control surface (a fixture deletion is a reviewer-visible diff). Maintenance bypass covers the false-positive escape valve. The v1.2.0 enforcement Goal is mechanically met.
- **Negatives.** Precedent shift on the WARN-vs-ERROR convention for skill-scoped linters. Adds four entries to the ERROR-tier stage of `tools/check-governance.sh`. If a fixture corpus is shipped weak, the first false-positive degrades trust in the policy (mitigated by precondition (i) + (iii)).
- **Cost.** Per-linter sub-task implementation per Epic 083 plan (5 sub-tasks 084–088); ADR review + acceptance.

### Option 3 — General per-skill ERROR-tier policy

Generalize Option 2 into a policy applicable to any skill: any skill MAY ship ERROR-tier linters provided preconditions (i)–(iii) hold. Future skills (e.g. `dramatica-scenarios-*`, `the-agency-system-architect`) would inherit the same allowance without authoring a separate ADR.

- **Positives.** Future-proofs the precedent; eliminates the per-skill ADR overhead. Establishes a clear gate (preconditions i/ii/iii) for any skill to graduate WARN → ERROR.
- **Negatives.** Speculation: no second skill currently needs ERROR-tier. Generalizing now means reviewers consider implications for skills that don't exist yet. Per [ADR principle](../research/adr-spec-research-synthesis/output/SPEC.md): capture decisions when they're being made, not in advance. Premature generalization risks locking in an interface that the second-skill-case reveals as wrong.
- **Cost.** Lower per-skill cost long-term; higher review-burden now (broader scope to evaluate).

### Option 4 — WARN-then-promote staged rollout

Ship the four linters at WARN-tier in Epic 083 sub-tasks 084–086, observe false-positive rates for one Epic-cycle (~2-4 weeks of dogfooding), then file ADR-001X to promote to ERROR-tier.

- **Positives.** Lowest risk against false-positives; a staged-rollout corpus emerges naturally from the WARN-tier observation window. Matches the cautious-introduction pattern used for `check-narrative-ontology-load.py` (initially WARN, slated for promotion only after corpus stabilizes).
- **Negatives.** Defers the v1.2.0 enforcement Goal by one Epic-cycle; the period between landing and promotion is a regression window. Adds the meta-overhead of a second ADR (the promotion). The fixture-corpus discipline of Option 2 already addresses most false-positive risk; the staged rollout is double-protection at the cost of timeline.
- **Cost.** Lowest per-step risk; highest total-elapsed time and meta-overhead.

## Decision Outcome

**Option 2 (ERROR-tier scoped to novel-architect family) is chosen, recorded as `adr_status: Proposed`.**

The four planned linters (`tools/check-{hard-rules,worksheet-order,scene-audit,canon-status}.py`) MAY ship at ERROR-tier under `tools/check-governance.sh`, provided preconditions (i)–(iii) above hold at landing time. The `worksheet_audit` body-schema check (Task 072 leftover) is folded into `check-hard-rules.py` under rule-IDs `WA.STEP_*_SET` and inherits the same ERROR-tier status.

ERROR-tier insertion in `tools/check-governance.sh` lands as a new gating stage between `tools/adr/cli.py validate` and `tools/fm/index_diff.py`, path-scoped to staged diffs touching `skills/novel-architect*/` or `novel-projects/`. Non-narrative commits remain unaffected.

### Falsifier triggers — re-open this ADR when any of the following hold

- **F1.** False-positive rate exceeds **5 ERROR-tier blockings per 30-day window** that are subsequently waived via `tools/check-maintenance-bypass.py` without a fix to the linter. Sustained false-positive pressure means the fixture corpus is incomplete or the rule is mis-specified; either way the ERROR-tier promotion was premature.
- **F2.** `tools/check-maintenance-bypass.py` accumulates **≥3 open bypass entries** for novel-architect-family linter rule-IDs simultaneously across **>30 days**. Bypass is the safety valve, not the steady state; sustained reliance on it means the linter is mis-calibrated.
- **F3.** A **second skill** (e.g. `dramatica-scenarios-*`, `the-agency-system-architect`, or any newly-authored skill) requests ERROR-tier for its own linter family. At that point the per-skill-ADR overhead becomes a real cost, and Option 3 (general per-skill policy) MUST be re-evaluated. The successor ADR generalizing Option 2 → Option 3 supersedes this one via `adr_supersedes: [ADR-0010]`.

When any falsifier triggers, a successor ADR MUST be authored that re-evaluates the options under the then-current evidence.

### Calendar sunset — 12-month forced review

Independent of the falsifier triggers, this ADR carries a **mandatory review trigger at 2027-05-12**. By that date a maintainer MUST either (a) flip `adr_status` to `Accepted` (formal ratification of the narrow scope), (b) author the successor ADR generalizing to per-skill policy (Option 3), or (c) author the successor ADR rolling back to WARN-tier (Option 1) if false-positive evidence accumulated.

Allowing the sunset to lapse without action is itself a friction signal (FRUSTRATED.md FL1+) and SHOULD surface in the Nightly Maintenance Run as an audit finding against `decisions/0010-*.md`.

### Status note on `adr_status: Proposed`

This ADR ships at `Proposed` rather than `Accepted` because preconditions (i)–(iii) cannot be verified until Epic 083 sub-tasks 084–086 have landed with their fixture corpora and the first 30-day observation window has elapsed. Premature ratification would lock the policy against the very corpus-quality and false-positive evidence the falsifier triggers are designed to surface. A maintainer flipping to `Accepted` SHOULD do so only after (a) all four linters have landed at ERROR-tier per Epic 083, (b) the 30-day post-landing window passes without F1/F2 firing, and (c) the fixture corpora pass an independent review.

## Consequences

### Positive

- The four prose `MUST` clauses landed by Tasks 072/073/075/076 become mechanically enforced; silent storyform schema-drift becomes impossible at pre-commit.
- Epic 083's v1.2.0 enforcement Goal is satisfiable via a single coherent policy rather than per-linter ad-hoc decisions.
- The fixture-corpus precondition (i) makes linter behaviour part of the change-control surface; a fixture deletion is a reviewer-visible diff rather than a silent regression.
- The maintenance-bypass safety valve (precondition iii) absorbs false-positives without forcing `--no-verify`, preserving the [CLAUDE.md §11](../CLAUDE.md#11-branch--commit-conventions) hook discipline.
- Per-path scoping (`tools/check-governance.sh` runs the new stage only on narrative-touching diffs) means non-narrative work pays zero additional cost.
- ADR-0010 establishes a per-skill-scoping precedent that complements [ADR-0007](./0007-skill-bundles-tools-frontmatter.md) (skill declares its tools) by adding "skill declares the linters that gate its tools."

### Negative

- Precedent shift on the WARN-vs-ERROR convention for skill-scoped linters. Future reviewers will reasonably ask "does my new skill linter qualify for ERROR-tier?"; the falsifier-trigger F3 + 12-month sunset are the structured answer, but the recurrence cost is real.
- If a fixture corpus ships weak (e.g. only the 3-minimum required, missing edge cases), the first false-positive in production degrades policy trust. Mitigation: precondition (i) is a MUST, and the linter sub-tasks (084-086) carry explicit fixture-corpus acceptance criteria.
- Adds four entries to the ERROR-tier stage of `tools/check-governance.sh`; +<2s pre-commit budget on narrative-touching diffs. Acceptable per Epic 083 acceptance criterion but not free.
- The narrow scope means the second skill needing ERROR-tier MUST author a successor ADR rather than inheriting. This is intentional (Option 3 rejection rationale) but adds review overhead at the second-skill-case.

### Neutral

- This ADR is the *sibling* decision to [ADR-0007](./0007-skill-bundles-tools-frontmatter.md) (skill declares its tools). Together they establish the per-skill-scoping pattern: skills are first-class scope-units for both tooling declarations (ADR-0007) and linter severity policy (ADR-0010).
- The "measure-friction-then-act" pattern shared with [ADR-0008](./0008-narrative-skills-status-quo.md) (narrative skills status quo) and [ADR-0009](./0009-root-spec-no-consolidation.md) (root-spec bundle status quo) is preserved: ratification to `Accepted` waits on measured evidence (the 30-day post-landing window).
- The successor-via-falsifier-trigger pattern (F1/F2/F3 plus calendar sunset) is the structured answer to "when do we revisit this?" rather than the looser "review periodically" alternative used by some other repo policies.
- No follow-on implementation Task is created by this ADR itself. Epic 083 and its sub-tasks (084–088) are the implementation surface; this ADR is the policy precondition they cite.

## Cross-references

- [Task 070 — novel-architect@1.1.0 Epic](../tasks/070-novel-architect-v110-epic/task.md) — the v1.1.0 Epic whose prose specs this policy enforces.
- [Task 072 — Phase 2 Worksheet-Loop](../tasks/072-novel-architect-phase2-worksheet-loop/task.md) — the binding worksheet-order + worksheet_audit spec.
- [Task 073 — Hard Rules Validation](../tasks/073-novel-architect-hard-rules-validation/task.md) — the binding H1–H12 spec.
- [Task 075 — Scene-Level-Bridge](../tasks/075-novel-architect-scene-level-bridge/task.md) — the binding scene-audit Q1–Q5 spec.
- [Task 076 — Canon-Status Schema](../tasks/076-novel-architect-canon-status-schema/task.md) — the binding canon-status hierarchy spec.
- [Task 077 — MIF Level 3 + SessionStart-Hook](../tasks/077-novel-architect-mif-learnings-sessionhook/task.md) — sibling v1.1.0 deliverable; informs the MIF L3 backport scoped in Epic 083 sub-task 088.
- [ADR-0007 — Skill-Bundles-Tools Frontmatter](./0007-skill-bundles-tools-frontmatter.md) — sibling per-skill-scoping precedent.
- [`tools/check-maintenance-bypass.py`](../tools/check-maintenance-bypass.py) — the precondition-(iii) safety valve.
- [`PRE_COMMIT.md §7.A`](../PRE_COMMIT.md#7a-toolchain-precedence-matrix) — toolchain precedence governing the new ERROR-tier stage.
- [`CLAUDE.md §6`](../CLAUDE.md#6-pre-commit-gate--what-runs-and-when) — pre-commit gate documentation; will gain a row for the new ERROR-tier novel-architect-checks stage when Epic 083 sub-task 084 lands.
