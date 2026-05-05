---
name: dramatica-vocabulary
description: Aktive Dramatica-Theorie für Storyform-Aufbau, Encoding und Storyweaving — kein passives Dictionary, sondern Werkzeug. Trigger explizit bei Dramatica, Storyform, Throughline, Class, Type, Variation, Element, Archetype, Dynamic Pair, MC, IC, Goal, Consequence, Cost, Dividend, Driver, Outcome, Judgment, Limit, sowie bei Archetypen-Namen Protagonist, Antagonist, Guardian, Contagonist, Sidekick, Skeptic, Reason, Emotion. Trigger proaktiv in Narrativ-Kontexten — bei novel-architect-Arbeit (Kohärenz Protokoll), Agency System Triptychon-Tracks (Album 1/2/3), Suno-Lyric-Arbeit mit klarem Charakterbogen, oder Diskussionen über Resolve (Steadfast/Change), Approach (Be-er/Do-er), Mental Sex (Linear/Holistic), Growth (Stop/Start). Liefert präzise Definitionen mit Dynamic Pairs, strukturelle Verortung in der Dramatica-Hierarchie, Encoding-Vorschläge und Konsistenz-Checks gegen die 75 Dynamic Pairs. Nicht greifen bei Hero's Journey, Save the Cat, Beat Sheets oder anderen explizit benannten Story-Modellen.
---

# Dramatica Vocabulary

Aktive Unterstützung für die Anwendung von Dramatica-Theorie auf konkrete Story-Arbeit. Kein passives Lexikon — ein Werkzeug zum Storyform-Aufbau, Encoding und Storyweaving.

## Was dieser Skill leistet

Wenn Dramatica-Konzepte in einem Gespräch auftauchen — explizit oder implizit — liefert dieser Skill:

1. **Präzise Definitionen** der 265 indexierten Terme mit korrekten Dynamic Pairs
2. **Strukturelle Verortung**: Wo sitzt ein Begriff in der Dramatica-Hierarchie (Class → Type → Variation → Element)?
3. **Encoding-Vorschläge**: Wie übersetzt man die abstrakte Storyform in konkrete Story-Erscheinungen?
4. **Konsistenz-Checks**: Passen Charakter-Archetyp, Throughline-Domain und Goal-Type zusammen? Welcher Dynamic Pair liegt einer Szene zugrunde?

Der Skill arbeitet **mit** anderen Skills, nicht gegen sie:

- **novel-architect** (Kohärenz Protokoll): liefert das Vokabular für Charakter-Verortung, Throughline-Trennung, Goal/Consequence/Cost-Architektur
- **the-agency-system-architect**: liefert die Storyform-Sprache für Triptychon-Bögen (Album 1 Outcome, Album 2 Wendepunkt, Album 3 Resolution), Archetypen-Mapping (System-Teile als Dramatica-Charaktere)
- **suno-lyric-writer**: liefert präzise Konflikt-Vokabel für Track-Strukturen — Element-Pairs werden zu Vers-Refrain-Spannungen

## Wann der Skill greift

**Explizite Trigger** — sofort konsultieren:

- Begriffe „Dramatica", „Storyform", „Throughline", „Storyform aufbauen", „Encoding", „Storyweaving"
- Strukturelle Termini: Class, Type, Variation, Element, Domain
- Archetypen-Namen: Protagonist, Antagonist, Guardian, Contagonist, Reason, Emotion, Sidekick, Skeptic
- Plot-Dynamics: Driver (Action/Decision), Limit (Optionlock/Timelock), Outcome (Success/Failure), Judgment (Good/Bad)
- Charakter-Dynamics: Resolve (Steadfast/Change), Approach (Be-er/Do-er), Mental Sex (Linear/Holistic), Growth (Stop/Start)

**Proaktive Trigger** — konsultieren, wenn der Nutzer das Vokabular wahrscheinlich produktiv nutzen würde:

- novel-architect-Arbeit am Kohärenz Protokoll, besonders bei Charakter-Beziehungs-Mapping oder Akt-Struktur
- Agency System Track-Entwicklung mit Konflikt-/Wendepunkt-/Auflösungs-Bezug
- Suno-Lyric-Arbeit, wenn der Track eine klare dramatische Bewegung trägt (Hauptfigur-Wandel, Antagonist-Konfrontation, etc.)
- Generelle Diskussionen über Charakterbögen, Konflikt-Strukturen, Theme, Story-Probleme — wenn Dramatica-Konzepte präziser wären als Hero's-Journey-Vokabular

**Nicht greifen**, wenn:
- Der Nutzer explizit auf ein anderes Story-Modell verweist (Hero's Journey, Save the Cat, Story Circle, etc.)
- Es nur um Sprache/Stil geht, nicht um Struktur
- Die Anfrage ein einfaches Lookup ohne Story-Kontext ist (dann reicht ein einzelnes File-Read ohne Skill-Aktivierung)

## Dramatica in 60 Sekunden

Dramatica-Theorie behauptet: Eine vollständige Story argumentiert eine bestimmte Sicht auf ein einzelnes inquiry-Thema. Dieses Argument hat eine messbare Struktur:

**Die vier Throughlines** — eine Story zeigt einen Konflikt aus vier Perspektiven gleichzeitig:

- **Overall Story (OS)**: das Problem aus der Vogelperspektive — alle Charaktere
- **Main Character (MC)**: das Problem aus *einem* persönlichen Standpunkt
- **Impact Character (IC)**: ein Gegenpol, der den MC herausfordert
- **Relationship (RS)**: die *Beziehung* zwischen MC und IC als eigene Erzähleinheit

Jede Throughline lebt in **einem Class** — einer von vier Welten:
- **Universe** (eine Situation/Zustand)
- **Physics** (eine Aktivität/Tätigkeit)
- **Psychology** (eine Denkart)
- **Mind** (eine Haltung/Festsetzung)

In jeder Class gibt es eine Hierarchie der Auflösung:

```
Class  →  Type  →  Variation  →  Element
(Welt)   (Bereich) (Concern)    (Charakteristik)
```

Die **Storyform** ist die spezifische Auswahl, welche Type, Variation und Element jede Throughline besetzt. Diese Auswahl ist keine Liste — sie ist ein **integriertes Argument**: bestimmte Wahlen bedingen oder schließen andere aus (das ist die Dramatica-Engine).

**Encoding** = Storyform → konkrete Story-Erscheinungen. Beispiel: das abstrakte Element „Test" (im Dynamic Pair mit „Trust") encoded als „Marie kann ihrem Bruder nicht glauben, ohne die Kontonummer zu prüfen".

**Storyweaving** = die Reihenfolge, in der diese Erscheinungen dem Publikum präsentiert werden. Storyform und Storytelling sind getrennt — derselbe Storyform kann auf hundert Arten erzählt werden.

## Die acht Archetypen

Acht quintessentielle Charakter-Anordnungen. Jede repräsentiert ein Element-Quad:

- **Protagonist** ↔ **Antagonist** (Pursuit ↔ Avoidance des Goals)
- **Guardian** ↔ **Contagonist** (Conscience ↔ Temptation)
- **Reason** ↔ **Emotion** (Logic ↔ Feeling)
- **Sidekick** ↔ **Skeptic** (Faith ↔ Disbelief)

Echte Geschichten nutzen oft *komplexe* Charaktere, die Elemente aus mehreren Archetypen kombinieren — die acht sind die Bausteine, nicht die Vorschrift.

## Charakter-Dynamics (vier Achsen für den Main Character)

- **Resolve**: Steadfast (hält an seiner Sicht fest) ↔ Change (wandelt sich)
- **Growth**: Start (muss etwas neu beginnen) ↔ Stop (muss etwas aufhören)
- **Approach**: Do-er (erst handeln) ↔ Be-er (erst sich anpassen)
- **Mental Sex** (Problem-solving style): Linear ↔ Holistic

Die Kombination dieser vier (plus die Story-Limit, Outcome, Judgment) macht den MC eindeutig.

## Plot-Dynamics

- **Driver**: Action (Handlungen treiben Entscheidungen) ↔ Decision (Entscheidungen treiben Handlungen)
- **Limit**: Optionlock (Optionen erschöpfen sich) ↔ Timelock (Zeit läuft ab)
- **Outcome**: Success ↔ Failure (Goal erreicht oder nicht)
- **Judgment**: Good ↔ Bad (MC am Ende bei sich oder unbefriedigt)

`Outcome × Judgment` erzeugt vier Story-Endungen:
- Success + Good = **Triumph** (klassischer Sieg)
- Success + Bad = **Pyrrhic** (Goal erreicht, MC zerbrochen)
- Failure + Good = **Personal Triumph** (Goal verfehlt, MC reift)
- Failure + Bad = **Tragedy** (alles verloren)

## Wie man hier nachschlägt

Das Vokabular ist nach struktureller Funktion organisiert — **17 Type-Bucket-Files** mit den 265 originalen Dictionary-Termen, plus **6 erweiterte Werkzeug-Files**, plus **2 Indexe**.

### Source-Files (17) — Original-Dictionary, nach Type konsolidiert

Beim Öffnen eines Type-Files siehst du **alle** Terme dieser Kategorie nebeneinander, was Encoding-Arbeit beschleunigt (z.B. beim Lookup auf „Ability" siehst du sofort den ganzen Element-Quad mit Desire, Pursuit, Avoid).

| File | Inhalt | Wann öffnen |
|------|--------|-------------|
| `classes.md` | Class-Einträge | Throughline-Verortung **(unvollständig — siehe `dramatica-fundamentals.md` für Universe + Mind)** |
| `domains.md` | Throughline-Domains | Perspektivische Verteilung |
| `types.md` | 40 Types | Akt-Sequenz pro Throughline |
| `variations.md` | 63 Variations | Concerns / Issues |
| `elements.md` | 70 Elements | Atomare Charakter- und Konflikt-Bausteine |
| `archetypes.md` | Protagonist, Antagonist, Guardian, Contagonist, Reason, Emotion, Sidekick, Skeptic | Charakter-Konstellation |
| `character-dynamics.md` | Resolve, Growth, Approach, Mental Sex u.a. | MC-Konfiguration **(Resolve-Eintrag leer — siehe Fundamentals)** |
| `plot-dynamics.md` | Driver, Limit, Outcome, Judgment u.a. | Story-Form-Achsen |
| `overview-appreciations.md` | Story-weite strukturelle Aussagen | Storyform-Analyse |
| `structural-terms.md` | Act, Signpost, Journey, Quad u.a. | Struktur-Mechanik |
| `dynamic-terms.md` | Theorie-interne Dynamik-Begriffe | Tiefenarbeit |
| `storytelling.md` | Storyform↔Storytelling Layer | Encoding/Weaving |
| `dramatica-terms.md` | Theme, Vocabulary Item u.a. | Foundational |
| `dramatica-definitions.md` | Kerndefinitionen der Theorie selbst | Meta |
| `plot-structures.md` | Plot-Strukturmuster | Selten |
| `character-appreciations.md` | Höher-Ebenen-Charakter-Kategorien | Selten |
| `main-vs-impact-character.md` | MC↔IC-Beziehungs-Spezifika | RS-Throughline |

### Extension-Files (6) — Erweiterungen jenseits des Original-Dictionary

Diese Files füllen Lücken im Source-Material und liefern aktive Werkzeuge. **Jedes beginnt mit einem `⚠ EXTENSION NOTE`-Block** der Quelle und Vertrauensgrad markiert. Inhaltlich beruhen sie auf öffentlichen Dramatica-Quellen (storymind.com, dramaticapedia.com, narrativefirst.com) plus Claude's Trainingswissen.

| File | Wofür | Wann öffnen |
|------|-------|-------------|
| `dramatica-fundamentals.md` | Universe + Mind als Class; Resolve substantiell; Steadfast / Change; Linear / Holistic; MC-Dynamics-Übersicht | Bei jeder MC- oder Class-Diskussion **zuerst** lesen — die Source-Files haben hier Lücken |
| `storyform-mechanics.md` | Throughline-Distribution; MC↔IC Diametralität; Type-Sequenzen pro Class; Storyform-Cascade; Archetypen-Element-Pair-Mapping; Konsistenz-Checks | Beim Storyform-Aufbau, immer wenn die Frage „passen meine Wahlen zusammen?" auftaucht |
| `element-quads.md` | Die 16 Element-Quads + 16 Variation-Quads (KTAD-Pattern); Quad-Beziehungs-Typen (dynamic / companion / dependent) | Bei Encoding eines Moments — der Quad ist die Encoding-Einheit, nicht das Einzel-Element |
| `encoding-patterns.md` | Casablanca + Star Wars Worked Examples; Encoding-Heuristiken nach MC-Class; Pattern-Übertragung auf Lyrics/Novel/Spec; Anti-Patterns | Wenn ein User „wie übersetze ich X konkret?" fragt |
| `essential-questions.md` | Die ~14 Storyform-Fragen in Workflow-Reihenfolge; worked walkthrough Casablanca | Beim Storyform-Aufbau von Null an, oder beim Diagnose eines unklaren Storyforms |
| `_synonym-lookup.md` | 512 Aliases von Alltagsbegriffen → kanonische Dramatica-Terme | Wenn der User einen Begriff nutzt, der nicht offensichtlich in den Source-Files steht (z.B. „flaw" → Critical Flaw) |

### Indexe (1)

| File | Wofür |
|------|-------|
| `dynamic-pairs-index.md` | 75 reziproke Paare extrahiert aus den Source-Files. **Nutzungs-Hinweis**: vermischt Hierarchie-Ebenen (Element-Pairs neben Variation-Pairs) — bei Encoding-Arbeit besser `element-quads.md` konsultieren, das nach Quad und Class strukturiert ist. |

### Lookup-Disziplin

1. **Begriff bekannt, Type bekannt** → entsprechendes Type-File öffnen → zur Term-Section springen
2. **Begriff bekannt, Type unbekannt** → `_synonym-lookup.md` → File-Pointer folgen
3. **Konzept-Frage (Resolve, Class-Verteilung, Quad-Mechanik)** → entsprechendes Extension-File
4. **Storyform aufbauen** → `essential-questions.md` als Workflow + `storyform-mechanics.md` für Konsistenz
5. **Encoding eines konkreten Moments** → `element-quads.md` (welcher Quad?) + `encoding-patterns.md` (welche Heuristik?)

### Wenn Source-File und Extension-File widersprechen

Die Source-Files haben dokumentierte Lücken (leere Resolve-Definition, fehlende Universe/Mind als Class, fehlende Quad-Listen). Die Extension-Files füllen diese Lücken aus öffentlichen Dramatica-Quellen und Claude's Trainingswissen. Bei direkten Konflikten:

- **Wortlaut einer existierenden Source-Definition** → Source-File hat Vorrang (das ist die Original-Dictionary)
- **Strukturelle Mechanik / Quads / Class-Distribution** → Extension-File hat Vorrang (Source-Files haben hier nichts)
- **Bei kritischen Storyform-Entscheidungen für reale Publikation** → gegen offizielle Dramatica-Software oder das Phillips/Huntley-Buch *Dramatica: A New Theory of Story* verifizieren

## Encoding-Workflow

Wenn der Nutzer eine konkrete Storyform oder Story-Komponente entwickelt, läuft die Arbeit in dieser Reihenfolge — jeder Schritt hat ein zugehöriges File:

1. **Storyform aufbauen oder diagnostizieren** → `essential-questions.md` durchgehen (~14 Schlüsselentscheidungen in Workflow-Reihenfolge)
2. **Throughline-Verteilung prüfen** → `storyform-mechanics.md` (MC↔IC Diametralitäts-Regel, Class-Distribution)
3. **Konkretes Element/Variation/Type identifizieren** → entsprechendes Source-File (`elements.md`, `variations.md`, `types.md`)
4. **Quad lokalisieren** → `element-quads.md` — dort sind die 4 Elemente jedes Quads gemeinsam aufgelistet, mit dynamic/companion/dependent Pair-Beziehungen
5. **Encoding-Vorschlag formulieren** → `encoding-patterns.md` für Heuristiken nach MC-Class und für worked examples
6. **Konsistenz-Check** → `storyform-mechanics.md` Abschnitt „Encoding consistency — quick checks"

Wichtig: **Vorschläge, keine Vorschriften.** Dramatica beschreibt Strukturen, die in vollständigen Geschichten messbar sind — sie diktiert nicht, wie eine Geschichte erzählt werden muss. Wenn der Nutzer eine bewusste Abweichung wählt, ist das ein gültiges künstlerisches Mittel; markiere die Abweichung als Kommentar, nicht als Fehler.

### Quick-Reference für die häufigsten Konzept-Lookups

| Frage | Wo nachschauen |
|-------|----------------|
| „Welche Class hat MC X?" | `dramatica-fundamentals.md` (Class-Definitionen) + `storyform-mechanics.md` (Diametralitäts-Regel) |
| „Was ist der Dynamic Pair von X?" | Term-Eintrag im Source-File hat `**Opposite**:` Zeile (wenn vorhanden); fallback `dynamic-pairs-index.md` |
| „Welche anderen Elemente sind im selben Quad wie X?" | `element-quads.md` |
| „Steadfast oder Change für meinen MC?" | `dramatica-fundamentals.md` (Resolve-Tabelle) + `essential-questions.md` (Q8) |
| „Wie encode ich diesen Moment konkret?" | `encoding-patterns.md` (Heuristik nach MC-Class) + `element-quads.md` (Quad-Komplikations-Menü) |
| „Welche Type-Sequenz traversiert mein Throughline?" | `storyform-mechanics.md` (Type-Sequenzen) |
| „Was bedeutet [Begriff] im Alltagssprachgebrauch?" | `_synonym-lookup.md` |

## Navigator

Strukturelle Lookups (Was ist der Dynamic Pair von X? Welche Variation rollt zu welchem Type? Welche Elemente sitzen im selben Quad?) gehen **schneller** über `tools/dramatica-nav/nav.py` als über das Lesen der Reference-Files.

```bash
python3 tools/dramatica-nav/nav.py by-id el.trust              # einzelnes Term-Record
python3 tools/dramatica-nav/nav.py by-id el.trust --include-pairs  # plus dp.* Eintrag(e)
python3 tools/dramatica-nav/nav.py by-alias "Vertrauen" --lang de  # Locale-Alias
python3 tools/dramatica-nav/nav.py by-scenario novel.crucial-element-audit --kind element
python3 tools/dramatica-nav/nav.py by-quad quad.logic-feeling-el
```

Output ist JSON + ein `term_file`-Pointer. Mit `--full` wird die Prose-Section via `extract.py` inline gehängt; ohne `--full` öffnet der Agent die Prose nur, wenn die strukturelle Antwort nicht ausreicht.

**Token-Ökonomie:** Im Step-12-Benchmark (notes.md im Task 015) liegt die durchschnittliche Reduktion bei **83.4 %** gegenüber dem prose-only Pfad — die Lookup-Disziplin oben bleibt korrekt für konzeptuelle Fragen; für strukturelle Fragen ist `nav.py` der vorgesehene Erstgriff.

Cross-Cutting: die Lade-Trigger (NO.1–NO.6) für die Narrative-Ontology stehen in [`AGENTS.md § Narrative Ontology`](../../AGENTS.md). Non-narrative Sessions laden die Ontology gar nicht (NO.5 — Token-Ökonomie).

## Integration mit Schwester-Skills

**Mit `novel-architect`** (Kohärenz Protokoll):
- Bei Charakter-Beziehungs-Diskussionen: prüfe, ob ein klar definierter MC und IC vorliegt, und welcher Dynamic Pair die RS-Throughline trägt.
- Bei Akt-Struktur: Type-Sequenz pro Throughline ist die Akt-Architektur. Ein Element wechselt seine Type alle ~25% der Story-Länge.
- Bei OQ-Diskussionen: wenn eine offene Frage Dramatica-Vokabular brauchbar macht, biete präzise Begriffe an.

**Mit `the-agency-system-architect`** (Triptychon):
- Album 1 „Together We Confide" → Outcome/Judgment-Frage des MC (System).
- Album 2 „Moment der Klarheit" → Wandel der Resolve oder Growth.
- Album 3 „Gegenüber" → IC wird unabhängiges Subjekt → das ist eine RS-Throughline-Verschiebung.
- Track-Mapping: jeder Track besetzt typischerweise ein Element-Pair als zentralen Konflikt.

**Mit `suno-lyric-writer`**:
- Wenn ein Track eine klare dramatische Bewegung trägt: nenne explizit den Element-Pair, der den Vers-Refrain-Bridge-Bogen trägt. Das hilft dem Lyric-Writer, präzise zwischen Vers (eine Seite des Pairs) und Refrain (Spannung oder Auflösung) zu unterscheiden.

**Mit `spec-skill`**:
- Falls Storyform-Entscheidungen als Spec dokumentiert werden sollen: Dramatica-Termini sind kanonische Schlüssel. Das Spec-Vokabular (MUST/SHOULD) referenziert eindeutig auf Dramatica-Concepts.

## Was dieser Skill nicht tut

- **Kein voller Engine-Ersatz**: Dramatica's eigene patentierte Software-Engine (US #5,734,916) entscheidet, welche Element-Wahlen kompatibel sind. Dieser Skill dokumentiert die *publizierten* Engine-Regeln in `storyform-mechanics.md`, kann aber nicht alle Cascade-Konsequenzen einer Wahl deterministisch propagieren. Bei kritischen Storyform-Entscheidungen für reale Publikation: gegen die offizielle Software verifizieren.
- **Keine Theorie-Predigt**: Wenn der Nutzer ohne Dramatica-Sprache arbeiten will, drängen wir nichts auf.
- **Keine andere Story-Theorie**: Hero's Journey, Save the Cat, Story Circle, Three-Act, etc. sind nicht Teil dieses Skills.
- **Kein Copyright-konformer Re-Print der Dramatica Dictionary**: die References sind für interne Storyform-Arbeit gedacht, nicht zur Publikation.

## Notizen zur Quelle

**Source-Files (17 konsolidierte Type-Buckets, 265 Term-Einträge):** Extraktion der offiziellen Dramatica Dictionary (© Screenplay Systems Inc., 2001), von OCR-Artefakten bereinigt (Form-feeds, Page-Breaks, Copyright-Footer); inhaltlicher Wortlaut erhalten. Bei einigen Termen wurden kaputte oder fehlende `type`-Felder rekonstruiert (`Theme` → Dramatica Term, `Quad` → Structural Term, etc.).

**Extension-Files (6, mit `⚠ EXTENSION NOTE`-Markierung):** Erweiterungen jenseits des Original-Dictionary. Beruhen auf öffentlicher Dramatica-Dokumentation (storymind.com, dramaticapedia.com, narrativefirst.com) und Claude's Trainingswissen. Diese Files füllen dokumentierte Lücken im Source-Material:
- L1: Universe + Mind als Class fehlten in Source → ergänzt in `dramatica-fundamentals.md`
- L3: Steadfast / Linear / Holistic fehlten als eigene Einträge → ergänzt in `dramatica-fundamentals.md`
- L4: `Resolve` Source-Eintrag war leer → substantielle Definition in `dramatica-fundamentals.md`
- L5: Die 16 Element-Quads waren nirgends aufgelistet → in `element-quads.md`
- L8/L9/L10: Storyform-Engine-Regeln, MC↔IC-Diametralität, Type-Sequenzen → in `storyform-mechanics.md`
- L11: Worked examples fehlten → Casablanca + Star Wars in `encoding-patterns.md`
- L12: Die 12 Essential Questions als Workflow → in `essential-questions.md`

Bei Diskrepanzen zwischen Source und Extension: Source hat Vorrang für Wortlaut von Original-Definitionen; Extension hat Vorrang für Mechanik/Quads/Engine-Regeln (wo Source schweigt).
