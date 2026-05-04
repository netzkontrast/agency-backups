---
type: cross_pollination
inject_into_category: C
source_category: B
full_name: Per-Session Locked Schema + Cross-Session Diff
selected_when: category == C
slots: {}
id: b-into-c
file: modules/cross-pollination/b-into-c.md
---

# Cross-Pollination: Category B → Category C

> Inject into a **Lifecycle** prompt (primary = C). Guards against the
> core C failure mode: per-session research that drifts into freeform
> note-taking, so cross-session comparability decays and the knowledge
> store stops being queryable.

## Paste-Ready Injection — One Step (minimum) into the Steps section

```markdown
### Step [i.b] — Per-Session Locked Schema (cross-pollination from Category B)

This step imports one extraction discipline from Category B because
lifecycle research without a locked per-session schema slowly degrades
into a journal: every session has a slightly different shape, and after
six months the cross-session comparison the user actually wanted is
impossible to reconstruct.

Perform the following at every session, immediately after the
Resumption Protocol and before any new search:

1. **Re-anchor the per-session schema.** The persistent knowledge
   store defines a fixed per-session record schema (see the Knowledge
   Store Schema in this prompt). Restate the schema verbatim at the
   start of every session. Do not silently extend or shrink it.

2. **Treat each session as one batch iteration.** Apply Replication
   Mechanism M3 (Batch-Explicit Framing) with cardinality = 1 per
   session. The session output is one record that fully populates
   every schema field, including the explicit "not-found — [reason]"
   marker for any field that genuinely cannot be filled this session.

3. **Cross-session diff.** Before closing the session, run a B-style
   diff between this session's record and the previous session's
   record on the same schema fields. Surface the diff in the
   Session-End Summary as a structured list:
   - Fields unchanged: [...]
   - Fields with new evidence: [...]
   - Fields whose values reversed since last session: [...] (these
     escalate into the World-Change Log per Method M07).

4. **Do not hybridize.** The Resumption Protocol, Compaction
   Protocol, and Assumption-Decay Audit (Category C core) remain in
   place. The locked schema sits inside the per-session record;
   it does not replace the lifecycle scaffolding.
```

## When to Apply

Every session. Cost: minimal — schema restatement is two minutes per
session. Benefit: the user can run a B-style cross-session comparison
at any future point without retroactively imposing structure on
already-written sessions.
