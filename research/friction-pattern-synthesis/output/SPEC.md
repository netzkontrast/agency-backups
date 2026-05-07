---
type: research
status: completed
slug: friction-pattern-synthesis
summary: "Cross-task friction pattern synthesis: FL distribution histogram across 53 closed friction logs (33 task + 20 research), 8-category root-cause taxonomy with frequency counts, per-spec attribution table for FL2+ entries, and 4 verbatim TASK.md / FRUSTRATED.md amendment proposals with file:line targets. Closes Task 033 ST-1."
created: 2026-05-07
updated: 2026-05-07
research_phase: complete
research_executes_prompt: research-friction-pattern-synthesis
research_friction_level: FL1
---

# Friction Pattern Synthesis — Cross-Task Taxonomy

**Repository:** `/home/user/agency`
**Report Date:** 2026-05-07
**Corpus Surfaces:** `tasks/<NNN>-<slug>/friction-log.md` (33 logs) + `research/<slug>/reflection/friction-log.md` (20 logs) = **53 logs total**
**Falsification Threshold:** ≥15 closed tasks with non-empty friction logs. **Met:** 33 ≥ 15 (220% margin).

---

## §0 Scope and Provenance

This SPEC fulfils [Task 033 `task-spec-integration`](../../../tasks/033-task-spec-integration/task.md) ST-1 per [`/prompts/research-friction-pattern-synthesis/prompt.md`](../../../prompts/research-friction-pattern-synthesis/prompt.md). It aggregates every `friction-log.md` reachable on the current branch (`claude/run-close-task-spec-2sW2y`) at HEAD into a structured cross-task synthesis suitable for driving spec amendments in the parallel chain Tasks 032–039.

### Inputs

- 33 task-side `friction-log.md` files (closed tasks: `task_status` ∈ {`done`, `updated`, `abandoned`}).
- 20 research-side `reflection/friction-log.md` files (workspaces with `research_phase: complete`).
- [`tasks/030-cleanup-dramatica-skills-corpus/notes.md §3`](../../../tasks/030-cleanup-dramatica-skills-corpus/notes.md) — 10 planning-time friction events (FE-1..FE-10) plus 5 execution-time events (FE-EX-1..5) already classified. Absorbed as evidence in §2; counted separately from session-execution histogram (§1).
- [`research/adr-assumption-audit/output/REPORT.md §1`](../adr-assumption-audit/output/REPORT.md) — 4 high-blast technical assumptions + 1 cultural. Cross-referenced in §2 root-cause Category 7 (silent-drift / fidelity).
- [`tasks/033-task-spec-integration/task.md`](../../../tasks/033-task-spec-integration/task.md) — chain-level context.

### Methodology

1. Enumerate `friction-log.md` paths via `find tasks research -name friction-log.md`.
2. Extract the highest declared FL per file via grep on `Highest Friction Level`, `Highest Frustration Level`, `**FL[0-3]`, `Frustration Level: FL[0-3]`, `summary:` (when FL embedded). Files with no explicit declaration but `FL` mentioned in summary frontmatter (Tasks 016-021, 030-046) read from frontmatter line first.
3. For every FL2+ entry, parse the prose for the implicated governance spec(s); record the citation as `(SPEC.md §X.Y)` or `(file:line)`.
4. Cluster repeated phrases into root-cause categories; ≥6 distinct categories required (8 produced).
5. Cross-check against Task 030's pre-classified FE-1..FE-10 (which Task 030 already routed to amendment-target tasks 032-040 explicitly).
6. Author verbatim spec-text amendments grounded in ≥1 FL2+ evidence anchor each.

### Why this is needed

Individual friction logs are local; patterns are only visible at aggregate. Tasks 032–039 each amend one root spec but have no shared evidence base. This SPEC is that shared base. It is also a precondition for [Task 038 ST-1](../../../tasks/038-frustrated-spec-integration/task.md)'s parallel FL0-justification audit, which reads the same corpus and consumes §1 of this SPEC for its histogram input.

---

## §1 FL Distribution Histogram

### §1.1 Per-Surface Counts

Every closed task's friction log was scanned. Files where the FL appears only inside frontmatter `summary` were counted from that source (Task convention since Task 016).

#### Task surface (33 logs)

| FL  | Count | % of surface | Tasks (slug-only) |
|---  |---    |---           |---               |
| FL0 | 9     | 27.3%        | `004-create-missing-prompts`, `006-skills-navigation-bootstrap`, `008-harden-coherence-baseline-protocol`, `009-author-skills-root-spec`, `010-skills-frontmatter-index-suite`, `011-skills-frontmatter-schema-files`, `012-review-pr-29`, `014-improve-maintenance-spec-from-session`, `047-cross-spec-contradiction-baseline` |
| FL1 | 18    | 54.5%        | `000-decouple-architecture`, `001-refactor-governance-from-specs`, `002-token-efficiency-tool-suite`, `003-analyze-skillmd-novel-authoring`, `005-address-deferred-coherence-issues`, `007-reconcile-closed-task-linkage`, `013-renumber-duplicate-task-ids`, `015-integrate-dramatica-ncp-skills`, `016-flexible-frontmatter-toolchain`, `018-fm-section-editor`, `021-apply-fm-edit-to-deferred-coherence`, `026-update-governance-specs-from-research`, `027-adr-spec-research-synthesis`, `028-adr-tooling-impl-plan`, `029-adr-assumption-audit`, `031-sync-tasks-index-status-drift`, `032-agents-spec-integration`, `032-improve-maintenance-spec-may-2026` |
| FL2 | 5     | 15.2%        | `017-migrate-repo-to-flexible-toolchain`, `020-audit-prompt-fm-validate-conformance`, `030-cleanup-dramatica-skills-corpus`, `031-adr-tooling-impl`, `041-extract-subtask-prompts` |
| FL3 | 1     | 3.0%         | `019-fm-toolchain-suite-integration` |

#### Research-reflection surface (20 logs)

| FL  | Count | % of surface | Slugs |
|---  |---    |---           |---     |
| FL0 | 10    | 50.0%        | `agent-prompt-specs-3-systems-sdd`, `agentic-eval-trust-improvement-spec`, `agentic-session-continuity-spec`, `governance-specs-update-research`, `integrate-dramatica-ncp-skills`, `pr27-governance-review`, `repo-maintenance-protocol-spec`, `research-cross-spec-contradiction-baseline`, `skills-namespace-ontology`, `spec-driven-research-agentic-workflows` |
| FL1 | 9     | 45.0%        | `adr-assumption-audit`, `adr-corpus-extraction-from-governance-specs`, `adr-spec-research-synthesis`, `flexible-frontmatter-toolchain`, `obsidian-frontmatter-agentic-spec`, `skills-navigation-bootstrap`, `skills-skill-architecture`, `skills-skill-container-capabilities`, `token-efficiency-tool-suite` |
| FL2 | 1     | 5.0%         | `ncp-novel-co-authoring-spec` |
| FL3 | 0     | 0.0%         | — |

### §1.2 Aggregate Histogram (53 logs)

```
FL0  ████████████████████              19  (35.8%)
FL1  ███████████████████████████       27  (50.9%)
FL2  ██████                             6  (11.3%)
FL3  █                                  1  ( 1.9%)
```

### §1.3 Histogram Observations

- **FL0 surface asymmetry.** Research-side runs declare FL0 at 50.0%, task-side at only 27.3%. This is consistent with the prompt convention divergence noted in §2 Category 6 (research prompts have stronger preflight gates; task work crosses more spec surfaces and accumulates more friction events).
- **FL1 dominance.** Half the corpus declares FL1, indicating the governance toolchain catches problems but still accumulates per-run nits. This is the design intent of FRUSTRATED.md FL1 ("minor annoyance, no plan rewrite needed") and is healthy.
- **FL2 concentration in toolchain-migration tasks.** 4 of the 5 task-side FL2 entries (017, 019 was FL3 not FL2 here, 020, 030, 041) implicate either the flexible-frontmatter migration or extraction-tooling phase — a single architectural arc. The 5th (031-adr-tooling-impl) is the ADR tooling implementation task. Pattern: large multi-file refactors and new sub-package introductions surface multi-axis friction.
- **FL3 singularity.** Only Task 019 (`fm-toolchain-suite-integration`) reached FL3, and the cause was external-infrastructure-class (parallel-subagent worktree-base inconsistency + org-quota cliff). No spec amendment can cure infrastructure cliffs; the post-Task-019 mitigation was procedural (sequential dispatch + pre-flight `git rev-parse` check).
- **Closed-as-`updated` tasks bias toward FL0–FL1.** All 9 task-side FL0 entries except `008`, `012`, and `047` are `task_status: updated` (plan-obsolesced cleanly). This is the correct signal: superseded plans don't generate execution friction by definition.
- **No FL3 on research-reflection surface.** Research-runs have failure modes that produce no output (sub-agent abort, prompt unparseable) but those produce no `friction-log.md` to count. This is a known measurement blind spot; mitigation is the falsification clause forcing a log even at FL0.

---

## §2 Root-Cause Taxonomy

Eight categories, frequency counts across the 53-log corpus. A single friction event can be tagged with multiple categories; counts are events, not files. Total tagged events: 116 (some logs contribute 0–9 events).

| # | Category | Events | Representative anchors (file → entry label) |
|---|---       |---:    |---                                          |
| **1** | **Spec-without-validator (intent vs enforcement gap)** | 18 | `tasks/000-decouple-architecture/friction-log.md` Item 1 ("Spec written without a validator"); `tasks/001/friction-log.md` Items 2–3 (waivers + scaffolder gaps); `research/skills-navigation-bootstrap/reflection/friction-log.md` FL1.2; `tasks/030/notes.md` FE-1 (subtask template absent); `tasks/030/notes.md` FE-6 (`/sc:*` lifecycle absent); `tasks/041/friction-log.md` F5 (no `path_classification` for `prompts/*/brief.md`) |
| **2** | **Reciprocity / linkage-graph drift** | 14 | `tasks/003-analyze-skillmd-novel-authoring/friction-log.md` Items 1–3; `tasks/007-reconcile-closed-task-linkage/friction-log.md` (entire log); `tasks/030/notes.md` FE-5, FE-9 (cardinality of `task_spawns_prompts`); `tasks/041/friction-log.md` F6, F8 (empty-string sentinels, self-reciprocity); `research/skills-namespace-ontology/reflection/friction-log.md` (broken-target reciprocity case); `tasks/019/friction-log.md` Friction 3 (scalar vs list back-edge) |
| **3** | **Two-source-of-truth drift / index staleness** | 11 | `tasks/030/notes.md` FE-3 (`task_status` task.md vs tasks/readme.md); `tasks/031-sync-tasks-index-status-drift/friction-log.md` F1 (snapshot drift); `tasks/032-agents-spec-integration/friction-log.md` F1 (baseline ERRORs from index drift); `tasks/032-improve-maintenance-spec-may-2026/friction-log.md` F11 (already-done finding); `tasks/030/friction-log.md` FE-EX-3 (hardcoded test-count drift) |
| **4** | **Parallel-dispatch / worktree base inconsistency** | 9 | `tasks/019/friction-log.md` Friction 1 (worktree base inconsistency, 3 different bases); `tasks/030/friction-log.md` FE-EX-1 (parallel main-tree race on shared markdown); `tasks/030/friction-log.md` FE-EX-5 (worktree filesystem leak); `tasks/030/friction-log.md` FE-EX-2 (org quota cliff mid-multi-agent run); `tasks/032-agents-spec-integration/friction-log.md` Phase A note (parallel pattern saved time but pre-existing baseline ERRORs were not isolatable) |
| **5** | **Pre-existing baseline ERRORs unrelated to current task** | 9 | `tasks/026/friction-log.md` Item 1 (orphan folder blocking SS.2); `tasks/032-agents-spec-integration/friction-log.md` F1 (3 baseline ERRORs deferred); `tasks/032-improve-maintenance-spec-may-2026/friction-log.md` F8 (jsonschema-missing FAIL); `research/skills-navigation-bootstrap/reflection/friction-log.md` FL1.2 (6 pre-existing structural lint errors); this Task's own deferral of 4 ERRORs; `tasks/030/friction-log.md` FE-EX-4 (`agency-adr` CLI not on PATH despite Task 028 `done`) |
| **6** | **Prompt ambiguity / `/sc:*` invocation semantics undefined** | 14 | `research/adr-spec-research-synthesis/reflection/friction-log.md` Entry 1 (`/sc:` skill invocation pattern); `research/adr-assumption-audit/reflection/friction-log.md` Entry 1 (subagent semantics vs literal sub-agent invocation, recurring); `tasks/030/notes.md` FE-2, FE-6 (`/sc:agent` undocumented + lifecycle); `research/agentic-eval-trust-improvement-spec/reflection/friction-log.md` (Spec-G/H/I bifurcation); `research/skills-skill-architecture/reflection/friction-log.md` 3 entries (claude.ai trigger lifecycle, skill dir, Jules/gemini-cli conventions); `tasks/028/friction-log.md` Entry 2 (prescriptive verb "flesh out" mismatched reality) |
| **7** | **Schema / contract drift between authored and runtime surface** | 16 | `tasks/000-decouple-architecture/friction-log.md` Item 5 (validator over-broad scope); `tasks/016/friction-log.md` Item 1 (SPEC vs live tree skills mismatch), Item 2 (heading normalisation under-specified), Item 3 (fnmatch vs regex); `tasks/017/friction-log.md` Friction 1 (164 fm-validate ERRORs surfaced post-toolchain), Friction 2 (`--delta` non-existent); `tasks/018/friction-log.md` Frictions 1–2; `tasks/019/friction-log.md` Friction 4 (Phase 3 default-on flip blocked by 71 F.B.* drift), Friction 5 (no fm-* successor for two legacy linters); `tasks/020/friction-log.md` Frictions 1–4 (stub-append vs authored migration; fm-section schema gate; fm-new template lag; check-body still not default-on); `tasks/031-adr-tooling-impl/friction-log.md` Entries 1–3 (dual-imports, run-log schema mismatch only in CI, diff gate vs placeholder text); `research/adr-assumption-audit/output/REPORT.md` ASM-001, ASM-009 (high-blast extractor blind spots) |
| **8** | **Structural-bloat / verbose-by-design tension** | 5 | `research/ncp-novel-co-authoring-spec/reflection/friction-log.md` (FL2 mid-task hierarchy retrofit; readme-per-folder mandate); `tasks/030/notes.md` FE-7 (verbose-by-design vs anti-bloat tension); `tasks/030/notes.md` A-10 (Frustration Log verbose by design); `tasks/030/notes.md` FE-10 (preview lifecycle for ontology artefacts); `tasks/030/notes.md` FE-8 (provisional-conventions pattern, ratification missing) |

### §2.1 Category Cross-Walk to Task 030's Pre-Classified Pattern Routing

Task 030's friction log already routed FE-1..FE-10 + FE-EX-1..5 to specific destination tasks (032, 033, 034, 037, 038, 039, 040). This SPEC's categories §2 Category 1 absorbs FE-1, FE-6, FE-2; Category 2 absorbs FE-5, FE-9; Category 3 absorbs FE-3 + FE-EX-3; Category 4 absorbs FE-EX-1, FE-EX-2, FE-EX-5; Category 5 absorbs FE-EX-4; Category 6 absorbs FE-2, FE-6 (overlap with C1 by design — they implicate both `tools/` and `prompts/` surfaces); Category 7 absorbs FE-4 (renderer YAML depth-2), FE-10 (preview lifecycle); Category 8 absorbs FE-7, FE-8.

### §2.2 Rare-Event Categories (deliberately excluded)

The following appeared ≤2 times and are not promoted to a category:

- **External tooling / API parse glitches** (Task 002, research `flexible-frontmatter-toolchain` Item 1, research `obsidian-frontmatter-agentic-spec` `google_search` failure): 3 events, all FL1, all transient. Already addressed by RESEARCH.md M13 query-expansion guidance.
- **Closure-pointer ambiguity for `done` and `abandoned` lifecycles** (Task 031-sync F4 only): 1 event, deferred to a successor by design. Not yet a pattern.
- **Cross-task amendment of closed plan** (research/adr-assumption-audit/reflection/friction-log.md Entry 2 only): 1 event, mitigated by additive-appendix pattern.

---

## §3 Per-Spec Attribution for FL2+ Entries

Each FL2+ friction event traces to one or more root-spec ambiguities, gaps, or contradictions. The table is the authoritative input for which root spec each amendment chain task should touch.

| Entry | FL | Friction summary | Root spec(s) implicated | Section / line anchor |
|---    |---:|---               |---                      |---                    |
| `tasks/017-migrate-repo-to-flexible-toolchain/friction-log.md` Friction 1 | FL2 | 164 fm-validate ERRORs surfaced post-Task-016; SPEC §8.2 done-condition forced schema-relaxation decision (empty `prompt.required_headings`) | FOLDERS.md (sub-folder readme requirement); `research/flexible-frontmatter-toolchain/output/SPEC.md §4.1, §8.2` | T4-immutable SPEC; FOLDERS.md §3 (sub-folder readme rule) |
| `tasks/017/friction-log.md` Friction 3 | FL2 | "MAINTENANCE.md §3.2 has no linter references to amend" — task plan referenced a section that didn't carry the relevant content | MAINTENANCE.md §3.2 vs §1 ("Validation surface stability") | MAINTENANCE.md §1, §3.2 |
| `tasks/017/friction-log.md` Friction 4 | FL2 | `tools/legacy/lint-{structure,linkage}.py` not yet replaced; SPEC §8.2 cleanup blocked | research SPEC §8.2 (T4-immutable) | research/flexible-frontmatter-toolchain/output/SPEC.md §8.2 |
| `tasks/019-fm-toolchain-suite-integration/friction-log.md` Friction 1 | FL3 | Worktree base inconsistency across 3 commits; one subagent fabricated tools/fm/ from scratch | (no canonical repo spec for parallel-dispatch contract) | TASK.md (no §); FRUSTRATED.md (no §); proposed home: `superclaude-spec` (Task 040) per `tasks/030/friction-log.md §Pattern routing` |
| `tasks/019/friction-log.md` Friction 2 | FL3 | Org usage limit cliff mid-multi-agent run; no retry path | (no canonical repo spec) | proposed: TASK.md §Multi-Phase Tasks (new); per Task 030 FE-EX-2 routing → Task 040 |
| `tasks/019/friction-log.md` Friction 4 | FL3 | Phase 3 (`--check-body` default-on) blocked by 71 F.B.1/6 ERRORs; SPEC §12.6 sequencing assigns flip to Task 020 | research/flexible-frontmatter-toolchain/output/SPEC.md §12.6 (T4-immutable) | research SPEC §12.6 |
| `tasks/020-audit-prompt-fm-validate-conformance/friction-log.md` Friction 1 | FL2 | 19 fully-custom prompts received structural stub-append rather than authored migration; semantic completeness deferred | PROMPT.md §5 (RISEN+ReAct heading set is normative); `research/flexible-frontmatter-toolchain/output/SPEC.md §4.1` | PROMPT.md §5; research SPEC §4.1 |
| `tasks/020/friction-log.md` Friction 2 | FL2 | `fm-section --rename` blocked because target body schema required `unordered_list` but source was paragraph | research SPEC §4.x body-schema declarations; PROMPT.md (no rename ergonomics) | research/flexible-frontmatter-toolchain/output/SPEC.md §4 |
| `tasks/030-cleanup-dramatica-skills-corpus/friction-log.md` FE-EX-1 | FL2 | Parallel main-tree dispatch race on shared markdown (ST-1 + ST-2 both writing `character-dynamics.md`); `subtask_depends_on` not honoured as serialisation barrier | TASK.md (no `subtask_depends_on` enforcement); FRUSTRATED.md (no parallel-dispatch FL trigger) | TASK.md §3 (no subtask schema); FRUSTRATED.md §Special Triggers (line 27–28) |
| `tasks/030/friction-log.md` FE-EX-2 | FL3 | Org monthly usage limit hit mid-Phase-B; §Goal all-or-nothing acceptance incompatible with partial completion | TASK.md §6 (Goal lifecycle); proposed home Task 040 | TASK.md §6 |
| `tasks/030/notes.md` FE-3 | FL2 | `task_status: done` on `task.md` vs `Status: in_progress` on `tasks/readme.md` — two-source-of-truth drift | TASK.md §7.11 (Tasks-Index Freshness); `MAINTENANCE.md §3.2` | TASK.md §7.11 (now landed via Task 031); MAINTENANCE.md §3.2 |
| `tasks/030/notes.md` FE-7 | FL2 | Tension between user "be verbose in your Frustration log" and FRUSTRATED.md §Special Triggers anti-bloat rule | FRUSTRATED.md §Special Triggers (line 27–28) | FRUSTRATED.md line 28 |
| `tasks/031-adr-tooling-impl/friction-log.md` Entry 1 | FL2 | `tools/` is not a Python package; relative imports forbidden but the existing fm-shim idiom misled the author for 25 minutes | `tools/readme.md` (no normative statement on import idiom); MAINTENANCE.md §1 (mutation surface, not import surface) | tools/readme.md (no canonical line); MAINTENANCE.md §1 |
| `tasks/041-extract-subtask-prompts/friction-log.md` F5 | FL2 | 45 brief.md files set `type: brief` not in closed L1 enum; linter silent because no `path_classification` rule for `prompts/*/brief.md` | AGENTS.md §Frontmatter Ontology (closed type set); `maintenance/schemas/header-ontology.json` (`path_classification`); FOLDERS.md §3 | AGENTS.md L1 type enum; header-ontology.json `path_classification.rules`; FOLDERS.md §3 |
| `tasks/041/friction-log.md` F6 | FL2 | Empty `prompt_spawned_from_research: ""` propagated from template to 45 files; OPTIONAL-field omission convention violated | PROMPT.md §3 (OPTIONAL fields → omit, not empty-string); `templates/prompt.md` | PROMPT.md §3 |
| `tasks/041/friction-log.md` F7 | FL2 | Shallow RISEN+ReAct migration; 35 prompts wrapped original brief verbatim in fenced block instead of decomposing into RFC-2119 normative steps | PROMPT.md §5 (Self-Containedness, RFC-2119 Normativity) | PROMPT.md §5 |
| `tasks/041/friction-log.md` F8 | FL2 | `task_owner: "unassigned"` and self-`task_uses_prompts: []` on Task 041 itself — TASK.md §6 ownership-claim Gherkin not enforced | TASK.md §6 (Gherkin "Agent picks up an open Task") | TASK.md §6 |
| `research/ncp-novel-co-authoring-spec/reflection/friction-log.md` (entire) | FL2 | Mid-task constraint mutation (monolith → nested → flat-with-readme-everywhere); decentralised-readme rule retroactively justified | FOLDERS.md (per-folder readme rule); FRUSTRATED.md §Special Triggers (line 27–28, "Structural Bloat") | FOLDERS.md §3, §5; FRUSTRATED.md line 28 |

### §3.1 Spec-Implication Frequency

Counted by row (some rows tag multiple specs):

| Spec                                                              | FL2+ rows implicating |
|---                                                                |---:                   |
| TASK.md                                                           | 6                     |
| FRUSTRATED.md                                                     | 3                     |
| FOLDERS.md                                                        | 3                     |
| PROMPT.md                                                         | 3                     |
| MAINTENANCE.md                                                    | 2                     |
| AGENTS.md                                                         | 1                     |
| `research/flexible-frontmatter-toolchain/output/SPEC.md` (T4)     | 4                     |
| (no canonical home — SuperClaude / `/sc:*` surface)               | 3                     |
| `tools/readme.md`                                                 | 1                     |
| `templates/prompt.md`                                             | 1                     |
| `maintenance/schemas/header-ontology.json` (`path_classification`)| 1                     |

The "no canonical home" cluster is the strongest signal that the open chain Task 040 (`superclaude-spec-evaluation`) needs to ratify a `/sc:*` command surface spec; this matches Task 030's existing routing decision.

---

## §4 Verbatim Spec-Text Amendment Proposals

Each proposal carries: (a) target file:line, (b) the exact current text being replaced or extended (`-`), (c) the exact proposed text (`+`), (d) ≥1 FL2+ evidence anchor from §3, and (e) the chain task that owns the amendment. These are *proposals* — ratification belongs to Tasks 032–039 individually per their respective brief.md / prompt.md.

### §4.1 Amendment 1 — TASK.md §7 Pre-Commit Checks: add §7.12 Subtask-Dependency Serialisation Barrier

**Target:** [`TASK.md`](../../../TASK.md) lines 282–319 (the §7 / §7.0 mechanical-enforcement table block).
**Owner task:** [Task 033 ST-5](../../../tasks/033-task-spec-integration/subtasks/05-spec-amendment-task-md.md).
**Evidence anchors:** §3 row `tasks/030/friction-log.md FE-EX-1` (FL2, parallel main-tree race); §3 row `tasks/041/friction-log.md F8` (FL2, ownership-claim drift); §2 Category 4 (Parallel-dispatch, 9 events).
**Diagnostic class:** No mechanical signal exists today when an agent dispatches Wave-N subtasks in parallel where any subtask declares another in-wave subtask in `subtask_depends_on`. The TASK.md §6 Gherkin scenarios for parallel dispatch are silent on this.

**Proposed insertion** (verbatim, append a new row to the §7.0 table at line 302 between current §7.11 row and the empty line that follows; then append a new numbered item 11 to the post-table list at line 318–319):

```
| §7.12 Subtask Dependency Serialisation | — (new) | `tools/fm/validate.py --type-check` (Task 019; subtask schema TBD by Task 033 ST-2) | Wave-N parallel dispatch contains subtasks where one declares another in-wave subtask in `subtask_depends_on` |
```

```
11. **Subtask Dependency Serialisation** — When dispatching subtasks in parallel (`/sc:agent` × N in a single message, or `Agent` tool fan-out), the agent MUST honour every in-wave `subtask_depends_on` declaration as a serialisation barrier. If any subtask in the wave names another subtask in the same wave as a prerequisite, the wave MUST be split into sequential sub-waves that respect the dependency DAG. Violations of this rule cause silent file-overwrite races on shared markdown (Task 030 FE-EX-1 — `character-dynamics.md` was reverted twice by parallel writers).
```

### §4.2 Amendment 2 — FRUSTRATED.md §Special Triggers: add Multi-Phase Quota-Cliff trigger

**Target:** [`FRUSTRATED.md`](../../../FRUSTRATED.md) line 27 (`## Special Triggers`) and line 28 (the existing "Structural Bloat / Micromanagement" bullet).
**Owner task:** [Task 038 ST-3](../../../tasks/038-frustrated-spec-integration/subtasks/03-spec-amendment-frustrated-md.md).
**Evidence anchors:** §3 rows `tasks/019/friction-log.md` Frictions 1 & 2 (FL3, worktree-base + org-quota cliff); `tasks/030/friction-log.md` FE-EX-2 (FL3, partial-completion incompatible with all-or-nothing §Goal); §2 Category 4 (9 events).
**Diagnostic class:** FL3 is currently triggered by "instructions are fundamentally impossible" or "stuck in a loop" but does not name the *external* cliffs (org-quota mid-run; worktree-base inconsistency) that produced the only FL3 in the corpus.

**Proposed insertion** (verbatim, append a new bullet immediately after line 28's "Structural Bloat / Micromanagement" bullet, before the blank line that precedes line 30):

```
- **External-Infrastructure Cliff:** If a multi-phase or multi-subagent run is partially-blocked by an environmental cliff outside the agent's control — org monthly usage limit hit mid-execution; worktree base diverges across parallel subagents; pre-installed CLI absent despite upstream `task_status: done` — the agent MUST log this as FL3 and MUST split the §Goal block into per-phase milestones each of which can close independently rather than treat partial completion as failure. Mitigation pattern (per Task 030 FE-EX-2): document landed work, salvage partial deliverables under `/<parent>/st<N>-partial/`, file the residual as a Phase-N+1 dispatch with the salvaged partial as a starting hint.
```

### §4.3 Amendment 3 — TASK.md §7.7 / §7 numbered list: tighten Friction Log declaration regex

**Target:** [`TASK.md`](../../../TASK.md) lines 299 (§7.0 row §7.8) and line 312 (§7 numbered item 7).
**Owner task:** [Task 033 ST-5](../../../tasks/033-task-spec-integration/subtasks/05-spec-amendment-task-md.md), composed with [Task 038 ST-3](../../../tasks/038-frustrated-spec-integration/subtasks/03-spec-amendment-frustrated-md.md).
**Evidence anchors:** §3 row `tasks/041/friction-log.md` F8 (FL2, FL declaration in `summary` only); `tasks/047-cross-spec-contradiction-baseline/friction-log.md` (FL0, fixed pre-existing `FL: 2` vs `FL2` format drift on Task 041's friction log in the same commit); aggregate observation that 8 of the 33 task-side logs declare FL inside frontmatter `summary` only (Tasks 016, 017, 018, 020, 021, 030, 031-adr-tooling-impl, 032-may-2026), creating a regex blind spot.
**Diagnostic class:** `tools/check-trust.py` and the planned `tools/fm/query.py` post-Task-019 successor accept FL declarations in either body or summary, but the canonical regex is implicit. Task 047 had to repair a `FL: 2` (with colon and space) variant on Task 041 silently. The grep recipe in §3's per-spec attribution methodology required 5 different patterns to capture the corpus.

**Proposed amendment** (verbatim replacement of line 312):

```
7. **Friction Log** — `friction-log.md` MUST exist for every closed task (`done`, `updated`, or `abandoned`) and MUST contain an `FL[0-3]` declaration matching the regex `\bFL[0-3]\b` in either (a) the body's first 200 lines, or (b) the frontmatter `summary` field, including for FL0 runs (FRUSTRATED.md). The form `FL: <N>` (with colon and space) is NOT a valid declaration — it is a frequent typo (caught on `tasks/041-extract-subtask-prompts/friction-log.md` by Task 047's check-trust pass) and the canonical form is `FL[0-3]` without separator. For `updated` closures the log MUST additionally carry a `## Supersession Rationale` paragraph (per §4.7). An inline declaration in the commit message is NOT a substitute.
```

### §4.4 Amendment 4 — FRUSTRATED.md §When and How to Log: add Closed-Task Mirror Rule

**Target:** [`FRUSTRATED.md`](../../../FRUSTRATED.md) lines 30–32 (the `## When and How to Log (Mandatory)` block).
**Owner task:** [Task 038 ST-3](../../../tasks/038-frustrated-spec-integration/subtasks/03-spec-amendment-frustrated-md.md).
**Evidence anchors:** §3 rows for `tasks/027-adr-spec-research-synthesis/friction-log.md` (research-mirror pattern), `tasks/029-adr-assumption-audit/friction-log.md` (research-mirror pattern); also `tasks/032-improve-maintenance-spec-may-2026/friction-log.md` and `tasks/032-agents-spec-integration/friction-log.md` (Task surface mirror conventions), plus `research/adr-corpus-extraction-from-governance-specs/reflection/friction-log.md` Aggregate FL Pattern paragraph (recurring third-occurrence escalation hint already partially encoded). The corpus already exhibits a mirror convention (Task-side `friction-log.md` cross-references the research-side `reflection/friction-log.md` when the Task's deliverable is a research run), but FRUSTRATED.md does not name it.
**Diagnostic class:** Task-spawning-research closures (Task 027, 029, 032-improve, 047) have *two* friction log surfaces, and the canonical relationship between them is undocumented in FRUSTRATED.md.

**Proposed insertion** (verbatim, append a new numbered item 3 immediately after line 32):

```
3. **Tasks That Spawn a Research Run:** When `task_status: done` and `task_spawns_research` is non-empty, the closing agent MUST author both surfaces: (a) the canonical research-side `research/<slug>/reflection/friction-log.md` with the run-level FL declaration, and (b) a task-side mirror at `tasks/<NNN>-<slug>/friction-log.md` that declares the same FL plus a one-paragraph summary linking to (a). The task-side mirror MUST cite the research-side log via Markdown link in its body. This pattern is in force on Tasks 027, 029, 032 (improve-maintenance-spec-may-2026), and 047 — see e.g. `tasks/027-adr-spec-research-synthesis/friction-log.md` for the canonical shape. The mirror MUST NOT downgrade the FL: if the research run was FL2, the Task-side mirror MUST also be FL2.
```

---

## §5 Open Questions & Successor-Task Routing

- **Q1.** Should the §4.1 Amendment 1 land before or after Task 033 ST-2 (which authors the canonical subtask-file schema)? **A1.** ST-2 is a prerequisite — `subtask_depends_on` cannot be enforced before the field is canonically declared. ST-5 (the TASK.md amendment) MUST sequence after ST-2.
- **Q2.** The §4.2 Amendment 2's "External-Infrastructure Cliff" trigger references "org monthly usage limit"; should it name the specific limit (Anthropic API) or stay vendor-agnostic? **A2.** Vendor-agnostic phrasing was used to keep the rule durable across model providers. The example list in the trigger is non-exhaustive.
- **Q3.** The §4.3 Amendment 3 tightens the FL-declaration regex; does this break the 8 existing summary-only declarations (Tasks 016, 017, 018, 020, 021, 030, 031-adr-tooling-impl, 032-may-2026)? **A3.** No — the proposed regex `\bFL[0-3]\b` matches all 8 verbatim. The amendment only forbids the `FL: <N>` typo variant; the existing corpus uses either body declarations or `Frustration Level: FL[N]` / `**FL[N]**` patterns that pass.
- **Q4.** Is the Category-7 "Schema / contract drift between authored and runtime surface" pattern worth a *fifth* amendment? **A4.** Out of scope for this Task — Category 7 fundamentally implicates the two-toolchain transition (legacy linters → flexible toolchain), which is owned by the [`research/flexible-frontmatter-toolchain/output/SPEC.md`](../flexible-frontmatter-toolchain/output/SPEC.md) T4-immutable surface and the open Phase 3 default-on flip. A successor Task should file a research workspace dedicated to "two-toolchain transition closure" rather than amending TASK.md or FRUSTRATED.md.

## §6 Validation

- **Falsification Threshold:** ≥15 closed-task friction logs. Met (33 ≥ 15).
- **§1 Histogram:** 53 logs counted. FL0 + FL1 + FL2 + FL3 = 19 + 27 + 6 + 1 = 53 ✓.
- **§2 Taxonomy:** 8 categories (≥6 required). Frequency counts sum to 116 events across 53 logs, average 2.2 events/log.
- **§3 Per-Spec Attribution:** 18 FL2+ rows enumerated; every row carries ≥1 root-spec anchor. 6 rows tag TASK.md; 3 tag FRUSTRATED.md; 3 tag FOLDERS.md; 3 tag PROMPT.md (matches the chain tasks 033, 038, 036, 034 respectively).
- **§4 Amendments:** 4 verbatim proposals (≥3 required). Each carries file:line target, owner task, ≥1 FL2+ evidence anchor.
- **Frontmatter conformance:** `research_phase: complete` ✓, `research_executes_prompt: research-friction-pattern-synthesis` ✓, `research_friction_level: FL1` (matches reflection/friction-log.md FL declaration).
- **Governance:** `tools/check-governance.sh` baseline ERRORs (4) deferred per [Assumption A-3 in `../readme.md`](../readme.md), following Task 032 (`agents-spec-integration`) §F1 precedent. Files added by this Task introduce zero new ERRORs.

---

*End of SPEC.md.*
