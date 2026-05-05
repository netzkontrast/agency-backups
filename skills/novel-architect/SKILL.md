---
name: novel-architect
description: >-
  Orchestrator für den deutschsprachigen Roman „Kohärenz Protokoll" (Hard-SF /
  Philosophical Horror, Dual-Storyform, 39 Kapitel, 13 Alters). State-Management
  läuft über NCP (Narrative Context Protocol v1.3.0) via ncp-author — Storyform
  A + B als zwei narratives, dynamics/storypoints/storybeats/moments als
  NCP-Entitäten. Nicht-strukturelle Canon-Daten (DKT, Prosa-Regeln, Mandate)
  in canon-meta.md. Lädt Workspace bei Session-Start, routet Skill-Pipeline
  (dramatica-theory, dramatica-vocabulary, ncp-author, memory-sync,
  research-prompt-optimizer, doc-coauthoring, drive-markdown-converter), packt
  sich nach signifikanten Schritten via skill-creator. Trigger — novel-architect,
  Kohärenz Protokoll, Roman Encoding, Storyweaving, Vortex, Throughline,
  Storyform A, Storyform B, NCP, ncp.json, Kanon, Kael, AEGIS, Juna, DKT,
  Kapitel-Entwurf, /analyze, /interview, /synthesize, /draft. Implizit bei
  Alters, Klimax, Dual-POV, Riss-Mandat, 39-Kapitel-Plan. NICHT bei
  Agency-System.
metadata:
  category: creative-writing
  project: Kohärenz Protokoll
  version: "0.3.3"
  status: active
  date_updated: "2026-05-03"
  workspace_root: "/home/claude/novel-architect-workspace"
  state_management: "ncp"
  ncp_schema_version: "1.3.0"
---

# novel-architect

Orchestrator für das Roman-Projekt **Kohärenz Protokoll**. Dieser Skill ist die **Source-of-Truth** für den Kanon: strukturelle Daten in `references/canon/kohaerenz-protokoll.ncp.json` (NCP v1.3.0), nicht-strukturelle Daten in `references/canon-meta.md`, Arbeitsstand in `progress.md`, offene Fragen in `open-questions.md`. Memory (userMemories) ist ein **älterer Snapshot oder lose Anregung** — kann stale sein, kann widersprüchlich sein, ist niemals autoritativ. Bei Diskrepanz: Skill-Files gewinnen, Memory ist Konsultations-Material.

## Mission

Vier Dinge, die dieser Skill leistet:

1. **Workspace aufsetzen** — schreibbare Kopie seiner selbst plus read-only Spiegel der Workflow-Skills nach `/home/claude/novel-architect-workspace/`. Ohne Workspace keine Arbeit. Bootstrap ist die erste Handlung jeder Session.

2. **Skill-Pipeline routen** — für jede Roman-Aufgabe (Encoding, Storyweaving, Vortex-Architektur, Open-Questions-Resolution, Chapter-Drafting, Research-Ingestion, Canon-Update) ist die Skill-Reihenfolge dokumentiert. Kein Rätselraten welcher Skill wann.

3. **Strukturellen Canon in NCP halten** — Storyform A + B, Players, Storypoints, Storybeats, Moments leben als JSON in `references/canon/kohaerenz-protokoll.ncp.json` (Narrative Context Protocol v1.3.0). Jede Mutation läuft über `ncp-author`. Nicht-strukturelle Canon-Daten (DKT-Physik, Prosa-Regeln, Mandate) bleiben in `references/canon-meta.md`.

4. **Eigenen Stand fortschreiben** — `references/progress.md`, `references/canon/kohaerenz-protokoll.ncp.json` und ggf. `references/canon-meta.md` werden nach jedem signifikanten Schritt aktualisiert, dann wird der Skill via `skill-creator/scripts/package_skill.py` neu gepackt und die `.skill`-Datei via `present_files` zurückgegeben. So überlebt der Arbeitsstand die Session.

---

## Bootstrap-Protocol (FIRST ACTION jeder Session)

Wenn dieser Skill triggert, ist der erste Schritt — vor jeder inhaltlichen Antwort — der Workspace-Setup. Grund: installierter Skill-Pfad ist read-only, alle anderen Skills liegen verstreut, der Arbeitsstand der letzten Session steht in `references/progress.md` aber muss erst gelesen werden.

### Bootstrap-Schritte

```bash
# 1. Workspace-Struktur
mkdir -p /home/claude/novel-architect-workspace/tmp/skills-ref
mkdir -p /home/claude/novel-architect-workspace/outputs/encoding
mkdir -p /home/claude/novel-architect-workspace/outputs/weaving
mkdir -p /home/claude/novel-architect-workspace/outputs/vortex
mkdir -p /home/claude/novel-architect-workspace/outputs/drafts
mkdir -p /home/claude/novel-architect-workspace/outputs/research
mkdir -p /home/claude/novel-architect-workspace/outputs/oq-resolved
mkdir -p /home/claude/novel-architect-workspace/archive

# 2. Schreibbare Skill-Kopie
cp -r /mnt/skills/user/novel-architect /home/claude/novel-architect-workspace/
chmod -R u+w /home/claude/novel-architect-workspace/novel-architect

# 3. Workflow-Skills spiegeln (read-only Referenzen)
for skill in dramatica-theory dramatica-vocabulary memory-sync ncp-author \
             research-prompt-optimizer pdf-to-markdown drive-markdown-converter \
             spec-skill; do
  cp -r /mnt/skills/user/$skill /home/claude/novel-architect-workspace/tmp/skills-ref/ 2>/dev/null
done
cp -r /mnt/skills/examples/doc-coauthoring /home/claude/novel-architect-workspace/tmp/skills-ref/ 2>/dev/null
mkdir -p /home/claude/novel-architect-workspace/tmp/skills-ref/skill-creator
cp /mnt/skills/examples/skill-creator/SKILL.md /home/claude/novel-architect-workspace/tmp/skills-ref/skill-creator/
cp -r /mnt/skills/examples/skill-creator/scripts /home/claude/novel-architect-workspace/tmp/skills-ref/skill-creator/

# 4. Helper-Skripte (preserved im Skill-Pack unter scripts/, kopiert in tmp/)
# convert_pdfplumber.py = PDF→MD Fallback wenn pymupdf4llm nicht installierbar (PyPI gesperrt im Sandbox)
if [ -f /home/claude/novel-architect-workspace/novel-architect/scripts/convert_pdfplumber.py ]; then
  cp /home/claude/novel-architect-workspace/novel-architect/scripts/convert_pdfplumber.py \
     /home/claude/novel-architect-workspace/tmp/
fi
```

### Nach dem Workspace-Setup

**Lesen heißt lesen. Nicht skimmen, nicht grep'en.** Jede der folgenden Reference-Files ist beim Bootstrap mindestens auf Sektion-Erst-Absatz-Niveau zu durchlaufen — nicht nur Section-Headers abscannen. Eine etablierte Canon-Klärung im Body, die im Header-Skim unsichtbar bleibt, macht ganze Session-Hälften redundant (Lesson 2026-05-03, siehe `references/learnings.md`).

1. **`references/progress.md` lesen** — Wo wurde aufgehört? Was ist der nächste angekündigte Schritt?
2. **`references/canon/kohaerenz-protokoll.ncp.json` lesen** — Strukturelle Canon-Daten (Storyform A + B, dynamics, players, storypoints, storybeats, moments). Diese Datei IST der strukturelle Kanon.
3. **`references/canon-meta.md` vollständig lesen** — Nicht-strukturelle Canon-Daten (DKT-Physik, Prosa-Regeln, Mandate, Projekt-Meta). **Insbesondere alle Sektionen mit `(kanonisiert YYYY-MM-DD)`-Markierung im Body durchlesen** — diese tragen die jüngsten Klärungen, die noch nicht in userMemories repliziert sind.
4. **`references/canon/README.md` lesen** — NCP-Validierungsstatus, was schon gefüllt ist, was noch leer ist.
5. **`references/open-questions.md` vollständig lesen** — Welche OQs blockieren was? **Insbesondere die ~~Strikethrough-resolved-Einträge~~ scannen** — sie zeigen, welche Fragen heute schon entschieden sind, damit man sie nicht versehentlich nochmal aufmacht.
6. **`references/learnings.md` lesen** — Was hat in früheren Sessions suboptimal funktioniert? Welche Korrekturen sind in Kraft? Verhindert Wiederholung derselben Fehler.
7. **Skill-interne Konsistenz prüfen** — Decken sich `progress.md`, NCP-Datei, `canon-meta.md` und `open-questions.md`? Falls Drift: zuerst beheben, dann arbeiten. Memory wird **nicht** als Vergleichsreferenz herangezogen — Memory ist Notiz, kein Maßstab.
8. **Pre-Action-Sanity-Check (Pflicht vor Action-Workflows wie /draft, /encoding, /research-ingestion):** Nach Bootstrap und vor erster Tool-Aktion explizit gegen die Liste der resolved-OQs (aus open-questions.md) abgleichen — *„hat das Issue, das ich gleich angehe, vielleicht schon eine resolved-OQ-Antwort?"* Wenn ja: das dem User aktiv anzeigen, statt das Issue komplett neu zu rollen.
9. **Erst dann** auf den User-Input antworten.

### Bootstrap-Heuristik

Der Bootstrap muss nicht bei jeder einzelnen User-Nachricht laufen — nur einmal pro Session. Wenn der Workspace bereits existiert (`/home/claude/novel-architect-workspace/novel-architect/SKILL.md` vorhanden) und in dieser Session schon gelesen wurde, übersprungen. Wenn unsicher: `ls /home/claude/novel-architect-workspace/` checken.

---

## Routing-Matrix: Workflow → Skill-Stack

Übersicht. Detail-Specs in `references/workflows.md`.

| Workflow | Trigger-Phrasen | Skill-Stack (Reihenfolge) | Output-Ziel |
|---|---|---|---|
| **bootstrap** | implicit, Session-Start | self | workspace ready |
| **throughline-encoding** | „Encoding", „Throughline", „Phase 1-4", „MC/IC/OS/RS encoden" | dramatica-theory → dramatica-vocabulary → ncp-author (storypoints schreiben) → novel-architect (Project-Constraints, Block-4-Anker) | NCP: `narratives[].subtext.storypoints[]` + `narratives[].subtext.players[]`. Begleit-Markdown: `outputs/encoding/<storyform>-<throughline>.md` |
| **dynamics-encoding** | „Driver-Pivot", „Limit", „Outcome", „Phase 5" | dramatica-theory → dramatica-vocabulary → ncp-author → novel-architect | NCP: `narratives[].subtext.dynamics[]` (Verfeinerung — Skeleton vorhanden) |
| **storyweaving** | „Storyweaving", „Kapitel-Plan", „Phase 6", „Polyphonie-Verteilung" | dramatica-theory → ncp-author (storybeats + moments) → novel-architect | NCP: `narratives[].subtext.storybeats[]` + `narratives[].storytelling.moments[]`. Begleit-Markdown: `outputs/weaving/chapter-map.md` |
| **vortex-architecture** | „Vortex", „Klimax", „Ch35-36", „Mnemosyne-Archipel", „Phase 7" | dramatica-theory → dramatica-vocabulary → ncp-author (5 spezifische storybeats + Klimax-moments) → novel-architect | NCP: 5 storybeats + 1-2 moments im Klimax-Bereich. Begleit-Markdown: `outputs/vortex/beat-<n>.md` |
| **open-questions-resolution** | „OQ", „Slot 16 entscheiden", „offene Fragen", „Phase 8" | novel-architect → dramatica-theory (Implikationen) → ncp-author (falls strukturelle Auswirkung) → canon-meta-Edit (falls nicht-strukturell) | `outputs/oq-resolved/<oq-id>.md` + ggf. NCP-Update + canon-meta-Update. Memory-Broadcast nur auf User-Wunsch. |
| **chapter-drafting** | „/draft", „Kapitel X entwerfen", „Prosa schreiben" | novel-architect (NCP + canon-meta laden) → dramatica-vocabulary (Term-Präzision) → docx | `outputs/drafts/ch-XX.docx`. Prosa lebt **außerhalb** von NCP — cross-reference via `moment.id`. |
| **research-ingestion** | „/analyze", „Gemini-Output verarbeiten", „Recherche zu X" | research-prompt-optimizer → (extern: Gemini Deep Research) → novel-architect (Synthese gegen Canon) → doc-coauthoring | `outputs/research/<topic>.md`, ggf. NCP/canon-meta-Update via /synthesize |
| **canon-update** | „/synthesize", „Kanon ändern", „das ist jetzt kanonisch", „korrigiere", „entschieden" | ncp-author (strukturell) UND/ODER canon-meta-Edit (nicht-strukturell) → novel-architect (progress + open-questions updaten) → memory-sync (optional, nur wenn User Memory-Broadcast wünscht) → drive-markdown-converter (optional) | NCP-Datei und/oder `references/canon-meta.md` werden geändert. Memory-Slots werden nur dann angefasst, wenn User explizit „Memory updaten" sagt. |
| **archive-material** | „alte PDFs konvertieren", „Material in Markdown" | pdf-to-markdown (oder pdfplumber-Fallback) → drive-markdown-converter | `archive/` |
| **drive-doc-ingest** | „Drive-Files als Markdown holen", „importiere die Outline-Files", „Bulk-Ingest" | search_files → download_file_content (exportMimeType=application/pdf) → pdfplumber-Fallback (`tmp/convert_pdfplumber.py`) → md5 dedupe + diff check → manifest unter `outputs/research/ingest-manifest-<datum>.md` | `ingest/*.md` + manifest |

### Routing-Heuristik

Wenn die Trigger-Phrase mehrdeutig ist (z. B. „Storyform anpassen" — Encoding oder Canon-Update?), kurz nachfragen via `ask_user_input_v0`. Multi-Variable-Entscheidungen kriegen 2-4 Optionen, keine Prosa.

Wenn der User innerhalb einer Session zwischen Workflows wechselt: `progress.md` notiert beide. Workflow-Pivot ist Checkpoint-Trigger (siehe Iteration Discipline).

---

## Iteration Discipline: Significance + Packaging

Detail-Heuristik in `references/significance-heuristics.md`. Hier die Kurzform.

### Was ist „signifikant" (= Checkpoint-Trigger)

Ein Checkpoint löst aus:
1. `references/progress.md` aktualisieren (was wurde gemacht, was kommt als nächstes)
2. **NCP-Update** falls strukturell: `references/canon/kohaerenz-protokoll.ncp.json` via ncp-author bearbeiten
3. **canon-meta.md aktualisieren** falls nicht-strukturell (DKT, Prosa-Regeln, Mandate, Projekt-Meta)
4. **`references/learnings.md` Eintrag (mandatorisch bei Session-End-Checkpoint, optional bei anderen)** — siehe „Learnings-Discipline" unten
5. memory-sync **nur** wenn User explizit Memory-Broadcast wünscht (Memory ist nicht Teil des Canon-Pfads)
6. Skill packen via `python /home/claude/novel-architect-workspace/tmp/skills-ref/skill-creator/scripts/package_skill.py /home/claude/novel-architect-workspace/novel-architect`
7. `present_files` mit der `.skill`-Datei (und ggf. dem Output-Artefakt)

Checkpoint triggert wenn EINS davon zutrifft:

- **Canon-Shift (strukturell)** — irgendetwas, das NCP ändert (Storyform-Slot festgelegt, Storypoint encoded, Storybeat positioniert, Player-Detail entschieden, Moment definiert)
- **Canon-Shift (nicht-strukturell)** — irgendetwas, das canon-meta.md ändert (DKT-Regel, Prosa-Regel, Mandate-Anpassung, Alter-Somatik gefüllt, Projekt-Meta geändert)
- **Phase-Unit complete** — eine atomare Phase-Einheit fertig: Throughline encoded (NCP storypoints + players), Dynamic verfeinert, Vortex-Beat operationalisiert (NCP storybeat), OQ resolved, 10-Kapitel-Block gemapped (NCP storybeats + moments), Chapter draft fertig
- **Workflow-Pivot** — User wechselt zu einem anderen Workflow (z. B. von Encoding zu Storyweaving)
- **Volume threshold** — 3+ neue Files in `outputs/` oder ~2000 Wörter substantielles Material seit letztem Checkpoint
- **Session-End** — immer

### Was ist NICHT signifikant (kein Package)

- Term-Lookup in dramatica-vocabulary
- Q&A ohne Canon-Berührung
- Einzelner Scene-Keim-Brainstorm ohne Festlegung
- Reference-Reading
- Interview-Antwort

`progress.md` darf bei jedem nicht-trivialen Schritt aktualisiert werden — das ist billig (Text-Edit). Packen passiert nur am Checkpoint.

### Beispiele

**Signifikant (package + present)**:
- „MC-Encoding für Storyform A ist fertig, alle 4 Storypoints in Szenen-Keimen." → Phase-Unit complete.
- „OQ-01 ist entschieden: Juna ist eigenständige Witness-Function." → Canon-shift + OQ resolved.
- „Wir wechseln jetzt zur Storyweaving-Phase." → Workflow-Pivot.
- „Session-Ende, lass speichern." → Session-end.

**Nicht signifikant (kein Package)**:
- „Was ist nochmal der Driver-Pivot?" → Term-Lookup.
- „Brainstorm: drei mögliche Bilder für Kael in Ch3." → Brainstorm ohne Festlegung.
- „Erklär mir kurz die OS-Throughline von B." → Q&A.

### Learnings-Discipline (User-Setzung 2026-05-03)

Self-Improvement ist **nicht optional und nicht „am Schluss zusammenfassen"**, sondern **kontinuierliche Pflicht**.

**Während der Session:** Wenn ich beobachte, dass etwas suboptimal lief — falsches Tool zuerst gegriffen, Token-Verschwendung, übersehener Konflikt zwischen Sources, Bootstrap-Lücke, etc. — sofort Eintrag in `references/learnings.md` notieren. Format pro Eintrag: **Datum, Trigger, Lesson, Action**. Nicht aufschieben, nicht „merken für später".

**Am Session-Ende-Checkpoint (immer):** Verifikation, dass mindestens ein Eintrag aus dieser Session in `learnings.md` steht. Wenn keine Lesson auftrat, das auch dokumentieren („nichts auffälliges, alle Pfade liefen wie spezifiziert" — auch eine Information). Anschließend Skill packen, damit der Eintrag persistiert.

**Bootstrap-Side:** Beim Workspace-Setup wird `learnings.md` mitgelesen (Schritt 6 in „Nach dem Workspace-Setup"). So sehe ich frühere Korrekturen am Session-Anfang und vermeide Wiederholungen.

**Inhaltliche Erwartung:** Ein Eintrag ist nutzlos, wenn er nur „X war suboptimal" sagt. Gut ist, wenn er konkretisiert: welche Skill-Datei wird angepasst, welcher Workflow bekommt einen Pflicht-Sub-Step, welche Heuristik erweitert sich. Action-Items zeigen auf SKILL.md, references/, oder commands/-Files — die Veränderung muss dort passieren, nicht nur in `learnings.md`.

---

## Skill-Improvement TODO

Beobachtungen über die Skill-Pipeline hinweg, die hier nicht gefixt werden, aber dokumentiert gehören. Detail in `references/skill-improvement-todo.md`. Diese Liste wächst — bei jeder Session, in der etwas Suboptimales auffällt, wird hier ergänzt.

Aktueller Stand-Highlights:
- **NCP als State-Layer ist commitment**, aber `ncp-author` ist WIP 0.1.0-draft — kein eigener Validator, schema-Drift in NCP upstream. Mitigations-Strategie in `references/canon/README.md` dokumentiert.
- `commands/` ist nur Stub — full prompt templates für /analyze, /interview, /synthesize, /draft fehlen
- NCP-Datei ist Skeleton: Storyform A + B + alle Dynamics gefüllt, aber `players[]`, `storypoints[]`, `storybeats[]`, `moments[]` werden Phase-für-Phase befüllt (initial leer)
- `memory-sync` braucht klare Outward-Only-Semantik — Skill→Memory broadcast, niemals umgekehrt
- Slot 16 (Per-Chapter Dual-POV) ist architektonische Hypothese in NCP-Form — Resolution-Workflow ausstehend
- Kein gemeinsames Inter-Skill-Handoff-Schema — wäre nützlich

---

## Reference-File-Index

| Datei | Inhalt | Wann laden |
|---|---|---|
| `references/progress.md` | Letzter Arbeitsstand, nächster geplanter Schritt | Bei jedem Bootstrap |
| `references/canon/kohaerenz-protokoll.ncp.json` | **Strukturelle Canon-Daten als NCP-JSON** (Storyform A+B, dynamics, perspectives, players, storypoints, storybeats, moments) | Bei jedem Bootstrap, bei jedem strukturellen Workflow — Mutation NUR via ncp-author |
| `references/canon/README.md` | NCP-Status, was gefüllt ist, Validierung, Risiken, Slot-16-Hypothese | Bei Bootstrap, bei NCP-Edit, bei Validierungs-Frage |
| `references/canon-meta.md` | Nicht-strukturelle Canon-Daten (DKT-Physik, Alter-Somatik, Riss-Mandate, Prosa-Regeln, Vortex-Beats-Übersicht, Projekt-Meta) | Bei Bootstrap, vor Workflow-Start |
| `references/open-questions.md` | Aktuelle OQs (blockierend / nicht-blockierend) | Vor /draft, vor Workflow-Start |
| `references/workflows.md` | Detail-Specs der 10 Workflows (Pre-Checks, Skill-Stack, Output-Format, Exit-Bedingung, NCP-Hooks) | Bei Workflow-Start |
| `references/significance-heuristics.md` | Detail-Heuristik für Checkpoint-Trigger inkl. Beispiele | Vor Checkpoint-Entscheidung |
| `references/skill-improvement-todo.md` | Liste der Skill-Lücken über die Pipeline, NCP-Reifegrad-Risiko | Skill-Wartung |
| `references/learnings.md` | Self-Improvement-Log: was lief in früheren Sessions suboptimal, welche Korrekturen sind in Kraft | Bei jedem Bootstrap (Schritt 6), bei jedem Session-End-Checkpoint (mandatorischer Eintrag) |
| `scripts/convert_pdfplumber.py` | Fallback PDF→Markdown Konverter (pdfplumber) für drive-doc-ingest und archive-material wenn pymupdf4llm nicht installierbar (PyPI gesperrt) | Wird beim Bootstrap nach `tmp/` kopiert |
| `commands/analyze.md` | Prompt-Template für /analyze (Gemini-Archivist) | Wenn /analyze triggert |
| `commands/interview.md` | Prompt-Template für /interview (max 3 Fragen/Runde, mit Implikationen) | Wenn /interview triggert |
| `commands/synthesize.md` | Prompt-Template für /synthesize (NCP + canon-meta primär, Memory optional outward-broadcast) | Wenn /synthesize triggert |
| `commands/draft.md` | Prompt-Template für /draft (Kapitel-Entwurf mit harten Pre-Checks) | Wenn /draft triggert |

---

## Constraints (nicht überschreibbar)

- **POV-Schutz**: Strukturelle/stilistische Signale im Draft erst bestätigen, dann ändern — nie stillschweigend glätten. Mosaikstruktur, unzuverlässige Erzähler und widersprüchliche Fußnoten sind Risse, kein Stil-Mangel.
- **Canon-Hierarchy**: **Skill-Files (NCP + canon-meta.md + open-questions.md + progress.md) > Memory > Training**. NCP-Datei und canon-meta.md SIND der strukturelle und nicht-strukturelle Kanon. Memory ist abgeleiteter Snapshot, kann älter sein, kann Anregung statt Fakt sein. Bei Diskrepanz: Skill-Files gewinnen.
- **NCP-Mutation NUR via ncp-author**: Direkte Hand-Edits an der NCP-Datei sind verboten — würden Schema-Drift erzeugen. Bei Notwendigkeit immer den ncp-author-Skill aufrufen.
- **Dual-Storyform-Integrität**: Storyform A + B laufen parallel als 5D-Interferenz. Niemals A komplett vor B encoden — Throughline-für-Throughline durch beide simultan. NCP unterstützt das nativ als zwei narratives.
- **Story-First**: Wenn Theorie und Draft sich widersprechen, gewinnt der Draft. Theorie ist Diagnose, kein Rezept.
- **Roman ist aktuell deprioritized** (User-Setzung): Skill ist verfügbar, drängt sich aber nicht auf. Keine Pressure, keine Push-Empfehlungen außerhalb des Auftrags.

---

## Navigator-Backed Lookups

Strukturelle Canon-Edits (Storyform-A/B-Slots, Storypoints, Players, Storybeats, Moments) referenzieren ab v0.1 Narrative-Ontology IDs statt freier Labels — Beispiel: `throughline.relationship` (kanonisch "Relationship Story") statt der älteren Bezeichnung "Subjective Story". Lade-Kontrakt liegt in [`AGENTS.md § Narrative Ontology`](../../AGENTS.md), Regel **NO.3** bindet Kohärenz-Protokoll-Strukturedits direkt.

Bevorzugte `nav.py`-Aufrufe pro Workflow-Lookup-Schritt:

| Workflow-Schritt | Lookup-Frage | Bevorzugter `nav.py`-Aufruf |
|---|---|---|
| throughline-encoding | „Welcher canonical_label hat die RS-Throughline?" | `nav.py by-id throughline.relationship` |
| dynamics-encoding | „Welcher Dynamic-Pair ist Crucial Element X?" | `nav.py by-id <el.id> --include-pairs` |
| storyweaving | „Welche Element pairs sitzen im Logic/Feeling Quad?" | `nav.py by-quad quad.logic-feeling-el` |
| open-questions-resolution | „Welche Terms tagged sind mit `novel.diagnose-flat-draft`?" | `nav.py by-scenario novel.diagnose-flat-draft` |
| canon-update (NCP) | „Was ist die NCP-Appreciation für Element X?" | `nav.py by-id <el.id>` (lese `ncp_appreciation`) |
| chapter-drafting | „Welche Variation rollt zu welchem Type?" | `nav.py by-id <var.id>` (lese `type_id`) |

Prose-Lookups bleiben für *konzeptuelle* Fragen (Was bedeutet Story Mind? Warum ist Resolve binär?) — die `nav.py`-Antwort enthält stets einen `term_file`-Pointer, der den Chapter-Read auf eine Section eingrenzt; `tools/dramatica-nav/extract.py <id>` liefert die Section ohne den umliegenden Chapter.

## Integration mit anderen Schreib-Skills

| Skill | Relation | Wann |
|---|---|---|
| `dramatica-theory` | Input / Reference | Storyform-Arbeit, Akt-Diagnose, Encoding-Patterns |
| `dramatica-vocabulary` | Companion | Bei jeder Dramatica-Term-Berührung — proaktiv |
| `ncp-author` | **State-Layer Owner** | Bei jeder strukturellen Canon-Mutation — NICHT optional, NICHT umgehen |
| `memory-sync` | Outward Broadcaster (optional) | Nur wenn User explizit Memory-Update wünscht — Skill→Memory, niemals Memory→Skill |
| `research-prompt-optimizer` | Upstream | Gemini-Deep-Research-Prompts für /analyze |
| `doc-coauthoring` | Downstream | Strukturierte Canon-Doc-Erstellung (canon-meta.md, Drive-Docs) |
| `pdf-to-markdown` | Utility | Alte Material-PDFs → Markdown |
| `drive-markdown-converter` | Utility | Drive-Synchronisation |
| `skill-creator` | Self-update | Packaging dieses Skills |
| `suno-lyric-writer` | DELEGIERT NICHT | Album-2-Tracks haben eigenen Skill (the-agency-system-architect + suno-lyric-writer) |

---

## Closing Note

Dieser Skill ist die Source-of-Truth des Romans. NCP-Datei und canon-meta.md sind der Kanon. Memory ist Notizfeld — kann stale sein, kann Anregung sein, ist nie Maßstab. Wenn die Memory etwas anderes sagt als der Skill: Skill gewinnt; Memory wird nur dann updated, wenn User es explizit verlangt. Wenn ein Workflow nicht passt: schreib ihn um in `references/workflows.md` und packe neu. Der Skill ist ein lebendes Dokument seiner eigenen Verwendung.
