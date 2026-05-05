---
type: research
status: active
slug: adr-assumption-audit
summary: "ADR Assumption Audit Report. 9 hidden assumptions (3 high-blast), 11 implicit-ADR candidates (5 P1), 7 pending decisions (3 open). Recommends Task 030 (first-batch ADR authoring with hybrid cardinality) and surfaces a previously-missing review/maintenance loop."
created: 2026-05-05
updated: 2026-05-05
research_phase: complete
research_executes_prompt: adr-assumption-audit
research_friction_level: FL1
---

# ADR Assumption Audit — Report

## §0 Scope and Provenance

This report synthesises the three subagent runs that executed [`/prompts/adr-assumption-audit/prompt.md`](../../../prompts/adr-assumption-audit/prompt.md) under [Task 029](../../../tasks/029-adr-assumption-audit/task.md). It is a **read-only** audit of:

- The ADR governance spec at [`research/adr-spec-research-synthesis/output/SPEC.md`](../../adr-spec-research-synthesis/output/SPEC.md) (T4-immutable per `MAINTENANCE.md §1`).
- The ADR tooling implementation plan at [`tasks/028-adr-tooling-impl-plan/implementation-plan.md`](../../../tasks/028-adr-tooling-impl-plan/implementation-plan.md).

Every finding is sourced from one of the workspace files:

- §1 ← [`workspace/m13-hidden-assumptions.md`](../workspace/m13-hidden-assumptions.md) (Subagent A, [M13])
- §2 ← [`workspace/m07-implicit-adrs.md`](../workspace/m07-implicit-adrs.md) (Subagent B, [M07])
- §3 ← [`workspace/m06-m08-pending-decisions.md`](../workspace/m06-m08-pending-decisions.md) (Subagent C, [M06]+[M08])
- §4 is this report's only synthetic content — actionable recommendations.

Quality bar: every finding cites a `file:line` or `file §section` evidence anchor. Findings without such an anchor were rejected at workspace draft time.

---

## §1 Hidden Assumptions (M13)

Sorted by blast radius (HIGH → LOW). Full evidence per ASM lives in [`workspace/m13-hidden-assumptions.md`](../workspace/m13-hidden-assumptions.md).

### High-Blast Assumptions (4)

| ASM | Axis | One-line Statement | Embedded At | Blast Radius |
|---|---|---|---|---|
| **001** | adjacent | Polarity inversion is undetectable by deterministic compression — `bcp14-keyword` fidelity does NOT catch a stripped `MUST NOT` qualifier. | SPEC §5.1 ADR.A.3.4; SPEC §5.3 rationale. | HIGH — agents may operate against an inverted rule with no validator signal. |
| **004** | opposing | The `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` marker check is *not* sufficient: typo-in-marker, duplicate marker pair (merge conflict), and embedded `-->` in ADR body all bypass it. | SPEC §2.3, §5.1 ADR.A.3.5. | HIGH — silent content drift between marker pairs over many synthesis runs. |
| **005** | opposing | Pre-commit-only enforcement is bypassable (`--no-verify`, force-push, GitHub web edit). The CI workflow specified in plan §4 does not yet exist. | SPEC §2.4, §7.1 ADR.A.5.8. | HIGH (until CI lands) — corrupt `AGENTS.md` commits via web UI bypass all gates. |
| **009** | orthogonal | Normatives outside `Decision Outcome` and `Consequences` (in tables, prose, Context section) are silently dropped by the extractor. | SPEC §5.1 ADR.A.3.1. | HIGH — the *true* compression ratio undercounts the denominator; agents read an under-specified contract. |

### High-Blast Cultural Assumption (1)

| ASM | Axis | One-line Statement | Embedded At | Blast Radius |
|---|---|---|---|---|
| **007** | abstraction | The spec assumes humans will proactively author ADRs. Zero of the repo's 14 catalogued implicit decisions were authored that way. | SPEC §3 (Aspect 1 — Explore); SPEC §4 (Aspect 2 — Plan). | HIGH (cultural) — the corpus risks staying empty (the *log4brains adoption-failure pattern*). |

### Medium-Blast Assumptions (3)

| ASM | Axis | One-line Statement | Embedded At | Blast Radius |
|---|---|---|---|---|
| **002** | adjacent | Sequential `ADR-NNNN` numbering is sufficient for unique identity in a multi-branch repo (the repo already has duplicate `task_id` precedent). | SPEC §4.1 ADR.A.2.7; §7.4 schema. | MEDIUM — caught post-merge by ADR.A.5.6; requires renumber. |
| **003** | adjacent | The MADR three-part body fits every governance decision. Several IADRs (taxonomies, schemas) fit awkwardly. | SPEC §4.1 ADR.A.2.1. | MEDIUM — forces awkward MADR fits or schema extensions. |
| **006** | opposing | Two simultaneously-Accepted contradictory ADRs without a `adr_supersedes` claim resolve non-deterministically. | SPEC §6.1 ADR.A.4.4. | MEDIUM — requires an arbitrary tiebreaker (e.g. lowest `adr_id`). |
| **008** | abstraction | Token efficiency is the binding constraint on `AGENTS.md` quality (rather than agent comprehension accuracy). | SPEC §0; §5.1 ADR.A.3.3; §5.3 rationale. | MEDIUM — mitigable by raising `--token-limit` and softening `--fidelity-floor`. |

### Worst-Case Composition

If ASM-001 (polarity inversion undetectable) AND ASM-009 (extraction blind spot) compose, the synthesised `AGENTS.md` may report ≥ 0.95 fidelity against the *recognised* extracted content while having silently dropped half the corpus normatives. The "true" compression ratio is then 2× the claimed ratio. This is the single highest-priority risk surfaced by the audit.

---

## §2 Implicit ADRs in Force (M07)

11 IADRs catalogued. Sorted by formalisation priority (P1 → P3). Full evidence per IADR lives in [`workspace/m07-implicit-adrs.md`](../workspace/m07-implicit-adrs.md).

### P1 — Must Be Bootstrapped Before Synthesis Pipeline Runs (5)

| IADR | Recommended ADR Title | Conflict With Spec? | Evidence |
|---|---|---|---|
| **001** | Mandatory Session Bootstrap and Governance Gate | none | `AGENTS.md:38-40` SS.1 |
| **002** | Operational Folder Topology and Exemption Protocol | none (resolved by SPEC §2.1 + §8 exemption-extension) | `FOLDERS.md:18-22, 99-103, 106-116` |
| **003** | Frontmatter as the Single Source of Truth for the Audit Graph | none | `FOLDERS.md:85-95`; `TASK.md:42-44` |
| **004** | YAML Depth-1 Constraint and Anti-Hallucination Rationale | none | `AGENTS.md:218-219`; `tools/fm/_core.py:41-44` |
| **005** | Repair Authority Tiers and Mutation Surface Boundaries | none (SPEC §6.1 inherits T4 paradigm) | `MAINTENANCE.md:24-32, 35` |

### P2 — Should Be Formalised After P1 (4)

| IADR | Recommended ADR Title | Conflict | Evidence |
|---|---|---|---|
| **006** | Two-Toolchain Migration Window (deferred until Task 019 flips the default) | partial — SPEC §7.3 elides transition | `MAINTENANCE.md:39-52`; `tools/check-governance.sh:32-48`; `PRE_COMMIT.md:55-67` |
| **007** | Slug-Folder Coupling and Renumbering Invariant (Task and ADR Variants) | partial — competes with SPEC §4.1 | `TASK.md:75, 325-326` |
| **008** | Hand-Rolled Frontmatter Parsing Over PyYAML | none | `tools/fm/_core.py:1-15`; `tools/requirements.txt:6-9` |
| **009** | Universal Friction Logging at Closure (FL0 Inclusive) | partial — SPEC §2.5 should cite | `FRUSTRATED.md:5-13`; `RESEARCH.md:103-107`; `TASK.md:282-300` |

### P3 — Optional / Deferred (2)

| IADR | Recommended ADR Title | Conflict | Evidence |
|---|---|---|---|
| **010** | Subagent Decomposition as a First-Class Authoring Pattern (deferred) | partial — SPEC §3.1 ambiguous | `tasks/029-adr-assumption-audit/task.md`; `tasks/030-cleanup-dramatica-skills-corpus/` |
| **011** | Pre-Commit Gate Composition via tools/check-governance.sh Numbered Steps | none | `tools/check-governance.sh:24-86` (numbered echo blocks) |

### Inter-IADR Contradictions

1. **IADR-002 ↔ IADR-007 (folder vs file ADR shape):** the operational topology IADR uses `<slug>` folders; the slug-folder coupling IADR ties slug to folder name. The SPEC chose `decisions/<NNNN>-<slug>.md` (file, not folder), creating a third filename invariant that neither IADR predicted. **Resolution recommendation:** ADR-0002 explicitly carves out `decisions/` as a file-rather-than-folder exception, citing the SPEC §2.1 rationale ("ADRs are immutable singletons; folders add overhead with no payoff").
2. **IADR-006 ↔ SPEC §7.3 (toolchain-transition behaviour):** if `agency-adr` ships before Task 019 flips the default, its validator-chain selection is ambiguous. **Resolution recommendation:** plan §1.1 (already authored) implicitly handles this — `agency-adr` reuses `tools/fm/_core.py` directly and doesn't depend on which validator wraps it. Document this in IADR-006's eventual ADR.

---

## §3 Pending Decisions (M06 + M08)

7 PDs. Sorted by blocking dependency on Task 028 modules. Full evidence per PD lives in [`workspace/m06-m08-pending-decisions.md`](../workspace/m06-m08-pending-decisions.md).

### Blocks Task 028 Modules

| PD | Question | Blocks | Status | Audit Recommendation |
|---|---|---|---|---|
| **PD-002** | Semantic fidelity measurement algorithm. | `tools/adr/fidelity.py` | open (sources conflict) | Ship `bcp14-keyword` (A) AND `adr-id-anchor` (B) together as deterministic v0; defer `llm-pass` (C). Composes A+B as the de-facto "ASM-001 + ASM-009 mitigation". |

### Blocks First ADR PR (Process)

| PD | Question | Blocks | Status | Audit Recommendation |
|---|---|---|---|---|
| **PD-005** | Bootstrap migration cardinality (Strategy A / B / C). | First-batch ADR authoring (Task 030 candidate). | deferred | **Option C (hybrid):** P1 IADRs each get their own ADR; P2 IADRs cluster into 1–2 records; P3 IADRs deferred. |
| **PD-006** | Human review loop for ADR PRs (NEW). | First ADR PR review. | open (novel finding) | Append a brief ADR review checklist to `PRE_COMMIT.md` (Option B). |

### Blocks Maintenance Integration

| PD | Question | Blocks | Status | Audit Recommendation |
|---|---|---|---|---|
| **PD-007** | Stale-`Proposed` ADR lifecycle (NEW). | Wiring `agency-adr` into the Coherence Check (`MAINTENANCE.md §2`). | open (novel finding) | Defer to a future Task; `MAINTENANCE.md §3.4` Stale-Task Audit is the analogous template. Default behaviour: `Proposed` ADRs are forever-open until human action. |

### Resolved (Documented for Audit Trail)

| PD | Question | Status | Where Decided |
|---|---|---|---|
| **PD-001** | ADR storage path. | resolved → `decisions/` | SPEC §2.1 |
| **PD-003** | `AGENTS.md` ownership model. | resolved → guarded section | SPEC §2.3 (placement deferred to OD.6) |
| **PD-004** | Supersession DAG storage. | resolved → frontmatter source-of-truth | SPEC §6.1 + plan §2.1 |

---

## §4 Recommended Actions

Each recommendation is one concrete next step. Owner and Task target are explicit.

### Action 1 — Mitigate ASM-001 + ASM-009 Composition (HIGHEST PRIORITY)

- **What:** Ship `agency-adr` v0 with **both** fidelity modes A (`bcp14-keyword`) and B (`adr-id-anchor`) running in series. The validate command MUST report both scores; both MUST clear the floor.
- **Why:** Composes the two checks so polarity inversion (caught by deeper keyword balance, not just count) and ADR-drop-out (caught by anchor-presence) are *both* gated.
- **Owner:** Implementing-agent Task that succeeds Task 028 (Task 030 candidate or higher).
- **Maps to:** plan §6 OD.2; SPEC §8 OQ.2; this PD-002.
- **Implementation hint:** plan §2.1 `tools/adr/fidelity.py` already exposes `score(...mode)`; v0 ships A+B and rejects synthesis if either fails. Cost: +1 day on the §7.1 estimate (M → M).

### Action 2 — Author First-Batch ADRs Using Hybrid Cardinality (Option C)

- **What:** Create Task 030 (ADR-Bootstrap-First-Batch) whose Plan authors:
  - **5 individual ADRs:** ADR-0001…ADR-0005 corresponding to the 5 P1 IADRs in §2.
  - **1–2 clustered ADRs:** ADR-0006 covers IADR-008 (parser) + IADR-009 (friction log); ADR-0007 covers IADR-006 (toolchain transition) + IADR-007 (slug-folder coupling).
  - **Defer P3 IADRs (010, 011):** to future ADRs once the patterns stabilise.
- **Why:** Resolves PD-005 (deferred) without locking in either Strategy A or B; matches the priority signal already in the IADR inventory.
- **Owner:** Maintainer-decision; once approved, an implementing agent authors under the Task.
- **Maps to:** SPEC §8 OQ.1; plan §6 OD.1; this PD-005.
- **Implementation hint:** This Task SHOULD be authored *after* the implementing-agent Task ships `agency-adr validate`, so the ADRs themselves can be validated as they land.

### Action 3 — Harden Marker Protocol (ASM-004 Mitigation)

- **What:** When the implementing-agent Task lands the `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` markers in `AGENTS.md`, it MUST *also*:
  1. Add a regex-strict marker validator (catches typos by demanding exact byte equality with the canonical strings).
  2. Reject any synthesis run that detects more than one BEGIN or END marker (catches merge-conflict duplication).
  3. Escape any literal `-->` inside synthesised content as `--&gt;` (catches embedded comment closure).
- **Why:** Three known bypass paths catalogued in ASM-004; mitigations are mechanical.
- **Owner:** Implementing-agent Task.
- **Maps to:** plan §6 OD.6 (extends with the three sub-mitigations).
- **Implementation hint:** plan §2.1 `tools/adr/synthesize.py` already gates on marker presence; this Action upgrades that gate from "present" to "present AND uniquely matched AND content-safe".

### Action 4 — Append ADR Review Checklist to PRE_COMMIT.md (PD-006)

- **What:** As part of the implementing-agent Task's `PRE_COMMIT.md §7.C` documentation block (per plan §5.1), add a sub-section §7.D with a 5-item ADR review checklist:
  1. Does the ADR's `Decision Outcome` cite a falsifiable choice (not just a description)?
  2. Does the ADR's `Consequences` enumerate at least one negative impact?
  3. Does the ADR's `adr_supersedes` list every Accepted ADR whose `Decision Outcome` is now contradicted?
  4. Is the proposed `adr_id` the next free integer (run `agency-adr validate --next-id`)?
  5. Does the post-synthesis `AGENTS.md` diff appear sensible (not 50%+ deletion)?
- **Why:** Closes the gap surfaced by PD-006 (the spec specifies validation but never specifies *human review*).
- **Owner:** Implementing-agent Task.
- **Maps to:** PD-006.

### Action 5 — Defer Stale-Proposed Lifecycle to Successor Task (PD-007)

- **What:** File a Task 031 candidate (ADR-Maintenance-Integration) AFTER the implementing-agent Task ships v0. Its scope: wire `agency-adr` into the Coherence Check per `MAINTENANCE.md §2`; specify the Stale-`Proposed`-ADR audit modelled on `MAINTENANCE.md §3.4`'s Stale-Task Audit; default classification window: 30 days (looser than Tasks' 7-day default to reflect ADR review cadence).
- **Why:** PD-007 is real but does not block v0; deferring it preserves the implementation-agent Task's scope.
- **Owner:** Maintainer (decides when to file Task 031).
- **Maps to:** PD-007.

### Action Summary Table

| # | Action | Maps To | Owner | Blocking? |
|---|---|---|---|---|
| 1 | Ship fidelity modes A+B together | OD.2 / OQ.2 / PD-002 | Implementing-agent Task | YES (blocks v0 ship) |
| 2 | First-batch ADR authoring (Strategy C hybrid) | OD.1 / OQ.1 / PD-005 | Maintainer → Task 030 | NO (informational) |
| 3 | Marker-protocol hardening | OD.6 (extends) | Implementing-agent Task | YES (blocks marker landing) |
| 4 | ADR review checklist in PRE_COMMIT.md | PD-006 | Implementing-agent Task | NO (improves first-PR review) |
| 5 | Defer stale-Proposed lifecycle to Task 031 | PD-007 | Maintainer (later) | NO (post-v0) |

### What Is Explicitly NOT Recommended

- **Do not modify `research/adr-spec-research-synthesis/output/SPEC.md`.** It is T4-immutable. Every spec-affecting Action above lands as plan/Task changes that the implementing agent applies.
- **Do not author `llm-pass` fidelity (Option C of PD-002) in v0.** The cost-benefit only justifies it after the deterministic A+B prove insufficient empirically.
- **Do not rush Task 030 (first-batch ADR authoring) before `agency-adr validate` ships.** The first ADR PR should pass the validator the moment it lands; otherwise Task 030 carries technical debt.
