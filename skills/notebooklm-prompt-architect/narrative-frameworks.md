# Narrative Frameworks — Mapping Sources To Story Arcs

Read this when the pitch needs a coherent narrative structure rather
than linear summarization. The default framework is Hero's Journey;
alternatives are documented at the end.

---

## Why A Framework Is Non-Optional

Without a framework, NotebookLM defaults to summarizing sources in the
order they appear in the source list. This produces a "highlight reel"
that lists facts without building toward a conclusion. A framework
forces the model to *cross-reference* all sources simultaneously and
pull the right material for each plot beat — which is precisely what
the RAG retrieval system is designed to do, but only when the prompt
gives it a beat structure.

The framework is encoded in the `_context.md` source-pack file (so it
survives across generations) and reinforced in the persona prompt's
pacing directive.

---

## The Hero's Journey For Pitch Podcasts

Joseph Campbell's monomyth maps cleanly to the structure of a
persuasive narrative because both follow the same logic: status quo →
disruption → resistance → trial → return with new value.

### Stage-by-stage mapping

| Campbell Stage | Pitch Translation | Pulls From |
|----------------|-------------------|------------|
| **The Ordinary World** | Vivid description of the current market / state-of-the-field. Highlight what is broken, painful, or under-served. | Background cluster |
| **Call to Adventure** | The catalyst: a market shift, technological breakthrough, regulatory change, or crisis that makes the status quo untenable. | Problem cluster |
| **Refusal of the Call** | Why nobody has solved this yet — competitor failures, false starts, conventional wisdom that prevented the obvious move. | Competitor / Status-Quo cluster |
| **Crossing the Threshold** | The point of commitment: founding the company, choosing the methodology, defining the thesis. Discarding old paradigms. | Solution cluster (origin story portion) |
| **Tests, Allies, Enemies** | Early validation: beta data, partner endorsements, identified competitive moats, the team assembled. | Validation cluster + Solution cluster |
| **The Ordeal / Dark Night** | Genuine threats: competitive attacks, technical limits, financial constraints, market resistance. Do NOT skip this. | Risks cluster |
| **The Reward / Seizing the Sword** | Survival of the Ordeal yields proof. The product / approach is hardened. | Validation cluster (post-trial portion) |
| **The Road Back** | Scaling questions: what does deployment at scale require? | Vision cluster (operational portion) |
| **The Return / Elixir** | The new world. ROI, long-term vision, ultimate value proposition. The market the listener can choose to live in. | Vision cluster (strategic portion) |

The Hero can be:

- **The product** (most common for B2B / SaaS pitches)
- **The founding team** (founder narrative pitches)
- **The customer** (consumer-narrative pitches; the customer's
  unsatisfied life is the Ordinary World, the product is the
  mentor/elixir)
- **The market itself** (large-scale strategic narratives)

Specify the Hero explicitly in `_context.md`. Without specification,
the model will drift between hero candidates within a single audio.

### Encoding the journey in `_context.md`

```markdown
# Narrative Arc — This Notebook

The audio overviews generated from this notebook follow the Hero's
Journey structure. The Hero is [HERO]. The journey unfolds across the
following stages, each drawing from specific source clusters:

## Stage 1 — The Ordinary World
Source clusters: 01_background
Required content: paint the current state of the [field/market] in
concrete, sensory terms. Highlight specific frictions documented in
[source name 1] and [source name 2].

## Stage 2 — The Call to Adventure
Source clusters: 02_problem
Required content: name the catalyst that makes the status quo
untenable. Cite the specific event or shift documented in [source
name].

[... continue through all stages ...]
```

This file lives in `00_governance/` and is always active. It is the
single source of truth for the arc.

### Common mistakes

- **Skipping the Ordeal.** Pitches that present only the upside read
  as marketing, not as serious propositions. The Skeptic host raises
  the Ordeal during Phase 4 of the persona pacing; the Visionary
  acknowledges the trial and explains how the proposition survived it.
- **Conflating Threshold and Ordeal.** The Threshold is the moment of
  commitment ("we decided to build this"). The Ordeal is the trial
  that tested the commitment ("the first prototype failed for nine
  months"). Different sources, different emotional registers.
- **Resolving the Return as marketing copy.** The Elixir should follow
  from the Ordeal, not from optimism. The proof of the Return is
  whatever survived the Ordeal.

---

## Alternative Frameworks

Use these when the Hero's Journey does not fit the source material.

### Three-Act Structure (compressed pitches, ~10–15 min)

For shorter or tightly-scoped pitches, collapse to three acts:

1. **Setup** — world + protagonist + inciting incident (~25%)
2. **Confrontation** — rising stakes, complications, midpoint reversal,
   crisis (~50%)
3. **Resolution** — climax, denouement, new equilibrium (~25%)

Map source clusters to acts:

- Act 1: Background + Problem
- Act 2: Competitors + Solution + Validation + Risks
- Act 3: Vision + a final synthesis beat

### Mystery / Reveal Structure (true-crime framing)

For pitches built around an unexplained anomaly, contradiction, or
"hidden truth" the sources expose. Particularly powerful for
investigative pitches, exposés, or any case where the proposition is
counter-intuitive.

Beats:

1. **The Anomaly** — present a specific, concrete contradiction or
   unexplained fact from the sources. Both hosts agree something is
   strange.
2. **False Leads** — Host 2 proposes the "obvious" explanations. Host
   1 systematically dismantles each using source evidence.
3. **The Pattern** — Host 1 begins assembling fragments from across
   sources that point to a hidden coherence.
4. **The Revelation** — the real explanation, with source citations.
5. **The Implication** — what this means for the listener, the
   industry, or the future.

The Skeptic role inverts: in mystery framing, Host 2 is the listener-
proxy who *wants* the simple answer; Host 1 is the investigator who
won't let it stand.

### Detective Procedural (process-heavy pitches)

When the pitch is fundamentally about *how* something is done — a
methodology, an investigative process, a forensic technique — frame
the audio as a procedural walkthrough.

Beats:

1. **The Case** — what question are we answering?
2. **The Evidence** — what do the sources contain?
3. **The Method** — how do we examine the evidence?
4. **The Findings** — what does the method yield?
5. **The Verdict** — what does this mean?

Effective for academic defenses and methodology-driven research
narratives. The hosts become co-investigators rather than
adversaries.

### Theseis-Antithesis-Synthesis (academic / philosophical pitches)

Hegelian dialectic. Use when the pitch advances a position by working
through an opposing position.

1. **Thesis** — the conventional view, presented at full strength
2. **Antithesis** — the contradiction or limitation in the thesis
3. **Synthesis** — the new position that incorporates both

The Skeptic defends Thesis; the Visionary defends Antithesis; both
arrive at Synthesis. Particularly effective for German-language
academic pitches where dialectical structure is culturally familiar.

---

## Choosing The Right Framework

| If the pitch is about... | Use |
|--------------------------|-----|
| A new product / company / methodology | Hero's Journey |
| A short-form executive summary | Three-Act |
| An exposé, anomaly, or counter-intuitive truth | Mystery / Reveal |
| A process or methodology | Detective Procedural |
| An academic or philosophical position | Thesis-Antithesis-Synthesis |
| A stress-test of an existing pitch | Hostile Interrogator (see `persona-templates.md`) |

When in doubt, default to Hero's Journey. It is the most flexible and
the most legible to listeners regardless of cultural background.
