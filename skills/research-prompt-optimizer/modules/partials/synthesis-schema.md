# Partial — Synthesis Schema

> The Synthesis section template that the executing AI fills at the
> very end of the run, after the Pre-Synthesis Integrity Check (M4)
> has passed. The schema is **category-specific** for the main body
> but shares a common scaffolding around it.

---

## Slot Definitions

```yaml
slots:
  category_specific_main_body:
    type: phase2_fill
    fill_strategy: "by_category"
    by_category_map:
      A: "Hypothesis Tree"
      B: "Output Matrix / Comparison Table"
      C: "Periodic Brief / Lifecycle Update"
  query_expansion_log_required: { type: literal, value: true }
  reflection_history_required: { type: literal, value: true }
  cross_pollination_log_required: { type: literal, value: true }
  contradiction_log_required: { type: literal, value: true }
  world_change_log_required:
    type: fill_from
    fill_from: "category"
    required_when: "category == 'C' OR cross_pollination contains 'c-into-b'"
```

---

## Rendered Output Template

```markdown
## SYNTHESIS — Final Output

You have completed the Pre-Synthesis Integrity Check. Now write the
synthesis filling the schema below. Every section is required unless
explicitly marked optional.

---

### Executive Summary
1–2 paragraphs. The single most important finding plus the next-most
important. No more than 200 words.

### Key Findings
Numbered list of the principal findings, each with:
- The finding in one sentence
- Confidence level (LOW / MEDIUM / HIGH)
- Top 2-3 sources by relevance
- Any caveats or single-source flags

### {{category_specific_main_body}}
{{category_specific_main_body_content_directive}}

### Contradictions Encountered
From your Method M07 Contradiction Log. For each contradiction:
- The two (or more) conflicting claims
- The sources
- Your characterisation of *why* the disagreement (methodology /
  time period / definitional / genuine empirical dispute)
- What additional evidence would resolve it

If no contradictions: write *"No contradictions encountered during this
research"* — but only after explicitly checking. Silence here without
verification is a Method M07 violation.

{{world_change_log_section_or_empty}}

### Query Expansion Log (Method M13)
The full log of adversarial query expansions. For each expansion entry:
- Axis (adjacent / opposing / abstraction / orthogonal)
- The new query
- Whether the search returned novel findings not covered by the seed
- Whether those findings modified a tentative conclusion

This section is mandatory regardless of category. An empty log indicates
M13 was not invoked, which is a Pre-Synthesis Integrity Check failure
(item 4) that must be repaired before delivery.

### Reflection History (Constraint Block 0)
All reflection entries written during this run, in chronological order,
verbatim as written. This includes:
- Kickoff reflection
- Mid-run reflection
- Post-Query-Expansion reflections (one per M13 pass)
- Pre-synthesis reflection
- Post-synthesis reflection (written *after* this Synthesis is drafted,
  appended below)

Reflections were written in writing during the run. If any are missing
here, the run is incomplete.

### Cross-Pollination Log (Phase 2b)
The two cross-pollinated steps from Phase 2b — what they returned and
whether they modified the final answer. Format per import:
- Source category (A / B / C)
- Step ID and title
- What it surfaced
- Did it change the conclusion? (yes / no / partially — explain)

### Open Questions / Unresolved
What this research could *not* settle. Be explicit. "We do not know"
is a legitimate finding when documented honestly.

### Sources
Structured source list:
- **Primary sources** first (peer-reviewed, official, primary documents)
- **Secondary sources** next (analyses, reports with editorial accountability)
- **Aggregators** last (only if used as discovery aids, not as evidence)

For each source: title, author/org, date, URL/citation, type tag.

### Methodology Note
Brief audit:
- Which critical-thinking methods were applied (refer by short anchor)
- Which methods were active for which findings
- Any "unanchored" / "single-source" / "unable to steelman" flags
- Total search iterations
- Any Pre-Synthesis Integrity Check items that flagged

This methodology note is the auditability handle — it is what allows
a reader to assess the trustworthiness of the synthesis without
re-running the research themselves.
```

---

## Category-Specific Main Body Sub-Templates

The `{{category_specific_main_body_content_directive}}` slot is filled
based on category. Each sub-template lives inside the corresponding
category inline-block file (`modules/categories/<category>.md`), but
the headers below stay consistent across runs:

### For Category A — Hypothesis Tree

```
A tree showing:
- All hypotheses considered (root level: alternatives)
- For each: evidence found, evidence against, status (confirmed /
  refuted / surviving)
- Branches abandoned and why
- The surviving branch with its triangulated evidence (per
  cross-pollination from Category B)
- The hypothesis half-life audit results (per cross-pollination
  from Category C)
```

### For Category B — Output Matrix

```
The locked output schema, fully populated. For each row:
- Every schema field has a value or "not found — [reason]"
- Sources cited per field
- World-Change Annotations where the cross-pollination from C fired
- The hidden-items / schema-gap candidates from cross-pollination
  from A (if any) listed in a separate "Out-of-Scope Candidates"
  table below the main matrix
```

### For Category C — Periodic Brief

```
Per-session record (this session):
- Session ID, date, active question at session start
- Assumption-Decay Audit result (PASS / FAIL / PARTIAL with detail)
- Findings added this session
- Contradictions logged
- World-change events
- Reflection entries written
- Query expansions invoked
- Cross-session diff (per cross-pollination from B): fields unchanged,
  fields with new evidence, fields whose values reversed
- Framing trial result (per cross-pollination from A, if active this
  session)
- Session-End Summary
```

---

## Why This Schema

The schema enforces auditability. A reader of the synthesis can
verify, without re-running the research:

- Were sources triangulated? → Sources section + Methodology Note
- Were contradictions handled? → Contradictions Encountered section
- Was M13 actually invoked? → Query Expansion Log
- Were reflections actually written? → Reflection History
- Did cross-pollination actually run? → Cross-Pollination Log
- Did world-change events show up? → World-Change Log (Cat C / b-into-c)

Each section answers one auditability question. Removing a section
removes a verification handle.
