---
name: sc-business-panel
description: >-
  Multi-expert business analysis with adaptive interaction modes (discussion, debate, Socratic). Use when the user invokes /sc:business-panel or asks for strategic analysis of a document through multiple business-thought-leader frameworks.
skill_kind: analysis
skill_target_agents: [claude-code]
skill_references_skills: [sc-spec-panel]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-business-panel — `/sc:business-panel` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:business-panel` command from SuperClaude_Framework. Simulates a panel discussion among nine business thought leaders (Christensen, Porter, Drucker, Godin, Kim & Mauborgne, Collins, Taleb, Meadows, Doumont) analyzing a document through their distinct frameworks. Adapted per ADR-0011 D.6/D.8: `sequential` + `context7` MCP bindings stripped; the 9-expert profile catalog and the three-sub-mode (discussion / debate / Socratic) playbooks are extracted into companion reference files to keep this SKILL.md ≤ 5 KB.

## When to use

Invoke when the user runs `/sc:business-panel [document]`, or asks for multi-perspective strategic analysis through named business frameworks (disruption, Five Forces, antifragility, systems thinking, Blue Ocean, etc.). **Synthesis-only** — does not implement recommendations.

## How to use

1. **Ingest**: `Read` the target document (PRD, strategic plan, market brief, etc.).
2. **Mode-select**: pick a sub-mode — *discussion* (default, collaborative), *debate* (adversarial), *socratic* (question-driven), or *adaptive* (auto-pick from content cues). Heuristics in [`references/sub-modes.md`](./references/sub-modes.md).
3. **Expert-select**: by default auto-pick 3–5 experts via the domain→expert mapping in [`references/sub-modes.md`](./references/sub-modes.md); honour `--experts "name1,name2,…"` or `--all-experts` if the user supplies them.
4. **Analyze**: walk the selected experts, each in their authentic voice and framework. Profiles + key questions in [`references/expert-profiles.md`](./references/expert-profiles.md).
5. **Synthesize**: extract convergent insights, productive tensions, system patterns, communication clarity, blind spots, strategic questions (templates in `references/sub-modes.md`).
6. **Output**: deliver a Markdown analysis document — expert perspectives, consensus, disagreements with reasoning, priority-ranked recommendations. STOP at the document — do NOT implement recommendations.

## Adaptations from upstream

- Stripped `sequential` and `context7` MCP bindings; reasoning is native Markdown synthesis and `Read` over the target document. `WebFetch` is OPTIONAL for external framework lookups.
- Extracted the 9-expert profile catalog from upstream `agents/business-panel-experts.md` into [`references/expert-profiles.md`](./references/expert-profiles.md) (one profile per expert; ~250 LOC).
- Extracted the three-sub-mode playbook + expert-selection algorithm + document-type mappings from upstream `modes/MODE_Business_Panel.md` into [`references/sub-modes.md`](./references/sub-modes.md). The mode itself is NOT bundled standalone (skipped per Task-092 row-41 triage — D.6 + content-overlap with the command body).
- The upstream `agents/business-panel-experts.md` is NOT registered as a standalone Agency skill (skipped per row-34 triage); its content is consolidated here.
- Preserved the upstream **SYNTHESIS OUTPUT ONLY** boundary verbatim in intent: no implementation, no architectural changes.

## References

- Upstream command: [`src/superclaude/commands/business-panel.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/business-panel.md) — verbatim mirror at [`references/upstream-sc-business-panel.md`](./references/upstream-sc-business-panel.md) (ADR-0011 D.3).
- Extracted expert catalog: [`references/expert-profiles.md`](./references/expert-profiles.md) (sourced from upstream `agents/business-panel-experts.md@22ad3f4`).
- Extracted sub-mode playbooks: [`references/sub-modes.md`](./references/sub-modes.md) (sourced from upstream `modes/MODE_Business_Panel.md@22ad3f4`).
- Sibling skill: [`skills/sc-spec-panel/SKILL.md`](../sc-spec-panel/SKILL.md) — shares the multi-expert panel pattern.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- MCP servers used: **none required**. Each upstream MCP is OPTIONAL:
  - **Sequential** — OPTIONAL; fallback: native Markdown reasoning across the 9 expert frameworks.
  - **Context7** — OPTIONAL; fallback: `WebFetch` on authorised external-docs URLs and `Read` on local references.
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0`. Re-syncs require a new Task per ADR-0011 D.9.
