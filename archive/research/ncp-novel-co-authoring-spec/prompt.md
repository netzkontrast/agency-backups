topic: "Narrative Context Protocol × Dramatica × Agentic Skills — A Single Specification for AI-Agent-Driven Novel Co-Authoring" slug: "ncp-novel-co-authoring-spec" research_category: "B" research_category_label: "Extraction" critical_thinking_methods:

"Source Triangulation (M06)"
"Contradiction Log (M07)"
"What Would Change My Mind (M08)"
"First-Principles Decomposition (M10)"
"Adversarial Query Expansion (M13)" prompt_engineering_framework_agentic_spine: "ReAct" prompt_engineering_framework_structural: "RISEN" bespoke_framework_provenance: "" cross_pollination:
source_category: "A" step_id: "i.a" description: "Hidden-items query + schema-gap hypothesis (guards against undiscovered NCP entities, Dramatica elements, and skill phases that the input list missed)"
source_category: "C" step_id: "i.c" description: "World-change check across NCP repo commits, Anthropic Skill Spec updates, and Spec-Driven Development tooling releases during the research run" constraint_blocks:
"0 — Reflection Baseline"
"1 — Source Priority Rules"
"2 — Temporal Scope"
"3 — Output Exclusions"
"4 — Spec Language Convention (RFC 2119 + Gherkin)"
"5 — Output Locking (Single Monolithic SPEC.md, English)" language: "en" target_agent: "model-agnostic" created: "2026-05-02" version: "1.0" source_skill: "research-prompt-optimizer v2.1.0"

Research Prompt: Narrative Context Protocol × Dramatica × Agentic Skills — A Single Specification for AI-Agent-Driven Novel Co-Authoring
For the executing AI: This prompt is self-contained. Every method, framework, and constraint you need is defined inline below. You do not need external context, prior training on specific methodologies, or knowledge of the skill that generated this prompt. Read the entire prompt before beginning. Your final deliverable is one monolithic Markdown file named SPEC.md that satisfies every Expectation listed in the Expectations section. The body of this research prompt explains how to get there.

Meta-Header — What This Prompt Is and How To Read It
This research prompt combines three independent layers:
1. Epistemological Layer — Category B (Extraction)
This research is an extraction, not an exploration. The answer exists in the world; your task is to locate it, verify it, and present it in a structured form. You are not generating new hypotheses about unknown phenomena — you are assembling a specification document by combining (a) the public NCP repository's data model and state machine, (b) the public literature on Spec-Driven Development, (c) the public literature on specification language conventions, (d) the public Dramatica theory canon, and (e) Anthropic's public Agentic Skill specification — into a single, coherent, self-contained SPEC.md.

What this means for your execution:
Follow the plan exactly. The Steps section below specifies an ordered procedure across five extraction tracks plus one synthesis. Execute end-to-end. Do not improvise alternative strategies. If the plan proves impossible, halt and report — never silently substitute another approach.
Fill every field of the output schema or flag it as missing. The final SPEC.md has a locked structural skeleton (specified in Expectations). Every section must be populated with evidence-backed content OR explicitly marked [NOT-FOUND — reason]. Never invent.
Source triangulation is mandatory (Method M06).
Handle contradictions transparently (Method M07).
Extraction is not interpretation. Your task is to collect, structure, and recommend with explicit trade-off reasoning — not to editorialize. Where a design decision is open (e.g., the NCP↔Dramatica relationship), present the candidate options, the trade-offs, and a recommended option with explicit justification.

Operational constraint: Speed is less important than completeness. If the structural skeleton is fully populated, every entity is mapped, and every constraint block has been demonstrably honored, the research is complete — further search produces diminishing returns.
2. Agentic Spine — ReAct (Reason → Act → Observe)
Every autonomous loop in this research follows the ReAct cycle. Each iteration consists of three phases:

Reason — Articulate your current understanding and plan the next action in plain language. State which hypothesis you are testing, which constraint block governs this step, and which critical-thinking method is active.
Act — Execute exactly one action (typically a search, a fetch, or a code-file read).
Observe — Record what the action returned and what it means for the plan. Explicitly decide: continue this branch, backtrack, or expand the query vocabulary (Method M13 — Adversarial Query Expansion).

Loop structure:
[Reason 1] → [Act 1] → [Observe 1] →
[Reason 2] → [Act 2] → [Observe 2] →
...
[Reason N] → [Pre-Synthesis Integrity Check] → [Synthesis = SPEC.md]

Your first action before Reason 1: Restate the Research Objective, Role, Narrowing, and all six Constraint Blocks. Do not skip directly to Act.

Inside every Reason phase you explicitly answer three questions:
What do I currently believe, and how strongly?
Which active critical-thinking method applies to this next Act?
Am I at risk of local-minimum lock-in? (If yes → invoke Method M13: Adversarial Query Expansion before choosing the next Act.)

3. Structural Layer — RISEN (Role · Input · Steps · Expectations · Narrowing)
RISEN governs how the sections of this prompt are organized; ReAct governs how you iterate within each step. RISEN stands for:
R — Role: Who you are acting as during this task.
I — Input: What materials, questions, or data you are starting with.
S — Steps: The explicit ordered procedure to follow.
E — Expectations: What a successful output looks like (format, coverage, depth).
N — Narrowing: Hard constraints, exclusions, and scope limits.

Your first action before Step 1: Restate the Role and Narrowing sections in your own words. Confirm you have internalized them. Do not begin Step 1 until this restatement is written.

Each section is labeled with its RISEN component in parentheses, e.g., "(R — Role)". Honor each component as a hard contract.

Research Objective
Produce a single, monolithic, self-contained Markdown file named SPEC.md, written in English, that specifies how the Narrative Context Protocol (open-source project at https://github.com/narrative-first/narrative-context-protocol) MUST be deployed to drive the end-to-end co-authoring of a full-length novel by AI coding agents — primarily Claude Code, secondarily Gemini Jules — using Dramatica theory as the narrative-structural backbone, the Anthropic Agentic Skill Spec (the formal SKILL.md contract) as the agent-side capability format, and the Hybrid Hexagonal pattern (per-phase router skills that delegate to finer-grained functional sub-skills) as the skill-architectural pattern.

Temporal scope: Last 36 months for tooling and method literature (specifications, agentic frameworks, software/spec-driven-development practice, Anthropic Skill Spec). All time for foundational theory (Dramatica, RFC 2119, Gherkin, IEEE 29148). Audience of the final output: A senior software architect / AI systems developer who will hand SPEC.md to a fresh Claude Code or Gemini Jules agent and expect that agent to be able to begin implementing the skill ecosystem and the NCP integration without further clarifying questions. Expected depth: Exhaustive — full repository code analysis (every source file, data schema, state machine, entry point); full canonical Dramatica structure; full Anthropic Skill anatomy; full normative specification language convention. Output format: One Markdown file (SPEC.md) following the structural skeleton defined in Expectations (E) below; written in RFC 2119 + Gherkin language per Constraint Block 4. Language: English throughout (per Constraint Block 5).
