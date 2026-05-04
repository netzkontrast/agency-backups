# Anti-Patterns Reference

Common prompt weaknesses and their fixes.
Load during Phase 3 gap identification to name problems precisely.

---

## The 10 Critical Anti-Patterns

### 1. Vague Qualifier (most common)
**Signal:** "good", "appropriate", "correct", "better", "nice", "clean"
**Problem:** Subjective terms force the model to guess success criteria.
**Fix:** Replace with measurable criteria.

```
❌  "Write a good analysis"
✓   "Write a 400-word analysis covering: current state, 3 risks, 2 recommendations"
```

---

### 2. Missing Output Contract
**Signal:** No mention of format, length, structure, or return type.
**Problem:** Model chooses arbitrarily; results are inconsistent.
**Fix:** Specify format + length + structure explicitly.

```
❌  "Summarize this document"
✓   "Summarize in 3 bullet points (max 20 words each), focus on action items"
```

---

### 3. Assumed Context
**Signal:** "the usual format", "as discussed", "the standard approach", pronouns without antecedents.
**Problem:** Model lacks access to implicit knowledge; forced to hallucinate.
**Fix:** Make all context explicit; define all terms.

```
❌  "Fix the problem in this code"
✓   "Fix the null pointer exception on line 47 when user input is empty"
```

---

### 4. Missing Audience
**Signal:** Writing / content task with no mention of reader.
**Problem:** Model cannot calibrate vocabulary, assumed knowledge, or tone.
**Fix:** Define audience expertise level, role, and what they care about.

```
❌  "Write a blog post about machine learning"
✓   "Write for non-technical product managers who need to evaluate ML vendor claims"
```

---

### 5. Contradictory Requirements
**Signal:** "be thorough but brief", "be creative but stick to the template"
**Problem:** Creates impossible constraints; model satisfies neither.
**Fix:** Clarify priorities or separate into sequential phases.

```
❌  "Be comprehensive but keep it under 100 words"
✓   "3-bullet executive summary first, then detailed analysis below"
```

---

### 6. No Role / Expertise Frame
**Signal:** Direct task instruction with no persona.
**Problem:** Model defaults to generic assistant mode; misses domain-specific idioms.
**Fix:** Add role only when expertise materially affects output quality.

```
❌  "Review this code for security issues"
✓   "As a senior security engineer, review for OWASP Top 10 vulnerabilities"
```

---

### 7. Scope Creep (Kitchen Sink)
**Signal:** "analyze from every angle", "consider all perspectives", "be thorough"
**Problem:** Dilutes focus; important insights get buried in noise.
**Fix:** Enumerate specific required dimensions only.

```
❌  "Analyze from every possible angle"
✓   "Analyze technical feasibility and business impact only"
```

---

### 8. Missing Constraints
**Signal:** Open-ended task with no limits, no "what NOT to do".
**Problem:** Model expands to fill available space; output overshoots need.
**Fix:** Add explicit scope boundaries and exclusions.

```
❌  "Write a function that handles user authentication"
✓   "Implement only the JWT verification step; exclude login UI and session storage"
```

---

### 9. False Precision
**Signal:** "rate this 1–100", "give exactly 7.5 examples"
**Problem:** Implies precision that doesn't exist; creates false confidence.
**Fix:** Use appropriate granularity.

```
❌  "Rate this code quality 1–100"
✓   "Rate as: Poor / Acceptable / Good / Excellent"
```

---

### 10. No Examples When Pattern is Non-Obvious
**Signal:** Creative task, unique format, or style requirement with no reference.
**Problem:** Model defaults to generic patterns; misses specific style target.
**Fix:** Provide 1–2 examples when the pattern is harder to describe than to show.

```
❌  "Write product descriptions in our brand voice"
✓   "Write product descriptions in our brand voice. Example: [paste example]"
```

---

## Gap Severity Classification

Use this when writing the `GAPS IN ORIGINAL` block:

| Severity | Label | Meaning |
|----------|-------|---------|
| **Critical** | [C] | Prevents correct output; model must guess fundamental parameters |
| **Major** | [M] | Causes inconsistent output; significant quality risk |
| **Minor** | [m] | Affects polish; output still usable |

**Example:**
```
GAPS IN ORIGINAL:    - [C] No output format defined — model cannot know return type
                     - [M] Audience unspecified — tone and vocabulary uncalibrated
                     - [m] No length constraint — risk of over-generation
```

---

## Quick Gap Checklist

Before writing the Analysis Block, scan the original prompt for:

- [ ] Output format / structure specified?
- [ ] Length or scope constraint present?
- [ ] Audience or consumer of output defined?
- [ ] Role / expertise frame needed and present?
- [ ] Success criteria measurable?
- [ ] Contradictory requirements present?
- [ ] Implicit context or assumed knowledge?
- [ ] Examples needed for non-obvious pattern?
- [ ] Explicit exclusions / "do NOT" boundaries?
- [ ] Variable elements identified and marked?
