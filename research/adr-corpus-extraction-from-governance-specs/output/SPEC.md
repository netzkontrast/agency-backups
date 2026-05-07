---
type: research
status: active
slug: adr-corpus-extraction-from-governance-specs
summary: "Catalogue of 18 implicit ADRs already in force across the 8 root governance specs. P1 subset (5 records) ratified as Proposed ADRs in /decisions/. Each candidate cites file:line for its source clause; no synthesised clauses."
created: 2026-05-07
updated: 2026-05-07
research_phase: complete
research_executes_prompt: research-adr-corpus-extraction
research_friction_level: FL1
---

# Implicit ADR Corpus — Extracted from Root Governance Specs

## §0 Status & Provenance

**Status:** ACTIVE.
**Target Repository:** [`netzkontrast/agency`](https://github.com/netzkontrast/agency).
**Provenance:** This SPEC is the authoritative implicit-ADR (IADR) corpus extracted from the eight root specs ([`AGENTS.md`](../../../AGENTS.md), [`TASK.md`](../../../TASK.md), [`PROMPT.md`](../../../PROMPT.md), [`RESEARCH.md`](../../../RESEARCH.md), [`FOLDERS.md`](../../../FOLDERS.md), [`PRE_COMMIT.md`](../../../PRE_COMMIT.md), [`FRUSTRATED.md`](../../../FRUSTRATED.md), [`MAINTENANCE.md`](../../../MAINTENANCE.md)). It builds on the 11-IADR catalogue at [`research/adr-assumption-audit/output/REPORT.md`](../../adr-assumption-audit/output/REPORT.md) §2 (lines 67–95) and conforms to the MADR shape ratified in [`research/adr-spec-research-synthesis/output/SPEC.md`](../../adr-spec-research-synthesis/output/SPEC.md).

**Predecessor citations.** Three IADRs from the audit catalogue are inherited as predecessors of this corpus:
- IADR-001 (Mandatory Session Bootstrap and Governance Gate) — see audit REPORT §2 line 75.
- IADR-002 (Operational Folder Topology and Exemption Protocol) — see audit REPORT §2 line 76.
- IADR-003 (Frontmatter as the Single Source of Truth for the Audit Graph) — see audit REPORT §2 line 77.

Two further audit-catalogue IADRs (IADR-004 YAML Depth-1 Constraint, IADR-005 Repair Authority Tiers) are also formalised as P1 ratified records below.

**Quality bar.** Every IADR cites at least one `file:line` evidence anchor pointing at the source clause in a root spec. No synthesised clauses; rephrasing is for readability only — the binding text is the cited source.

---

## §1 Scope and Methodology

### §1.1 Inclusion Criteria

An IADR is included in this corpus if and only if:

1. The decision is *currently in force* (binding on every agent that reads the cited file).
2. The decision is *architecturally significant* per [SPEC §3.1 ADR.A.1.3](../../adr-spec-research-synthesis/output/SPEC.md): it materially affects repository structure, dependencies, governance, or token-efficiency budgets.
3. The decision was *never authored as an explicit ADR* — it lives only as a clause inside a root spec (or its tooling).
4. The decision's source clause is *citable as `file:line`* — no folklore, no oral tradition.

### §1.2 Cardinality Strategy

This corpus uses **Strategy C (hybrid)** per audit REPORT §4 Action 2: P1 IADRs each get an individual ADR; P2/P3 IADRs are catalogued but not ratified in this run. The 5 P1 entries are filed as `decisions/0001-…md` through `decisions/0005-…md` with `adr_status: Proposed`.

### §1.3 MADR Compression

In this SPEC each IADR is rendered in *condensed* form (one row per MADR section) to keep the corpus in one file. The full MADR prose is reserved for the ratified files in `/decisions/`. A condensed entry MUST round-trip to a full MADR file when promoted from Proposed to Accepted.

---

## §2 Catalogue Overview

| IADR | Title | Priority | Source spec(s) | Ratified file |
|---|---|---|---|---|
| IADR-001 | Mandatory Session Bootstrap and Governance Gate | P1 | `AGENTS.md:38-42` | `decisions/0001-mandatory-session-bootstrap.md` |
| IADR-002 | Operational Folder Topology and Exemption Protocol | P1 | `FOLDERS.md:18-23, 105-122` | `decisions/0002-operational-folder-topology.md` |
| IADR-003 | Frontmatter as the Single Source of Truth for the Audit Graph | P1 | `FOLDERS.md:85-99`; `TASK.md:42-46` | `decisions/0003-frontmatter-source-of-truth.md` |
| IADR-004 | YAML Depth-1 Constraint and Anti-Hallucination Rationale | P1 | `AGENTS.md:218-222`; `tools/fm/_core.py:41-44` | `decisions/0004-yaml-depth-one-constraint.md` |
| IADR-005 | Repair Authority Tiers and Mutation Surface Boundaries | P1 | `MAINTENANCE.md:24-37` | `decisions/0005-repair-authority-tiers.md` |
| IADR-006 | RFC 2119 / BCP 14 Normative Keyword Binding (Repo-Wide) | P2 | `AGENTS.md` (RFC 2119 binding); `TASK.md` (inheritance); SPEC §1.1 | (deferred) |
| IADR-007 | Gherkin Acceptance Scenarios with Stable Anchors | P2 | `AGENTS.md:44-60`; SPEC §1.2 | (deferred) |
| IADR-008 | Mandatory Friction Logging at Closure (FL0 Inclusive) | P2 | `FRUSTRATED.md:5-32`; `PRE_COMMIT.md:15-18` | (deferred) |
| IADR-009 | Closing Run Procedure via `/sc:createPR` | P2 | `AGENTS.md:72-87` | (deferred) |
| IADR-010 | Decentralised `readme.md` Rule (Folder-Adjacent Docs) | P2 | `FOLDERS.md:40-49` | (deferred) |
| IADR-011 | Three-File Mandatory Scaffold for `/prompts/<slug>/` | P2 | `FOLDERS.md:57-69` | (deferred) |
| IADR-012 | Pre-Commit Gate via `tools/check-governance.sh` Composition | P2 | `PRE_COMMIT.md:35-54` | (deferred) |
| IADR-013 | Two-Toolchain Migration Window (Legacy ↔ Flexible) | P2 | `MAINTENANCE.md:39-52`; `PRE_COMMIT.md:55-68` | (deferred) |
| IADR-014 | Frontmatter Waivers — Burn Protocol (Never-Growing) | P2 | `PRE_COMMIT.md:70-82` | (deferred) |
| IADR-015 | Audit-Graph Linkage Through Reciprocal Frontmatter Keys | P2 | `FOLDERS.md:86-101` | (deferred) |
| IADR-016 | Subfolder Threshold Heuristic (4+ Files of Same Category) | P3 | `FOLDERS.md:51-55`; `TASK.md:40` | (deferred) |
| IADR-017 | Hand-Rolled Frontmatter Parser Over PyYAML | P3 | `tools/fm/_core.py:1-15`; `AGENTS.md:218-222` | (deferred) |
| IADR-018 | Research Workspace Immutability Post-Closure (T4) | P3 | `MAINTENANCE.md:33`; `PRE_COMMIT.md:76` | (deferred) |

Five P1 entries are ratified in `/decisions/`; thirteen further candidates are catalogued condensed-form below.

---

## §3 P1 — Ratified Records (Condensed Mirrors)

These five IADRs are ratified as `adr_status: Proposed` files in `/decisions/`. The condensed MADR mirror below MUST agree with the full prose in the ratified file.

### §3.1 IADR-001 — Mandatory Session Bootstrap and Governance Gate

| MADR Section | Content |
|---|---|
| Context and Problem Statement | An agent that begins a session in a half-installed environment will silently produce broken artefacts (missing `PyYAML`, stale schemas), corrupting the audit graph before any governance check runs. Source clause: `AGENTS.md:38-42` ("**SS.1** An agent MUST run `./install.sh` … **SS.2** … `tools/check-governance.sh` … **SS.3** MUST NOT skip setup"). |
| Decision Drivers | (1) Idempotent bootstrap is cheap; broken-tooling debugging is expensive. (2) Governance gate must precede any read or write to prevent compounding drift. |
| Considered Options | (a) Bootstrap-on-demand (lazy) — rejected, leaves windows where reads precede installs. (b) Mandatory `install.sh` + `check-governance.sh` at session start — chosen. (c) CI-only enforcement — rejected, agents act outside CI. |
| Decision Outcome | Every agent MUST run `./install.sh` then `tools/check-governance.sh` before reading or writing any repository file; non-zero exit halts the session. |
| Consequences | Positive: any tooling-environment defect surfaces in seconds, not after broken commits. Negative: idempotent reruns add ≈ 1–2 s to every fresh shell. Neutral: the rule is now the bootstrap baseline every other ADR can assume. |

### §3.2 IADR-002 — Operational Folder Topology and Exemption Protocol

| MADR Section | Content |
|---|---|
| Context and Problem Statement | Without a hard partition between orchestration (`/tasks/`), instruction (`/prompts/`), evidence (`/research/`), and capability (`/skills/`), folders mix kinds and the audit graph becomes unwalkable. Non-operational folders (`/tools/`, `/maintenance/`, `/decisions/`, `/templates/`, `/Agency-System/`) need an explicit exemption so they don't accidentally fall under the operational rules. Source clauses: `FOLDERS.md:18-23` (top-level table) and `FOLDERS.md:105-122` (anti-pattern list + §8 exemption table). |
| Decision Drivers | (1) Mechanical enforcement requires a closed list of operational paths. (2) Non-operational stores need first-class status without polluting the orchestration partition. (3) The exemption list is the only sanctioned place to declare new top-level folders. |
| Considered Options | (a) Free-form folders + per-file frontmatter routing — rejected, no static ground truth. (b) Closed operational partition + named exemptions — chosen. (c) Single monolithic `/repo/` tree — rejected, regresses to undifferentiated content. |
| Decision Outcome | The repository's top-level tree is partitioned into the operational quartet (`/tasks/`, `/prompts/`, `/research/`, `/skills/`) and the named exemption set (`/tools/`, `/maintenance/`, `/decisions/`, `/templates/`, `/Agency-System/`); any new top-level folder MUST land via amendment to `FOLDERS.md` §8. |
| Consequences | Positive: lint tooling can hard-code path globs without walking the entire tree. Negative: every new storage class requires a doc edit. Neutral: this is the structural backbone every other ADR composes against. |

### §3.3 IADR-003 — Frontmatter as the Single Source of Truth for the Audit Graph

| MADR Section | Content |
|---|---|
| Context and Problem Statement | Body-level Markdown links between Tasks/Prompts/Research are convenient for humans but unparseable by tooling without HTML/markdown ASTs. The audit graph (Task → Prompt → Research → Prompt) MUST be queryable mechanically. Source clauses: `FOLDERS.md:86-99` (linkage keys + reciprocity); `TASK.md:42-46` (Layered Schema with Namespacing). |
| Decision Drivers | (1) Mechanical reciprocity requires structured linkage. (2) Humans still want body-level links for navigation; the two surfaces co-exist. (3) A future graph-CLI or render pipeline depends on the structured edge being authoritative. |
| Considered Options | (a) Body-Markdown-link as ground truth — rejected, unparseable at scale. (b) Separate edge-list file — rejected, duplicates state. (c) Frontmatter-as-ground-truth + body-links for nav — chosen. |
| Decision Outcome | Every cross-directory edge in the audit graph MUST be expressed in frontmatter (`task_uses_prompts`, `prompt_relates_to_task`, `research_executes_prompt`, etc.); body-level links are encouraged for navigation but are not consumed by tooling. |
| Consequences | Positive: `tools/lint-linkage.py` walks the tree without parsing prose. Negative: humans MUST update frontmatter (not just body links) when re-routing. Neutral: this is the graph backbone every audit and synthesis tool reuses. |

### §3.4 IADR-004 — YAML Depth-1 Constraint and Anti-Hallucination Rationale

| MADR Section | Content |
|---|---|
| Context and Problem Statement | LLMs hallucinate nested YAML — silent indentation drift produces semantically wrong frontmatter that round-trips through `yaml.load` without error. The repo standardises on a depth-1 constraint with hand-rolled parsing. Source clauses: `AGENTS.md:218-222` ("YAML frontmatter MUST NOT nest beyond one level. Lists MUST contain scalars or short strings only."); `tools/fm/_core.py:41-44` (parser implements the constraint). |
| Decision Drivers | (1) LLM-authored frontmatter MUST be deterministically parseable. (2) Hand-rolled parsing avoids PyYAML's tolerance for ambiguous nesting. (3) Lists-of-scalars is sufficient for every L1/L2 namespace currently in use. |
| Considered Options | (a) Full YAML 1.2 — rejected, hallucination surface too wide. (b) JSON-only — rejected, breaks Obsidian rendering. (c) Depth-1 YAML with scalar lists — chosen. |
| Decision Outcome | All frontmatter in this repository MUST be YAML restricted to depth-1; lists MUST contain only scalars or short strings; nested mappings are rejected by the parser. |
| Consequences | Positive: parser is ≈ 50 LoC, audit-grade reliable. Negative: complex structured metadata cannot live in frontmatter (must be referenced from a body-level table or schema file). Neutral: this is the parsing baseline for the entire toolchain. |

### §3.5 IADR-005 — Repair Authority Tiers and Mutation Surface Boundaries

| MADR Section | Content |
|---|---|
| Context and Problem Statement | Without a tier-classification rule, agents either over-modify (rewrite an entire Task to fix a typo) or under-modify (open a Task PR for a missing date). The repo declares four tiers (T1 mechanical, T2 additive, T3 structural, T4 research-touching) with explicit permitted actions. Source clauses: `MAINTENANCE.md:24-32` (tier table); `MAINTENANCE.md:33` (T4 immutability); `MAINTENANCE.md:35` (root-spec ceiling at T2). |
| Decision Drivers | (1) Drift is cheap to fix at T1/T2 and expensive to fix structurally. (2) Closed research and root specs MUST resist accidental rewriting. (3) The mutation surface (`tools/fm/edit.py`) reifies the tier rule mechanically. |
| Considered Options | (a) Single "edit anything" rule — rejected, conflates tiers. (b) Four-tier classification with a canonical mutator — chosen. (c) Branch-protection-only enforcement — rejected, doesn't help in-session. |
| Decision Outcome | Every change MUST be classified T1–T4 before mutation; T1/T2 land in-place via `tools/fm/edit.py`; T3 land via Tasks; T4 (closed research workspaces, Accepted ADRs) MUST NOT be mutated at all — alterations land via successor records. |
| Consequences | Positive: agents can self-classify in seconds; the canonical mutator rejects T3/T4 by construction. Negative: the tier boundary is a judgement call at the margin (e.g. a body-paragraph rewording). Neutral: this is the lifecycle paradigm the ADR supersession model inherits. |

---

## §4 P2/P3 — Catalogued (Condensed Only)

These IADRs are catalogued for future formalisation. Each cites file:line and proposes an MADR shape; ratification is deferred to a successor Task per audit REPORT §4 Action 2.

### §4.1 IADR-006 — RFC 2119 / BCP 14 Normative Keyword Binding (Repo-Wide)

- **Source.** [`AGENTS.md`](../../../AGENTS.md) "RFC 2119 Normative Keywords" section (also surfaced in [`research/adr-spec-research-synthesis/output/SPEC.md`](../../adr-spec-research-synthesis/output/SPEC.md) §1.1).
- **Decision Outcome.** Every uppercase MUST/SHOULD/MAY in any spec under this repo is bound by RFC 2119 + RFC 8174.
- **Consequences.** Positive: deterministic keyword semantics across agents and humans. Negative: requires every author to know the binding. Neutral: every other ADR in this corpus inherits this convention.

### §4.2 IADR-007 — Gherkin Acceptance Scenarios with Stable Anchors

- **Source.** [`AGENTS.md:44-60`](../../../AGENTS.md) (Gherkin scenarios with `# anchor:` comments).
- **Decision Outcome.** Every normative rule worth testing MUST carry a Gherkin scenario whose anchor is `<spec-id>.<aspect>.<n>` and is referenced from validator diagnostics.
- **Consequences.** Positive: validator output points at a stable anchor humans can grep. Negative: scenario authoring is overhead for trivial rules. Neutral: this is the anchor format the ADR governance SPEC inherits as `ADR.A.<aspect>.<n>`.

### §4.3 IADR-008 — Mandatory Friction Logging at Closure (FL0 Inclusive)

- **Source.** [`FRUSTRATED.md:5-32`](../../../FRUSTRATED.md) ("**This log is MANDATORY for every session.**"); [`PRE_COMMIT.md:15-18`](../../../PRE_COMMIT.md) (rule 3).
- **Decision Outcome.** Every session, including FL0 (zero-friction) sessions, MUST close with an explicit friction declaration; research closures use `/reflection/friction-log.md`, standard tasks use a `## Frustration Log` section.
- **Consequences.** Positive: aggregate FL pattern data accumulates without survivorship bias. Negative: trivial sessions still incur log overhead. Neutral: this surfaces recurring friction (e.g. cross-task amendments) as Task-creation triggers.

### §4.4 IADR-009 — Closing Run Procedure via `/sc:createPR`

- **Source.** [`AGENTS.md:72-87`](../../../AGENTS.md) (CR.1–CR.6).
- **Decision Outcome.** A Claude Code session MUST close by invoking `/sc:createPR` after `git push`; the skill is idempotent and re-runs `tools/check-governance.sh` before opening the PR.
- **Consequences.** Positive: session closure is mechanically uniform. Negative: ties closure to the SuperClaude Framework. Neutral: ADR-affecting commits (per SPEC §2.5) inherit this closure rule.

### §4.5 IADR-010 — Decentralised `readme.md` Rule (Folder-Adjacent Docs)

- **Source.** [`FOLDERS.md:40-49`](../../../FOLDERS.md) ("EVERY folder MUST contain a `readme.md`").
- **Decision Outcome.** Every operational folder MUST contain `readme.md` covering What/Why, Linked Navigation, and Assumptions Log; updates batch at pre-commit, not per-file change.
- **Consequences.** Positive: no separate `/docs/` tree drifts; readers trust adjacent docs. Negative: cleaner workflows must remember readme-batching at pre-commit. Neutral: enforced by `tools/lint-structure.py`.

### §4.6 IADR-011 — Three-File Mandatory Scaffold for `/prompts/<slug>/`

- **Source.** [`FOLDERS.md:57-69`](../../../FOLDERS.md) (`prompt.md`, `brief.md`, `readme.md` table + ERROR-on-absent rule).
- **Decision Outcome.** Every prompt folder MUST contain `prompt.md`, `brief.md`, and `readme.md` at creation time; absence is a structural lint failure even if `prompt.md` body is otherwise complete.
- **Consequences.** Positive: prompts are always reader-discoverable without spelunking. Negative: minor template overhead. Neutral: the rule applies even to follow-up prompts spawned mid-run.

### §4.7 IADR-012 — Pre-Commit Gate via `tools/check-governance.sh` Composition

- **Source.** [`PRE_COMMIT.md:35-54`](../../../PRE_COMMIT.md) (§7 Mechanical Governance Checks).
- **Decision Outcome.** All pre-commit governance checks MUST be composed inside `tools/check-governance.sh` as numbered steps; direct modification of `.githooks/pre-commit` is prohibited.
- **Consequences.** Positive: hook stays simple; new checks land as numbered steps. Negative: composition order matters and is implicit. Neutral: ADR governance landed as the next numbered step per SPEC §2.4.

### §4.8 IADR-013 — Two-Toolchain Migration Window (Legacy ↔ Flexible)

- **Source.** [`MAINTENANCE.md:39-52`](../../../MAINTENANCE.md) (§1.1); [`PRE_COMMIT.md:55-68`](../../../PRE_COMMIT.md) (§7.A toolchain matrix).
- **Decision Outcome.** Legacy linters gate the commit; the flexible toolchain runs advisory until Task 019 flips `FM_TOOLCHAIN=1` to default; the flexible toolchain MUST NOT be used to bypass a legacy ERROR.
- **Consequences.** Positive: phased migration without flag-day risk. Negative: dual toolchain doubles cognitive load during the window. Neutral: ADR-tooling reuses `tools/fm/_core.py` so it inherits whichever toolchain wraps it.

### §4.9 IADR-014 — Frontmatter Waivers — Burn Protocol (Never-Growing)

- **Source.** [`PRE_COMMIT.md:70-82`](../../../PRE_COMMIT.md) (§7.B rules 1–5).
- **Decision Outcome.** `tools/.frontmatter-waivers` MUST never gain a new `/research/` entry; every coherence-check run SHOULD remove at least one waiver; rationale and tracking-Task ID are mandatory per line.
- **Consequences.** Positive: waiver list shrinks monotonically. Negative: requires per-coherence-run discipline. Neutral: the protocol is the precedent for the ADR exemption-list model.

### §4.10 IADR-015 — Audit-Graph Linkage Through Reciprocal Frontmatter Keys

- **Source.** [`FOLDERS.md:86-101`](../../../FOLDERS.md) (linkage table + reciprocity check).
- **Decision Outcome.** Every Task↔Prompt and Prompt↔Research edge MUST be reciprocal in frontmatter; `tools/lint-linkage.py` rejects asymmetric edges.
- **Consequences.** Positive: graph integrity is a CI-checkable invariant. Negative: edge edits are two-step (forward + back). Neutral: ADR supersession edges (`adr_supersedes`/`adr_superseded_by`) inherit this reciprocity model directly.

### §4.11 IADR-016 — Subfolder Threshold Heuristic (4+ Files of Same Category)

- **Source.** [`FOLDERS.md:51-55`](../../../FOLDERS.md) (Subfolder Heuristics 1–3); [`TASK.md:40`](../../../TASK.md) (Task subfolder threshold mirrored).
- **Decision Outcome.** A new subfolder MUST NOT be created until 4+ files of the same category accumulate; consolidation in the parent is preferred; no empty scaffolding.
- **Consequences.** Positive: trees stay flat and traversable. Negative: judgement call near the threshold. Neutral: the rule is the universal anti-bloat backstop.

### §4.12 IADR-017 — Hand-Rolled Frontmatter Parser Over PyYAML

- **Source.** [`tools/fm/_core.py:1-15`](../../../tools/fm/_core.py) (module docstring); [`AGENTS.md:218-222`](../../../AGENTS.md) (depth-1 binding).
- **Decision Outcome.** The flexible toolchain implements its own frontmatter parser (FRONTMATTER_RE + scalar-list handling) and MUST NOT depend on PyYAML for the depth-1 schema.
- **Consequences.** Positive: parser is ≈ 50 LoC and rejects ambiguous nesting deterministically. Negative: bug fixes don't come for free from upstream. Neutral: composes with IADR-004 (depth-1) and the LLM-hallucination prevention rationale.

### §4.13 IADR-018 — Research Workspace Immutability Post-Closure (T4)

- **Source.** [`MAINTENANCE.md:33`](../../../MAINTENANCE.md) (T4 row); [`PRE_COMMIT.md:76`](../../../PRE_COMMIT.md) (no-new-research-waivers rule).
- **Decision Outcome.** A `/research/<slug>/` workspace whose frontmatter is `research_phase: complete` MUST NOT be modified; new findings MUST land via a successor research run or an ADR.
- **Consequences.** Positive: research is a stable epistemic anchor. Negative: errata require a successor run rather than an in-place fix. Neutral: this is the immutability paradigm the ADR `Accepted` lifecycle inherits.

---

## §5 Inter-IADR Dependencies

| Dependency | Direction | Note |
|---|---|---|
| IADR-001 → IADR-012 | uses | Session bootstrap depends on `check-governance.sh` already being composable. |
| IADR-002 → IADR-010 | uses | The folder partition is the precondition for the universal `readme.md` rule. |
| IADR-003 → IADR-015 | uses | Frontmatter-as-truth makes reciprocity machine-checkable. |
| IADR-004 → IADR-017 | uses | Depth-1 makes a hand-rolled parser feasible. |
| IADR-005 → IADR-018 | uses | T4 immutability is the mutation-surface boundary. |
| IADR-013 → IADR-014 | uses | The waiver burn protocol is per-toolchain; re-expression at the flip is mandatory. |

No cycles detected; the graph is a DAG.

---

## §6 Appendix — Rejected Candidates (False-Positive Control)

The following candidates were considered and rejected; each citation makes clear why the clause does not meet the §1.1 inclusion bar.

### §6.1 Rejected Candidate R1 — "Subagent Decomposition as a First-Class Authoring Pattern"

- **Why considered.** Audit REPORT §2 IADR-010 (P3) raises the pattern.
- **Citation.** `tasks/029-adr-assumption-audit/task.md`; observed in Task 030 lineage.
- **Why rejected.** The pattern is *practice*, not a binding clause in any root spec. No root spec mandates subagent decomposition; the friction log calls out the *ambiguity*, which is itself a pending decision, not an in-force rule. Inclusion would synthesise a rule that no source declares.

### §6.2 Rejected Candidate R2 — "Skill Provenance Footer Format"

- **Why considered.** `AGENTS.md:76-78` (the Skill Provenance section under Closing Run Procedure) describes where `/sc:createPR` lives.
- **Citation.** `AGENTS.md:76-78`.
- **Why rejected.** This is *attribution metadata* about an external skill, not a binding architectural decision; it does not mandate that future skills carry footer attribution, and changing the wording would not break any agent contract. Fails §1.1 criterion 2 (architecturally significant).

### §6.3 Rejected Candidate R3 — "Markdown Header Formatting Consistency"

- **Why considered.** `PRE_COMMIT.md §5` ("Formatting & Linting") states all Markdown files MUST have consistent header formatting and valid relative links.
- **Citation.** `PRE_COMMIT.md:24-25`.
- **Why rejected.** This is a *style* clause without a binding mechanical enforcement (no validator catches header-style drift). It is a SHOULD-in-spirit even though it uses MUST language. Fails §1.1 criterion 1 (currently in force) — there is no mechanical gate, and the rule is broken in numerous existing files without rejection.

### §6.4 Rejected Candidate R4 — "Slug-Folder Coupling for Task Variants"

- **Why considered.** Audit REPORT §2 IADR-007 (P2) raises slug-folder coupling.
- **Citation.** `TASK.md:75, 325-326`.
- **Why rejected.** The decision is *partially in conflict* with the ratified ADR SPEC §4.1 ADR.A.2.7 (`decisions/<NNNN>-<slug>.md` is *file*, not folder), per audit REPORT §2 inter-IADR contradiction note (lines 99–100). It cannot be ratified as a single ADR until the contradiction is resolved by an explicit ADR; deferring is the correct disposition. (This is *deferral*, not rejection of the underlying rule for Tasks; the IADR-007 entry remains in the audit catalogue.)

---

## §7 Knowledge Base Index

### §7.1 Sources Consumed

| # | Source | Tier | Used For |
|---|---|---|---|
| 1 | [`AGENTS.md`](../../../AGENTS.md) | repo-canon | IADR-001, IADR-004, IADR-006, IADR-007, IADR-009 |
| 2 | [`TASK.md`](../../../TASK.md) | repo-canon | IADR-003, IADR-016 |
| 3 | [`PROMPT.md`](../../../PROMPT.md) | repo-canon | IADR-011 (cross-reference) |
| 4 | [`RESEARCH.md`](../../../RESEARCH.md) | repo-canon | IADR-008, IADR-018 |
| 5 | [`FOLDERS.md`](../../../FOLDERS.md) | repo-canon | IADR-002, IADR-003, IADR-010, IADR-011, IADR-015, IADR-016 |
| 6 | [`PRE_COMMIT.md`](../../../PRE_COMMIT.md) | repo-canon | IADR-008, IADR-012, IADR-013, IADR-014, IADR-018 |
| 7 | [`FRUSTRATED.md`](../../../FRUSTRATED.md) | repo-canon | IADR-008 |
| 8 | [`MAINTENANCE.md`](../../../MAINTENANCE.md) | repo-canon | IADR-005, IADR-013, IADR-018 |
| 9 | [`tools/fm/_core.py`](../../../tools/fm/_core.py) | repo-tooling | IADR-004 (parser implementation), IADR-017 |
| 10 | [`research/adr-spec-research-synthesis/output/SPEC.md`](../../adr-spec-research-synthesis/output/SPEC.md) | repo-research | MADR shape, anchor convention |
| 11 | [`research/adr-assumption-audit/output/REPORT.md`](../../adr-assumption-audit/output/REPORT.md) | repo-research | predecessor IADR catalogue (§2) |

### §7.2 Predecessor Acknowledgement

This SPEC explicitly cites the following audit-catalogue entries as predecessors:
- IADR-001 (audit REPORT §2 line 75) — promoted unchanged.
- IADR-002 (audit REPORT §2 line 76) — promoted unchanged.
- IADR-003 (audit REPORT §2 line 77) — promoted unchanged.
- IADR-004 (audit REPORT §2 line 78) — promoted unchanged.
- IADR-005 (audit REPORT §2 line 79) — promoted unchanged.

P2 and P3 entries from the audit catalogue (IADR-006…IADR-011 in audit numbering) are folded into the §4 catalogue with renumbering to keep the corpus self-contained.

### §7.3 Open Questions Surfaced (Outward Routing)

| ID | Open question | Routing |
|---|---|---|
| OQ.1 | Should the slug-folder coupling rule for Tasks (audit IADR-007) become an ADR, given it conflicts with ADR governance SPEC §4.1 ADR.A.2.7? | Defer to a future Task that explicitly resolves the contradiction. |
| OQ.2 | Should this corpus's P2 entries (IADR-006…IADR-015) be ratified in a single batch ADR or one-by-one? | Recommend hybrid: cluster IADR-013+IADR-014 (toolchain), cluster IADR-010+IADR-011 (folder discipline), individual otherwise. |
| OQ.3 | Should `adr_status: Proposed` files participate in the ADR-driven friction-log (per IADR-008)? | Defer; the audit found this question is identical to OQ.5 in the ratified SPEC §8. |
