---
type: note
status: active
slug: 040-superclaude-spec-evaluation-friction-log
summary: "Mandatory closure friction log for Task 040 (TASK.md §7.7). Records FL[0-3] for the Gemini SuperClaude spec evaluation."
created: 2026-05-07
updated: 2026-05-07
---

# Task 040 Friction Log

**Highest Frustration Level: FL2**

## Summary

Task 040 evaluated a Gemini-authored "binding/IN-FORCE" SuperClaude orchestration spec against repo reality. The dual-lens (backend-architect + frontend-architect) review produced a converging verdict — 0 ACCEPT-AS-IS, 8 AMEND-AND-ACCEPT, 4 MERGE-INTO existing tasks, 1 REJECT — and a per-anchor remap table that folded all `SC.CMD.*` proposed anchors into existing host-spec namespaces.

## FL Declaration

The task closed without blockers; the recorded frictions are:

1. **FL2 — External spec self-asserts binding status (RESEARCH.md §6.5 violation).** The Gemini source ships with `status: in-force` framing as if pre-evaluated. Per `RESEARCH.md §6.5` external research is raw material until a downstream Task evaluates it. ≈ 20 min was spent producing the §A classification matrix specifically to refute the self-binding claim per aspect, when the right move was to override the frontmatter at ingestion. Future ingestion of external specs MUST strip the `in-force` claim at the scaffold step (Task 040 added this as a §D process note).

2. **FL2 — MCP-server citations as load-bearing without integration.** Eight MCP servers (Tavily, Playwright, Morphllm, Chrome DevTools, Magic, Sequential, Context7, Serena) were cited as load-bearing. Zero are configured in this repo. The §C reality-check matrix took ≈ 30 min to produce mostly because each server required a "hallucinated vs aspirational vs ambient" classification. A repo-side allowlist (which MCP servers may be cited in normative spec amendments) would have made this triage mechanical.

3. **FL1 — Anchor-namespace proliferation pressure.** The spec proposes `SC.CMD.<aspect>.<n>` as a 10th top-level Gherkin namespace alongside the existing nine (`ADR.A.*` / `T.B.*` / `P.B.*` / `R.B.*` / `F.B.*` / `PC.B.*` / `FR.B.*` / `M.B.*` / `AG.*`). Choosing option (ii) — fold into host-spec namespaces — required producing the per-anchor remap table (§B) by hand. ≈ 10 min cost. Future external specs proposing new anchor schemes SHOULD be pre-screened against the host-namespace catalog before classification.

4. **FL1 — Skill-name drift (`sc-document` vs `sc:document`; `confidence-check` non-existent).** The frontend-architect lens caught these conflations (synthesis §F.note). ≈ 5 min cost; mitigated by the dual-lens approach itself.

5. **FL0 — Phase-5 maintainer hand-off.** Three of the five MERGE patches landed in commit 9e3b59f (synthesis records: Tasks 033/038/039). The remaining two (§3.1 → Task 034, §6 → Task 037) landed in this closure commit as cross-reference notes in the existing `/prompts/<slug>/brief.md` files for the host subtasks. No friction; the audit-graph edges (`task_uses_prompts ↔ prompt_relates_to_task`) were already in place from Task 041.

None of the above blocked closure.

## Outcome

- §A classification matrix, §B anchor remap table, and §C MCP reality-check matrix are filed in [`synthesis.md`](./synthesis.md).
- All 5 MERGE patches have landed (3 in commit 9e3b59f against Tasks 033/038/039; 2 in this closure commit against the briefs for Tasks 034 ST-4 and 037 ST-4).
- `tools/check-governance.sh` exits with the same diagnostic set as before this commit (the surviving ERRORs — `tasks/046-...` missing `## Todo`, `tasks/readme.md` missing 045/046 bullets, `tasks/031-...` friction-log missing FL[0-3], optional `jsonschema` import — are pre-existing and out of scope for Task 040).
- Tasks 032–039 carry the salvaged Gemini-spec content as host-spec amendments; the source folder at `research/gemini/superclaude-agency-orchestration-spec/` remains as the cited artefact, no longer mistakable for binding repo governance.
