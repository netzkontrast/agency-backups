# Framework Components Reference

Quick-access component definitions for all 27 frameworks.
Load when filling framework fields during Phase 3 prompt construction.

---

## CREATE Family

### APE — Action · Purpose · Expectation
| Component | Fill With |
|-----------|-----------|
| Action | One verb-driven instruction — what to do |
| Purpose | Why it's needed — one sentence on use/audience |
| Expectation | Quality bar — format, length, tone |

### RTF — Role · Task · Format
| Component | Fill With |
|-----------|-----------|
| Role | Expertise / perspective needed |
| Task | Exactly what needs to be done |
| Format | Output structure, length, style |

### CTF — Context · Task · Format
| Component | Fill With |
|-----------|-----------|
| Context | Situation, background, why this task exists |
| Task | The specific deliverable |
| Format | How output should be structured |

### RACE — Role · Action · Context · Expectation
| Component | Fill With |
|-----------|-----------|
| Role | Expertise / persona |
| Action | Task and deliverable |
| Context | Situation, constraints, audience |
| Expectation | What a good result looks like |

### CRISPE — Capacity+Role · Insight · Instructions · Personality · Experiment
| Component | Fill With |
|-----------|-----------|
| Capacity & Role | Expertise level + domain |
| Insight | Background context / briefing |
| Instructions | The specific task |
| Personality | Tone, voice, style |
| Experiment | N variants along which dimension |

### BROKE — Background · Role · Objective · Key Results · Evolve
| Component | Fill With |
|-----------|-----------|
| Background | Situation, history, constraints |
| Role | Professional persona |
| Objective | Specific task + deliverable |
| Key Results | Measurable KPIs / OKRs |
| Evolve | "Suggest 3 improvements after responding" |

### CARE — Context · Ask · Rules · Examples
| Component | Fill With |
|-----------|-----------|
| Context | Who you are, situation |
| Ask | Specific request |
| Rules | Combined must/must-not list |
| Examples | 1–3 reference outputs |

### CO-STAR — Context · Objective · Style · Tone · Audience · Response
| Component | Fill With |
|-----------|-----------|
| Context | Background, situation, constraints |
| Objective | Clear specific goal |
| Style | Writing style, format preferences |
| Tone | Emotional quality, formality |
| Audience | Who will read / use the output |
| Response | Format, length, structure |

### RISEN — Role · Instructions · Steps · End goal · Narrowing
| Component | Fill With |
|-----------|-----------|
| Role | Expertise / perspective |
| Instructions | Guiding principles / methodology |
| Steps | Sequential numbered actions |
| End Goal | Success criteria / acceptance criteria |
| Narrowing | Explicit do-NOT list / out-of-scope items |

### TIDD-EC — Task type · Instructions · Do · Don't · Examples · Context
| Component | Fill With |
|-----------|-----------|
| Task Type | Category of activity |
| Instructions | Specific steps to follow |
| Do | Explicit positive requirements |
| Don't | Explicit negative prohibitions |
| Examples | Concrete output samples |
| Context | Background / user-provided data |

### RISE-IE — Role · Input · Steps · Expectation
| Component | Fill With |
|-----------|-----------|
| Role | Perspective / expertise |
| Input | Data format, characteristics, quirks |
| Steps | Processing / transformation sequence |
| Expectation | Output format, required elements |

### RISE-IX — Role · Instructions · Steps · Examples
| Component | Fill With |
|-----------|-----------|
| Role | Persona / expertise level |
| Instructions | Main task + core requirements |
| Steps | Workflow / methodology |
| Examples | 2–3 reference output samples |

---

## TRANSFORM Family

### BAB — Before · After · Bridge
| Component | Fill With |
|-----------|-----------|
| Before | Current state — what exists, what's wrong |
| After | Desired end state — qualities, success |
| Bridge | Transformation rules — what to preserve/change |

### Self-Refine — Generate → Feedback → Refine
| Component | Fill With |
|-----------|-----------|
| Initial Output | First draft to improve |
| Feedback Dimensions | Specific quality axes (clarity, completeness, tone…) |
| Refinement | Rewrite addressing every feedback point |
| Stop Condition | When to stop iterating |

### Chain of Density — Iterative Compression
| Component | Fill With |
|-----------|-----------|
| Source Content | Text to compress / densify |
| Optimization Goal | What to improve per iteration |
| Iterations | Number of passes (typically 2–4) |
| Output Format | Final format |

### Skeleton of Thought — Outline First
| Component | Fill With |
|-----------|-----------|
| Skeleton | Key points, one per line, N. [name] \| [description] |
| Expansion | Per-point depth target |

---

## REASON Family

### Plan-and-Solve (PS+)
**Trigger phrase:** "Let's first understand the problem, extract relevant
variables and their corresponding numerals, and devise a complete plan.
Then, let's carry out the plan, calculate intermediate values, pay attention
to computation, and solve the problem step by step."

### Chain of Thought
**Trigger phrase:** "Think step by step." / "Show your reasoning at each stage."

### Least-to-Most
| Phase | Fill With |
|-------|-----------|
| Decompose | Ordered subproblems, simplest → most complex |
| Solve sequentially | Each answer feeds the next |

### Step-Back
| Component | Fill With |
|-----------|-----------|
| Step-Back Question | Abstract principle governing the original question |
| Principle Application | Apply retrieved principle to original |

### Tree of Thought
| Component | Fill With |
|-----------|-----------|
| Problem | What to solve, constraints |
| Branches | 2–5 distinct approaches |
| Evaluation Criteria | How to compare branches |
| Conclusion | Select best + rationale |

### RCoT — Reverse Chain-of-Thought
Four-step: Initial Answer → Reconstruct Question → Cross-Check → Correct

---

## CRITIQUE Family

### CAI Critique-Revise
| Component | Fill With |
|-----------|-----------|
| Principle | Specific standard to enforce |
| Initial Output | Output to critique |
| Critique | Quote violations, explain why |
| Revision | Rewrite satisfying the principle |

### Devil's Advocate
| Component | Fill With |
|-----------|-----------|
| Position to Attack | The argument / plan / decision |
| Attack Dimensions | Assumptions · logic · risks · alternatives |
| Severity Ranking | Top 3 most fatal flaws |

### Pre-Mortem
| Component | Fill With |
|-----------|-----------|
| Project / Decision | What is being analyzed |
| Future Date | Time horizon for the failure |
| Failure Assumption | "Has already failed catastrophically" |
| Domain Analysis | Technical · People · Market · Financial · External |
| Warning Signs | Earliest observable indicators |

---

## META / AGENTIC Family

### RPEF — Reverse Prompt Engineering
| Component | Fill With |
|-----------|-----------|
| Input Sample | Input that produced the output (optional) |
| Output Sample | Output to reverse-engineer |
| Analysis Instructions | Tone · structure · implicit constraints |
| Recovered Prompt | Reusable template with `[PLACEHOLDER]` |

### Reverse Role Prompting
| Component | Fill With |
|-----------|-----------|
| Intent Statement | 1–2 sentence goal |
| Interview Trigger | "Ask me all questions before responding" |
| Mode | FATA (batch) or conversational |

### ReAct — Reasoning + Acting
| Component | Fill With |
|-----------|-----------|
| Goal | End state / success definition |
| Available Tools | Name + description of each tool |
| Constraints | Rules, stop conditions, max iterations |
| Cycle | Thought → Action → Observation (repeat) |
