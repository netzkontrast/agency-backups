---
name: ralph-skill
description: "Use when generating Ralph agentic-loop files (loop.sh, PROMPT_build.md, PROMPT_plan.md, AGENTS.md, IMPLEMENTATION_PLAN.md), customizing or extending an existing Ralph workflow, auditing a Ralph setup for playbook compliance, or when research-prompt-optimizer output needs conversion into Ralph specs and an implementation plan. Triggers on: ralph, ralph loop, ralph playbook, loop.sh, PROMPT_build, PROMPT_plan, AGENTS.md, IMPLEMENTATION_PLAN.md, build loop, agentic coding loop, autonomous build agent, subagent orchestration, backpressure, JTBD specs, specs from research, loop instructions, implementation loop, git worktrees parallel, context isolation agentic, incremental verification loop."
metadata:
  category: agentic-workflow
  source: user
  date_added: "2026-05-02"
  version: "1.2.0"
  research_sources: "agent-prompt-specs-3-systems-sdd (SPEC.md: Spec-A Jules, Spec-B Claude Code, Spec-C Gemini Deep Research); Jules-vs-Claude-Code-Ralph research (Claude Code v2.1.123, May 2026)"
  triggers: "ralph, ralph loop, ralph playbook, loop.sh, PROMPT_build, PROMPT_plan, AGENTS.md, IMPLEMENTATION_PLAN.md, agentic loop, autonomous coding agent, backpressure, JTBD specs, research to specs, subagent orchestration, loop instructions, build loop, git worktrees, parallel implementation, context isolation, incremental verification"
---

# Ralph Skill — Agentic Loop Generator & Auditor

Generates, customizes, extends, and audits Ralph agentic-coding-loop file sets.
Uses **spec-skill** (apply mode) against `references/ralph-spec.md` before producing any loop prompts.

> **Three Pillars** — validated across Jules, Claude Code, and Gemini Deep Research (SPEC.md Common Conventions):
> - **Incremental Verification** — validate every unit of work before committing; never batch validation across tasks
> - **Explicit Planning** — a dedicated planning phase before any implementation; never merge planning and execution
> - **Context Isolation** — fresh context per task; subagents for reads; never let exploration pollute reasoning context

---

## ⚡ Quick Decision Tree

| Situation | Mode |
|-----------|------|
| New project, needs full Ralph setup from scratch | **[Generate](#mode-1-generate)** |
| Has Ralph files, needs project-specific filling | **[Customize](#mode-2-customize)** |
| Wants to add specs-mode, plan-work, SLC, reverse-engineer, git worktrees, or non-deterministic backpressure | **[Extend](#mode-3-extend)** |
| Has existing Ralph setup, wants compliance check | **[Audit](#mode-4-audit)** |
| Has research-prompt-optimizer output, wants to feed into Ralph | **[Research Bridge](#research-bridge)** |

---

## Mode 1: Generate

**Trigger**: User wants a new Ralph project from scratch.

### Step 1 — Elicit project context

Ask only what is missing; don't ask for things already in context:

1. **Project goal** — one sentence describing the end state (fills `[project-specific goal]` in PROMPT_plan.md)
2. **Source layout** — where does source code live? (default: `src/`, `src/lib/`)
3. **Backpressure commands** — test, typecheck, lint commands (fills AGENTS.md Validation section)
4. **Subagent budget** — max parallel subagents (default: 500 for reads, 1 for build/test)
5. **Parallel work needed?** — if yes, recommend git worktrees extension (see Mode 3)
6. **Enhancements wanted** — any of: specs-mode, plan-work, SLC-planning, reverse-engineer, non-deterministic backpressure?

### Step 2 — Apply spec-skill to derive normative requirements

**REQUIRED SUB-SKILL**: Load `references/ralph-spec.md` and apply spec-skill (apply mode).
Identify which normative statements (R.2.x through R.7.x) govern the target files before generating them.
Mark derived content with `# from R.X.Y` comments.

### Step 3 — Generate file set

Produce in this order:

| File | Source |
|------|--------|
| `loop.sh` | `references/loop-variants.md` → base variant |
| `PROMPT_plan.md` | `references/prompt-templates.md` → plan template, fill project goal |
| `PROMPT_build.md` | `references/prompt-templates.md` → build template |
| `AGENTS.md` | `references/prompt-templates.md` → AGENTS skeleton, fill backpressure commands |
| `IMPLEMENTATION_PLAN.md` | `references/prompt-templates.md` → empty comment stub |

For each requested enhancement, add the corresponding `PROMPT_*.md` and patch `loop.sh`.
See `references/loop-variants.md` for enhanced, streamed, and git-worktrees variants.

### Step 4 — Post-generation checklist

- [ ] `[project-specific goal]` placeholder replaced in PROMPT_plan.md
- [ ] Backpressure commands filled in AGENTS.md (real commands, not `[test command]`)
- [ ] `loop.sh` is executable (`chmod +x loop.sh` reminder included)
- [ ] Enhancement prompt files generated for each requested mode
- [ ] loop.sh patched with mode branches for each enhancement
- [ ] User warned about `--dangerously-skip-permissions` and sandbox requirements

---

## Mode 2: Customize

**Trigger**: User already has Ralph files but they contain unfilled placeholders or generic commands.

1. Read the existing files provided by the user.
2. Run spec-skill (audit mode) against `references/ralph-spec.md` to identify gaps.
3. Ask only for information needed to fill identified gaps.
4. Return updated files with a diff summary of what changed.

**Critical checks**:
- `[project-specific goal]` in PROMPT_plan.md → must be filled
- Backpressure commands in AGENTS.md → must be project-specific (not placeholder)
- AGENTS.md length → target 60 lines empirically (see R.2.6 and §8 Known Limitations for the 60 vs 200 line debate)
- PROMPT_build.md guardrail 99999999999999 references `Opus 4.7` — update model string if project uses different version
- loop.sh `--model` flag — confirm model name is `claude-opus-4-7` for Anthropic API (see `references/loop-variants.md` Model String Reference; Bedrock/Vertex still uses `claude-opus-4-6`)

---

## Mode 3: Extend

**Trigger**: User wants to add one or more enhancement modes to an existing Ralph setup.

Read `references/loop-variants.md` for full script details on each extension.

| Extension | New file(s) | loop.sh patch | Spec basis |
|-----------|-------------|---------------|------------|
| **specs-mode** | `PROMPT_specs.md` | `elif [ "$1" = "specs" ]` | R.3.2, R.3.3 |
| **plan-work** | `PROMPT_plan_work.md` | `elif [ "$1" = "plan-work" ]` + `envsubst` | R.2.8, R.4.5 |
| **SLC-planning** | `PROMPT_plan_slc.md` + `AUDIENCE_JTBD.md` | `elif [ "$1" = "slc" ]` | — |
| **reverse-engineer** | `PROMPT_reverse_engineer_specs.md` | `elif [ "$1" = "reverse" ]` | R.3.2, R.3.3 |
| **git-worktrees** | — (workflow; no new prompt file needed) | No loop.sh patch | R.2.9, B.5.2 |
| **streamed output** | `parse_stream.js` + `loop_streamed.sh` | Separate script | — |
| **non-deterministic backpressure** | `src/lib/llm-review.ts` + `llm-review.test.ts` | No patch; AGENTS.md note | R.6.5 |

**Git Worktrees workflow** (from Spec-B B.5.2, validated by ralph-spec.md R.2.9):
When the user needs to implement multiple independent features simultaneously without context bleed between tasks:
```bash
# Create a worktree per feature branch
git worktree add ../my-project-auth feature/auth
git worktree add ../my-project-api feature/api

# Run plan-work in each worktree to create scoped plans
cd ../my-project-auth && ./loop.sh plan-work "user authentication with OAuth"
cd ../my-project-api && ./loop.sh plan-work "REST API for product catalog"

# Build independently in each worktree (sequential or parallel)
cd ../my-project-auth && ./loop.sh 20
cd ../my-project-api && ./loop.sh 20
```
Each worktree gets its own `IMPLEMENTATION_PLAN.md`. The main branch plan remains untouched. See `references/loop-variants.md` for the complete git worktrees section.

For each extension:
1. Apply spec-skill (apply mode) against the relevant aspect in `references/ralph-spec.md`
2. Note which normative statements the extension satisfies or introduces
3. Add a brief usage example showing the new `./loop.sh <mode>` invocation

---

## Mode 4: Audit

**Trigger**: User has an existing Ralph setup and wants to verify it. Also triggers when user reports: loop going in circles, AGENTS.md getting cluttered, duplicated work, wrong tasks being implemented, or stale plans.

1. Load `references/ralph-spec.md`.
2. Apply spec-skill (audit mode) against each Ralph file.
3. Output a structured findings report.

**Audit targets**:

| File | Primary spec sections | Common failure patterns |
|------|-----------------------|------------------------|
| `PROMPT_plan.md` | R.4.x, R.3.x, R.2.x | Unfilled `[project-specific goal]` |
| `PROMPT_build.md` | R.5.x, R.6.x, R.7.x | Missing backpressure guardrails; stale model string |
| `AGENTS.md` | R.2.5, R.2.6, R.2.10 | Status notes polluting operational content; length drift |
| `loop.sh` | R.2.7, R.2.9, R.5.2 | Missing `--dangerously-skip-permissions`; stale model string |
| `IMPLEMENTATION_PLAN.md` | R.4.3, R.7.2, R.7.3 | No prioritization; completed items not cleared |
| `specs/*.md` | R.3.1, R.3.2, R.3.3 | Over-scoped topics; implementation details in specs |

**Findings format**: Use spec-skill audit output shape (schema conformance → normative discipline → cross-cutting issues).

---

## Research Bridge

**Trigger**: User ran research-prompt-optimizer and now wants to feed the research output into a Ralph workflow. Also triggers when user has any research document (Gemini Deep Research, Perplexity, custom research) describing a software system they want to build.

### Workflow

**Step 1 — Structure the research using the four-part formula** (sourced from Spec-C C.2.2):
For each JTBD area in the research document, frame it as:
- **Task**: What outcome does this JTBD produce?
- **Grounding**: What did the research actually confirm (vs. infer or speculate)?
- **Context**: What constraints or dependencies exist?
- **Format**: What does success look like (behavioral outcome, observable result)?

This four-part frame becomes the skeleton of each `specs/NN-kebab-case.md` file.

**Step 2 — Apply topic scope test** — "One sentence without 'and'" — split over-scoped topics.

**Step 3 — Generate specs with source attribution** (sourced from Spec-C C.7.1):
Each spec derived from research MUST carry a `## Source Attribution` section listing which sections of the research document support its claims. Research-sourced specs without attribution are treated as ungrounded and SHOULD be flagged for human verification before planning begins.

**Step 4 — Flag data gaps as LOW CONFIDENCE** (sourced from Spec-C C.7.5):
Where the research document explicitly identified gaps, limitations, or single-source claims, the corresponding spec MUST carry a `**[LOW CONFIDENCE — research gap]**` annotation. Ralph's planning loop SHOULD treat these specs as lower priority until the user validates them.

**Step 5 — Seed implementation plan** — Use the research's identified gaps, missing components, and priorities to pre-populate `IMPLEMENTATION_PLAN.md` with a first-pass prioritized task list.

**Step 6 — Generate Ralph setup** — If no loop.sh exists, run Mode 1 Generate.

**Step 7 — Wire project goal** — Fill `[project-specific goal]` in PROMPT_plan.md from the research document's stated objective.

**Note**: The research document is the authoritative upstream source. If Ralph's planning loop contradicts it, the research document wins until the user explicitly changes specs. LOW CONFIDENCE specs must be verified by the user before they drive significant implementation work.

---

## Integration Notes

**spec-skill** (REQUIRED SUB-SKILL for modes 1, 2, 3):
- Apply mode: derive normative requirements from `references/ralph-spec.md` before generating files
- Audit mode: check generated or existing files against the spec

**research-prompt-optimizer** (upstream partner):
- Its output is valid input for Ralph's specs phase
- When research-prompt-optimizer produces a finalized Deep Research document, this skill handles the Ralph-side operationalization via the Research Bridge

---

## 📚 Reference Index

| File | Contents |
|------|----------|
| `references/ralph-spec.md` | Normative spec (spec-skill schema) governing all Ralph loop behavior — updated with R.2.9, R.2.10, §8 contradiction log |
| `references/prompt-templates.md` | All PROMPT_*.md templates plus Staff Engineer pattern and research-sourced spec format |
| `references/loop-variants.md` | loop.sh variants, git worktrees workflow, model string reference |

---

## ✅ Pre-Deploy Checklist

Before delivering any Ralph file set to the user:

- [ ] spec-skill (apply mode) was run against `references/ralph-spec.md`
- [ ] No `[project-specific goal]` placeholders remain unfilled
- [ ] Backpressure commands in AGENTS.md are real commands, not `[test command]`
- [ ] AGENTS.md is operational-only; no status/progress notes present
- [ ] loop.sh has execute permission reminder
- [ ] Model strings in loop.sh and PROMPT_build.md guardrail 99999999999999 are current
- [ ] Each generated file has a brief header comment explaining its role
- [ ] Requested enhancements have their companion files generated
- [ ] User warned about `--dangerously-skip-permissions` and sandbox requirements
- [ ] Research-sourced specs carry source attribution and LOW CONFIDENCE flags where applicable (Research Bridge only)
