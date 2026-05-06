---
type: note
status: draft
slug: task-040-synthesis
summary: "Task 040 Phases 2–4 synthesis — final per-aspect classification (§A), anchor-scheme reconciliation decision (§B = option (ii)), MCP reality-check matrix (§C). Built atop evaluation-notes.md (backend) + evaluation-notes-frontend.md."
created: 2026-05-06
updated: 2026-05-06
---

# Task 040 — Phase 2/3/4 Synthesis

This document consolidates the backend-architect (`evaluation-notes.md`) + frontend-architect (`evaluation-notes-frontend.md`) lenses into final binding decisions for Task 040. Phases 5 (concrete patches) and 6 (governance check) are implemented in separate commits; this synthesis is their input.

---

## §A. Final Per-Aspect Classification (Phase 2)

13 rows, one per Gemini § (or sub-§). Both lenses converge on **0 ACCEPT-AS-IS** and **1 outright REJECT**. The remaining 12 rows split into 8 AMEND-AND-ACCEPT (vocabulary worth lifting; bindings dropped or rewritten) and 4 MERGE-INTO-existing-task.

| Gemini § | Topic | Final verdict | Host (if MERGE) | Rationale |
|---|---|---|---|---|
| §0 | DAG of execution + 8-workspace ↔ 8-server table | **AMEND-AND-ACCEPT** | — | Lift the *DAG-of-execution* framing; reject the 8↔8 symmetry table (operationally false per backend-architect §D). Use as a 2-line preamble in MAINTENANCE.md §1.1.2 amendment. |
| §1.1 | `/sc:pm` as background orchestrator | **AMEND-AND-ACCEPT** | — | Reject "MUST on session init" (unauditable per backend-architect §D.3). Lift the *PDCA loop* vocabulary into AGENTS.md §3 prose only. |
| §1.2 | `/sc:index-repo` / `/sc:save` / `/sc:load` | **AMEND-AND-ACCEPT** | — | Mention as available manual operations in FOLDERS.md §3 (operator surface), not as MUST-on-clone. Strip Serena MCP citations until configured. |
| §2.1 | `/sc:spawn` Planner | **MERGE-INTO** | Task 033 (TASK.md) | Lift the Planner / Tech-Lead vocabulary into Task 033 ST-5 (TASK.md amendment). Reject the SC.CMD.2.1 4-hour threshold (no machinery emits an effort estimate). |
| §2.2 | `/sc:task` Tech Lead | **MERGE-INTO** | Task 033 (TASK.md) | Same MERGE target as §2.1; treat as one paragraph. |
| §2.3 | `/sc:workflow` PRD→roadmap | **AMEND-AND-ACCEPT** | — | Useful conceptual framing for `/prompts/<slug>/` authoring (PROMPT.md §2 prose). No mandate. |
| §3.1 | `/sc:brainstorm` Socratic | **MERGE-INTO** | Task 034 (PROMPT.md) | Already implemented as research-prompt-optimizer Phase 1. Add a one-line cross-reference in Task 034 ST-4 (PROMPT.md amendment). |
| §3.2 | `/sc:research` autonomous discovery | **AMEND-AND-ACCEPT** | — | Useful framing. Strip Tavily/Playwright/Morphllm citations (none integrated). Keep Sequential reference only. Land as a one-paragraph option in RESEARCH.md §2.2 alongside the manual research workflow. |
| §3.3 | `/sc:spec-panel` ≥ 7.0 scoring gate | **REJECT** | — | The `≥ 7.0` gate is invented; no upstream machinery emits a consumable score (per backend-architect §D.1; the upstream skill brief shows `7.2/10` only as illustrative output). |
| §4 | `/sc:design` + `/sc:implement` | **AMEND-AND-ACCEPT** | — | Out of scope for the spec-integration chain (which targets governance, not feature implementation). Lift one sentence about "design-before-implement" into AGENTS.md §60–65 if it strengthens the assumption-log discipline. Otherwise drop. |
| §5 | `/sc:analyze` + `/sc:troubleshoot` + `/sc:test` | **AMEND-AND-ACCEPT** | — | The `--readonly` default for `/sc:troubleshoot` is a sound *pattern* worth lifting into PRE_COMMIT.md §7 prose. Reject auto-invocation mandates. |
| §6 | `/sc:reflect` + `/sc:git` in pre-commit | **MERGE-INTO** | Task 037 (PRE_COMMIT.md) | Lift `--readonly` diagnostic pattern + smart-commit framing as a *Gherkin scenario* under PC.B.* anchors in Task 037 ST-4. Reject the parallel-pipeline framing (would compete with `tools/check-trust.py` + `tools/check-governance.sh` per backend-architect §D.2). |
| §7 | `sc-document` + ReflexionPattern + `confidence-check` | **MERGE-INTO** | Task 038 (FRUSTRATED.md) | Lift the *Reflexion pattern* concept into FRUSTRATED.md §FL.Log via Task 038 ST-3. Reject the `sc-document` skill conflation (frontend-architect §F.note: actual `sc:document` is for code-doc, not friction-logging). Reject the `confidence-check` skill mandate (skill does not exist locally). |
| §8 | `/sc:improve` + `/sc:cleanup` + `/sc:build` (nightly) | **MERGE-INTO** | Task 039 (MAINTENANCE.md) | Vocabulary aligns. Strip MorphLLM citation (not integrated). Land in Task 039 ST-6 (MAINTENANCE.md amendment) §1.1.2 / §3 prose. |

**Aggregate:** 0 ACCEPT-AS-IS / 8 AMEND-AND-ACCEPT / 4 MERGE-INTO-existing-task / 1 REJECT.

---

## §B. Anchor-Scheme Reconciliation Decision (Phase 3)

**Decision: option (ii) — fold `SC.CMD.<aspect>.<statement>` into host-spec namespaces.**

Rationale:

1. The repo already has 9 anchor namespaces (`ADR.A.*`, `T.B.*`, `P.B.*`, `R.B.*`, `F.B.*`, `PC.B.*`, `FR.B.*`, `M.B.*`, plus the AGENTS.md `AG.*` family). Adding `SC.CMD.*` as a 10th creates proliferation without a single host file (the `SC.CMD.*` claims span every root spec).
2. Every Gemini scenario re-anchors cleanly into a host-spec namespace: `SC.CMD.6.A.1` (reflect-before-commit) becomes `PC.B.SECREFL.1` in PRE_COMMIT.md; `SC.CMD.5.A.1` (security audit) becomes `PC.B.SECAUDIT.1`; `SC.CMD.7.A.1` (Reflexion on rate-limit) becomes `FR.B.REFLEX.1` in FRUSTRATED.md.
3. The host-namespace approach matches the precedent set by Task 031 (`ADR.A.*` lives in the ADR-spec ecosystem, not as a top-level spec governance namespace).

### Per-Gemini-anchor remapping table (apply during Phase-5 patches)

| Gemini anchor | New anchor | Host file |
|---|---|---|
| `SC.CMD.1.A.1` (PM init reads AGENTS.md) | `AG.PM.1` | AGENTS.md |
| `SC.CMD.1.A.2` (`/sc:index-repo` on clone) | `F.B.IDX.1` | FOLDERS.md |
| `SC.CMD.2.A.1` (Spawn Epic decomposition) | `T.B.SPAWN.1` | TASK.md |
| `SC.CMD.2.A.2` (Task delegation to security persona) | `T.B.DELEG.1` | TASK.md |
| `SC.CMD.3.A.1` (Brainstorm Socratic) | `P.B.BRAIN.1` | PROMPT.md |
| `SC.CMD.3.A.2` (External API research) | `R.B.EXTAPI.1` | RESEARCH.md |
| `SC.CMD.4.A.1` (JWT implement) | (REJECT — out of scope) | — |
| `SC.CMD.5.A.1` (Security audit) | `PC.B.SECAUDIT.1` | PRE_COMMIT.md |
| `SC.CMD.5.A.2` (Diagnostic halt) | `PC.B.DIAG.1` | PRE_COMMIT.md |
| `SC.CMD.6.A.1` (Reflect-before-commit) | `PC.B.REFL.1` | PRE_COMMIT.md |
| `SC.CMD.7.A.1` (Reflexion on 429) | `FR.B.REFLEX.1` | FRUSTRATED.md |

**Mechanical implication:** Task 040 Phase-5 patches MUST use the right-column anchor when adding any salvaged scenario to a host spec. No `SC.CMD.*` anchor lands in any final spec.

---

## §C. MCP Reality-Check Matrix (Phase 4)

| Server | Cited by Gemini for | Status | Final action |
|---|---|---|---|
| **Serena** | AGENTS.md + FOLDERS.md memory persistence | **Aspirational** — referenced as a manual-invocation MCP via `/sc:save` / `/sc:load`; no auto-persistence integration with `tools/check-governance.sh` or pre-commit. | Strip every "MUST utilize Serena" mandate. Mention as available manual surface in AGENTS.md §3 prose only. |
| **Sequential** | TASK.md + PRE_COMMIT.md reasoning | **Ambient** — available to Claude Code but no repo machinery configures it. | Keep mentions where they describe agent reasoning capability; drop where they describe binding behaviour. |
| **Context7** | PROMPT.md + PRE_COMMIT.md framework lookup | **Ambient** — same as Sequential. | Same treatment. |
| **Tavily** | RESEARCH.md web search | **Hallucinated for this repo** — not configured anywhere. | Strip from all merged amendments. RESEARCH.md §2.2 amendment (Task 035 ST-5) cites repo's actual web tools (`WebSearch`, `WebFetch`) instead. |
| **Playwright** | RESEARCH.md scraping + `/sc:test` E2E | **Hallucinated** — no Playwright config; no `tests/e2e/` infrastructure in this repo. | Strip from every merged amendment. |
| **Magic** | `/sc:implement` UI generation | **Out of scope** — no UI artefacts in `agency` repo (the Agency-System frontend HTML files are demos, not active development). | Drop entirely. |
| **MorphLLM** | MAINTENANCE.md large refactors | **Aspirational** — could be useful for the bulk T1/T2 mutation pattern, but not configured today. | Strip the SHOULD mandate from Task 039 ST-6 (MAINTENANCE.md amendment) §1.1.2; mention as a future option in a footnote. |
| **Chrome DevTools** | FRUSTRATED.md diagnostics | **Category error** — FRUSTRATED.md is a 32-line FL0–FL3 friction-log spec, not a browser-debug surface. | Drop entirely from any merged amendment. |

**Aggregate:** 0 of 8 servers integrated with the repo's pipeline today; 2 ambient (usable but not pipeline-bound); 2 aspirational (worth integration as future work); 4 either hallucinated or category-errors.

**Implication for Task 039 ST-6 (MAINTENANCE.md amendment):** the §1.1.2 three-way table (Legacy / Flexible / ADR) MUST NOT silently grow a fourth column for "MCP servers". MCP is a separate concern; if a future Task wants to introduce MCP-as-a-toolchain, it does so explicitly with its own scaffolded chain.

---

## §D. Process Notes for Phase 5 Maintainer

When applying patches per §A's MERGE rows:

1. **Use the §B remapping table verbatim** for any anchor identifier in a salvaged scenario.
2. **Strip MCP citations per §C** — never cite Tavily / Playwright / MorphLLM / Chrome DevTools / Magic in any merged amendment, even passingly.
3. **Vocabulary lifts are prose-only.** "Planner / Tech-Lead", "Reflexion pattern", "PDCA loop" go into prose paragraphs in the host spec. They do NOT become RFC-2119 `MUST` clauses unless the host spec already has machinery to enforce them.
4. **Cite this synthesis** in every merged amendment's Phase-5 commit message: `(per Task 040 §A row N + §B remap)`.

---

## §E. Phases 5 + 6 Status

- **Phase 5** (concrete patches): **three** highest-leverage MERGE patches applied in commit `9e3b59f` (Loop 5 of `/sc:improve`) — Task 033 ST-5 (Planner/Tech-Lead vocabulary), Task 038 ST-3 (Reflexion pattern), Task 039 ST-6 (three-column toolchain table; strip MorphLLM citation). Remaining MERGE rows for **Tasks 034** (§3.1 brainstorm Socratic → PROMPT.md amendment cross-reference) and **Task 037** (§6 reflect-before-commit → PRE_COMMIT.md PC.B.REFL.1 scenario) are queued for the maintainer.
- **Phase 6** (governance check + closure): runs after every Phase-5 patch lands. Final closure transitions Task 040 to `task_status: done` with friction-log.md.
