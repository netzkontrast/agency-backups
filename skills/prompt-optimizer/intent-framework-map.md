# Intent → Framework Map

Complete selection logic for all 27 frameworks across 7 intent categories.
Load during Phase 1 to select the optimal framework.

---

## A. RECOVER — Reconstruct a prompt from an existing output

**Signal:** "I have a good output but need / lost the prompt"

→ **RPEF** (Reverse Prompt Engineering Framework)

---

## B. CLARIFY — Requirements are unclear

**Signal:** "I know roughly what I want but struggle to specify the details"

→ **Reverse Role Prompting** (AI-Led Interview / FATA)

---

## C. CREATE — Generating new content from scratch

Discriminate within CREATE using the signal column:

| Signal | Framework | Key Differentiator |
|--------|-----------|-------------------|
| Ultra-minimal, one-off, no role needed | **APE** | Action · Purpose · Expectation |
| Simple, expertise-driven | **RTF** | Role defines everything |
| Simple, situation-driven (background > persona) | **CTF** | Context first, no persona |
| Role + context + explicit outcome | **RACE** | Adds Expectation to RTF |
| Multiple output variants needed (A/B options) | **CRISPE** | Experiment component |
| Business deliverable with KPIs / OKRs | **BROKE** | Key Results + Evolve loop |
| Explicit rules/compliance + examples | **CARE** | Combined rules + examples |
| Separate Do / Don't lists | **TIDD-EC** | Split positive/negative lists |
| Audience · tone · style are critical | **CO-STAR** | Full communication framework |
| Multi-step procedure + methodology | **RISEN** | Steps + Narrowing |
| Data transformation (input → output) | **RISE-IE** | Input-Expectation variant |
| Content creation with reference examples | **RISE-IX** | Instructions-Examples variant |

**TIDD-EC vs CARE disambiguation:**
- Separate DO and DON'T lists → TIDD-EC
- Combined rules section + examples → CARE

**RISE-IE vs RISE-IX disambiguation:**
- Processing specific data (CSV, JSON, text) → RISE-IE
- Creating content with style references → RISE-IX

---

## D. TRANSFORM — Improving or converting existing content

| Signal | Framework |
|--------|-----------|
| Rewrite / refactor / convert — clear before/after | **BAB** |
| Iterative quality improvement (multi-dimensional) | **Self-Refine** |
| Compress or densify — information density goal | **Chain of Density** |
| Outline-first then expand sections | **Skeleton of Thought** |

---

## E. REASON — Solving a reasoning or calculation problem

| Signal | Framework |
|--------|-----------|
| Numerical / calculation, zero-shot | **Plan-and-Solve (PS+)** |
| Multi-hop with ordered dependencies (A before B) | **Least-to-Most** |
| Needs first-principles before answering | **Step-Back** |
| Multiple distinct approaches to compare | **Tree of Thought** |
| Verify reasoning didn't overlook conditions | **RCoT** |
| Linear step-by-step reasoning | **Chain of Thought** |

---

## F. CRITIQUE — Stress-testing, attacking, or verifying

| Signal | Framework |
|--------|-----------|
| General quality improvement loop | **Self-Refine** |
| Align output to explicit principle / standard | **CAI Critique-Revise** |
| Find the strongest opposing argument | **Devil's Advocate** |
| Identify failure modes before they happen | **Pre-Mortem** |
| Verify reasoning didn't miss conditions | **RCoT** |

**Self-Refine vs CAI disambiguation:**
- Any quality improvement → Self-Refine
- Specific stated principle to enforce → CAI Critique-Revise

**Devil's Advocate vs Pre-Mortem disambiguation:**
- Attack the reasoning / position → Devil's Advocate
- Assume failure, find causes → Pre-Mortem

---

## G. AGENTIC — Tool-use with iterative reasoning

**Signal:** "Task requires tools; each result informs the next step"

→ **ReAct** (Reasoning + Acting)

---

## Framework Complexity Index

| Complexity | Frameworks |
|-----------|-----------|
| **Minimal** | APE |
| **Low** | RTF · CTF · BAB · RPEF · Devil's Advocate · Pre-Mortem · Plan-and-Solve |
| **Medium** | RACE · CRISPE · BROKE · CARE · RISE-IE · RISE-IX · Self-Refine · CoT · Least-to-Most · Step-Back · Tree-of-Thought · RCoT · Chain-of-Density · Skeleton-of-Thought · ReAct · CAI Critique-Revise · Reverse-Role |
| **High** | CO-STAR · RISEN · TIDD-EC |

---

## Scoring Tiebreaker

When two frameworks score equally, apply:
1. Prefer lower complexity if output quality is equivalent
2. Prefer the framework whose **unique component** is present in the prompt
   (e.g., CRISPE wins over RACE if the user asked for "options" or "variants")
3. When in doubt between CO-STAR and RISEN: CO-STAR for writing tasks,
   RISEN for procedural / technical tasks with hard constraints
