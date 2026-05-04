# Output Format Reference

Canonical Phase 3 output format with annotated examples.
Load when constructing the Analysis Block + Optimized Prompt.

---

## Phase 3 Output Structure

```
[Analysis Block]
[Optimized Prompt — fenced code block]
[Execution — full response]
```

Nothing else. No preamble. No "Here is your optimized prompt:".
Start directly with the Analysis Block.

---

## Analysis Block Format

```
INTENT DETECTED:     CREATE / TRANSFORM / REASON / CRITIQUE / AGENTIC / RECOVER / CLARIFY
FRAMEWORK SELECTED:  [Framework Name] — [one-line rationale tied to specific signal in prompt]
GAPS IN ORIGINAL:    - [specific weakness 1]
                     - [specific weakness 2]
                     - [specific weakness 3]
IMPROVEMENTS MADE:   - [specific change 1 and what it adds]
                     - [specific change 2 and what it adds]
                     - [specific change 3 and what it adds]
```

**Rules:**
- Gaps must name the actual missing element (not generic labels like "too vague")
- Improvements must pair the change with its purpose ("Added audience definition
  → allows the model to calibrate vocabulary and assumed knowledge")
- 2–5 bullets each; no single-word entries

---

## Optimized Prompt Block Rules

```markdown
‎```
[optimized prompt here]
‎```
```

**Mandatory rules:**
- Flat natural prose — zero framework headers (no ROLE:, CONTEXT:, BEFORE:, etc.)
- `[PLACEHOLDER]` notation for every variable element
- Self-contained: the user can copy + paste and run immediately
- No instructions to the model about what framework is being used

**Forbidden patterns inside the block:**
```
❌  ROLE: You are a senior developer...
✓   As a senior developer with expertise in [DOMAIN]...

❌  CONTEXT: We are building a SaaS product...
✓   The product is a SaaS platform targeting [AUDIENCE]...

❌  NARROWING: Do not use deprecated libraries.
✓   Avoid deprecated libraries; use only [TECH_STACK] conventions.

❌  EXPERIMENT: Provide 3 variants.
✓   Generate 3 versions: [VARIANT_A_DIMENSION], [VARIANT_B_DIMENSION],
    and [VARIANT_C_DIMENSION].
```

---

## Annotated Example — RTF

**Original prompt:**
> "Write a function to validate emails"

**Output:**

```
INTENT DETECTED:     CREATE
FRAMEWORK SELECTED:  RTF — simple expertise-driven task; no context or audience needed
GAPS IN ORIGINAL:    - No programming language specified
                     - No validation rules defined (RFC 5321? Basic regex? MX check?)
                     - No output contract (return bool? raise exception? return error string?)
IMPROVEMENTS MADE:   - Role added → calibrates language idioms and style
                     - Language placeholder → makes prompt reusable across stacks
                     - Explicit return contract → eliminates ambiguity in output shape
                     - Edge cases listed → prevents silent failures on common inputs
```

```
As a senior [LANGUAGE] developer who writes clean, well-documented code,
implement an email validation function.

Validate against these rules:
- Contains exactly one @ symbol
- Domain has at least one dot
- No spaces anywhere
- Local part (before @) is non-empty
- Domain part (after @) is non-empty

Return a boolean. Add a docstring with parameters, return type, and
2–3 usage examples. Include edge case handling for: empty string,
None/null input, and strings with only whitespace.
```

[Execution follows immediately]

---

## Annotated Example — CO-STAR

**Original prompt:**
> "Write a blog post about AI trends"

**Output:**

```
INTENT DETECTED:     CREATE
FRAMEWORK SELECTED:  CO-STAR — writing task where audience/tone/style are critical
GAPS IN ORIGINAL:    - No audience defined (developers? executives? consumers?)
                     - No specific angle or thesis
                     - No tone guidance (authoritative? accessible? opinionated?)
                     - No length or structure requirements
IMPROVEMENTS MADE:   - Audience defined → allows vocabulary and assumed-knowledge calibration
                     - Specific thesis added → prevents generic list articles
                     - Tone specified → ensures consistent voice throughout
                     - Structure defined → 800w with sections and CTA
```

```
You are writing for [TARGET_PUBLICATION], a newsletter read by senior product
managers at B2B SaaS companies. Readers are technically literate but not
engineers; they care about business implications over implementation details.

Write an 800-word article arguing that [SPECIFIC_AI_TREND] will reshape
[SPECIFIC_BUSINESS_PROCESS] within 18 months. Take a clear position —
do not hedge every claim.

Structure: hook paragraph (no more than 3 sentences), 3 main sections
with subheadings, closing paragraph with one concrete action the reader
should take this quarter.

Tone: confident, evidence-backed, occasionally contrarian. Avoid:
AI hype language, passive voice, and generic "AI will change everything"
framing.
```

[Execution follows immediately]

---

## Annotated Example — BAB (TRANSFORM)

**Original prompt:**
> "Rewrite this email to sound better"

**Output:**

```
INTENT DETECTED:     TRANSFORM
FRAMEWORK SELECTED:  BAB — existing content with clear before/after state
GAPS IN ORIGINAL:    - "Better" is undefined (more formal? less stiff? shorter?)
                     - No audience specified for the email
                     - No constraints on what to preserve
IMPROVEMENTS MADE:   - Defined current failure mode (passive, stiff)
                     - Defined target voice (direct, peer-to-peer)
                     - Explicit preservation rule (facts must remain unchanged)
                     - Tone and length constraints added
```

```
Rewrite the following email. The current version is written in passive voice,
uses corporate jargon, and feels stiff — it reads like legal boilerplate
rather than a human message.

[PASTE ORIGINAL EMAIL HERE]

The rewritten version should sound like it was written by a thoughtful
colleague, not a legal department. Use active voice throughout. Replace
all corporate jargon with plain language (e.g., "leverage" → "use").
Keep all factual information and commitments unchanged.

Target tone: direct, warm, professional.
Target length: same or shorter than the original.
```

[Execution follows immediately]

---

## Execution Section

The execution section immediately follows the code block.
No separator, no header, no "Now executing:".

Format:
```
[Analysis Block]

```[optimized prompt]```

[Full response to the optimized prompt, starting immediately]
```

If the optimized prompt requests a deliverable (article, code, analysis),
deliver it in full. Never summarize, never plan, never say "I would now...".
