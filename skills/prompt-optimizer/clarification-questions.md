# Clarification Questions — Per-Framework Catalog

Reference for Phase 2: if a critical gap blocks framework selection or
component filling, ask exactly ONE question from this catalog.

Priority rule: ask the question that unlocks the most framework components.
Never ask more than one question. Never ask what can be inferred.

---

## CREATE Family

### APE
1. What is the core action to take?
2. Why is this needed — how will it be used?
3. What does a good result look like (format, length, quality bar)?

### RTF
1. What expertise or perspective is needed?
2. What exactly needs to be done?
3. How should the output be formatted?

### CTF
1. What is the current situation or background?
2. What exactly needs to be done?
3. How should the output be formatted?

### RACE
1. What role or expertise should be embodied?
2. What exactly needs to be done?
3. What is the background and constraints?
4. What does a successful output look like?

### CRISPE
1. What expertise level and role should be embodied?
2. What background context is needed?
3. What are the specific instructions?
4. What tone and personality should the output have?
5. **Key discriminator:** How many variants to compare, and along what dimension?

### BROKE
1. What is the current situation and background?
2. What is the specific objective/deliverable?
3. **Key discriminator:** What measurable business outcomes should this drive?
4. Should the AI suggest 3 improvements after responding?

### CARE
1. What is the situation and background?
2. What is the specific request?
3. **Key discriminator:** What rules or constraints govern the output?
4. Can you provide 1-3 examples showing desired quality or style?

### CO-STAR
1. What is the background context?
2. What is the specific goal?
3. What writing style or format is needed?
4. What tone is appropriate?
5. **Key discriminator:** Who is the target audience — expertise level, characteristics?
6. How should the response be structured?

### RISEN
1. What role or expertise level should be demonstrated?
2. What principles or guidelines should guide the approach?
3. What are the specific steps or sequence of actions?
4. What defines success?
5. **Key discriminator:** What should be avoided? What are the hard constraints?

### TIDD-EC
1. What type of task is this?
2. What are the exact instructions?
3. **Key discriminator:** What MUST be included? (explicit Do list)
4. **Key discriminator:** What must be AVOIDED? (explicit Don't list)
5. Can you provide examples of good output?
6. What context or background is relevant?

### RISE-IE
1. What role or perspective is needed?
2. **Key discriminator:** What input are you providing — format, structure, characteristics?
3. What processing or transformation steps are needed?
4. What should the output look like?

### RISE-IX
1. What role or persona is most appropriate?
2. What are the main instructions?
3. What workflow or steps should be followed?
4. **Key discriminator:** Can you provide 2-3 examples of desired output or style?

---

## TRANSFORM Family

### BAB
1. **Key discriminator:** What is the current state — what exists, what's wrong?
2. What should it become — the desired end state?
3. What rules govern the transformation — what to preserve, what to change?

### Self-Refine
1. What output needs to be improved?
2. **Key discriminator:** What dimensions to evaluate — clarity, completeness, tone, security?
3. How many refinement cycles, and what's the stop condition?

### Chain of Density
1. What content needs to be compressed or densified?
2. **Key discriminator:** What should each iteration optimize for?
3. How many iterations, and what's the stopping criterion?

### Skeleton of Thought
1. What is the topic or question to structure?
2. **Key discriminator:** How many skeleton points — typically 5-8?
3. How deeply should each point be expanded?

---

## REASON Family

### Plan-and-Solve PS+
1. **Key discriminator:** What is the full problem including all relevant numbers and variables?

### Chain of Thought
1. What problem needs to be reasoned through?
2. Should intermediate reasoning steps be shown?

### Least-to-Most
1. What is the full complex problem?
2. **Key discriminator:** What are the simpler prerequisite subproblems, in dependency order?

### Step-Back
1. What is the specific question?
2. **Key discriminator:** What higher-level principle or concept governs this question?

### Tree of Thought
1. What decision or problem needs to be solved?
2. **Key discriminator:** What are the 2-5 distinct approaches to explore?
3. What criteria should be used to evaluate each branch?

### RCoT
1. What is the question with all its conditions?
2. Do you have an initial answer to verify, or should one be generated first?

---

## CRITIQUE Family

### CAI Critique-Revise
1. **Key discriminator:** What is the specific principle or standard to enforce?
2. What output should be critiqued against this principle?

### Devil's Advocate
1. **Key discriminator:** What position, plan, or decision should be attacked?
2. What dimensions to attack?
3. Should the 3 most fatal flaws be ranked at the end?

### Pre-Mortem
1. What project or decision is being analyzed?
2. **Key discriminator:** What time horizon?
3. What domains to cover?

---

## META / REVERSE Family

### RPEF
1. **Key discriminator:** What output do you want to reverse-engineer?
2. Do you have the input that produced this output?
3. Should the recovered prompt be specific or a generalized template?

### Reverse Role Prompting
1. What is your goal in 1-2 sentences?
2. **Key discriminator:** What domain or expertise should the AI bring?
3. Batch questions (all at once) or conversational (one at a time)?

---

## AGENTIC Family

### ReAct
1. What is the goal to achieve?
2. **Key discriminator:** What tools are available?
3. What constraints apply — max iterations, stop conditions?

---

## One-Question Priority Rules

When in doubt which single question to ask, the **Key discriminator** markers
above show which question unlocks the most framework components.

General priority:
1. Questions that determine WHICH framework to use
2. Questions that fill the unique/defining component of the selected framework
3. Questions about constraints and success criteria
4. Questions about format (lowest priority — often inferrable)
