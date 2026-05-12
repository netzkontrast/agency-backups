---
type: note
status: active
slug: sc-business-panel-sub-modes
summary: "Extracted three-sub-mode playbook (discussion/debate/socratic) + expert-selection algorithm + document-type mappings + synthesis templates for /sc:business-panel. Sourced from upstream modes/MODE_Business_Panel.md @ 22ad3f48; abridged per ADR-0011 D.6 (MCP refs trimmed)."
created: 2026-05-12
updated: 2026-05-12
---

# Business Panel — Sub-Mode Playbook

Extracted from `SuperClaude-Org/SuperClaude_Framework/src/superclaude/modes/MODE_Business_Panel.md @ 22ad3f48` per ADR-0011 D.6. The full upstream mode (11.8 KB, MCP-bound) is **not bundled standalone** (skipped per Task-092 row-41 triage); this distillation keeps only the parts the host skill operates on, MCP references stripped.

## Sub-mode 1: DISCUSSION (default — collaborative)

**When**: strategic plans, market analysis, research reports, low-controversy syntheses.

**Process**:
1. **Ingest** the document.
2. **Auto-select 3–5 experts** via the domain mapping (below).
3. Each expert applies their unique framework lens.
4. **Cross-pollination**: experts reference + build on each other's points.
5. Identify convergent themes and complementary perspectives.

**Output template**:
```
**[EXPERT]**: *Framework-specific analysis in authentic voice*
**[EXPERT] building on [OTHER]**: *Complementary insights connecting frameworks*
```

## Sub-mode 2: DEBATE (adversarial)

**When**: controversial decisions, competing strategies, risk assessments, high-stakes calls. Triggers: explicit user request, conflicting expert positions, "risk" / "trade-off" / "challenge" cues.

**Process**:
1. Identify points of expert disagreement.
2. Each expert articulates + defends their position with framework evidence.
3. Structured rebuttal: respectful challenge with alternative interpretations.
4. Synthesis through tension — extract insights from productive disagreement.

**Output template**:
```
**[EXPERT] challenges [OTHER]**: *Respectful disagreement with evidence*
**[OTHER] responds**: *Defense or concession with supporting logic*
**MEADOWS on system dynamics**: *How the conflict reveals system structure*
```

## Sub-mode 3: SOCRATIC INQUIRY (question-driven)

**When**: learning requests, capability-building, strategic education, complex problems where the user wants to develop their own thinking.

**Process**:
1. Each expert formulates probing questions from their framework.
2. Cluster questions by strategic theme.
3. Present to user; await reflection / response.
4. Follow-up inquiry: experts respond to user answers with deeper questions.
5. Extract strategic-thinking patterns and meta-learning.

**Output template**:
```
**Panel Questions for You:**
- **CHRISTENSEN**: "Before concluding innovation, what job is it hired to do?"
- **PORTER**: "If successful, what prevents competitive copying?"
*[User responds]*
**Follow-up Questions**: …
```

## Adaptive Mode Selection (content cues)

| Cue keywords | Suggested mode |
|---|---|
| strategy, plan, analysis, market, business model | **discussion** (default) |
| controversial, risk, decision, trade-off, challenge | **debate** |
| learn, understand, develop, capability, "how", "why" | **socratic** |

## Domain → Expert Mapping

| Domain | Primary experts | Secondary experts |
|---|---|---|
| innovation | christensen, drucker | meadows, collins |
| strategy | porter, kim_mauborgne | collins, taleb |
| marketing | godin, christensen | doumont, porter |
| risk | taleb, meadows | porter, collins |
| systems | meadows, drucker | collins, taleb |
| communication | doumont, godin | drucker, meadows |
| organizational | collins, drucker | meadows, porter |

## Document-Type Recognition Presets

| Document type | Default panel | Default mode | Focus |
|---|---|---|---|
| strategic plan | porter, kim_mauborgne, collins, meadows | discussion | competitive positioning + execution |
| market analysis | porter, christensen, godin, taleb | discussion | market dynamics + opportunities |
| business model | christensen, drucker, kim_mauborgne, meadows | discussion | value creation + capture |
| risk assessment | taleb, meadows, porter, collins | debate | uncertainty + resilience |
| innovation strategy | christensen, drucker, godin, meadows | discussion | systematic innovation |
| organizational change | collins, meadows, drucker, doumont | socratic | change management + communication |

## Expert-Selection Algorithm (5 steps)

1. **Content classification**: identify primary business domains in the document.
2. **Relevance scoring**: score each expert's framework against the content.
3. **Diversity optimisation**: ensure complementary perspectives across the selected set.
4. **Interaction dynamics**: prefer experts with productive interaction patterns.
5. **Final validation**: confirm the selected panel covers all key aspects of the document.

## Synthesis Framework (six output dimensions)

| Dimension | Definition | Symbol |
|---|---|---|
| Convergent insights | Areas where multiple experts agree, supported by multiple frameworks | ✅ |
| Productive tensions | Disagreements that reveal important strategic trade-offs | ⚖️ |
| System patterns | Structural themes identified by systems thinking (Meadows-led) | 🔄 |
| Communication clarity | Actionable takeaways with clear structure (Doumont-led) | 💬 |
| Blind spots | What no single framework captured adequately; gaps to mitigate | ⚠️ |
| Strategic questions | Next exploration priorities; framework-specific follow-ups | 🤔 |

## Quality Standards

- **Framework authenticity**: each expert maintains true-to-source methodology and voice.
- **Cross-framework integrity**: synthesis preserves distinctiveness while creating integration.
- **Evidence requirements**: all conclusions supported by framework logic.
- **Strategic actionability**: analysis produces implementable insights.

The full upstream mode (with persona-coordination + wave-mode + MCP integration sections) remains available verbatim at `tasks/091-port-external-skill-corpora/references/upstream-snapshot/superclaude_framework/src/superclaude/modes/MODE_Business_Panel.md`.
