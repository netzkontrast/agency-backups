# Kohärenz Protokoll — Novel-Writing Incubator

This directory is the **development home** for turning the existing novel /
Dramatica / NCP material in this repo into a clean **novel-writing capability**
for the Agency plugin. We incubate here until the design is solid, then merge it
upstream into `agency` as a feature. The separate `kohaerenzprotokoll` repo holds
only the **novel content** (German canon prose); no tooling lives there.

> Working language for this engineering work is **English**.
> The novel's canon prose is **German — never translate it**.

## Goal

Produce a *researched and brainstormed* design for how a novel should be written
with the Agency plugin: which narrative primitives become agency **capability
verbs**, what stays as data, and how the four concepts (Intent · Capability ·
Lifecycle · Memory) carry a novel from idea to draft. The proven patterns already
exist in this repo's `skills/`, `tasks/`, `tools/`, and
`maintenance/schemas/narrative-ontology/`; we decompose them from first
principles and check them for **conceptual coherence** against the plugin model.

## How the work runs (Jules sessions)

Jules is a **web-UI agent with no subagents of its own** — so each session must
be **fully self-contained**. Each session:

1. Reads **only one doc for the plugin model**: [`PLUGIN-CONCEPTS.md`](./PLUGIN-CONCEPTS.md)
   in this directory. **No repo cloning. No agency checkout.** The concepts it
   needs are summarised there.
2. Reads its slice's **source material, already present in this repo** (paths in
   its `BRIEF.md`).
3. Writes **only inside its own slice directory** here.
4. Produces three short files:
   - `CONCEPTS.md` — the irreducible concepts of the slice, mapped onto the
     plugin's four concepts + wire contract.
   - `COHERENCE.md` — a coherence check: where the existing material fits the
     plugin model cleanly, where it fights it, and what would have to change.
   - `PROPOSAL.md` — how this slice should look as part of the novel-writing
     capability (verbs, data, on-disk artefacts).

## The five slices

| # | Dir | Slice | Source in this repo |
|---|---|---|---|
| 1 | `01-dramatica-engine/` | Dramatica model & lookup | `skills/dramatica-theory`, `skills/dramatica-vocabulary`, `tools/dramatica-nav`, `maintenance/schemas/narrative-ontology` |
| 2 | `02-ncp-protocol/` | Narrative Context Protocol | `skills/ncp-author`, `research/ncp-novel-co-authoring-spec` |
| 3 | `03-novel-architect-orchestration/` | Phase orchestration & gates | `skills/novel-architect` (+ `-legacy`) |
| 4 | `04-character-and-world/` | Character & world subsystems | `skills/novel-architect-character`, `skills/novel-architect-world` |
| 5 | `05-structure-scene-coherence/` | Structure, scene & coherence/linters | `skills/novel-architect-structure`, `skills/novel-architect-scene`, related `tasks/` |

A pilot session (slice 1) runs first; the remaining four follow once the shape is
confirmed. A final `SYNTHESIS.md` (authored here) reconciles the five proposals
into one capability design.
