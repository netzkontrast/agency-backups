# Framework Selection — Intent Routing & Discriminator Logic

Full decision logic for Phase 1 of the Prompt Optimizer.
Derived from the prompt-architect 27-framework catalog.

---

## Step 1: Detect Primary Intent

Score the user's prompt against these 7 intent categories.
Pick the highest-scoring category. Default to CREATE if ambiguous.

### A. RECOVER
**Signal:** User has a good output but lost or needs the prompt.
- Keywords: "reverse engineer", "recover prompt", "what prompt made this",
  "lost prompt", "reconstruct prompt", "template from output"
- Framework: **RPEF** (Reverse Prompt Engineering Framework)
- No discriminator needed — RPEF is the only option.

### B. CLARIFY
**Signal:** Requirements are unclear; user can't articulate what they need.
- Keywords: "not sure what I need", "help me figure out", "ask me questions",
  "interview me", "what do I need", "don't know how to start"
- Framework: **Reverse Role Prompting** (AI-Led Interview / FATA)
- No discriminator needed.

### C. CREATE
**Signal:** Generating new content from scratch.
- Keywords: write, create, draft, generate, compose, build, make, produce, develop
- Apply CREATE Discriminators below.

### D. TRANSFORM
**Signal:** Improving or converting existing content.
- Keywords: rewrite, refactor, convert, improve, edit, revise, transform,
  compress, summarize, densify, expand, restructure, rephrase
- Apply TRANSFORM Discriminators below.

### E. REASON
**Signal:** Solving a reasoning or calculation problem.
- Keywords: calculate, compute, solve, figure out, reason, analyze, evaluate,
  determine, derive, logic, math, should I, which is better, compare options
- Apply REASON Discriminators below.

### F. CRITIQUE
**Signal:** Stress-testing, attacking, or verifying existing output/decision.
- Keywords: review, critique, find flaws, what could go wrong, attack, challenge,
  verify, check, validate, risks, failure modes, weaknesses, problems with
- Apply CRITIQUE Discriminators below.

### G. AGENTIC
**Signal:** Tool-use with iterative reasoning cycles.
- Keywords: use tools, search and, run code, execute, fetch, query database,
  look up, agent, automate, multi-step with tools
- Framework: **ReAct** (Reasoning + Acting)
- No discriminator needed.

---

## Step 2: Apply Discriminators

### CREATE Discriminators

Ask in order — stop at first match:

1. **Is the task ultra-minimal, one-off, no role/context needed?**
   → **APE** (Action · Purpose · Expectation)

2. **Is expertise framing the primary driver? Is context minimal?**
   → **RTF** (Role · Task · Format)

3. **Is background/situation the primary driver? Is expertise obvious?**
   → **CTF** (Context · Task · Format)

4. **Do you need role + situational context + explicit success criteria?**
   → **RACE** (Role · Action · Context · Expectation)

5. **Do you need multiple output variants to compare?**
   → **CRISPE** (Capacity+Role · Insight · Instructions · Personality · Experiment)

6. **Are measurable business outcomes (KPIs) explicitly defined?**
   → **BROKE** (Background · Role · Objective · Key Results · Evolve)

7. **Are rules/constraints present AND examples help clarify the standard?**
   (combined rules+examples, not separate Do/Don't lists)
   → **CARE** (Context · Ask · Rules · Examples)

8. **Are audience, tone, and style the critical success factors?**
   → **CO-STAR** (Context · Objective · Style · Tone · Audience · Response)

9. **Is this a multi-step procedure where constraints define the boundary?**
   → **RISEN** (Role · Instructions · Steps · End Goal · Narrowing)

10. **Are explicit separate DO lists and DON'T lists required?**
    → **TIDD-EC** (Task · Instructions · Do · Don't · Examples · Context)

11. **Is there well-defined input data being transformed into output?**
    → **RISE-IE** (Role · Input · Steps · Expectation)

12. **Is this content creation where style examples are the key reference?**
    → **RISE-IX** (Role · Instructions · Steps · Examples)

---

### TRANSFORM Discriminators

| Signal | Framework |
|--------|-----------|
| Existing content → new form (rewrite, refactor, migrate) | **BAB** (Before · After · Bridge) |
| Iterative quality improvement across multiple dimensions | **Self-Refine** |
| Compress or densify — information density is the goal | **Chain of Density** |
| Outline-first structure, then expand each section | **Skeleton of Thought** |

---

### REASON Discriminators

| Signal | Framework |
|--------|-----------|
| Numerical/calculation, zero-shot, variables present | **Plan-and-Solve (PS+)** |
| Linear step-by-step reasoning, single path | **Chain of Thought** |
| Multi-hop with ordered dependencies (A needed before B) | **Least-to-Most** |
| Needs first-principles before answering | **Step-Back** |
| Multiple distinct approaches to compare | **Tree of Thought** |
| Verify reasoning didn't overlook conditions | **RCoT** |

---

### CRITIQUE Discriminators

| Signal | Framework |
|--------|-----------|
| General quality improvement, multi-dimensional | **Self-Refine** |
| Align output to an explicit stated principle/standard | **CAI Critique-Revise** |
| Find the strongest opposing argument | **Devil's Advocate** |
| Identify failure modes before they happen | **Pre-Mortem** |
| Verify reasoning completeness, multi-condition | **RCoT** |

**Disambiguation:**
- Self-Refine = any quality improvement
- CAI = principle compliance (specific standard stated)
- Devil's Advocate = opposing arguments (attack position)
- Pre-Mortem = failure analysis (assume failure, work backwards)
- RCoT = condition verification (missed conditions in reasoning)

---

## Framework Complexity Map

| Complexity | Frameworks |
|-----------|-----------|
| Minimal | APE |
| Low | RTF · CTF · BAB · PS+ · RPEF · Devil's Advocate · Pre-Mortem |
| Medium | RACE · CARE · CRISPE · BROKE · RISE-IE · RISE-IX · CoT · LtM · Step-Back · ToT · RCoT · Self-Refine · CAI · ReAct · CoD · SoT |
| High | CO-STAR · RISEN · TIDD-EC |
| Meta/Reverse | RPEF · Reverse Role |

---

## Common Mistakes in Framework Selection

- **Using CARE when explicit Do/Don't lists are needed** → use TIDD-EC instead
- **Using RISEN when task has no sequential steps** → downgrade to RACE or RTF
- **Using CO-STAR for technical analysis** → audience/tone irrelevant → use RACE or RISEN
- **Using BAB when creating from scratch** (no "before") → no transformation → use CREATE family
- **Using ReAct without tools** → no agentic loop needed → use CoT instead
- **Using ToT when one approach is clearly correct** → overhead → use CoT
