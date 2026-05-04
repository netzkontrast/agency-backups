# Framework Templates — All 27 Component Structures

Reference for Phase 3B: use these templates to build the optimized prompt.
Strip all section headers before presenting to user — flatten to natural prose.

---

## CREATE Family

### APE — Action · Purpose · Expectation
```
[ACTION: clear verb-driven instruction]
[PURPOSE: why it's needed, one sentence]
[EXPECTATION: what a good result looks like — format, length, quality bar]
```

### RTF — Role · Task · Format
```
As a [ROLE with expertise level], [TASK — specific deliverable].
Format: [structure, length, sections, style requirements]
```

### CTF — Context · Task · Format
```
[CONTEXT: situation, background, why this is needed, constraints]
[TASK: exactly what needs to be done]
[FORMAT: structure, length, style requirements]
```

### RACE — Role · Action · Context · Expectation
```
[ROLE: expertise or persona]
[ACTION: what needs to be done — task and deliverable]
[CONTEXT: background, situation, constraints, audience]
[EXPECTATION: success criteria, format, quality bar, what to prioritize]
```

### CRISPE — Capacity+Role · Insight · Instructions · Personality · Experiment
```
[CAPACITY AND ROLE: expertise level and professional role]
[INSIGHT: background context, data, constraints]
[INSTRUCTIONS: specific task and deliverable]
[PERSONALITY: tone, voice, communication style]
[EXPERIMENT: N variants along [dimension] — e.g., "3 versions: one X, one Y, one Z"]
```

### BROKE — Background · Role · Objective · Key Results · Evolve
```
[BACKGROUND: current situation, why this task exists, relevant history]
[ROLE: professional persona and expertise]
[OBJECTIVE: specific task and deliverable]
[KEY RESULTS: measurable outcomes — how success is defined in business terms]
[EVOLVE: "After responding, provide 3 specific suggestions for improving this output."]
```

### CARE — Context · Ask · Rules · Examples
```
[CONTEXT: who you are, the situation, why this task exists]
[ASK: specific request and deliverable]
[RULES: what must be included / what must be avoided / format / length / tone / compliance]
[EXAMPLES: 1-3 examples showing desired output format, tone, or quality]
```

### CO-STAR — Context · Objective · Style · Tone · Audience · Response
```
[CONTEXT: background information, situation, constraints]
[OBJECTIVE: clear specific goal and success criteria]
[STYLE: writing style, format preferences, structural approach]
[TONE: emotional quality — professional / casual / urgent / empathetic / authoritative]
[AUDIENCE: who will read this — expertise level, characteristics, what they care about]
[RESPONSE FORMAT: length, sections, detail level, format requirements]
```

### RISEN — Role · Instructions · Steps · End Goal · Narrowing
```
[ROLE: expertise level, persona, or perspective to adopt]
[INSTRUCTIONS: high-level guiding principles and methodology]
Steps:
1. [First specific action]
2. [Second specific action]
3. [Continue...]
[END GOAL: success criteria and final desired outcome]
[NARROWING:
- Do NOT: [constraint]
- Avoid: [pattern to avoid]
- Out of scope: [what's excluded]
- Stay within: [boundaries]]
```

### TIDD-EC — Task · Instructions · Do · Don't · Examples · Context
```
[TASK TYPE: clear activity category]
[INSTRUCTIONS:
1. [Step]
2. [Step]]
DO:
- [Required action or element]
- [Required language or structure]
DON'T:
- [Error to prevent]
- [Approach to avoid]
[EXAMPLES:
Example 1 (Good): [detailed example]
Example 2 (Avoid): [counter-example]]
[CONTEXT: background, constraints, standards that apply]
```

### RISE-IE — Role · Input · Steps · Expectation
```
[ROLE: perspective or expertise needed for this analytical task]
[INPUT: format and structure / key characteristics / quirks]
Steps:
1. [Processing action]
2. [Analysis step]
3. [Continue...]
[EXPECTATION: output format / required elements / length / structure]
```

### RISE-IX — Role · Instructions · Steps · Examples
```
[ROLE: persona or expertise level]
[INSTRUCTIONS: main task / core requirements / key guidelines]
Steps:
1. [Approach or methodology step]
2. [Step]
3. [Continue...]
[EXAMPLES:
Example 1: [reference demonstrating desired style]
Example 2: [second example]]
```

---

## TRANSFORM Family

### BAB — Before · After · Bridge
```
[BEFORE: current state — what exists, what's wrong, specific problems]
[AFTER: desired end state — qualities it should have, success criteria, audience]
[BRIDGE: transformation rules — what to preserve / what to change / constraints on approach]
```

### Self-Refine — Generate → Feedback → Refine
```
[INITIAL OUTPUT: paste output to improve, or ask AI to generate first draft]
FEEDBACK DIMENSIONS:
1. [Dimension — e.g., "Clarity: any ambiguous sentences?"]
2. [Dimension — e.g., "Completeness: what's missing?"]
3. [Dimension — e.g., "Tone: appropriate for audience?"]
For each: quote problematic passages, explain issue, suggest improvement.
REFINEMENT: Rewrite addressing every feedback point. Show refined version only.
```

### Chain of Density — Iterative Compression
```
[SOURCE CONTENT: content to compress/densify]
OPTIMIZATION GOAL: [e.g., "Reduce word count 20% each pass while retaining all key information"]
NUMBER OF ITERATIONS: [2-4]
ITERATION INSTRUCTIONS: Each pass — identify what to cut/compress/clarify → apply → verify improvement.
STOP WHEN: [criterion — e.g., "under 150 words" / "3 iterations complete"]
OUTPUT FORMAT: [paragraph / bullets / structured sections]
```

### Skeleton of Thought — Outline-First Expansion
```
PHASE 1 — SKELETON:
Generate a skeleton outline for [topic/question].
List key points only: N. [Point name] | [one-line description]
Do not expand yet.

PHASE 2 — EXPAND:
Expand each point into [2-4 sentences / a paragraph / detailed coverage].
Each point should be self-contained and complete.
```

---

## REASON Family

### Plan-and-Solve PS+ — Zero-Shot Calculation
```
[PROBLEM: question with all relevant numbers and variables]

Let's first understand the problem, extract relevant variables and their
corresponding numerals, and devise a complete plan. Then, let's carry out
the plan, calculate intermediate values, pay attention to computation,
and solve the problem step by step.
```

### Chain of Thought
```
[PROBLEM: clearly stated with all conditions and constraints]

Solve this step-by-step. For each step:
1. State what you're doing and why
2. Show your work / intermediate result
3. Verify before moving to the next step
FINAL ANSWER: [state clearly after the reasoning chain]
```

### Least-to-Most — Sequential Decomposition
```
PROBLEM: [full complex problem]
DECOMPOSE: Break into ordered subproblems, simplest prerequisite first.
Subproblem 1: [simplest prerequisite]
Subproblem 2: [builds on #1]
Subproblem 3: [builds on #1-2]
Final: [original problem, now solvable using all prior answers]
SOLVE SEQUENTIALLY: solve each in order, use prior answers as context.
```

### Step-Back — Principles First
```
ORIGINAL QUESTION: [specific question]
STEP-BACK: Before answering, first answer this higher-level question:
[abstract question about underlying principles/concepts]
PRINCIPLE APPLICATION: Using those principles, now answer the original question.
```

### Tree of Thought — Branch Exploration
```
PROBLEM: [what needs solving, constraints, success criteria]
EXPLORE THESE BRANCHES:
Branch 1: [approach name]
Branch 2: [approach name]
Branch 3: [approach name]
For each: describe approach / work through reasoning / strengths / weaknesses / risks.
EVALUATION CRITERIA: [what matters most, in priority order]
CONCLUSION: [select best branch with reasoning, or explain trade-offs]
```

### RCoT — Reverse Chain-of-Thought Verification
```
STEP 1: Answer this question step-by-step: [QUESTION with all conditions]
STEP 2: Looking only at your answer (not the question), reconstruct what
the question must have contained — every condition and constraint.
STEP 3: Compare reconstructed vs. actual question. Identify overlooked
conditions or assumptions not stated.
STEP 4: If discrepancies found, generate corrected answer. If none, confirm.
```

---

## CRITIQUE Family

### CAI Critique-Revise — Principle-Based
```
PRINCIPLE: [specific standard the output must satisfy — be precise and measurable]
INITIAL OUTPUT: [output to evaluate]
CRITIQUE: Identify passages that violate the principle. Quote each.
Explain precisely why each violates it.
REVISION: Rewrite to fully satisfy the principle. Address every critique point.
```

### Devil's Advocate
```
You are a rigorous devil's advocate. Generate the strongest possible case
AGAINST the following position. Do NOT give a balanced view.

POSITION TO ATTACK: [position, plan, or decision]
ATTACK DIMENSIONS:
1. Core assumptions (what must be true for this to work?)
2. Internal logic (where does the reasoning break down?)
3. Execution risks (what makes this fail in practice?)
4. Overlooked alternatives (what better options exist?)
SEVERITY RANKING: After the attack, list the THREE MOST FATAL flaws.
```

### Pre-Mortem — Failure Analysis
```
PROJECT/DECISION: [describe the project, timeline, resources, key goals]
FAILURE ASSUMPTION: It is [DATE] and [project] has completely failed.
It did not achieve [primary goal].
FAILURE CAUSES: Identify 8-12 specific reasons this failed.
For each — CAUSE: [what went wrong] / DOMAIN: [Technical/People/Market/Financial/External/Timeline] / WARNING SIGN: [earliest observable indicator]
PRIORITY: 3 most likely · 3 most preventable · any single point of failure
```

---

## META / REVERSE Family

### RPEF — Reverse Prompt Engineering
```
You are an expert Prompt Engineer performing reverse prompt engineering.
TASK: Analyze the following output. Reconstruct the reusable prompt template
that would consistently produce it. Use [PLACEHOLDER] for variable elements.
[INPUT DATA (if applicable):]
OUTPUT SAMPLE: [paste the output]
ANALYSIS: Examine for implied role / tone / structure / constraints / reasoning style.
RECOVERED PROMPT: Generate reusable template. Only proceed when ≥80% confident.
```

### Reverse Role Prompting — AI-Led Interview
```
You are an expert [DOMAIN] consultant.
My goal: [1-2 sentence intent]
Before you begin, interview me to understand my context, constraints, goals,
and relevant background. Ask your questions [one at a time / all at once].
Only proceed with [the task] once confident you have everything you need.
[Optional: After the interview, synthesize into a structured prompt before executing.]
```

---

## AGENTIC Family

### ReAct — Reasoning + Acting
```
GOAL: [end state to achieve — what does success look like?]
AVAILABLE TOOLS:
- [tool_name]: [what it does]
- [tool_name]: [what it does]
CONSTRAINTS: [rules / stop condition / max iterations]
APPROACH:
Thought: [reason about current state and next step]
Action: [tool_name] — [specific query or operation]
Observation: [result]
[repeat until goal reached]
Final Answer: [deliver result]
```
