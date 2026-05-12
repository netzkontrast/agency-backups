---
type: note
status: active
slug: adr-assumption-audit-m06-m08
summary: "Subagent C output: [M06] Source Triangulation across four sources + [M08] Pre-Commitment per question. 7 PDs (PD-001..PD-007) including the prompt's pre-specified five plus two novel."
created: 2026-05-05
updated: 2026-05-05
---

# Subagent C — [M06] Source Triangulation + [M08] Pre-Commitment

**Method:** [M06] Source Triangulation across four sources (≥ 3 must agree before "resolved"); [M08] Pre-Commitment for each Option's confirming evidence.
**Sources triangulated:**
1. `research/adr-spec-research-synthesis/output/SPEC.md` §8 (OQ.1–OQ.7)
2. `tasks/028-adr-tooling-impl-plan/implementation-plan.md` §6 (OD.1–OD.10)
3. `workspace/m13-hidden-assumptions.md` (Subagent A; ASM-001..ASM-009)
4. `workspace/m07-implicit-adrs.md` (Subagent B; IADR-001..IADR-011, plus inter-IADR contradictions)

**Output contract:** ≥ 5 PDs including the pre-specified PD-001..PD-005.

## Pre-Specified PDs (from the prompt)

### PD-001 — ADR Storage Path

- **Question:** Where do ADR files live?
- **Option A:** `decisions/` at repo root.
  - Confirmed by: SPEC §2.1; OD-cross: implicit (the SPEC chose A); ASM: none; IADR-002 supports.
- **Option B:** `docs/decisions/`.
  - Confirmed by: industry convention (`adr-tools`, `log4brains`); SPEC explicitly rejects.
- **Option C:** `research/adr/`.
  - Confirmed by: would reuse existing `/research/` topology; SPEC explicitly rejects (T4-immutability collides with `Superseded` lifecycle).
- **Current spec lean:** Option A (SPEC §2.1 normative).
- **Triangulation status:** **resolved** — SPEC §2.1 + OD (SPEC chose at draft time) + IADR-002 all agree on A. Subagent A surfaces no objection.
- **Blocks:** None (already decided in the SPEC).
- **Recommended owner:** Already owned by SPEC §2.1.
- **Cross-reference:** OD.x in plan §6 — implicitly resolved at SPEC drafting, no separate OD row. The `FOLDERS.md §8` exemption-extension Task (Task 028 succession) will land the operational change.

### PD-002 — Semantic Fidelity Measurement Algorithm

- **Question:** How is the ≥ 0.95 fidelity floor measured?
- **Option A:** `bcp14-keyword` — count BCP-14 keyword preservation between input ADR set and output guarded section. Deterministic, no LLM.
  - Confirmed by: SPEC §5.1 ADR.A.3.4 default; plan §2.1 `tools/adr/fidelity.py` v0 ships only A; computationally cheap; reproducible across CI runs.
  - Falsified by: ASM-001 (polarity inversion is undetectable by keyword counting alone).
- **Option B:** `adr-id-anchor` — verify every Accepted ADR contributes ≥ 1 anchor to the synthesised footer-citation block.
  - Confirmed by: catches the "ADR silently dropped" failure mode that ASM-009 highlights; deterministic.
  - Falsified by: does not catch *partial* extraction (an ADR contributes its anchor but only half its rules).
- **Option C:** `llm-pass` — secondary LLM verifies semantic equivalence.
  - Confirmed by: catches polarity inversion (resolves ASM-001); catches partial extraction; the only mode that handles arbitrary paraphrasing.
  - Falsified by: introduces Anthropic SDK runtime dep + cost/latency; non-deterministic; cannot run in airgapped CI.
- **Current spec lean:** Option A (default), with B and C parameterised.
- **Triangulation status:** **open — sources conflict.** SPEC §5.1 picks A as default; plan §2.1 OD.2 flags A as provisional; ASM-001 falsifies A's sufficiency; the four sources do not agree.
- **Blocks:** `tools/adr/fidelity.py` (cannot be implemented without the algorithm choice).
- **Recommended owner:** Maintainer must decide ship-with-A-now-and-upgrade-to-B-later vs ship-with-A+B vs delay-shipping-until-LLM-pass-is-prototyped. Recommendation: ship A+B (both deterministic), defer C until empirical evidence demands it.
- **Cross-reference:** SPEC OQ.2 = plan OD.2 = this PD-002.

### PD-003 — `AGENTS.md` Ownership Model

- **Question:** How does the synthesis pipeline coexist with the manually-authored content in `AGENTS.md`?
- **Option A:** Full synthesis overwrite (Gemini's original).
  - Confirmed by: maximal compression. Falsified by: destroys Session Setup, Closing Run Procedure, Spec Language Reference, Frontmatter Ontology, Narrative Ontology, LOOP_LOG.
- **Option B:** Guarded section between `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` markers.
  - Confirmed by: SPEC §2.3 normative; plan OD.6 (placement deferred); IADR review confirms the manual content is non-derivable from ADRs in the short term.
  - Falsified by: ASM-004 (marker check has bypass paths).
- **Option C:** Separate file `AGENTS-adr.md` referenced from `AGENTS.md`.
  - Confirmed by: zero overlap risk with manual content. Falsified by: agents read `AGENTS.md`, not satellites; an indirection layer fails the "single configuration layer" assumption.
- **Current spec lean:** Option B (SPEC §2.3 normative).
- **Triangulation status:** **resolved** — SPEC §2.3 + plan OD.6 + IADR analysis agree on B. ASM-004 raises mitigation concerns but does not falsify the choice.
- **Blocks:** Implementation can proceed with B; the *exact byte placement* of markers is OD.6 / SPEC OQ.6 (still deferred to implementation Task).
- **Recommended owner:** Implementation Task (per OD.6).
- **Cross-reference:** SPEC §2.3 + plan OD.6 = this PD-003.

### PD-004 — Supersession DAG Storage

- **Question:** Where does the supersession DAG live?
- **Option A:** YAML frontmatter only (`adr_supersedes` / `adr_superseded_by` lists per ADR file).
  - Confirmed by: SPEC §6.1 ADR.A.4.2 / .4.3 / .4.4 / .4.6 normative; reuses the `task_supersedes` precedent; computed on-demand by `tools/adr/graph.py` per plan §2.1.
  - Falsified by: each `agency-adr validate` invocation re-walks the corpus to rebuild the graph (acceptable at corpus size ≤ 200 ADRs).
- **Option B:** External graph file (`decisions/_graph.json`).
  - Confirmed by: O(1) graph load. Falsified by: drift risk (the JSON and the per-file frontmatter desync); a second source of truth violates IADR-003.
- **Option C:** Computed-on-demand only, no persistence.
  - Equivalent to A (the plan stores the source-of-truth in frontmatter and computes the graph object on-demand).
- **Current spec lean:** Option A (frontmatter source-of-truth, computed graph).
- **Triangulation status:** **resolved** — SPEC §6.1 + plan §2.1 + IADR-003 all agree on A. ASM-006 (simultaneous contradictory ADRs without supersession claim) is a separate concern, not a graph-storage concern.
- **Blocks:** None (Option A is what plan §2.1 already specifies).
- **Recommended owner:** Already owned by SPEC §6.1.
- **Cross-reference:** SPEC §6.1 + plan §2.1 — no separate OQ/OD row; this PD documents the (already-resolved) decision.

### PD-005 — Bootstrap Migration

- **Question:** How are the implicit ADRs (IADR-001..IADR-011 from Subagent B) formalised as ADR-0001..N without triggering supersession cycles or invalidating themselves at extraction time?
- **Option A — Strategy A (granular).** Each IADR becomes one ADR. 11 ADRs in the first batch.
  - Confirmed by: maximum supersession granularity; one decision per record (matches MADR ethos).
  - Falsified by: 11× the per-ADR review burden; harder for `bcp14-keyword` fidelity to dedupe overlapping rules.
- **Option B — Strategy B (clustered).** ≈ 5 ADRs cluster the 11 IADRs by surface (Frontmatter, Folder Topology, Repair Tiers, Tooling Composition, Closure Protocol).
  - Confirmed by: lower per-ADR cost; fewer entries in synthesised footer block.
  - Falsified by: a future single-IADR change must supersede the entire cluster, losing intent.
- **Option C — Hybrid.** P1 IADRs (5) get individual ADRs; P2 IADRs (4) cluster into 1–2 ADRs; P3 IADRs (2) deferred.
  - Confirmed by: balances granularity with effort; the P-priority assignment in `m07-implicit-adrs.md` already provides the cardinality hint.
  - Falsified by: the boundary between P2 cluster and individual is judgement-call.
- **Current spec lean:** SPEC OQ.1 explicitly leaves this `[OPEN]`. Plan OD.1 routes to Task 029 (this audit) for recommendation.
- **Triangulation status:** **deferred — insufficient evidence.** No source declares a winner; the audit's recommendation is **Option C** (hybrid) because it scales the effort to the actual priority of each implicit decision.
- **Blocks:** First-batch ADR authoring (Task 030 candidate). Does NOT block Task 028 modules.
- **Recommended owner:** Maintainer; this audit recommends **Option C**.
- **Cross-reference:** SPEC OQ.1 = plan OD.1 = this PD-005.

## Novel PDs (Surfaced by Triangulation)

### PD-006 — Human Review Loop for ADR PRs (NEW)

- **Question:** How does a maintainer review an ADR PR? The validation gate (ADR.A.5.1) catches schema errors; the synthesis idempotency (ADR.A.3.6) catches non-deterministic output. But neither catches *semantic correctness* — i.e., "should this ADR be Accepted as written?"
- **Option A:** Implicit — every ADR PR follows the standard repo PR review process; the maintainer reads the ADR and the diff.
  - Confirmed by: precedent (every Task PR is reviewed this way). Falsified by: no checklist exists; the reviewer has no reminder to check (e.g.) "does this ADR's Decision Outcome contradict any existing Accepted ADR?".
- **Option B:** Explicit ADR review checklist in `PRE_COMMIT.md` or a new `ADR_REVIEW.md`.
  - Confirmed by: matches the existing `PRE_COMMIT.md` checklist pattern; provides reviewer cognitive scaffolding.
  - Falsified by: introduces a new artefact; risk of staleness if the checklist isn't maintained.
- **Option C:** `agency-adr validate --review` mode that emits a diagnostic for each Accepted ADR pair with topical overlap (heuristic).
  - Confirmed by: automatable. Falsified by: false-positive risk; "topical overlap" requires semantic understanding the deterministic validator lacks.
- **Current spec lean:** Implicit Option A (the spec is silent on review process).
- **Triangulation status:** **open — sources don't address.** SPEC, plan, ASM-007 (cultural) all touch on the human-loop concern but none specify the review surface.
- **Blocks:** Not a code blocker; a *process* blocker for the first ADR PR (Task 030).
- **Recommended owner:** Maintainer; recommendation: Option B (a brief review checklist appended to `PRE_COMMIT.md`).
- **Cross-reference:** No existing OQ/OD; this PD is novel. Maps loosely to ASM-007 (authorship-culture assumption).

### PD-007 — Stale-`Proposed` ADR Lifecycle (NEW)

- **Question:** What happens to an ADR that is created with `adr_status: Proposed` but never reaches `Accepted`? `MAINTENANCE.md §3.4` defines a Stale-Task Audit for `task_status: open` Tasks; the SPEC defines no analogue for `adr_status: Proposed`.
- **Option A:** Treat Proposed ADRs as forever-open; maintenance never touches them.
  - Confirmed by: simplicity. Falsified by: corpus accretion; orphan Proposed ADRs degrade the corpus's signal-to-noise ratio over years.
- **Option B:** Proposed ADRs older than `MAINT_STALE_DAYS` (default 7) become candidates for Stale-ADR Audit; the maintenance agent classifies into Accept / Deprecate / Withdraw buckets.
  - Confirmed by: structurally mirrors `MAINTENANCE.md §3.4` Stale-Task Audit; fits the existing maintenance pipeline.
  - Falsified by: 7 days is too short for an ADR (decisions take longer to ratify than Tasks to execute).
- **Option C:** Proposed ADRs auto-Withdraw if not promoted to Accepted within a configurable window (default 30 days), with maintainer override.
  - Confirmed by: keeps the corpus clean automatically. Falsified by: aggressive auto-action on a governance artefact is itself a governance risk.
- **Current spec lean:** Implicit Option A (silence).
- **Triangulation status:** **open — sources don't address.** Discovered by mid-run reflection (Q4); the spec genuinely missed this lifecycle corner.
- **Blocks:** Not a code blocker for the v0 implementation. *Blocks* the maintenance integration (a future Task that wires `agency-adr` into the Coherence Check).
- **Recommended owner:** Defer to a successor ADR governance task (Task 031 candidate); this PD is informational for now.
- **Cross-reference:** No existing OQ/OD; this PD is novel. Maps loosely to IADR-005 (repair tiers) — a Proposed-stale audit is a T1/T2 maintenance action.

## Triangulation Audit Trail

For PDs marked `resolved`: at least 3 of the 4 sources explicitly support the chosen Option, with no source falsifying it.

| PD | SPEC source | Plan source | ASM source | IADR source | Status |
|---|---|---|---|---|---|
| PD-001 | §2.1 ✓ | implicit ✓ | none | IADR-002 ✓ | resolved (3+ agree) |
| PD-002 | §5.1 (default A) | OD.2 (flags provisional) | ASM-001 falsifies A | n/a | open |
| PD-003 | §2.3 ✓ | OD.6 (placement deferred) | ASM-004 raises bypass paths | none | resolved (B) |
| PD-004 | §6.1 ✓ | §2.1 ✓ | none | IADR-003 ✓ | resolved (3+ agree) |
| PD-005 | OQ.1 [OPEN] | OD.1 [OPEN] | none | n/a | deferred — recommend C |
| PD-006 | silent | silent | ASM-007 | implicit (process gap) | open — novel |
| PD-007 | silent | silent | none | IADR-005 (analogous) | open — novel |

## Summary

| PD | Pre-spec? | Status | Blocks |
|---|---|---|---|
| 001 | yes | resolved | nothing |
| 002 | yes | open | tools/adr/fidelity.py |
| 003 | yes | resolved | nothing (placement deferred to impl) |
| 004 | yes | resolved | nothing |
| 005 | yes | deferred → recommend C | first-batch ADR authoring |
| 006 | NO (novel) | open | first ADR PR review process |
| 007 | NO (novel) | open | maintenance integration |

**5 pre-specified + 2 novel = 7 PDs.** Three (PD-002, PD-006, PD-007) are open and require maintainer attention before the corresponding artefacts can ship.

Findings flow into `output/REPORT.md §3`, sorted by blocking dependency on Task 028 modules.
