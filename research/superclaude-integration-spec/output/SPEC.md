---
type: research
status: completed
slug: superclaude-integration-spec
summary: "Governance spec mapping SuperClaude v4.3.0 commands, agents, and skills to Agency workflow phases; defines integration patterns, SC Integration Block template, and maintenance scan protocol."
created: 2026-05-04
updated: 2026-05-04
research_phase: complete
research_executes_prompt: superclaude-integration-spec
research_friction_level: FL1
---

# SuperClaude Integration Specification

**SuperClaude Framework v4.3.0 × Agency Governance**

> This spec is the authoritative source for integrating SuperClaude capabilities into Agency workflows. Future specs and maintenance runs MUST reference this document per §4 and §5.

---

## 1. Catalog

### 1.1 Slash Commands (`/sc:*`)

Installed at `~/.claude/commands/sc/`. Invoked by typing the command in a Claude Code session.

| Command | Category | One-Line Purpose |
|---------|----------|------------------|
| `/sc:research` | workflow | Deep web research with adaptive planning and multi-hop search |
| `/sc:implement` | workflow | Feature/code implementation with multi-persona coordination |
| `/sc:analyze` | utility | Multi-domain analysis: quality, security, performance, architecture |
| `/sc:spawn` | special | Decompose complex tasks into coordinated Epic → Story → Task hierarchies |
| `/sc:pm` | orchestration | Project Manager: orchestrates all sub-agents and manages workflows |
| `/sc:design` | planning | System architecture, API, and component interface design |
| `/sc:workflow` | planning | Generate structured implementation workflows from PRDs |
| `/sc:task` | execution | Execute complex tasks with intelligent workflow management |
| `/sc:agent` | delegation | Spawn and coordinate domain-specialist sub-agents |
| `/sc:spec-panel` | review | Multi-expert spec review using renowned engineering experts |
| `/sc:brainstorm` | discovery | Interactive requirements discovery via Socratic dialogue |
| `/sc:reflect` | quality | Task reflection and validation using Serena MCP analysis |
| `/sc:improve` | quality | Systematic code/spec quality improvements |
| `/sc:cleanup` | quality | Remove dead code, optimize project structure |
| `/sc:test` | quality | Execute tests with coverage analysis and quality reporting |
| `/sc:build` | execution | Build, compile, and package with intelligent error handling |
| `/sc:git` | vcs | Git operations with intelligent commit messages |
| `/sc:document` | docs | Generate focused documentation for components, APIs, features |
| `/sc:index` | docs | Generate comprehensive project documentation and knowledge base |
| `/sc:index-repo` | docs | Repository indexing (94% token reduction: 58K → 3K tokens) |
| `/sc:explain` | learning | Clear explanations of code, concepts, and system behavior |
| `/sc:estimate` | planning | Development estimates for tasks, features, or projects |
| `/sc:troubleshoot` | debugging | Diagnose and resolve issues in code, builds, deployments |
| `/sc:business-panel` | analysis | Multi-expert business strategy analysis |
| `/sc:select-tool` | utility | Intelligent MCP tool selection based on complexity scoring |
| `/sc:recommend` | utility | Recommend the most suitable SuperClaude commands for any input |
| `/sc:load` | session | Load session context via Serena MCP |
| `/sc:save` | session | Save session context via Serena MCP |
| `/sc:sc` | meta | SuperClaude command dispatcher |
| `/sc:help` | meta | List all available /sc commands and their functionality |

### 1.2 Agents

Installed at `~/.claude/agents/`. Invoked via the `Agent` tool with `subagent_type` parameter.

| Agent (`subagent_type`) | Domain | One-Line Purpose |
|------------------------|--------|------------------|
| `deep-research` | research | Adaptive research specialist for external knowledge gathering |
| `deep-research-agent` | research | Comprehensive research with adaptive strategies and intelligent exploration |
| `system-architect` | architecture | Scalable system design focused on maintainability and long-term decisions |
| `backend-architect` | architecture | Reliable backend systems: data integrity, security, fault tolerance |
| `frontend-architect` | UI/UX | Accessible, performant interfaces with modern frameworks |
| `devops-architect` | infrastructure | Infrastructure automation and deployment reliability |
| `pm-agent` | orchestration | Self-improvement workflow executor; documents implementations and maintains knowledge |
| `requirements-analyst` | analysis | Transform ambiguous ideas into concrete specifications via systematic discovery |
| `root-cause-analyst` | debugging | Systematic root-cause investigation through evidence-based analysis |
| `security-engineer` | security | Vulnerability identification and security compliance |
| `quality-engineer` | testing | Comprehensive testing strategies and systematic edge-case detection |
| `performance-engineer` | optimization | Measurement-driven performance analysis and bottleneck elimination |
| `python-expert` | coding | Production-ready Python: SOLID principles and modern best practices |
| `refactoring-expert` | coding | Systematic refactoring and technical debt reduction |
| `technical-writer` | docs | Clear, comprehensive technical documentation for specific audiences |
| `learning-guide` | education | Progressive learning through practical examples |
| `socratic-mentor` | education | Socratic method for programming knowledge discovery |
| `self-review` | quality | Post-implementation validation and reflexion partner |
| `business-panel-experts` | strategy | Multi-expert business strategy panel (Christensen, Porter, Drucker, et al.) |
| `repo-index` | docs | Repository indexing and codebase briefing assistant |

### 1.3 Skills

| Skill | Available As | Trigger | One-Line Purpose |
|-------|-------------|---------|------------------|
| `confidence-check` | System skill (Skill tool) | Pre-implementation | Assess confidence ≥90% before starting; 25-250x token-saving ROI |
| `session-start-hook` | File-based (`~/.claude/skills/`) | Session start | Initialize repository context for Claude Code on the web |

---

## 2. Phase Mapping

Each row maps an Agency workflow phase to the most relevant SuperClaude tools.

| Agency Phase | Spec Reference | Primary SC Commands | Primary SC Agents | SC Skills |
|-------------|---------------|--------------------|--------------------|----------|
| **Prompt Authoring** | PROMPT.md §4 | `/sc:brainstorm`, `/sc:design` | `requirements-analyst`, `technical-writer` | `confidence-check` |
| **Research: Kickoff** | RESEARCH.md §4.1–4.2 | `/sc:load`, `/sc:recommend` | `pm-agent` | `confidence-check`, `session-start-hook` |
| **Research: Execution** | RESEARCH.md §4.4 | `/sc:research` | `deep-research-agent`, `deep-research` | — |
| **Research: Synthesis** | RESEARCH.md §4.6 | `/sc:analyze`, `/sc:reflect` | `self-review`, `system-architect` | — |
| **Research: Reflection** | RESEARCH.md §4.7 | `/sc:reflect`, `/sc:spec-panel` | `root-cause-analyst`, `self-review` | — |
| **Research: Output** | RESEARCH.md §4.8 | `/sc:document`, `/sc:spec-panel` | `technical-writer` | — |
| **Task: Orchestration** | TASK.md §4.1–4.3 | `/sc:spawn`, `/sc:pm`, `/sc:workflow` | `pm-agent`, `system-architect` | `confidence-check` |
| **Task: Execution** | TASK.md §4.4 | `/sc:implement`, `/sc:build`, `/sc:test` | `backend-architect`, `python-expert`, `quality-engineer` | — |
| **Task: Closure** | TASK.md §4.6 | `/sc:git`, `/sc:reflect` | `self-review` | — |
| **Maintenance Run** | MAINTENANCE.md §1–5 | `/sc:index-repo`, `/sc:analyze` | `repo-index`, `root-cause-analyst` | `session-start-hook` |

---

## 3. Integration Patterns

### 3.1 Pattern: Confidence Gate (All Phases)

Before starting any research run, implementation task, or maintenance action, an agent MUST invoke the `confidence-check` skill.

```
# Via Skill tool in Claude Code session:
/confidence-check

# In prompt.md body, declare:
# "Before executing step 1, invoke the confidence-check skill.
#  Proceed only if confidence ≥90%."  (per PROMPT.md §5.1)
```

**When to use**: At the start of every session. Especially before RESEARCH.md §4.1 (Resolve the Prompt).
**ROI**: Spending 100–200 tokens on a confidence check saves 5,000–50,000 tokens on wrong-direction work (KNOWLEDGE.md).

---

### 3.2 Pattern: Deep Research Execution

When RESEARCH.md §4.4 (Work in Workspace) calls for multi-hop web exploration, an agent MUST prefer `/sc:research` over ad-hoc `WebSearch` calls.

```
/sc:research "[research question from /prompts/<slug>/prompt.md §Instructions]" --depth deep --strategy unified
```

**Integration point**: The invocation and its output path MUST be recorded in `/research/<slug>/workspace/session.log`.

**Agent variant** (for multi-session exploration):
```python
Agent(
    subagent_type="deep-research-agent",
    prompt="Execute the research query from /prompts/<slug>/prompt.md §Instructions. "
           "Save all findings to /research/<slug>/workspace/. "
           "Log chronological tool trace to session.log."
)
```

---

### 3.3 Pattern: Synthesis Analysis

During RESEARCH.md §4.6 (Synthesize Structurally), an agent SHOULD use `/sc:analyze` to detect contradictions, quality gaps, or missing coverage in collected workspace evidence.

```
/sc:analyze /research/<slug>/workspace/ --focus quality --depth deep
```

The analysis output SHOULD be saved to `/research/<slug>/synthesis/post-synthesis-log.md`.

---

### 3.4 Pattern: Spec Panel Review

Before closing a research run, an agent SHOULD invoke `/sc:spec-panel` on `output/SPEC.md` for multi-expert review. This catches structural weaknesses before commit.

```
/sc:spec-panel
# Target: /research/<slug>/output/SPEC.md
```

The panel's findings SHOULD be recorded as an appended section in `/research/<slug>/reflection/friction-log.md`.

---

### 3.5 Pattern: Task Decomposition

When TASK.md §4.2 (Plan) identifies a task spanning 3+ domains or 5+ steps, an agent MUST use `/sc:spawn` to generate the task hierarchy before writing `task.md`.

```
/sc:spawn "[task goal]" --strategy adaptive --depth deep
```

The spawn output's Epic decomposition MUST be copied into `task.md`'s `## Plan` section (verbatim or summarized with attribution).

---

### 3.6 Pattern: Session Continuity for Long Research

For research runs spanning multiple Claude Code sessions, an agent MUST use `/sc:save` at session end and `/sc:load` at session start.

```
# End of session:
/sc:save

# Start of next session:
/sc:load
# Resume at last checked step in /research/<slug>/synthesis/state.md
```

Save/load events SHOULD be recorded in `session.log` with timestamps.

---

### 3.7 Pattern: Maintenance Indexing

At the start of every Maintenance Run (MAINTENANCE.md §5.1), an agent MUST execute:

```
/sc:index-repo
```

After indexing, the agent SHOULD run:

```
/sc:analyze --focus architecture
```

The analysis SHOULD inform which `readme.md` files need updates (MAINTENANCE.md §2).

---

### 3.8 Pattern: Technical Writer for Output

When generating `output/SPEC.md` or `output/REPORT.md`, an agent SHOULD spawn the `technical-writer` agent to enforce clarity, structure, and audience calibration.

```python
Agent(
    subagent_type="technical-writer",
    prompt="Draft the final SPEC.md for research slug '<slug>'. "
           "Target audience: future Claude Code agents. "
           "Required sections: per RESEARCH.md §2. "
           "Input material: /research/<slug>/synthesis/. "
           "Output to: /research/<slug>/output/SPEC.md."
)
```

---

### 3.9 Pattern: Prompt Authoring via Brainstorm

When a new research need is identified (during Maintenance or task execution), an agent SHOULD use `/sc:brainstorm` before writing `prompt.md`.

```
/sc:brainstorm
# Answer Socratic questions to refine:
# - What specific question should the prompt execute?
# - What framework fits? (RISEN / RISE-DX / ReAct / RISEN+ReAct / CoT)
# - What deliverable format is required?
```

The brainstorm output forms the content of `/prompts/<slug>/brief.md`.

---

## 4. New Spec Template — SuperClaude Integration Block

Every spec added to this repository after 2026-05-04 MUST include a **SuperClaude Integration Block**. This block MUST appear immediately before `## Anti-Patterns` (or at the end if no such section exists).

### 4.1 Mandatory Block Format

```markdown
## SC Integration

> *This section is governed by
> [SuperClaude Integration Spec](../../research/superclaude-integration-spec/output/SPEC.md).*

### Recommended SC Tools for This Spec's Domain

| Phase | SC Command | SC Agent | Notes |
|-------|-----------|---------|-------|
| [Phase name] | `/sc:[command]` | `[agent-name]` | [Why this tool fits this phase] |

### Invocation Pattern

```
[Concrete example invocation for the primary use case of this spec]
```

### Confidence Gate

Agents MUST invoke `confidence-check` before executing any step marked `MUST` in this spec.
```

### 4.2 Minimum Content Requirements

A SuperClaude Integration Block MUST contain:
1. A back-link to `/research/superclaude-integration-spec/output/SPEC.md` (relative path).
2. At least one row in the SC Tools table.
3. At least one concrete invocation example.
4. The confidence gate reminder.

A SuperClaude Integration Block SHOULD include:
- Session continuity notes if the spec governs multi-session workflows.
- Agent spawning examples if the spec involves delegation.

### 4.3 Minimal Block for Simple Specs

For specs governing a narrow domain (e.g., a tool instruction prompt), the block MAY be condensed:

```markdown
## SC Integration

> See [SuperClaude Integration Spec](../../research/superclaude-integration-spec/output/SPEC.md).

Use `/sc:[most relevant command]` for [primary use case]. Invoke `confidence-check` before starting.
```

### 4.4 Path Convention for Back-Links

The relative path to this SPEC.md depends on the nesting level of the referencing file:

| File Location | Back-Link Path |
|--------------|---------------|
| Root spec (e.g., `RESEARCH.md`) | `./research/superclaude-integration-spec/output/SPEC.md` |
| Research output (e.g., `/research/<slug>/output/SPEC.md`) | `../../superclaude-integration-spec/output/SPEC.md` |
| Task file (e.g., `/tasks/<NNN>-<slug>/task.md`) | `../../research/superclaude-integration-spec/output/SPEC.md` |
| Prompt file (e.g., `/prompts/<slug>/prompt.md`) | `../../research/superclaude-integration-spec/output/SPEC.md` |

---

## 5. Root Spec Link Recommendations

The following root governance specs SHOULD be updated to cross-link to this spec. The table provides the exact callout text and suggested placement.

| Root Spec | Placement | Exact Text to Add |
|-----------|-----------|------------------|
| `AGENTS.md` | After the Task Type Routing table | `> **SC Integration:** For SuperClaude command/agent mappings per workflow phase, see [SuperClaude Integration Spec](./research/superclaude-integration-spec/output/SPEC.md).` |
| `RESEARCH.md` | §4 before step 1 | `> **SC Tooling:** Consult [SuperClaude Integration Spec §3](./research/superclaude-integration-spec/output/SPEC.md) for recommended \`/sc:*\` commands per research phase.` |
| `TASK.md` | §4 before step 2 (Plan) | `> **SC Tooling:** For 3+ domain tasks, use \`/sc:spawn\`; for orchestration, use \`/sc:pm\`. See [SuperClaude Integration Spec §3.5](./research/superclaude-integration-spec/output/SPEC.md).` |
| `PROMPT.md` | §4 before step 1 | `> **SC Tooling:** Use \`/sc:brainstorm\` to elicit prompt requirements. See [SuperClaude Integration Spec §3.9](./research/superclaude-integration-spec/output/SPEC.md).` |
| `MAINTENANCE.md` | §1 after first bullet | `> **SC Tooling:** Use \`/sc:index-repo\` and \`/sc:analyze\` at run start. See [SuperClaude Integration Spec §3.7](./research/superclaude-integration-spec/output/SPEC.md) and §5 of this file.` |

---

## 6. Anti-Patterns

The following patterns MUST NOT appear in Agency workflows after this spec is adopted:

1. **Ad-hoc web search without `/sc:research`**: When a research run requires multi-hop exploration, an agent MUST NOT call `WebSearch` directly without the structured depth/strategy framing that `/sc:research` provides.

2. **Manual plan for 3+ domain tasks**: An agent MUST NOT write a `task.md` plan for a complex multi-domain task without first using `/sc:spawn` to generate the canonical task hierarchy.

3. **No confidence gate**: An agent MUST NOT begin a research run or implementation task without invoking `confidence-check`. The 25-250x token-saving ROI is documented in KNOWLEDGE.md.

4. **Prompt authoring without `/sc:brainstorm`**: An agent SHOULD NOT write `brief.md` without at least one `/sc:brainstorm` pass when the research question is ambiguous. Exception: trivial follow-up prompts with clear scope.

5. **Spec output without `/sc:spec-panel`**: An agent SHOULD NOT close a research run by committing `output/SPEC.md` without a `/sc:spec-panel` review pass when the spec governs multi-agent behavior.

6. **Over-delegation**: An agent MUST NOT spawn a sub-agent for single-domain tasks completable in fewer than 5 steps. Direct tool calls are cheaper. Use `/sc:select-tool` to resolve ambiguity.

7. **Missing SC Integration Block**: Specs added after 2026-05-04 MUST include a SuperClaude Integration Block per §4. Specs without this block are non-compliant with Agency governance.

---

## SC Integration

> *This section is governed by this document itself.*

### Recommended SC Tools for Maintaining This Spec

| Phase | SC Command | SC Agent | Notes |
|-------|-----------|---------|-------|
| Re-executing integration scan | `/sc:research` | `deep-research-agent` | Use when a new SC Framework version is installed |
| Reviewing spec completeness | `/sc:spec-panel` | `self-review` | Before committing a revised version of this SPEC.md |
| Generating updated catalog | `/sc:index-repo` | `repo-index` | 94% token reduction when re-scanning the repository |

### Invocation Pattern (Maintenance Re-Run)

```
# When SuperClaude Framework is updated:
/sc:research "What changed in SuperClaude v[X.Y.Z] vs v4.3.0?" --depth standard
# Then re-execute the superclaude-integration-spec prompt:
# /prompts/superclaude-integration-spec/prompt.md
```

### Confidence Gate

Agents MUST invoke `confidence-check` before re-executing this spec or amending its output.
