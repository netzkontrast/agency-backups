---
type: adr
status: active
slug: 0008-narrative-skills-status-quo
summary: "Six narrative skills + narrative-ontology + dramatica-nav stay in this repo. The AGENTS.md NO.5 don't-load rule and WARN-tier linter remain the partition. Extraction deferred until a falsifier trigger fires."
created: 2026-05-11
updated: 2026-05-13
adr_id: ADR-0008
adr_status: Proposed
adr_owner: agency-maintainer
adr_tags:
  - skills
  - narrative-ontology
  - folder-topology
  - token-cost
---

# ADR-0008 — Narrative Skills Stay In-Repo (NO.5 Workaround Ratified)

## Context and Problem Statement

The repository hosts six narrative-craft skills — `skills/dramatica-theory/`, `skills/dramatica-vocabulary/`, `skills/ncp-author/`, `skills/novel-architect/`, `skills/the-agency-system-architect/`, `skills/suno-lyric-writer/` — plus a 19-file ontology under `maintenance/schemas/narrative-ontology/` and a 34-file navigator at `tools/dramatica-nav/`. The skills total ~128 files and ~2.2 MB on disk; together with the ontology and the navigator the narrative footprint is ~3.0 MB and ~180 files.

The `AGENTS.md` rule `NO.5` instructs agents doing non-narrative work *not to load* the Narrative Ontology because it is large, off-domain, and bootstrap-cost expensive. The rule is mechanically enforced WARN-tier by `tools/check-narrative-ontology-load.py` (Task 032 ST-2). This is a *workaround*: the content stays in the repo and an agent must remember to skip it.

[Task 053](../tasks/053-core-architecture-review-followups/) finding B.5 flagged the workaround as evidence that the narrative subtree might not belong in this governance-substrate repository at all. The single falsifiable outcome of [Task 056](../tasks/056-narrative-skills-extraction-adr/) is this ADR, choosing one of:

1. Extract the narrative subtree into a sibling repo (`agency-narrative/`).
2. Isolate the narrative subtree into a `skills/narrative/` namespace with its own root spec (`NARRATIVE.md`).
3. Status-quo: keep NO.5 + the linter; do not migrate.

## Decision Drivers

- **Actual token cost of NO.5 today.** The "Narrative Ontology — Dramatica × NCP × Novel-Architect Bridge" section in `AGENTS.md` (lines 290–356) is **8.6 KB / ~2150 tokens** in the bootstrap bundle. The bootstrap bundle is ~50 K tokens total (9 root specs per README §10), so the narrative section is **~4 %** of session boot. Not zero; not catastrophic.
- **Mechanical enforcement already exists.** `tools/check-narrative-ontology-load.py` WARN-fires when a non-narrative Task references the ontology, and `tools/check-governance.sh` runs it on every commit. The workaround is *enforced*, not merely *documented*. The fail-open is bounded.
- **Migration cost is real and concentrated.** Cross-references into the narrative subtree exist from 4 root specs (`AGENTS.md`, `SKILLS.md`, `PRE_COMMIT.md`, `MAINTENANCE.md`), 5+ tools (`tools/dramatica-nav/`, `tools/check-narrative-ontology-load.py`), and **>30 tasks/prompts/research workspaces** built on the existing paths. Any extraction or namespace change ripples through all of them.
- **In-flight Tasks would be disrupted.** [Task 030](../tasks/030-cleanup-dramatica-skills-corpus/) (done), [Task 042](../tasks/042-dramatica-nav-followups/) (open), [Task 015](../tasks/015-integrate-dramatica-ncp-skills/) (done) all assume the current `skills/<name>/` topology and the `maintenance/schemas/narrative-ontology/` path. Migrating mid-stream would invalidate their audit-graph edges.
- **The carve-out precedent exists.** [ADR-0006](./0006-agency-system-prototype-exemption.md) already records the `/Agency-System/` folder as exempt from operational-folder rules; its rationale (one-skill consumer + asset opacity + bounded blast radius) maps cleanly to the narrative subtree's situation, modulo the multi-skill consumer count.
- **The repo's purpose is governance + orchestration, not narrative authoring.** [`README.md §1`](../README.md) frames the repo as "a governance and orchestration substrate for long-horizon work performed by AI agents". The narrative skills *use* the substrate (frontmatter, audit graph, ADRs); they are not *the substrate itself*. This argues for eventual extraction.
- **Recurrence of the friction is the only honest signal.** The Task 053 finding raised the question once; it has not recurred under sustained operation. Until friction patterns from the maintenance run (FRUSTRATED.md FL1+) accumulate against the workaround, the data does not support a costly migration.

## Considered Options

### Option 1 — Extract to sibling repo (`agency-narrative/`)

Move all six narrative skills + the ontology + the navigator into a new sibling repo. `agency` retains only governance and orchestration substrate; cross-repo references via submodule or external URL.

- **Positives.** Cleanest separation; eliminates NO.5 entirely; the substrate repo's session-boot drops the ~4 % narrative token cost; future narrative skills land in the dedicated repo without negotiating governance churn.
- **Negatives.** Cross-repo CI burden (two repos must coordinate ADR governance, frontmatter linters, tools/fm/* updates); submodule-or-symlink discipline becomes a new failure mode (out-of-sync HEAD); audit-graph queries that today walk `task → prompt → research → skill` across one repo would have to walk across two; Tasks 030 / 042 mid-flight break; `tools/dramatica-nav/`, `tools/check-narrative-ontology-load.py`, and the four root-spec cross-references must be either duplicated, deleted, or pointer-redirected; the SKILLS.md ladder (T1/T2/T3 content tiers) was authored over the existing skill paths and would need adaptation.
- **Cost.** High (multi-week migration, plus ongoing two-repo coordination).

### Option 2 — Isolate as `skills/narrative/` namespace with own root spec

Move the six narrative skills under a new `skills/narrative/<skill>/` namespace; author `NARRATIVE.md` as a sibling root spec dedicated to narrative concerns; demote the `NO.1`–`NO.6` rules in AGENTS.md to a one-line pointer ("for narrative work, see NARRATIVE.md").

- **Positives.** Preserves single-repo audit graph; narrative concerns become a discoverable sub-substrate rather than a workaround; the AGENTS.md narrative section shrinks from ~70 lines to ~3 lines; future narrative tasks would `task_affects_paths: skills/narrative/...` which is mechanically simpler than the current per-skill enumeration.
- **Negatives.** Path churn across all >30 tasks/prompts/research workspaces; new root spec `NARRATIVE.md` adds to the 9-spec boot bundle (partial offset by the AGENTS.md shrink); `tools/dramatica-nav/`, `tools/check-narrative-ontology-load.py`, `PRE_COMMIT.md §7.A` matrix all carry hardcoded paths needing rewrite; `SKILLS.md`'s tier ladder language at line 235 references the dramatica corpus directly; new root spec means a maintenance burden equal to the current AGENTS.md narrative section.
- **Cost.** Medium (single-repo refactor; one root spec authored once).

### Option 3 — Status quo (chosen)

Keep the existing topology. `AGENTS.md` `NO.5` plus `tools/check-narrative-ontology-load.py` remain the partition mechanism. Future narrative skills land in `skills/<name>/` like the existing six. No migration.

- **Positives.** Zero migration cost. Tasks 030/042 unaffected. Audit-graph integrity preserved. The 4 % token cost of the AGENTS.md narrative section is a real but bounded expense; the mechanical NO.5 linter prevents *additional* loading inside non-narrative sessions, which is where the actual cost would compound. Cross-references in 4 root specs and 5+ tools remain stable.
- **Negatives.** AGENTS.md retains the `NO.1`–`NO.6` section (~70 lines, ~4 % of session boot). The substrate-vs-content distinction is fuzzed; new readers must learn the NO.5 workaround as their entry into narrative-skill discipline.
- **Cost.** Zero migration; ongoing AGENTS.md maintenance for the NO.* rules; periodic re-evaluation under the trigger conditions below.

## Decision Outcome

**Option 3 (status quo) is chosen, recorded as `adr_status: Proposed`.** The narrative subtree stays in `agency`; the `AGENTS.md` `NO.1`–`NO.6` rules plus `tools/check-narrative-ontology-load.py` remain the binding partition between substrate-work and narrative-work.

### Falsifier triggers — re-open this ADR when any of the following hold

- **F1.** The narrative-skill count exceeds **10** (today: 6). Extraction or namespace-isolation re-enters the cost-benefit analysis when the AGENTS.md narrative section is forced past ~120 lines.
- **F2.** The bootstrap-bundle token cost exceeds **60 K tokens** (today: ~50 K). The AGENTS.md narrative section's contribution becomes material when total bundle cost climbs.
- **F3.** Sustained FL1+ friction in the Nightly Maintenance Run cites the NO.5 workaround as cause across **three or more** sessions in a 14-day window. The workaround is workable; sustained friction means it is not.
- **F4.** A narrative-skill change requires a T3 amendment to a root spec **other than** `SKILLS.md` or the dedicated AGENTS.md `## Narrative Ontology` section. This signals the narrative concerns are bleeding into substrate concerns; isolation is the correct response.
- **F5.** A third-party adopter of this substrate requests narrative-content exclusion as a hard prerequisite. The substrate's primary value proposition is governance; if narrative content actively blocks adoption, extraction earns its cost.

When any falsifier triggers, a successor ADR MUST be authored that re-evaluates Options 1 and 2 against the then-current evidence and supersedes this one via `adr_supersedes: [ADR-0008]`.

### How the triggers are measured

The binding measurement mechanism for F1–F5 is [`tools/maintenance/adr-trigger-audit.py`](../tools/maintenance/adr-trigger-audit.py) (Task 069). The audit composes [`tools/maintenance/bundle-size-snapshot.py`](../tools/maintenance/bundle-size-snapshot.py) for F2 (bundle-token cost) and computes F1 / F3 / F4 directly; F5 surfaces as `MANUAL` rather than a fire/no-fire predicate because no in-repo signal exists for third-party-adopter requests. The audit MUST be invoked on the Nightly Maintenance Run cadence per [MAINTENANCE.md §3.6](../MAINTENANCE.md#36-adr-falsifier-trigger-audit-nightly-cadence); a fire emits `<path>::WARN:ADR-0008.F<n>:<msg>` and exits `2`, signalling that this ADR's successor MUST be authored. The trigger predicates above remain authoritative; the audit script is the *how-we-test-this* footnote, not a re-definition of the triggers.

### Status note on `adr_status: Proposed`

This ADR ships at `adr_status: Proposed` rather than `Accepted` because the falsifier triggers above have not been observed yet, and ratification to `Accepted` would prematurely lock the topology against the very evidence the triggers are designed to surface. A maintainer flipping to `Accepted` SHOULD do so only after either (a) the triggers go un-fired for a sustained period (≥ 90 days) or (b) explicit operator confirmation that the status-quo topology is the long-term commitment.

## Consequences

### Positive

- Zero migration cost.
- Tasks 030 / 042 / 015 audit-graph integrity preserved.
- The `NO.5` discipline remains mechanically enforced (WARN-tier; no false-positive cascade).
- The substrate-vs-content tension is *visible* rather than buried — future maintenance agents see the ADR, see the falsifier triggers, and can revisit the decision with evidence.

### Negative

- AGENTS.md retains ~70 lines (~2150 tokens, ~4 % of bootstrap bundle) of narrative-specific content that ~80 % of sessions do not need.
- The repo's surface area appears larger than its substrate purpose strictly requires; new contributors must read NO.5 to understand the partition.
- A successor ADR will eventually be required (when a trigger fires); the deferral is real, not permanent.

### Neutral

- [ADR-0006](./0006-agency-system-prototype-exemption.md) handles `/Agency-System/` via the same "carve-out exemption" pattern. This ADR does **not** extend that exemption to the narrative skills; the narrative skills *follow* the operational-folder rules (they live under `/skills/` and carry frontmatter), they are simply exempted from the *auto-load* default. The two ADRs are complementary partition mechanisms at different layers.
- The narrative skills' own internal authority (Dramatica × NCP × Kohärenz-Protokoll cross-references) remains governed by [Task 015](../tasks/015-integrate-dramatica-ncp-skills/) and its successors. This ADR governs the *substrate-side* partition rule, not the narrative skills' internal cohesion.
- No follow-on implementation Task is created. If a falsifier fires, the successor ADR will spawn the migration Task at that time.

## Cross-references

- [Task 056 — Narrative Skills Extraction (ADR)](../tasks/056-narrative-skills-extraction-adr/task.md) — this ADR's parent task.
- [Task 053 — Core Architecture Review Follow-ups](../tasks/053-core-architecture-review-followups/) finding B.5 — the dispatch.
- [AGENTS.md §"Narrative Ontology — Dramatica × NCP × Novel-Architect Bridge"](../AGENTS.md) — the binding NO.1–NO.6 rules being preserved.
- [`tools/check-narrative-ontology-load.py`](../tools/check-narrative-ontology-load.py) — the mechanical enforcer of NO.5.
- [ADR-0006 — `/Agency-System/` Frontend-Prototype Exemption](./0006-agency-system-prototype-exemption.md) — sibling partition decision.
- [`research/adr-spec-research-synthesis/output/SPEC.md`](../research/adr-spec-research-synthesis/output/SPEC.md) — ADR authoring contract.
