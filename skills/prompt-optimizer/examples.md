# Framework Examples — One Filled Prompt per Framework

Each example shows a complete, copy-pasteable prompt.
No framework headers inside — flattened to natural prose as Phase 3B requires.

---

## CREATE Family

### APE

```
Translate the following error message into plain German suitable for a
non-technical end user. It will appear as a toast notification in a SaaS
dashboard. Keep it under 15 words, warm and solution-focused.

[ERROR_MESSAGE]
```

---

### RTF

```
As a senior Python developer who writes clean, well-documented code,
refactor the function below to replace nested callbacks with async/await,
add proper error handling, and include a docstring with usage example.

Format: return only the refactored function in a Python code block,
followed by a 2-sentence explanation of the key changes.

[FUNCTION_CODE]
```

---

### CTF

```
We are three days from a product launch and our lead copywriter is
unavailable. The landing page headline currently reads "Advanced Analytics
Platform" — written by engineers. The target buyer is a non-technical
operations manager at a mid-size company who cares about saving time.

Write a replacement headline (max 8 words) and one supporting subheadline
(max 20 words) that communicate business value without technical jargon.

Deliver as: Headline / Subheadline — no other commentary.
```

---

### RACE

```
You are a senior API architect with deep expertise in REST design and
developer experience.

Review the API endpoint definitions below for consistency, naming
conventions, and potential versioning issues. Flag anything that would
create breaking changes or frustrate third-party developers.

This API will be made public in 30 days. The team is small (3 engineers),
has no prior public API experience, and cannot make breaking changes
after launch.

Return a prioritized list of issues: severity (Critical / High / Medium),
the specific problem, and a concrete fix for each. Focus on Critical and
High first.

[API_DEFINITIONS]
```

---

### CRISPE

```
Act as an expert B2B SaaS copywriter with 10+ years experience writing
trial-to-paid email sequences.

Background: Our project management tool for engineering teams has a 14-day
free trial. Current trial-to-paid conversion sits at 12%. Data shows most
conversions happen on days 3–5 or not at all. Key value props: GitHub
integration, sprint planning, automated reporting.

Write a Day 4 mid-trial activation email targeting engineering team leads.

Voice: direct and peer-to-peer — like advice from a fellow engineer,
not a sales rep. Short. Respect the reader's time.

Provide 2 versions: one leading with a feature-value hook (GitHub
integration), one leading with a social proof hook (what teams achieved
in their first sprint).
```

---

### BROKE

```
We are a B2B SaaS company (40 employees, $3M ARR) selling to mid-market
operations teams. Average deal size $24K ARR. Sales cycle has lengthened
from 45 to 90 days over the last 2 quarters. Win rate holds at 28% —
the problem is not qualification, it's cycle time. Primary bottleneck:
legal review now averages 35 days after verbal agreement.

You are an experienced enterprise SaaS sales consultant who specializes
in deal velocity and friction reduction at the close stage.

Identify the root causes of the 35-day legal review bottleneck and
provide a prioritized action plan to cut it in half within two quarters.

Key results to drive:
- Reduce legal review from 35 to 15 days within 2 quarters
- Reduce sales rep time on legal coordination by 50%
- Increase win rate from 28% to 32% by removing close-stage friction

After your response, provide 3 specific suggestions for how this analysis
or action plan could be improved with additional data or a different approach.
```

---

### CARE

```
I am a UX researcher at a healthcare startup preparing a remote moderated
usability study on our patient-facing mobile app's medication reminder flow.
Participants are adults aged 45–70 who are comfortable with smartphones
but not technically sophisticated.

Write 6 post-task interview questions probing comprehension, confidence,
and friction in the reminder-setup flow.

Rules:
- All questions must be open-ended — no yes/no
- Use plain everyday language — no UX or medical jargon
- Do not suggest answers inside the question (no leading questions)
- Each question addresses exactly one thing
- Avoid "why" phrasing — use "what made you..." instead
- Maximum 15 words per question

Example of a good question: "What went through your mind when you reached
the confirmation screen?"
Example of a bad question: "Was the confirmation screen clear and easy
to understand?"
```

---

### CO-STAR

```
We are a 10-person developer tools startup. This is part of a blog series
on engineering productivity. Previous posts covered async communication
and code review culture; this post covers AI-assisted development.

Write an 800-word article that argues AI coding assistants change what
skills matter for junior developers — not that they replace juniors.

Use a conversational technical blog style: short paragraphs (2–3 sentences),
subheadings every 150–200 words, one concrete anecdote to open.

Tone: honest and slightly contrarian — challenge the "AI replaces juniors"
narrative without dismissing real concerns.

Audience: senior engineers and engineering managers who are skeptical of
AI hype but genuinely curious about team impact.

Structure: hook anecdote → thesis → 3 supporting sections with subheadings
→ practical takeaway → 1-sentence closer. No bullet-point lists.
```

---

### RISEN

```
You are a senior security engineer with expertise in OWASP Top 10 and
Node.js/Express application security.

Conduct a security-focused code review prioritizing vulnerability
identification over style issues. Apply OWASP guidelines throughout.

Steps:
1. Scan for injection vulnerabilities (SQL, NoSQL, command injection)
2. Review authentication and session management logic
3. Examine all input validation and sanitization
4. Check for sensitive data exposure (logging, responses, headers)
5. Assess third-party dependency risks
6. Evaluate error handling — ensure stack traces never reach clients
7. Document each finding with file path, line number, severity, and fix

End goal: A security assessment report categorizing findings as Critical /
High / Medium / Low, with concrete remediation steps, prioritized by
risk-to-effort ratio. Suitable for sharing with the development team.

Narrowing:
- Do NOT flag style or formatting issues
- Do NOT suggest complete rewrites — targeted fixes only
- Avoid generic advice; all findings must reference specific code locations
- Do NOT redesign the architecture
- Out of scope: performance optimization, test coverage

[CODEBASE]
```

---

### TIDD-EC

```
Task type: Customer Support Response — Billing Complaint Resolution

Steps:
1. Acknowledge the customer's frustration and validate their concern
2. Apologize clearly in the first sentence
3. Explain what happened in plain language (if known)
4. Provide one concrete resolution with a specific timeline
5. Close with a direct follow-up contact option

DO:
- Address the customer by first name
- State the exact refund amount and processing time (3–5 business days)
- Use active voice throughout
- Keep response between 120–180 words
- End with a single clear call to action

DON'T:
- Use passive voice ("mistakes were made")
- Include ticket numbers or internal system references
- Make promises outside our refund policy
- Use template phrases like "We apologize for any inconvenience"
- Exceed 180 words

Example of a good response:
"Hi Sarah, I'm truly sorry — you were charged twice for your March
subscription due to a system error on our end. I've already processed
a full $49 refund to your original payment method; you'll see it within
3–5 business days. I've also added a $10 credit to your account as an
apology. If you have any questions, reply here or reach me directly at
support@company.com. — Alex"

Context: Premium subscriber, 2-year customer, overcharged $49 this month,
first billing issue in account history. Company policy: full refund + $10
credit for billing errors.

[CUSTOMER_MESSAGE]
```

---

### RISE-IE

```
You are a customer insights analyst specializing in sentiment analysis
and theme extraction.

You will receive 50 app store reviews for a B2B mobile app. Each review
contains a star rating (1–5), written feedback, date, and user segment
(free / premium).

Steps:
1. Categorize each review by sentiment: Positive / Neutral / Negative
2. Extract recurring themes and topics (aim for 5–8 distinct themes)
3. Separate feature requests from complaints from praise
4. Segment findings by user type (free vs. premium)
5. Flag any issue mentioned 3+ times as urgent

Return a structured analysis with:
- Sentiment distribution table (count + percentage per category)
- Top 5 themes ranked by frequency with representative quotes
- Feature request list ranked by mention count
- Critical issues list (urgent flags only)
- Free vs. premium comparison paragraph
- 3 actionable recommendations

[REVIEWS_DATA]
```

---

### RISE-IX

```
You are a senior technical writer specializing in developer documentation
for public REST APIs.

Write the complete reference documentation for the POST /charges endpoint
of a payment processing API. Cover: endpoint overview, authentication
requirements, request body parameters (as a table), response codes with
meanings, a curl example request, a JSON example response, and a common
errors section.

Steps:
1. Open with a one-sentence endpoint description
2. State auth requirements (Bearer token, OAuth scope needed)
3. Build the parameters table: Name / Type / Required / Description
4. List all response codes developers will encounter
5. Show a complete, copy-pasteable curl example
6. Show the full JSON response for a successful charge
7. List the 3 most common errors with cause and fix

Example of the desired tone and structure — modeled on Stripe's API docs:
"Retrieves a PaymentIntent object. Supply the unique PaymentIntent ID,
and Stripe returns the corresponding PaymentIntent object."

Second style reference — concise parameter tables like:
| amount | integer | Required | Amount in smallest currency unit (e.g., cents) |
```

---

## TRANSFORM Family

### BAB

```
The JavaScript function below uses nested callbacks three levels deep.
It fetches user data, then fetches their orders, then fetches order details.
It is difficult to read, nearly impossible to unit test, and any error
swallows the full stack trace.

The function should use async/await with a single top-level try/catch,
preserve all existing API call structure and variable names, and be
readable by a junior developer unfamiliar with the original code.

Transformation rules:
- Replace callback nesting with async/await — no Promises directly
- Add one top-level try/catch; do not nest additional try/catch blocks
- Keep all existing variable names and API endpoint paths unchanged
- Add inline comments explaining the async flow (one per logical step)
- Do not change the function signature or its return value

[FUNCTION_CODE]
```

---

### Self-Refine

```
Review the following technical proposal draft and improve it.

[DRAFT]

Evaluate the draft across these dimensions:
1. Clarity — are there sentences that require re-reading or could be
   misunderstood by a non-technical stakeholder?
2. Completeness — what important scenarios, risks, or stakeholders
   are not addressed?
3. Logical flow — does the argument build coherently from problem
   to solution to recommendation?
4. Conciseness — what can be removed without losing meaning?

For each dimension: quote specific problematic passages, explain the
issue in one sentence, and suggest a concrete improvement.

Then rewrite the full proposal incorporating every point of feedback.
Show the revised version only — no commentary after it.
```

---

### Chain of Density

```
Compress the following architecture decision record into progressively
denser versions without losing any decision rationale or constraint.

[ADR_DOCUMENT]

Optimization goal: maximum information density — every word must earn
its place. Remove filler, redundancy, and transitional prose.

Run 3 iterations:
Iteration 1: reduce by ~25%, preserve all key decisions and constraints
Iteration 2: reduce by another ~25%, eliminate all filler phrases
Iteration 3: final pass — tightest possible version that still makes
             sense to a reader who wasn't in the original discussion

Stop condition: 3 iterations complete or word count drops below 150.
Output format: clean prose paragraphs.
Show all three iterations so the evolution is visible.
```

---

### Skeleton of Thought

```
Phase 1 — Skeleton:
Generate a skeleton outline for an explanation of event-driven architecture
for a senior engineer evaluating whether to migrate a monolithic backend.
List exactly 6–8 key points in this format:
N. [concept name] | [one sentence describing what this point covers]
Do not expand yet. Skeleton only.

Phase 2 — Expand:
Expand each skeleton point into 2–3 paragraphs. Each section must be
self-contained — a reader should understand it without reading the others.
Include at least one concrete trade-off per point relevant to a migration
decision from a monolith.
```

---

## REASON Family

### Plan-and-Solve PS+

```
A SaaS company starts Q1 with 500 customers paying $200/month. Monthly
churn is 5%. They acquire 30 new customers each month. What is their
MRR at the end of month 6, and what is the net customer count change
over that period?

Let's first understand the problem, extract relevant variables and their
corresponding numerals, and devise a complete plan. Then, let's carry out
the plan, calculate intermediate values, pay attention to computation,
and solve the problem step by step.
```

---

### Chain of Thought

```
Our API endpoint averages 800ms response time. Target is under 200ms.
The stack is Node.js + PostgreSQL. No caching layer exists. Database
queries average 600ms per request. The service is read-heavy — 90%
of requests are product catalog lookups.

Diagnose this step-by-step:
1. Identify what the 600ms database time likely consists of (query
   planning, data transfer, index misses — reason through each)
2. Identify the highest-leverage optimization for the specific profile
   described (read-heavy, no cache, PostgreSQL)
3. Estimate the realistic latency reduction from that optimization
4. Identify the next highest-leverage change after that

For each step: state your reasoning before stating your conclusion.
Verify each intermediate conclusion before continuing.
Final answer: a prioritized 3-step optimization plan with expected
latency impact per step.
```

---

### Least-to-Most

```
Problem: What are the full tax implications for a US citizen employed
by a US company who works remotely from Portugal for 90 days in a
single calendar year?

Decompose into ordered subproblems, simplest prerequisite first:

Subproblem 1: What are the basic US tax rules for citizens earning
income while abroad — including FEIE and FTC fundamentals?

Subproblem 2: What is Portugal's rule for when a foreign visitor
becomes a tax resident — specifically the day-count threshold?

Subproblem 3: Does 90 days in Portugal trigger Portuguese tax
residency? (Use answers from 1 and 2)

Subproblem 4: If both US and Portuguese obligations could apply,
what does the US-Portugal tax treaty say about double taxation?

Final: Given all of the above, what are the practical implications
and what should the employee do before the trip?

Solve each subproblem in order. Use prior answers as explicit context
for each subsequent subproblem. Show each solution before continuing.
```

---

### Step-Back

```
Original question: Should we use event sourcing for our order management
service, given that we have a 5-person engineering team, PostgreSQL as
our primary datastore, and a 3-month delivery deadline?

Step-back: Before answering, first answer this higher-level question:
What are the fundamental architectural trade-offs of event sourcing —
specifically around operational complexity, consistency guarantees,
and team skill requirements — and under what conditions does it provide
net value over a traditional CRUD approach?

Principle application: Using those principles, now evaluate the specific
scenario: 5-person team, PostgreSQL, 3-month deadline. Should we use
event sourcing for the order management service? State the single
biggest assumption that could change your recommendation.
```

---

### Tree of Thought

```
We are deciding on a primary database for a real-time collaborative
document editor. Constraints: 10-person team (most with SQL experience),
6-month delivery timeline, expected 100k users at launch, must support
real-time sync, offline mode, and conflict resolution.

Explore these three branches:

Branch 1: PostgreSQL with operational transforms
Branch 2: CRDTs with a document store (e.g., Firestore)
Branch 3: Event sourcing with an append-only log (e.g., EventStoreDB)

For each branch: describe the approach / how it handles real-time sync
and conflict resolution / team learning curve / operational complexity
at 100k users / known production use cases for this pattern.

Evaluation criteria (in priority order):
1. Correctness of conflict resolution under concurrent edits
2. Team ability to ship in 6 months
3. Scalability ceiling beyond 100k users

Conclusion: recommend one branch with clear reasoning. State the single
biggest assumption that, if wrong, would change the recommendation.
```

---

### RCoT

```
Step 1 — Answer:
A store offers 20% off, then an additional 15% off the discounted price.
A customer also has a $10 flat coupon applied after both percentage
discounts. The original item price is $120. What does the customer pay?
Work through this step-by-step.

Step 2 — Reconstruction:
Looking only at your answer above (do not re-read the question),
reconstruct the question that must have produced this answer.
List every condition, constraint, and number the question must have
contained.

Step 3 — Cross-check:
Compare your reconstructed question to the original above.
Identify any conditions present in the original but missing from your
reconstruction (overlooked in reasoning) and any assumptions you made
that were not stated.