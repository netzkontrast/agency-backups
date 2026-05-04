---
type: cross_pollination
inject_into_category: B
source_category: A
full_name: Exploration Sanity Pass (Hidden-items + Schema-gap)
selected_when: category == B
slots: {}
id: a-into-b
file: modules/cross-pollination/a-into-b.md
---

# Cross-Pollination: Category A → Category B

> Inject into an **Extraction** prompt (primary = B). Guards against
> the core B failure mode: "the list of items is complete and the
> schema is right" being silently wrong.

## Paste-Ready Injection — One Step (minimum) into the Steps section

```markdown
### Step [i.a] — Exploration Sanity Pass (cross-pollination from Category A)

This step imports one sanity pass from Category A (Exploration) because
even a well-scoped extraction can miss items that belong in the list
but were never named, or can lock on a schema that hides the real
variation.

Perform the following before finalizing any batch result:

1. **Hidden-items query.** Run one orthogonal search designed to find
   items that would belong in the list but were not in the original
   input. Phrase it as: *"[item type] that [trait that would make it
   qualify] but is rarely included in typical lists of [item type]"*.
   If the query returns a credible candidate, raise it as an
   **Out-of-Scope Candidate** in the Contradiction Log with the note:
   *"Item [NAME] appears to satisfy the inclusion criteria but is not
   in the input list."*

2. **Schema-gap hypothesis.** Write down one hypothesis of the form:
   *"The output schema as given may be missing the field [FIELD] because
   [REASON]."* Test it with one targeted search across the item set.
   If the hypothesis survives, raise it as an **Out-of-Scope Candidate
   Field** in the Contradiction Log.

3. **Do not hybridize.** These two checks are explicitly scoped. They
   produce candidates for the user to decide on, not silent changes to
   the input list or the schema. The extraction proceeds against the
   locked input + locked schema as before.
```

## When to Apply

Always. If the user's prompt is a pure extraction with no hint of
hidden-list risk, this step is still cheap and surfaces the risk-if-
it-exists. Cost: one or two extra queries per batch.
