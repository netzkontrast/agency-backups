# Source Architecture — Chunking, Folders, Governance Injection

This reference covers how to stage source material so NotebookLM's RAG
retrieval surfaces governance rules alongside factual content. Read
this whenever the user has documents to organize, or asks how to
structure their notebook before generating a pitch.

---

## 1. Hard System Limits — Stay Inside The Box

Before any optimization, confirm the project fits within NotebookLM's
ingestion ceiling. Exceeding any of these triggers an immediate import
failure or silent truncation:

| Constraint | Limit | Mitigation if exceeded |
|------------|-------|------------------------|
| Notebooks per account | 100 | Archive completed projects |
| Sources per notebook | 50 | Merge thematically related minor files into aggregates |
| Words per source file | 500,000 | Split file at thematic boundaries |
| File size | 200 MB | Convert image-heavy PDFs to text; strip embedded media |
| Encrypted PDFs | Not supported | Decrypt before upload |
| Daily chat queries | 50 | Plan prompts; do not iterate live |
| Daily audio generations | 3 | Validate the prompt offline before generating |

The 3-generations-per-day cap is the most operationally painful. Treat
every audio generation as a deliberate, pre-validated launch — never
exploratory.

---

## 2. Thematic Chunking — Defeat Retrieval Drift

A monolithic 400-page PDF causes the retrieval algorithm to gravitate
toward the beginning and end of the document, skip the middle, and
hallucinate connections. Always split monoliths into thematic chunks
*before* upload.

### Chunking heuristic

For a typical pitch project, separate sources into at least these
clusters:

1. **Background / market context** — what is the world like today?
2. **Problem evidence** — what is broken, painful, or under-served?
3. **Competitor / status-quo profiles** — who are the antagonists?
4. **The proposed solution** — product spec, methodology, thesis
5. **Validation / proof** — beta data, case studies, financial models
6. **Risks / counter-arguments** — what could go wrong?
7. **Vision / projection** — the future state if the pitch succeeds

Each cluster becomes one or more focused documents. When the persona
prompt later says "for the Ordeal stage, draw from the Risks cluster",
retrieval is dramatically more accurate than asking it to find risk
discussion buried inside a 400-page omnibus.

### Chunking does not mean fragmenting

Do not split a single coherent argument across three files just to
fit the structure. The unit is the *theme*, not the page. A 50-page
competitor analysis stays as one file. A 400-page strategy document
that covers seven themes becomes seven files.

---

## 3. Folder Routing — Toggleable Generation Scopes

NotebookLM supports folder structures inside the source list. Folders
do not change retrieval behavior algorithmically, but they let the
user toggle entire clusters on or off before generating.

This unlocks a powerful pattern: **per-act source isolation**. Generate
"Act 1: The Ordinary World" with only the Background cluster active;
generate "Act 2: The Ordeal" with only Competitor + Risks active.
Concatenate the audio outputs.

Folder structure for a typical pitch:

```
notebook/
├── 00_governance/                # always active
│   ├── _governance.md
│   ├── _rules.md
│   ├── _dosanddonts.md
│   └── _phonetic-glossary.md
├── 01_background/
├── 02_problem/
├── 03_competitors/
├── 04_solution/
├── 05_validation/
├── 06_risks/
└── 07_vision/
```

The `00_governance/` folder stays active for *every* generation. Other
folders toggle based on which arc segment is being generated.

---

## 4. Markdown Injection — The Governance Hack

This is the core technique. NotebookLM treats source material as
canonical truth. Therefore behavioral rules uploaded as Markdown
sources outrank instructions in the customization field. They survive
across generations, queries, and conversation resets.

### The six governance files

| File | Purpose | Always active? |
|------|---------|----------------|
| `_governance.md` | Top-level behavioral contract, citation format, persona priors | Yes |
| `_rules.md` | Narrative framing rules ("frame status quo as failure") | Yes |
| `_context.md` | Meta-narrative arc, Hero's Journey stage map, time-block plan | Yes for arc-driven pitches |
| `_dosanddonts.md` | Explicit negative constraints (banned phrases, forbidden tones) | Yes |
| `_output_rules.md` | Duration mandate, sentence cadence, climax handling | Yes for long-form |
| `_phonetic-glossary.md` | Pronunciation overrides for jargon, brand names, surnames | Yes if any non-trivial proper nouns |

All six files start with an underscore so they sort to the top of the
source list and are visually distinct from research material. The
underscore is not technically required but is a strong organizational
convention.

### Why this works

When the user asks NotebookLM to generate audio, the RAG system pulls
the most semantically relevant chunks across all selected sources. If
the customization field says "be skeptical" but a research paper in
the source pool says "this technology is revolutionary", retrieval
weights the research paper higher because it is in the canonical
source set.

By promoting the governance rules to *also* live in the canonical
source set, they win the retrieval competition. The model treats "be
skeptical of all claims" with the same epistemic weight as a peer-
reviewed citation.

### Anti-pattern: putting rules only in the customization field

The 10,000-character custom instruction is necessary but insufficient.
It is interpreted as *instructions about what to do*, which the model
weighs against *what the sources say*. If you only want a one-shot
generation tweak, the customization field is fine. For a notebook that
will host repeated generations of a pitch, governance must live in
sources.

---

## 5. Phonetic Glossaries As Sources

The phonetic glossary is technically a governance file but deserves
separate treatment because it solves a specific high-cost failure: a
mispronounced brand name baked into a 60-minute audio file. There is
no spot correction.

### Format

A phonetic glossary source file contains entries like:

```markdown
# Phonetic Pronunciation Reference

When generating audio, pronounce the following terms exactly as
specified. These pronunciations override default text-to-speech
behavior.

| Term | Pronunciation | Notes |
|------|---------------|-------|
| Netzkontrast | "Nets-kon-TRAST" | Hard T at end |
| ASDLS | "A-S-D-L-S" (spelled letter by letter) | Never pronounce as a word |
| Köln | "Köln" with German ö, not "Cologne" | Use German form even in English audio |
| AEGIS | "EE-jis" | Single syllable + soft 'jis' |
```

Tables are clearer than prose for the model. Always include a "Notes"
column for ambiguous cases.

### When to record an audio sample

For terms with no clear phonetic spelling (a poet's name with unusual
diacritics, a brand whose intended pronunciation contradicts its
spelling), record a 5-second clip of the user pronouncing the term and
upload it as a multimodal source. The system can ingest audio cues for
pronunciation reference.

---

## 6. Source Hygiene — What To Strip Before Upload

| Strip | Why |
|-------|-----|
| Author bios, ToCs, indexes, copyright pages | Pad the file, distract retrieval |
| Page headers and footers (if extractable) | "Confidential — page 47 of 312" leaks into audio |
| Embedded promotional sidebars | Pull retrieval toward marketing language |
| Repeated executive summaries at the start of every chapter | Cause the model to repeat itself |
| Untranslated foreign-language quotes | Trigger language-switch hallucinations |

When in doubt, ask: *if a host quotes this verbatim during the audio,
is that desirable?* If no, strip it.

---

## 7. The Pre-Upload Checklist

Run through this list before the user clicks Upload:

- [ ] All sources fit under 200 MB and 500K words
- [ ] No encrypted PDFs in the stack
- [ ] Monoliths have been chunked into thematic clusters
- [ ] Folders organize clusters logically
- [ ] All six governance files are drafted (or explicitly deferred)
- [ ] Phonetic glossary covers every brand name, acronym, and surname
- [ ] Source language matches target audio language (or translation
      step is scheduled)
- [ ] The notebook is dedicated to this single project (no contamination
      from prior personas)
- [ ] Total source count is ≤50

If any item fails, fix it before upload. Re-uploading later does not
"refresh" the retrieval embeddings — it adds new sources alongside the
old ones, which dilutes the governance signal.
