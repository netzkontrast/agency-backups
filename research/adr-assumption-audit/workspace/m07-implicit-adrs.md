---
type: note
status: active
slug: adr-assumption-audit-m07
summary: "Subagent B output: [M07] contradiction-log scan of root specs + tooling, surfacing decisions that are architecturally in force but never formally recorded as ADRs. 11 IADRs catalogued."
created: 2026-05-05
updated: 2026-05-05
---

# Subagent B — [M07] Implicit ADR Inventory

**Method:** [M07] Contradiction Log applied as a *scan* — for each root spec / tool file, identify normative architectural choices that are *enacted* but not *stated as ADRs*.
**Targets:** root specs (`AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `MAINTENANCE.md`, `FRUSTRATED.md`, `README.md`); tooling (`tools/check-governance.sh`, `tools/fm/_core.py`, `tools/fm/{validate,extract,edit,query}.py`).
**Output contract:** ≥ 8 IADRs with `Implicit-ADR ID / Decision / Evidence / Conflict / Spec section / Priority / Recommended title`.

This inventory extends the 14 implicit decisions catalogued in Task 027's [`workspace/analysis.md §A`](../../adr-spec-research-synthesis/workspace/analysis.md) — the entries below either deepen those (with file:line evidence) or surface additional decisions that the Task 027 analysis missed (it scanned root specs only; this scan also covers tooling).

## IADR Inventory

### IADR-001 — `AGENTS.md` is a layered runtime contract, not just documentation

- **Decision:** Every Claude Code session MUST run `./install.sh` then `tools/check-governance.sh` before reading or writing any repository file. This is a hard precondition, not a recommendation.
- **Evidence:** `AGENTS.md:38-40` "SS.1 An agent MUST run `./install.sh` at the start of every session before reading or writing any repository file."
- **Contradiction with spec:** No conflict. The ADR governance spec inherits `tools/check-governance.sh` as the gate; this IADR is the upstream rule that makes that inheritance meaningful.
- **Spec section at issue:** SPEC §2.4 (hook integration) inherits this; should cite it.
- **Formalization priority:** **P1.** This is the most-violated implicit ADR in agent runs (agents skip `install.sh` "because deps look installed").
- **Recommended title:** `ADR-0001 — Mandatory Session Bootstrap and Governance Gate`.

### IADR-002 — Three-folder operational topology is the indivisible orchestration surface

- **Decision:** Operational work happens in exactly three top-level folders (`/tasks/`, `/prompts/`, `/research/`). New top-level operational folders are an anti-pattern.
- **Evidence:** `FOLDERS.md:18-22` (table); `FOLDERS.md:99-103` (anti-pattern); `FOLDERS.md:106-116` (exemption table for non-operational folders).
- **Contradiction with spec:** The ADR spec adds `/decisions/` as a fourth top-level folder, mitigated via the §8 exemption-table extension. The IADR is preserved but its enforcement *exemption surface* grows.
- **Spec section at issue:** SPEC §2.1 (storage path).
- **Formalization priority:** **P1.** Every new contributor must understand this rule before authoring; making it implicit risks accidental top-level folder creation.
- **Recommended title:** `ADR-0002 — Operational Folder Topology and Exemption Protocol`.

### IADR-003 — Frontmatter is the load-bearing schema; bodies are secondary

- **Decision:** Cross-directory linkage flows *exclusively* through frontmatter keys (`task_uses_prompts`, `task_spawns_research`, etc.); body-level Markdown links are advisory only.
- **Evidence:** `FOLDERS.md:85-95` "the **frontmatter is the source of truth** for any future CLI/graph tooling"; `TASK.md:42-44` "L1 + L2 mandatory in operational directories".
- **Contradiction with spec:** No conflict. The ADR spec uses `adr_supersedes` / `adr_superseded_by` as the canonical edge representation, consistent with this IADR.
- **Spec section at issue:** SPEC §2.2, §6.1.
- **Formalization priority:** **P1.** This is the architectural cornerstone of the audit graph.
- **Recommended title:** `ADR-0003 — Frontmatter as the Single Source of Truth for the Audit Graph`.

### IADR-004 — YAML is intentionally crippled at depth 1

- **Decision:** YAML frontmatter MUST NOT nest beyond one level. Lists MUST contain only scalars. This is a hard constraint motivated by LLM YAML-parsing hallucinations.
- **Evidence:** `AGENTS.md:218-219` "YAML MUST NOT nest beyond one level. Lists MUST contain scalars or short strings only. This is a hard constraint to prevent LLM YAML-parsing hallucinations."; `tools/fm/_core.py:41-44` (parser docstring); enforced at `tools/fm/_core.py:parse_frontmatter`.
- **Contradiction with spec:** No conflict; SPEC §2.2 inherits.
- **Spec section at issue:** SPEC §7.4 JSON-Schema.
- **Formalization priority:** **P1.** The rationale (LLM hallucinations) belongs in an ADR so future maintainers don't naively "upgrade" to nested YAML.
- **Recommended title:** `ADR-0004 — YAML Depth-1 Constraint and Anti-Hallucination Rationale`.

### IADR-005 — Repair authority is tiered (T1/T2/T3/T4) with hard surface boundaries

- **Decision:** Maintenance agents may apply T1 (mechanical) and T2 (additive) fixes in-place; T3 (structural) MUST become a Task; T4 (research-touching, post-`complete`) is forbidden.
- **Evidence:** `MAINTENANCE.md:24-32` (table); `MAINTENANCE.md:35` "Root governance specs are subject to T1/T2 repairs only."
- **Contradiction with spec:** No conflict. SPEC §6.1 ADR.A.4.1 explicitly inherits the T4 paradigm.
- **Spec section at issue:** SPEC §6.1.
- **Formalization priority:** **P1.** Underlies every maintenance run; deserves explicit ADR formalization.
- **Recommended title:** `ADR-0005 — Repair Authority Tiers and Mutation Surface Boundaries`.

### IADR-006 — Two-toolchain coexistence is a deliberate transition state

- **Decision:** Legacy linters (`tools/validate-frontmatter.py`, `tools/lint-{structure,linkage,runlog}.py`) and the flexible toolchain (`tools/fm/validate.py`) coexist deliberately during the Task 016→019 migration window. `tools/check-governance.sh` toggles via `FM_TOOLCHAIN=1`.
- **Evidence:** `MAINTENANCE.md:39-52` (transition table); `tools/check-governance.sh:32-48` (the dual-run code path); `PRE_COMMIT.md:55-67` (toolchain selection matrix).
- **Contradiction with spec:** Partial conflict. SPEC §7.3 rationale acknowledges the transition; SPEC §7.1 does not specify which validator chain `agency-adr` composes with at a given moment. The plan §1.1 resolves this for the implementation, but the SPEC itself elides it.
- **Spec section at issue:** SPEC §7.3 (rationale only; no normative coverage).
- **Formalization priority:** **P2.** Resolves itself once Task 019 flips the default; until then, ADR-formalising it would freeze a temporary state.
- **Recommended title:** `ADR-0006 — Two-Toolchain Migration Window (deferred until Task 019 flips the default)`.

### IADR-007 — Slug equals folder name; renumbering changes only `<NNN>`

- **Decision:** A folder's `slug` (frontmatter) MUST equal the folder name (minus the `<NNN>-` prefix for tasks). Renumbering changes only `<NNN>`, never `slug`.
- **Evidence:** `TASK.md:75` "slug | string | Kebab-case identifier; MUST match folder name where applicable."; `TASK.md:325-326` "The Task slug MUST remain stable across renumbering; only `<NNN>` changes."
- **Contradiction with spec:** Partial conflict. SPEC §4.1 ADR.A.2.7 imposes a *coupled* `slug + adr_id` filename invariant (`<NNNN>-<slug>.md`), which is a different rule from the Task convention. The ADR rule is *stricter* (filename encodes both); this IADR is the looser Task convention.
- **Spec section at issue:** SPEC §4.1.
- **Formalization priority:** **P2.** The two filename conventions need explicit ADR documentation so contributors don't conflate them.
- **Recommended title:** `ADR-0007 — Slug-Folder Coupling and Renumbering Invariant (Task and ADR Variants)`.

### IADR-008 — Frontmatter parsing is hand-rolled, not PyYAML

- **Decision:** The flexible toolchain parses frontmatter with a hand-rolled depth-1 parser (`tools/fm/_core.py:parse_frontmatter`), not PyYAML, despite PyYAML being in `requirements.txt`. PyYAML is reserved for `tools/dramatica-nav/`.
- **Evidence:** `tools/fm/_core.py:1-15` (module docstring "frontmatter parsing (hand-rolled, no PyYAML)"); `tools/requirements.txt:6-9` "PyYAML: used by tools/dramatica-nav/".
- **Contradiction with spec:** No conflict. SPEC §7.1 ADR.A.5.9 mandates `agency-adr` reuse `tools/fm/_core.py`, so it inherits the hand-rolled parser by transitivity.
- **Spec section at issue:** none directly; affects SPEC §7.1 by inheritance.
- **Formalization priority:** **P2.** The decision to forgo PyYAML is non-obvious; an ADR would prevent a future "let's just use PyYAML" cleanup PR from un-picking the rationale.
- **Recommended title:** `ADR-0008 — Hand-Rolled Frontmatter Parsing Over PyYAML for Hallucination-Hardened Strictness`.

### IADR-009 — Friction logs are universally mandatory, including FL0

- **Decision:** Every closed Task / completed Research run MUST produce a `friction-log.md` with an FL[0–3] declaration, even if the work was frictionless.
- **Evidence:** `FRUSTRATED.md:5-13`; `RESEARCH.md:103-107`; `TASK.md:282-300` (§7.7 mechanical enforcement).
- **Contradiction with spec:** Partial conflict. SPEC inherits the friction-log obligation only by transitivity (an ADR PR is a Task closure). The SPEC does not normatively bind ADR PRs to the FL declaration.
- **Spec section at issue:** SPEC §2.5 (closure protocol) — should cite FL obligation.
- **Formalization priority:** **P2.** Improves spec completeness; not blocking.
- **Recommended title:** `ADR-0009 — Universal Friction Logging at Closure (FL0 Inclusive)`.

### IADR-010 — Subagent decomposition is a first-class authoring pattern

- **Decision:** Tasks may delegate to multiple parallel subagents, each with a distinct critical-thinking method. The subagent outputs merge into a single REPORT or SPEC.
- **Evidence:** `tasks/029-adr-assumption-audit/task.md` (this very task — three subagents A/B/C); precedent in `tasks/030-cleanup-dramatica-skills-corpus/` "Nine subtasks dispatch via /sc:agent".
- **Contradiction with spec:** No direct conflict, but the SPEC §3 "Explore" aspect is silent on whether ADR exploration MAY be subagent-decomposed. If yes, ADR.A.1.5 ("the agent MUST file a research-proposal Prompt") needs clarification on per-subagent vs aggregate prompt.
- **Spec section at issue:** SPEC §3.1 ADR.A.1.5.
- **Formalization priority:** **P3.** Pattern is observable but not yet normatively documented; a later ADR can codify it once the pattern stabilises.
- **Recommended title:** `ADR-0010 — Subagent Decomposition as a First-Class Authoring Pattern (deferred)`.

### IADR-011 — `tools/check-governance.sh` numbered-step composition is the gate's source of truth

- **Decision:** The pre-commit gate is composed of numbered steps inside `tools/check-governance.sh`. Adding a new validator means adding a new numbered step, not editing `.githooks/pre-commit` directly. Step numbering must remain in declaration order.
- **Evidence:** `tools/check-governance.sh:24-86` (numbered `[N/M]` echo blocks). The narrative-ontology validator at line 70-77 exemplifies the "gracefully optional" pattern (gated on a file existing).
- **Contradiction with spec:** No conflict; SPEC §2.4 ADR.A.5.8 explicitly cites this convention.
- **Spec section at issue:** SPEC §2.4.
- **Formalization priority:** **P3.** The convention is well-documented in `PRE_COMMIT.md §7`; an ADR would consolidate it but is not high-priority.
- **Recommended title:** `ADR-0011 — Pre-Commit Gate Composition via tools/check-governance.sh Numbered Steps`.

## Inter-IADR Contradictions

### Contradiction: IADR-002 ↔ IADR-007

- **Why:** IADR-002 establishes the three-folder operational topology with `<slug>` folders. IADR-007 establishes that slugs equal folder names. The ADR spec introduces `/decisions/<NNNN>-<slug>.md` (file, not folder). Two filename invariants now coexist:
  - Task / Prompt / Research: `<slug>` is the folder; `<NNNN>-` is a Task-only prefix.
  - ADR: `<NNNN>-<slug>.md` is the file; no folder per ADR.
- **Resolution needed:** A human (or an ADR) must declare whether ADRs deviate from the "every operational artefact lives in a folder" implicit rule, or whether `/decisions/<NNNN>-<slug>/<NNNN>-<slug>.md` (folder per ADR) is required. SPEC currently chose the file-only path; the contradiction with the folder convention is not surfaced.

### Contradiction: IADR-006 ↔ SPEC §7.3

- **Why:** IADR-006 says the two-toolchain coexistence is *deliberate and temporary*. SPEC §7.3 says `agency-adr` will "re-register against the flexible toolchain" when Task 019 flips the default — but does not specify behaviour during the transition window if `agency-adr` ships before Task 019 flips.
- **Resolution needed:** Either Task 028 implementation explicitly handles both validator chains until Task 019 ships, or it blocks until Task 019 ships. Currently ambiguous.

## Summary

| IADR | Priority | Conflict | Pending action |
|---|---|---|---|
| 001 | P1 | none | Author as ADR-0001. |
| 002 | P1 | none (resolved by SPEC §2.1 + §8 exemption ext.) | Author as ADR-0002. |
| 003 | P1 | none | Author as ADR-0003. |
| 004 | P1 | none | Author as ADR-0004. |
| 005 | P1 | none | Author as ADR-0005. |
| 006 | P2 | partial — SPEC §7.3 elides transition behaviour | Defer until Task 019 flips. |
| 007 | P2 | partial — competes with SPEC §4.1 ADR convention | Document both. |
| 008 | P2 | none | Author. |
| 009 | P2 | partial — SPEC §2.5 should cite FL obligation | Author. |
| 010 | P3 | partial — SPEC §3.1 ambiguous on subagent decomposition | Defer. |
| 011 | P3 | none | Defer; well-documented in PRE_COMMIT.md. |

**5 P1 + 4 P2 + 2 P3 = 11 IADRs.** Five are unconflicted P1 candidates for the first-batch ADR authoring (Strategy A or B per SPEC OQ.1).

Findings flow into `output/REPORT.md §2`, sorted by priority.
