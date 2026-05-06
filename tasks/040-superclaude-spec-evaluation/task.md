---
type: task
status: active
slug: superclaude-spec-evaluation
summary: "Evaluate the Gemini-authored 'SuperClaude Orchestration & Meta-Governance Specification' (research/gemini/superclaude-agency-orchestration-spec/) against repo reality, decide binding status (accept-as-is / amend / merge-into-tasks-032-039 / reject), and integrate accepted portions as concrete amendments to the existing 8-task chain."
created: 2026-05-06
updated: 2026-05-06
task_id: "040"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_affects_paths:
  - tasks/032-agents-spec-integration/
  - tasks/033-task-spec-integration/
  - tasks/034-prompt-spec-integration/
  - tasks/035-research-spec-integration/
  - tasks/036-folders-spec-integration/
  - tasks/037-pre-commit-spec-integration/
  - tasks/038-frustrated-spec-integration/
  - tasks/039-maintenance-spec-integration/
  - research/gemini/superclaude-agency-orchestration-spec/
---

# Task 040 — Evaluate the SuperClaude Orchestration Spec (Gemini)

## Goal

Decide what (if anything) from the Gemini-authored "SuperClaude Orchestration & Meta-Governance Specification" — at `research/gemini/superclaude-agency-orchestration-spec/` — should be lifted into binding repo governance, and if so, where. The Task is **done** when (a) every §1–§8 aspect of the Gemini spec has been classified into one of {ACCEPT-AS-IS, AMEND-AND-ACCEPT, MERGE-INTO-EXISTING-TASK-032-039, REJECT-AS-MISALIGNED}, with rationale, (b) every ACCEPT/AMEND/MERGE classification has produced a concrete diff against either an existing task in the 032–039 chain *or* a new spec amendment, (c) the `SC.CMD.<aspect>.<statement>` Gherkin anchor scheme is reconciled with the existing `ADR.A.*` (Task 031) and the new `T.B.*` / `P.B.*` / `R.B.*` / `F.B.*` / `PC.B.*` / `FR.B.*` / `M.B.*` schemes (Tasks 032–039), and (d) `tools/check-governance.sh` exits 0 on the resulting tree.

## Context

Gemini-authored spec ingested 2026-05-06. The doc self-asserts "binding, IN-FORCE governance"; per `RESEARCH.md §6.5` external results are raw material until a Task evaluates them. This Task is that evaluation.

### Critical-eye observations from ingestion

These are the maintainer's pre-evaluation flags; the Task's job is to confirm or disprove them:

1. **Workspace↔command mapping is asserted, not derived.** The §0 table maps `AGENTS.md → /sc:pm`, `TASK.md → /sc:spawn+/sc:task`, etc. as if this were a discovery; it is a *proposal*. Whether each mapping holds against repo reality is an open question per command.
2. **MCP servers cited but not integrated.** Tavily, Playwright, Morphllm, Chrome DevTools are referenced as load-bearing. None are configured in this repo today. Either (a) the spec describes a *target state* requiring tooling work, or (b) the citations are aspirational and should be stripped.
3. **Skill-name drift.** The doc cites `sc-document` (hyphen) and `confidence-check`. The repo's actual skill list uses `sc:document` and has no `confidence-check` skill. Wording must be reconciled, or the missing skill must be authored.
4. **Self-overlap with Task 031 ADR governance.** §0.1 mandates a `SC.CMD.<aspect>.<statement>` Gherkin scheme that parallels — and might compete with — the live `ADR.A.<aspect>.<statement>` scheme from Task 031. Tasks 032–039 introduced sibling schemes (`T.B.*`, `P.B.*`, etc.). Whether SC.CMD becomes a fifth namespace or merges with the existing schemes is the highest-leverage decision.
5. **FL0–FL3 alignment exists already.** The spec's friction-level claim *does* match `FRUSTRATED.md`'s existing FL0-FL3, so there is no contradiction here; but the §7.1 `ReflexionPattern` is a fresh concept worth evaluating against the existing friction-aggregation pipeline.
6. **The 30 /sc: commands claim is roughly accurate but not exhaustive.** Repo skill list shows ~38 `sc:*` skills; some Gemini-cited commands (e.g., `/sc:pm` as a *background* layer) describe behavior the local skill `sc:pm` does not actually exhibit.
7. **Architectural overlap with Tasks 032–039.** Several §-level claims map onto in-flight tasks: §1.1 ↔ Task 032 (AGENTS.md), §2 ↔ Task 033 (TASK.md), §3 ↔ Task 034/035 (PROMPT.md / RESEARCH.md), §6 ↔ Task 037 (PRE_COMMIT.md), §7 ↔ Task 038 (FRUSTRATED.md), §8 ↔ Task 039 (MAINTENANCE.md). Per-aspect MERGE decisions should refer to the corresponding 032–039 task as the integration target.

## Plan

1. **Phase 1 — Parallel architect-review.** Dispatch two architect agents in parallel (already done in this commit; see `evaluation-notes.md`):
   - **backend-architect** — critique the orchestration / DAG / MCP-server-boundary claims; identify which §-level normatives are operationally sound vs. aspirational.
   - **frontend-architect** — critique the agent-UX / operator-CLI / persona-handoff claims; identify how the spec affects developer-facing command surface and human-in-the-loop touchpoints.
2. **Phase 2 — Per-aspect classification.** For each §1–§8 in the Gemini spec, assign one of {ACCEPT-AS-IS, AMEND-AND-ACCEPT, MERGE-INTO-EXISTING-TASK-NNN, REJECT}. Output: `evaluation-notes.md` §A (classification matrix).
3. **Phase 3 — Anchor-scheme reconciliation.** Decide whether `SC.CMD.<aspect>.<statement>` is (i) adopted as a fifth Gherkin anchor namespace alongside `ADR.A.*` / `T.B.*` / `P.B.*` / `R.B.*` / `F.B.*` / `PC.B.*` / `FR.B.*` / `M.B.*`, or (ii) folded into the existing schemes per host-spec. Output: `evaluation-notes.md` §B.
4. **Phase 4 — MCP server reality-check.** Determine for each cited MCP server (Serena, Sequential, Context7, Tavily, Playwright, Magic, MorphLLM, Chrome DevTools) whether (i) it is currently integrated, (ii) integration is planned/desirable, or (iii) the citation is aspirational and should be dropped. Output: `evaluation-notes.md` §C.
5. **Phase 5 — Concrete diffs per accepted aspect.** For every ACCEPT/AMEND/MERGE row in §A, produce the actual edit (either a patch against an existing task in 032–039, or a new amendment file). Output: per-task patches.
6. **Phase 6 — Sync indexes + governance check.** Update `tasks/readme.md`, `research/readme.md` (already done at scaffold time), run `tools/check-governance.sh`, fix any ERRORs.

## Sample Gherkin (shape the maintainer authoring §B reconciliation should produce)

```gherkin
# anchor: SC.CMD.040.A.1 — anchor-scheme reconciliation contract
Scenario: A new SC.CMD.* scenario lands without colliding with existing schemes
  Given the Gemini spec proposes scenario `SC.CMD.5.A.1` (security audit)
  And the repo already owns scenarios under `ADR.A.*`, `T.B.*`, `P.B.*`,
        `R.B.*`, `F.B.*`, `PC.B.*`, `FR.B.*`, `M.B.*`
  When the maintainer evaluates the proposed anchor
  Then either (i) `SC.CMD.*` is adopted as a fifth top-level Gherkin namespace
        documented in `maintenance/language-spec.md`,
       or (ii) the scenario is re-anchored under the host-spec namespace
        (e.g., `PC.B.SECAUDIT.1` if it lands in PRE_COMMIT.md)
  And the chosen path MUST be applied uniformly to all SC.CMD.* anchors;
        no mixed-mode adoption.
```

## Preconditions (satisfied at branch-time)

- **Task 027/028/029/031** — ADR machinery is the existence-proof for `<scheme>.<aspect>.<statement>` Gherkin anchoring; §B reconciliation in this Task uses ADR.A.* as the precedent.
- **Tasks 032–039** — the existing 8-task spec-integration chain that this Task may fold accepted Gemini content into.

## Build-On

- **`tools/adr/cli.py validate`** — anchor-scheme validator pattern; if SC.CMD.* is adopted, this Task's §B output specifies how `tools/adr/cli.py validate` (or a sibling) extends to recognize it.
- **`research/adr-spec-research-synthesis/output/SPEC.md`** — precedent for "evaluate Gemini external research, produce repo-native spec" (Task 027 did this for the ADR Gemini run).
- **`research/adr-assumption-audit/output/REPORT.md`** — precedent for the multi-method critical audit pattern (M06/M07/M13) that Phase 1 architect-review parallels.

## Todo

- [ ] 1. Phase 1 — read backend-architect + frontend-architect findings (filed under `evaluation-notes.md` at session-end).
- [ ] 2. Phase 2 — produce §A classification matrix (per Gemini-spec §, one row).
- [ ] 3. Phase 3 — produce §B anchor-scheme reconciliation decision.
- [ ] 4. Phase 4 — produce §C MCP-server reality-check matrix.
- [ ] 5. Phase 5 — author concrete patches against accepted-aspect host tasks.
- [ ] 6. Phase 6 — run `tools/check-governance.sh`; fix ERRORs.
- [ ] 7. Update `tasks/readme.md` + `research/readme.md` for status transitions.
- [ ] 8. Author `friction-log.md` with FL[0-3].
- [ ] 9. Set `task_status: done`.

## Links

- Folder index: [`readme.md`](./readme.md)
- Source research: [`research/gemini/superclaude-agency-orchestration-spec/`](../../research/gemini/superclaude-agency-orchestration-spec/)
- Sibling chain (potential MERGE targets): [Tasks 032–039](../032-agents-spec-integration/task.md)
- Precedent: [Task 027 — adr-spec-research-synthesis](../027-adr-spec-research-synthesis/task.md) (the same shape — Gemini external research → repo-native spec).
- Governing specs: [`RESEARCH.md`](../../RESEARCH.md) §6, [`MAINTENANCE.md`](../../MAINTENANCE.md), [`README.md`](../../README.md) §11.3
