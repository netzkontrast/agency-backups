---
topic: "Obsidian Frontmatter & Metadaten-Ontologie für agentic Workflows — Spec-Grundlage für tokeneffiziente Navigation"
slug: "obsidian-frontmatter-agentic-spec"
research_category: "A"
research_category_label: "Exploration"
critical_thinking_methods:
  - "Falsification (Popper)"
  - "First-Principles Decomposition"
  - "Steelmanning"
  - "Contrast Classes"
  - "Adversarial Query Expansion"  # M13 — immer vorhanden (v2.1)
prompt_engineering_framework_agentic_spine: "ReAct"
prompt_engineering_framework_structural: "RISEN"
bespoke_framework_provenance: null
cross_pollination:
  - source_category: "B"
    step_id: "i.b"
    description: "Surviving-Branch Triangulation — überlebende Schema-Hypothesen gegen real existierende Tools und Vault-Implementierungen triangulieren"
  - source_category: "C"
    step_id: "i.c"
    description: "Hypothesis Half-Life Audit — Schema-Annahmen die in frühen Iterationen stabilisiert wurden, gegen spätere Fundings auf Verfall prüfen"
constraint_blocks:
  - "0 — Reflection Baseline"
  - "1 — Source Priority Rules"
  - "2 — Temporal Scope"
  - "3 — Output Exclusions"
  - "4 — Obsidian-Kompatibilitätspflicht"
  - "5 — Agentic-Konsumenten-Dualität"
language: "de"
target_agent: "model-agnostic"
created: "2026-05-02"
version: "1.0"
source_skill: "research-prompt-optimizer v2.1.0"
---

# Research Prompt: Obsidian Frontmatter & Metadaten-Ontologie für agentic Workflows

> **Für die ausführende KI:** Dieser Prompt ist vollständig selbst-contained. Jede Methode,
> jedes Framework, jede Constraint die du benötigst ist inline definiert. Du brauchst
> keinen externen Kontext, keine Vorkenntnis über spezifische Methodologien, kein
> Wissen über das Skill das diesen Prompt erzeugt hat. Lies den vollständigen Prompt
> bevor du beginnst.

---

## Meta-Header — Was dieser Prompt ist und wie er gelesen werden soll

Dieser Research-Prompt kombiniert drei unabhängige Schichten:

### Schicht 1 — Epistemologische Ebene (Research Category A — Exploration)

**Category A — Exploration (Recursive Search / Tree of Thoughts):**
Kategorie A wird gewählt wenn die Antwort wirklich unbekannt ist — nicht nur ungesammelt,
sondern unentdeckt. Ziel ist das Erzeugen und Testen von Hypothesen, nicht das Aggregieren
bekannter Fakten.

**Kernstrategie:** Baumsucheeüber einem Hypothesenraum mit explizitem Backtracking. Du —
die ausführende KI — formulierst mehrere konkurrierende Hypothesen, führst für jede
bestätigende UND orthogonale (widerlegende) Suchen durch, machst Backtracking wenn ein Ast
scheitert, und surfst den vollen Hypothesenbaum im Output — nicht nur den überlebenden Ast.

**Warum Category A für diesen Prompt:** Es gibt viele Obsidian-Best-Practices, es gibt
LLM-Context-Management-Literatur, es gibt Zettelkasten-Theorie — aber niemand hat das für
agentic workflows und tokeneffizientes Arbeiten auf einem Niveau synthetisiert, das als Spec
für ein Python-Tool und mehrere Agent-Konsumenten-Typen gleichzeitig taugt. Die Lücke ist
real; sie muss durch Exploration aufgedeckt werden, nicht durch Extraktion.

**Abbruchkriterium für diese Kategorie:** Akzeptiere „wir wissen es nicht" als validen
Endzustand. Zwinge keine Schlussfolgerung wenn die Evidenz dünn ist.

### Schicht 2 — Agentic Spine: ReAct (Reason + Act + Observe)

**ReAct — immer aktiv, jede Iteration:**
Jede autonome Research-Schleife folgt dem ReAct-Zyklus. Jede Iteration besteht aus:

- **Reason:** Du formulierst dein aktuelles Verständnis und planst die nächste Aktion.
  Du benennst welche Hypothese du testest, welcher Constraint Block diesen Schritt regiert,
  welche Critical-Thinking-Methode aktiv ist.
- **Act:** Du führst genau eine Aktion aus (typischerweise eine Suche oder ein Retrieval).
- **Observe:** Du hältst fest was die Aktion zurückgegeben hat und was das für den Plan
  bedeutet. Du entscheidest explizit: diesen Ast fortsetzen, Backtrack, oder
  Query-Vocabular erweitern (Methode: Adversarial Query Expansion).

**Schleifenstruktur:**
```
[Reason 1] → [Act 1] → [Observe 1] →
[Reason 2] → [Act 2] → [Observe 2] →
...
[Reason N] → [Pre-Synthesis Integrity Check] → [Synthesis]
```

**Deine erste Aktion vor Reason 1:** Restiere das Research-Ziel und alle aktiven
Constraint Blocks. Starte nicht direkt mit Act.

**Innerhalb jeder Reason-Phase beantwortest du explizit drei Fragen:**
1. Was glaube ich gerade, und wie stark?
2. Welche aktive Critical-Thinking-Methode gilt für diese nächste Act?
3. Bin ich in Gefahr eines Local-Minimum-Lock-In? (Falls ja → invoke Adversarial
   Query Expansion bevor du die nächste Act wählst.)

### Schicht 3 — Strukturelle Ebene: RISEN Framework

**RISEN — Structural Layer:**
RISEN regiert die Makro-Organisation dieses Prompts; ReAct regiert die Mikro-Iteration
innerhalb jedes Steps. RISEN steht für:

- **R — Role:** Wer du während dieser Aufgabe bist.
- **I — Input:** Welche Materialien, Fragen oder Daten du als Ausgangspunkt hast.
- **S — Steps:** Die explizite geordnete Prozedur.
- **E — Expectations:** Wie ein erfolgreicher Output aussieht.
- **N — Narrowing:** Harte Constraints, Ausschlüsse, Scope-Grenzen.

**Deine erste Aktion vor Step 1:** Restiere die Role- und Narrowing-Sektionen in
deinen eigenen Worten. Bestätige dass du sie internalisiert hast. Beginne Step 1 nicht
bevor diese Restatement-Bestätigung geschrieben ist.

---

## Research-Ziel (I — Input)

**Kernfrage:** Welche Frontmatter/Metadaten-Architektur für Obsidian-Vaults ist so
gestaltet, dass sie gleichzeitig drei Konsumenten-Typen bedient — Obsidian-UI,
menschliche Autoren/Entwickler, und autonome KI-Agenten — ohne Konflikte zwischen
diesen zu erzeugen? Und welche Regeln/Heuristiken bestimmen, wann eine Datei in ein
Expansion-Pattern (Datei bleibt als Index-Node, Inhalt wandert in Unterordner)
überführt werden soll?

**Kontext der Anwendung:** Auf Basis dieser Research-Ergebnisse soll eine Spec
entwickelt werden, die (a) ein minimales Python-Script trägt das Metadaten tokeneffizient
ausliest, (b) als SKILL.md-Referenz für Agent-Skills nutzbar ist, (c) von Claude Code,
einem Agent Skill, und Google Jules gleichzeitig als Tool konsumiert werden kann.

**Temporaler Scope:** 2020–2026. Obsidian erschien 2020; alles davor ist nur relevant als
Vorläufer (Zettelkasten-Theorie, PKM-Prinzipien).

**Zielgruppe des finalen Outputs:** Technischer Architect der eine Metadaten-Spec und
ein Python-Tool entwickelt. Output muss synthetisierend und operationalisierbar sein —
keine reine Linkliste, sondern strukturierte Erkenntnisse die direkt in eine Spec
übersetzbar sind.

**Erwartete Tiefe:** Exhaustive innerhalb des Scopes. Wo direkte Quellen fehlen, muss
die KI selbst synthetisieren und das explizit kennzeichnen.

**Output-Format:** Strukturierter Report mit Hypothesenbaum, Befunde-Matrix, und
einem Synthesis-Abschnitt der direkt als Spec-Grundlage dient. Deutscher Fließtext
für Synthese, Englisch für Schema-Definitionen und Code-Beispiele.

---

## CONSTRAINT BLOCKS

### CONSTRAINT BLOCK 0 — Reflection Baseline (Immer aktiv · v2.1)

Reflection ist kein Polierschritt. Es ist eine **basale operative Anforderung** die
parallel zu jeder anderen Aktivität in dieser Research läuft. Du führst gezielte
Reflektion an jedem definierten Checkpoint durch, schriftlich, mit dem Template unten.
Ein Checkpoint der ohne Reflektion-Eintrag erreicht wird ist ein unvollständiger
Checkpoint — gehe nicht darüber hinaus.

**Reflection Checkpoints (Minimum):**

1. **Kickoff-Reflektion** — direkt nach der Restatement von Role/Narrowing und vor
   der ersten Suche.
2. **Mid-Run-Reflektion** — nach dem ersten Suchbatch, wenn eine tentative Richtung
   existiert aber noch nicht committed wurde.
3. **Post-Query-Expansion-Reflektion** — nach jedem Adversarial Query Expansion Pass
   (siehe Methode M13).
4. **Pre-Synthesis-Reflektion** — direkt vor dem Pre-Synthesis Integrity Check.
5. **Post-Synthesis-Reflektion** — nach der Entwurfs-Synthese, vor der Auslieferung.

**Reflection Template — Verbatim verwenden:**

> **Q1. Was glaube ich gerade tatsächlich, und wie confident bin ich?**
> (Ein Satz. Explizites Confidence-Band: niedrig / mittel / hoch.)
>
> **Q2. Was ist das stärkste Gegenbeispiel gegen meine aktuelle Überzeugung?**
> (Nenne die spezifische Quelle oder Beobachtung. Wenn du keine nennen kannst,
> ist das selbst die Antwort — und eine Warnung.)
>
> **Q3. Wo liege ich am wahrscheinlichsten falsch, und warum?**
> (Nicht generisch — nenne den spezifischen Claim, die Annahme oder Inferenz
> die am schwächsten ist.)
>
> **Q4. Was würde ich anders machen wenn ich die Research von vorne beginnen würde
> mit dem Wissen das ich jetzt habe?**
> (Erzwingt De-Anchoring vom bereits gegangenen Pfad.)
>
> **Q5. Was ist die einzige höchstwertige nächste Aktion?**
> (Muss ein konkreter, ausführbarer nächster Schritt sein — eine spezifische Suche,
> eine spezifische Verifikation, eine spezifische Hypothesenast die geöffnet oder
> geschlossen werden soll.)

**Regeln:**
- Reflektionen sind geschrieben, nicht intern. Sie werden Teil der Research-Notes
  und des finalen Outputs.
- Reflektionen dürfen nicht übersprungen werden „weil die Antwort offensichtlich ist".
  Wenn die Antwort offensichtlich scheint, schreibe sie in einer Zeile — aber lass den
  Eintrag nicht weg.
- Wenn eine Reflektion eine Maßnahme in Q5 produziert die dem aktuellen Step-Plan
  widerspricht, hat die Maßnahme Vorrang. Aktualisiere den Plan, notiere die Änderung,
  fahre fort.

**Anti-Rationalization Guard:** Wenn du merkst dass du „N/A" oder „nichts zu
reflektieren" schreibst — stop und lies die fünf Fragen erneut. Mindestens Q2 und Q3
haben immer eine echte Antwort.

---

### CONSTRAINT BLOCK 1 — Source Priority Rules

Diese Regeln regieren jede Quellenauswahl. Sie bleiben in jedem Step aktiv;
du restatierst sie vor jedem Major Step.

1. **Primärquellen haben Vorrang:** Offizielle Obsidian-Dokumentation, Obsidian
   GitHub (Issues, Changelogs, RFCs), peer-reviewed PKM-Forschung, offizielle
   Plugin-Repositorys — vor allen anderen.
2. **Aggregatoren nur für Discovery:** Community-Foren (Obsidian Forum, Reddit
   r/ObsidianMD), Discord-Exports, Blog-Posts dürfen für Entdeckung verwendet
   werden, aber nie als alleinige Quelle für faktische Ansprüche.
3. **Praktiker-Vaults und Open-Source Implementierungen** gelten als Sekundärquellen.
   GitHub-Repos mit YAML-Frontmatter-Schemas, llm-wiki-Projekte,
   Zettelkasten-Implementierungen — für Muster-Extraktion valide, aber triangulierend
   belegt.
4. **Bei Quell-Konflikten:** Wende die Contradiction Log Methode an — wähle nicht
   stillschweigend eine Seite.
5. **Synthetische Erkenntnis** (wo keine direkte Quelle existiert, du aber
   ableitest): Markiere explizit als `[SYNTHESE — keine direkte Quelle]`.

---

### CONSTRAINT BLOCK 2 — Temporal Scope

Research deckt **2020–2026** ab. Obsidian v1.0 erschien Oktober 2022; das ist ein
wichtiger Wendepunkt (Properties UI, standardisiertes YAML-Frontmatter). Quellenunter
2020 nur wenn sie Zettelkasten- oder PKM-Vorläufer-Konzepte belegen.

**Ausnahme:** Agentic/LLM-spezifische Quellen ab **2022** (Beginn der praktischen
LLM-Adoption). Für den agentic-workflow Teil des Prompts gilt 2022–2026.

---

### CONSTRAINT BLOCK 3 — Output Exclusions

Du musst NICHT einschließen:
- Obsidian-Plugin-Implementierungsdetails (wie man ein Plugin entwickelt) — nur
  welche Plugins existieren, was sie an Metadaten ermöglichen, als Linkliste.
- Allgemeine PKM-Philosophie ohne direkten Bezug zu Metadaten/Frontmatter.
- Vergleiche Obsidian vs. andere Tools (Notion, Logseq, Roam) — außer wo sie
  direkt Metadaten-Schema-Entscheidungen informieren.
- Marketing-Material und Feature-Ankündigungen ohne technischen Substanz.

---

### CONSTRAINT BLOCK 4 — Obsidian-Kompatibilitätspflicht

Jede Schema-Empfehlung die du entwickelst oder synthetisierst muss gegen diese
Obsidian-Hardgrenzen validiert sein:

1. **YAML-Frontmatter-Only:** Obsidian Properties UI versteht nur den YAML-Block
   zwischen `---` Delimitern. Kein TOML, kein JSON, kein inline-Metadata.
2. **Maximal 2 Verschachtelungsebenen:** Obsidian's Properties-UI bricht bei tiefer
   Verschachtelung. `key: value` und `key: [list]` und `parent:\n  child: value`
   sind sicher. Tiefer nicht.
3. **Obsidian-native Typen:** `string`, `list`, `date`, `datetime`, `number`, `bool`,
   `link` (Wikilink-Format). Keine Custom-Types.
4. **Reservierte Keys:** `tags`, `aliases`, `cssclasses` sind Obsidian-intern. Schema
   darf sie verwenden, aber nicht umdefinieren.
5. **Dateigröße hat kein hartes Obsidian-Limit**, aber Graph-Performance degradiert
   über ~500 Dateien ohne strukturierte Metadaten erheblich.

Jede Empfehlung die eine dieser Grenzen verletzt ist als **Obsidian-inkompatibel**
zu flaggen, auch wenn sie agentic nützlich wäre.

---

### CONSTRAINT BLOCK 5 — Agentic-Konsumenten-Dualität

Die Metadaten-Spec muss drei Konsumenten gleichzeitig bedienen. Jede Schema-Entscheidung
muss gegen alle drei getestet werden:

| Konsument | Primärbedürfnis | Token-Constraint |
|-----------|----------------|------------------|
| **Obsidian UI** | Graph-Traversal, Search, Backlinks, Properties-Anzeige | Nicht relevant |
| **Menschlicher Autor/Entwickler** | Lesbarkeit, semantische Reichhaltigkeit, schnelles Verständnis | Nicht relevant |
| **Autonomer KI-Agent** (Claude Code, Jules, Agent-Skill) | Navigieren ohne Dateien zu öffnen, Entscheidungen aus Metadaten allein | KRITISCH — minimale Token-Last bei maximaler Navigations-Präzision |

**Goldene Regel für die ausführende KI:** Wenn ein Metadaten-Feld für Konsument 3
(Agent) nicht aus dem Frontmatter allein entscheidbar ist ob eine Datei relevant ist —
dann ist es ein Design-Failure, kein Feature.

---

## CRITICAL-THINKING METHODS — Aktiv durch die gesamte Ausführung

Die folgenden Critical-Thinking-Methoden sind während der gesamten Ausführung
aktiv. Du restatierst den „Wie anwenden"-Abschnitt jeder Methode bei jedem Major
Step per dem Restatement-Checkpoint-Protokoll.

---

### Method: Falsification (Karl Popper's Disconfirmation Principle)

**Was es ist:** Statt nach Evidenz zu suchen die eine Hypothese stützt, suchst du
aktiv nach Evidenz die sie widerlegen würde. Eine Hypothese verdient Glaubwürdigkeit
erst nachdem sie ernsthafte Widerlegungsversuche überlebt hat.

**Warum in diesem Prompt:** Confirmation Bias ist der dominante Failure Mode autonomer
Research-Agenten. Ohne explizite Falsifikationsschritte wirst du Belege surfacen die
das überlebende Schema stützen und Widersprüche untergewichten.

**Wie anwenden — Schritt für Schritt:**
1. Schreibe vor der Suche die Hypothese als falsifizierbaren Statement (einer der
   prinzipiell durch beobachtbare Evidenz widerlegt werden kann).
2. Für jedes unterstützende Fundstück führe eine **matched disconfirmation query** aus —
   eine Suche die speziell designt ist das stärkste Gegenbeispiel zu surfacen.
   Beispiel: Wenn du findest „L0+L1+L2 Ebenenarchitektur ist best practice" → suche
   auch nach „flat frontmatter schema is better than layered", „YAML nesting causes
   agent confusion".
3. Gewichte Widerlegungsversuche gleichwertig oder höher als Bestätigungen.
4. Wenn kein ernsthafter Widerlegungsversuch Gegenbeispiele surfaced: explizit
   angeben: „Diese Hypothese überlebte N Falsifikationsabfragen."

**Abbruchkriterium:** Stopp wenn die Hypothese mindestens drei orthogonale
Falsifikations-Queries überlebt hat ODER wenn Gegenbeweise über 20% des Gesamtevidenz-
Pools ausmachen.

---

### Method: First-Principles Decomposition

**Was es ist:** Du zerlegst die Research-Frage in ihre grundlegendsten, empirisch oder
logisch fundamentalen Komponenten — weigerst dich jedes Zwischenkonzept ohne
Rechtfertigung zu akzeptieren. Dann baust du die Analyse von diesen Grundebenen
aufwärts.

**Warum in diesem Prompt:** „Metadaten-Schema" und „agentic navigation" und „Obsidian-
Kompatibilität" sind geerbte Begriffe die ungeprüfte Annahmen einschmuggeln. Was ist
ein Metadatum wirklich? Was ist agentic navigation im Token-ökonomischen Sinne?
Was bedeutet Obsidian-Kompatibilität operativ?

**Wie anwenden — Schritt für Schritt:**
1. Schreibe die Research-Frage in Alltagssprache.
2. Für jedes Substantiv oder Adjektiv: „Was ist das *wirklich* — auf der
   fundamentalsten Ebene?" Ersetze den Begriff durch seine zerlegten Komponenten.
3. Iteriere bis die Frage nur noch in direkt beobachtbaren oder logisch notwendigen
   Komponenten ausgedrückt ist.
4. Beantworte die zerlegte Version. Dann übersetze zurück in das originale Vokabular,
   und notiere wo die Übersetzung Annahmen einführt.

**Abbruchkriterium:** Stopp wenn weitere Zerlegung keine neue Struktur mehr aufdeckt
— typischerweise nach 2–3 Ebenen.

**Beispiel-Trigger:** „Frontmatter-Spec" zerfällt in: Was ist Frontmatter? (YAML-Block,
parsed by remark-frontmatter, gerendert als Properties) — Was ist eine Spec? (normatives
Dokument mit Muss/Kann/Darf-nicht Regeln) — Was ist das Minimum? (Was ist die kleinste
Menge Felder die alle drei Konsumenten bedient?)

---

### Method: Steelmanning (Strongest-Version Reconstruction)

**Was es ist:** Bevor du eine Hypothese oder Ansatz aufgibst, rekonstruierst du ihre
stärkste mögliche Version. Du stiftest sie nicht mit dem schwächsten Argument.

**Warum in diesem Prompt:** Es gibt konkurrierende Paradigmen — „flat schema ist besser
für Agenten", „reichhaltig semantisches Schema ist besser für Menschen", „kein YAML,
nur Inline-Links" — und es ist verlockend diese an ihren schwächsten Vertretern
zu messen.

**Wie anwenden:**
1. Bevor du eine konkurrierende Architektur/Ansatz verwirfst: Schreibe den stärksten
   Fall für sie in 2–3 Sätzen.
2. Nur wenn der Straw-Man-Test bestanden ist (du kannst den stärksten Fall artikulieren)
   darf du ihn als „schwächer als Alternative X" bewerten.
3. Notiere „Straw-Man-Test: Bestanden" oder „Straw-Man-Test: Fehlgeschlagen
   (konnte stärksten Fall nicht formulieren)" explizit.

**Abbruchkriterium:** Stopp wenn du für jeden verworfenen Ansatz einen
Straw-Man-Bestätigung-Eintrag hast.

---

### Method: Contrast Classes

**Was es ist:** Du machst bei jeder evaluativen Aussage explizit „verglichen womit?"
Eine Metadaten-Architektur ist nicht „gut" — sie ist gut verglichen mit einer spezifischen
Alternative unter spezifischen Bedingungen.

**Warum in diesem Prompt:** Aussagen wie „layered schema ist besser" sind wertlos ohne
expliziten Kontrast. Besser für Obsidian UI? Besser für Agenten? Besser für kleine
Vaults? Besser für 50.000 Dateien?

**Wie anwenden:**
1. Für jede evaluative Aussage: Schreibe die Contrast Class explizit.
   Format: „[AUSSAGE] — verglichen mit [ALTERNATIVE] — unter [BEDINGUNG]."
2. Wenn du keine Contrast Class formulieren kannst, ist die Aussage noch
   nicht operabel.

**Abbruchkriterium:** Jede Empfehlung im finalen Output hat eine explizite Contrast Class.

---

### Method: Adversarial Query Expansion

**Was es ist:** Eine ständige Direktive die dich zwingt, das Such-Vokabular autonom
an definierten Checkpoints zu erweitern. Du bist nicht an die Abfrage-Begriffe des
initialen Prompts gebunden; du bist verpflichtet sie zu überarbeiten. Ziel ist
**Local-Minimum-Lock-In** zu verhindern.

**Warum in diesem Prompt:** Das initiale Vokabular — „Obsidian Frontmatter", „YAML
Metadata", „agentic navigation" — trägt die Framing-Blinden Flecken des Auftraggebers.
Kritische Begriffe wie „sidecar files", „knowledge graph ontology", „property-graph PKM",
„PKMS" (Personal Knowledge Management Systems), „second brain tooling", „LLM context
compression" gehören möglicherweise zum relevanten Lösungsraum, werden aber im Seed-
Vokabular nicht erwähnt.

**Wie anwenden — Schritt für Schritt:**

1. **Seed Query Set bauen.** Schreibe zu Beginn die Abfragen auf die der Prompt
   impliziert oder explizit nennt. Das ist dein Startvokabular.

2. **Expansion entlang vier Achsen bei jedem Major Checkpoint.** Nach jedem
   Suchbatch (oder alle 10 Minuten agentic Zeit, je nachdem was früher kommt),
   generiere neue Abfragen entlang jeder dieser Achsen und führe die
   vielversprechendste pro Achse aus:

   - **Adjacent Axis:** Synonyme, verwandte Subfelder, benachbarte Disziplinen,
     äquivalente Industrie-Begriffe, anderssprachige Begriffe. Beispiel:
     „Obsidian YAML frontmatter" → „PKM metadata taxonomy", „Zettelkasten
     property schema", „knowledge graph node attributes", „Obsidian Dataview
     query fields".

   - **Opposing Axis:** Die Negation, der Failure Case, die entgegengesetzte
     Schule, die „X funktioniert nicht"-Literatur. Beispiel: „structured
     frontmatter for AI agents" → „YAML frontmatter limitations LLM",
     „frontmatter schema fragility", „metadata overhead zettelkasten".

   - **Abstraction Axis:** Eine Ebene rauf oder runter. Rauf: die Kategorie
     zu der das Thema gehört. Runter: ein konkreter Sub-Fall. Beispiel:
     „Obsidian agent workflow" ↑ „knowledge base agent navigation" ↑
     „graph-structured document retrieval for LLM agents" ↓ „Claude Code
     Obsidian vault tool".

   - **Orthogonal Axis:** Ein Winkel den das originale Framing überhaupt nicht
     bedacht hat. Oft am wertvollsten. Frage: „Welche Linse hat noch niemand
     in meinem Seed-Set verwendet?" Beispiele für diesen Prompt: Bibliotheks-
     wissenschaftliche Metadaten-Standards (Dublin Core, Schema.org), Code-
     Repository-Metadaten-Patterns (CODEOWNERS, package.json als Analogie),
     Game-Engine-Asset-Management-Schemas als Analogie für große Dateibestände.

3. **Jede Expansion loggen.** Führe ein **Query Expansion Log**: Für jede
   Expansion, (a) die Achse, (b) die neue Abfrage, (c) ob die Suche novel
   findings zurückgab die der Seed-Set nicht abdeckt, (d) ob diese Findings
   eine tentative Schlussfolgerung modifiziert haben.

4. **Expansionen zurück in Hypothesen speisen.** Wenn eine Expansion ein Finding
   surfaced das die aktuelle Arbeitshypothese widerspricht oder erweitert: als
   First-Class-Input behandeln.

5. **Expansion durch Reflexion steuern, nicht durch Token-Budget.** Vor jedem
   Expansion-Pass: Schreibe einen Satz der beantwortet „Was übersehe ich gerade
   am wahrscheinlichsten, und warum?"

**Abbruchkriterium:** Stopp die Expansion einer Achse wenn zwei aufeinanderfolgende
Expansionen entlang dieser Achse keine novel findings produzieren.

**Hard Anti-Rationalization Rule:** Wenn du denkst „das Seed-Vokabular ist bereits
umfassend" — das ist das Signal zur Expansion, nicht das Signal zum Überspringen.

---

## R — Role (RISEN)

Du bist ein **PKM-Architekt und LLM-Systems-Ingenieur** mit tiefer Expertise in:

- Obsidian-Vault-Design (inkl. YAML-Frontmatter-Spezifikation, Obsidian Properties API,
  Plugin-Ökosystem)
- Knowledge-Graph-Modellierung und Ontologie-Design (RDF, Dublin Core, Schema.org als
  Analogien; nicht als Ziel-Technologien)
- Token-ökonomisches Design für LLM-Context-Windows (wie man große Datenbestände
  navigiert ohne Dateien vollständig laden zu müssen)
- Agent-Tool-Design (CLI-Tools, Python-Bibliotheken die von Claude Code, Jules, und
  Agent-Skills konsumiert werden)
- Zettelkasten-Methodik und PKM-Praxis (Luhmann-Original, digitale Varianten,
  Evergreen-Notes-Konzepte)

Du forschst für einen Software-Architekten der eine Obsidian-Vault-Metadaten-Spec
entwickeln will. Die Spec muss (a) eine normative Basis für ein Python-Script bilden
das tokeneffizient Metadaten ausliest, (b) von Claude Code, einem Agent-Skill (SKILL.md),
und Google Jules konsumierbar sein, und (c) vollständig Obsidian-kompatibel bleiben.

---

## S — Steps (RISEN)

### RESTATEMENT CHECKPOINT vor Step 1

Restiere vor Step 1 (und vor jedem weiteren Step): Role-Definition in eigenen Worten,
alle aktiven Constraint Blocks (0–5), die fünf aktiven Critical-Thinking-Methoden.
Schreibe den Restatement aus — paraphrasiere nicht nur.

**Kickoff-Reflektion (CONSTRAINT BLOCK 0):** Führe jetzt die Kickoff-Reflektion aus
(Q1–Q5 nach Template). Beginne Step 1 erst danach.

---

### Step 1 — First-Principles Zerlegung der Kernbegriffe

*[ReAct: Reason → Akt als Begriffszerlegung → Observe was neu ist]*

**Ziel:** Operationale Definitionen entwickeln bevor irgendeine Suche startet.

Zerlege folgende Begriffe nach der First-Principles Methode:

**1.1 — Was ist „Obsidian Frontmatter"?**

Zerlege: YAML-Parser, Delimiter-Konvention, Obsidian Properties UI-Rendering,
Unterschied zu Inline-YAML, Verhältnis zu Obsidian-Plugins (Dataview, Templater).
Suche: offizielle Obsidian-Doku zu Properties und Frontmatter.

**1.2 — Was ist „tokeneffizientes Navigieren"?**

Zerlege: Was ist ein Token in diesem Kontext? Was ist Navigieren (Entscheiden ob eine
Datei relevant ist, ohne sie vollständig zu laden)? Wie viele Tokens kostet ein
YAML-Block à 10 Felder vs. das Laden einer 5k-Token Markdown-Datei? Berechne die
Order-of-Magnitude-Differenz.

Suche: LLM context window management patterns, agentic RAG metadata-first retrieval.

**1.3 — Was ist das „Expansion Pattern"?**

Zerlege: Unter welcher Bedingung wird eine Datei zu einem Index-Node? Was genau
wandert in den Unterordner (Inhalt ohne Identity)? Was bleibt in der Originaldatei
(Identity + Metadaten + Querverweise)? Was ist eine README.md in diesem Kontext
(Manifest-Datei, nicht Dokumentation)?

Suche: Zettelkasten folder structure patterns, Obsidian folder note plugin, large
vault organization strategies.

**1.4 — Was ist das Minimum einer „Spec"?**

Zerlege: Was ist der Unterschied zwischen MUSS (normativ verpflichtend), KANN
(optional empfohlen), und DARF NICHT (explizit verboten)? Welche Felder braucht
jeder Konsumenten-Typ als absolutes Minimum?

**Restatement Checkpoint nach Step 1:**
Restiere die aktiven Constraint Blocks 0–5 und die fünf Methoden verbatim.

---

### Step 2 — Hypothesenbaum: Welche Metadaten-Schichtarchitektur ist richtig?

*[ReAct: Reason → systematische Suche je Ast → Observe je Ast mit Falsifikation]*

**Übergeordnete Hypothese:** Es gibt eine Metadaten-Schichtarchitektur für Obsidian-
Vaults die alle drei Konsumenten gleichzeitig bedient ohne Kompromisse die einen
Konsumenten effektiv ausschließen.

**Formuliere vor Beginn drei konkurrierende Hypothesen:**

- **H1 — Flat Schema:** Alle Metadaten auf einer Ebene, maximal 15 Keys,
  keine Verschachtelung. Vorteil: Obsidian-kompatibel, Agent-lesbar. Nachteil?
- **H2 — Layered Schema mit Namespacing:** L0 (Obsidian-nativ) + L1 (Vault-Core)
  + L2 (Domain-Extension per Prefix) + L3 (Agent-Only). Vorteil: Semantische
  Reichhaltigkeit. Nachteil?
- **H3 — Sidecar-Model:** Hauptdatei hat minimales Frontmatter; Agent-spezifische
  Metadaten in einer `.meta.yml` Sidecar-Datei. Vorteil: Obsidian-UI sauber.
  Nachteil?

**Suche für jede Hypothese:**

2a. Suche bestätigende Evidenz: Implementierungen, Best-Practice-Guides, Community-
    Konsens auf Obsidian Forum und GitHub. Keywords: „Obsidian frontmatter schema layers",
    „YAML metadata namespacing knowledge base", „PKM metadata architecture".

2b. Suche widerlegende Evidenz (Falsifikation): „flat frontmatter better than layered",
    „YAML sidecar metadata drawbacks", „Obsidian Properties nesting problems",
    „agent YAML parsing errors nested schema".

2c. Suche spezifisch nach agentic Obsidian Implementierungen: „LLM wiki Obsidian agent",
    „Claude Code Obsidian vault tool", „AI agent Obsidian navigate metadata", „Jules
    Google Obsidian workflow", „agentic Zettelkasten LLM", „second brain AI agent
    navigate".

2d. Steelmanning: Bevor du H1, H2, oder H3 verwirfst — formuliere den stärksten Fall.
    Notiere Straw-Man-Test Ergebnis.

**Adversarial Query Expansion Pass 1 (M13):**
Nach 2a–2d: Führe den ersten Query-Expansion-Pass durch (alle vier Achsen).
Logge im Query Expansion Log.

**Mid-Run-Reflektion (CONSTRAINT BLOCK 0):** Führe jetzt die Mid-Run-Reflektion
aus (Q1–Q5).

**Restatement Checkpoint nach Step 2:**
Restiere Constraint Blocks 0–5 und die fünf Methoden verbatim.

---

### Step 3 — Die vier Metadaten-Ebenen im Detail: Was kann Obsidian von Haus aus?

*[ReAct: Reason → gezielte Suche pro Ebene → Observe mit Contrast-Class-Validierung]*

**Ziel:** Vollständige, quellenbasierte Aufstellung was Obsidian nativ verarbeitet,
was es ignoriert, und was es bricht.

**3.1 — L0: Obsidian Default (Minimal):**

Suche: Offizielle Obsidian Properties-Doku, Obsidian Help-Vault, GitHub obsidianmd.
Spezifisch: Welche Keys sind Obsidian-reserviert? (`tags`, `aliases`, `cssclasses`,
`publish`). Welche Types erkennt Obsidian Properties nativ (seit v1.0)?

**3.2 — L1: Vault Core (was muss jede Datei haben):**

Synthese-Schritt: Was ist das Minimum das alle drei Konsumenten-Typen gleichzeitig
brauchen? Suche: „Obsidian minimum frontmatter", „required YAML fields knowledge base",
„LLM metadata minimum viable". Contrast Class: Was ist das Minimum verglichen mit
einem reinen Obsidian-Vault ohne Agenten-Anforderung? Was kommt durch den
Agenten-Bedarf hinzu?

Kandidaten für L1-Pflichtfelder (zu validieren, nicht vorgebend):
- `type` — Was ist das? (note / index / manifest / resource / log)
- `status` — Wo im Lifecycle? (draft / active / archived / deprecated)
- `summary` — Eine-Satz-Zusammenfassung für Agenten
- `created` / `modified` — Timestamps
- `tags` — Obsidian-nativ
- `created_by` — human / agent / human+agent

Prüfe für jeden Kandidaten: Brauchbar für alle drei Konsumenten? Obsidian-kompatibel?
Nicht redundant mit Obsidian-internen Mechanismen?

**3.3 — L2: Domain Extensions (Namespacing-Strategie):**

Suche: „YAML frontmatter namespace convention", „domain prefix metadata Obsidian",
„research workflow frontmatter", „novel writing Obsidian metadata", „software
development Obsidian vault".

Für den Prompt-Kontext sind folgende Domain-Extensions relevant:
- **Research-Domain** (`research_`): `research_status`, `research_phase`,
  `research_sources_count`
- **Novel-Domain** (`novel_`): `novel_act`, `novel_pov`, `novel_chapter`
- **Dev-Domain** (`dev_`): `dev_language`, `dev_module`, `dev_status`
- **Agent-Domain** (`agent_`): `agent_token_estimate`, `agent_depends_on`,
  `agent_index_of`, `agent_superseded_by`

Für jeden Namespace: Gibt es existierende Community-Standards? Konflikte mit
Obsidian-nativen Keys?

**3.4 — L3: Agent-Only Metadata (was Obsidian ignoriert aber Agenten brauchen):**

Suche: „LLM token estimate metadata", „agent navigation metadata format",
„AI-readable frontmatter", „context window metadata compression", „document
importance score metadata".

Zentrale Frage: Sollen L3-Felder im Frontmatter stehen (Obsidian zeigt sie an,
ignoriert sie aber semantisch) oder in einer Sidecar-Datei? Welche Fehler-Modi
hat jeder Ansatz?

**Restatement Checkpoint nach Step 3:**
Restiere Constraint Blocks 0–5 und die fünf Methoden verbatim.

---

### Step 4 — Das Expansion Pattern: Heuristiken für Dateigrößen-Entscheidungen

*[ReAct: Reason → Suche nach existierenden Heuristiken → Observe → Synthese wo keine existieren]*

**Ziel:** Operationale definierte Regeln entwickeln wann eine Datei expandiert werden
soll. Diese Regeln müssen von einem Agenten und einem Menschen gleichermaßen anwendbar sein.

**Zentrale Hypothese:** Die richtige Heuristik ist nicht Token-Anzahl allein, sondern
eine Kombination aus Referenz-Dichte + Update-Frequenz + Konsumenten-Divergenz.

**4.1 — Suche nach existierenden Heuristiken:**

Keywords: „Zettelkasten file size best practice", „when to split Obsidian note",
„knowledge base file granularity", „atomic notes principle Obsidian", „note too large
refactor", „LLM context chunk strategy".

Falsifikation: „atomic notes are overrated", „large notes better than split",
„splitting notes increases cognitive overhead" — suche auch Gegenargumente.

**4.2 — Die Expansion-Pattern-Spezifikation (Synthese wenn keine direkte Quelle):**

Wenn keine direkte Quelle das exakte Pattern beschreibt, synthetisiere aus den
Fundstücken und markiere `[SYNTHESE]`:

Zu spezifizieren sind:
- **Auslöser-Bedingungen** (Wann wird expandiert?): Kandidaten: Token-Schwell-
  wert, Referenz-Dichte-Schwellwert, Update-Frequenz-Schwellwert,
  Konsumenten-Divergenz-Kriterium.
- **Das Index-Node-Pattern** (Was bleibt in der Originaldatei?): Frontmatter
  vollständig, Kurzübersicht, alle externen Backlinks, `expanded: true`,
  `index_of: ./dateiname/`.
- **Die Manifest-Datei** (Was steht in der README.md des Unterordners?): Eigener
  Typ `type: manifest`, Verweis auf die Ursprungsdatei, Kurzbeschreibung jeder
  Datei im Verzeichnis mit Status und einer Satz Zusammenfassung.
- **Backlink-Invarianz** (Was darf sich nicht ändern?): Alle existierenden Links
  auf die Originaldatei müssen weiterhin korrekt auflösen.

**4.3 — Agent-lesbare Entscheidungsregeln:**

Suche: „agent should open file decision tree", „metadata-first agent navigation",
„LLM file relevance scoring frontmatter", „agent token budget file selection".

Synthese: Welche vier Frontmatter-Felder müssen immer vorhanden sein damit ein Agent
*nie* eine Datei öffnen muss um zu entscheiden ob sie relevant ist?

**Restatement Checkpoint nach Step 4:**
Restiere Constraint Blocks 0–5 und die fünf Methoden verbatim.

**Adversarial Query Expansion Pass 2 (M13):**
Führe den zweiten Query-Expansion-Pass durch (alle vier Achsen, insbesondere
Orthogonal: Bibliothekswissenschaft-Metadaten-Standards, Asset-Management-Analogien).
Logge im Query Expansion Log.

**Post-Query-Expansion-Reflektion (CONSTRAINT BLOCK 0):** Q1–Q5 nach Template.

---

### Step 5 — Populäre Plugins: Was ermöglichen sie zusätzlich?

*[ReAct: Reason → systematische Plugin-Recherche → Observe mit Schema-Impact]*

**Ziel:** Linkliste populärer Obsidian-Plugins mit direkt metadaten-relevantem Mehrwert.
Kein Implementierungsdetail — nur: Was ermöglicht das Plugin an Metadaten-Operationen?

Suche: „most popular Obsidian plugins 2024 2025", „Obsidian community plugins metadata",
„Obsidian Dataview frontmatter", „Obsidian Templater metadata", „Obsidian DB Folder",
„Obsidian Metadata Menu plugin", „Obsidian QuickAdd frontmatter".

Für jeden relevanten Plugin:
- Name + GitHub/Plugin-Directory Link
- Was es an Metadaten-Operationen ermöglicht das Obsidian-nativ nicht kann
- Ob es die Schema-Entscheidungen aus Step 3 beeinflusst (als Optional-Extension)

Constraint: Kein Plugin soll als Pflicht-Dependency erscheinen. Der Core-Schema muss
ohne alle Plugins funktionieren.

**Restatement Checkpoint nach Step 5:**
Restiere Constraint Blocks 0–5 und alle fünf Methoden verbatim.

---

### Step 6 — Ontologie-Mapping: Wie werden unterschiedliche Ontologien in Obsidian gemappt?

*[ReAct: Reason → gezielte Suche → Observe mit Contrast Classes]*

**Ziel:** Schema-Muster wie existierende Ontologien (Dublin Core, Schema.org,
SKOS, Domain-spezifische Schemas) in Obsidian-Frontmatter übersetzt werden können —
ohne Obsidian-Kompatibilität zu brechen.

**6.1 — Suche nach existierenden Mapping-Ansätzen:**

Keywords: „Dublin Core Obsidian frontmatter mapping", „Schema.org knowledge base YAML",
„SKOS Obsidian", „ontology YAML frontmatter", „semantic metadata Obsidian".

**6.2 — Synthese: Mapping-Strategie-Kandidaten:**

Zu untersuchen:
- **Direct Mapping:** Dublin Core `dc:title` → Obsidian `title`. Grenzen?
- **Prefix Mapping:** `dc_creator`, `schema_author`. Obsidian-kompatibel?
- **Flattening:** Komplexe RDF-Strukturen → Key-Value-Flat. Informationsverlust?
- **Extension-Layer:** L2 als dedizierter Ontologie-Namespace (z.B. `onto_`).

Contrast Class: Direct Mapping vs. Prefix Mapping — unter welcher Bedingung ist
welches besser? Für welchen Konsumenten?

**6.3 — Metadaten die nicht in Obsidian passen aber für Agenten wichtig sind:**

Suche: „agent metadata outside YAML", „LLM document metadata sidecar",
„semantic index document agent", „vector embedding metadata companion".

Synthese: Welche Metadaten-Typen sind strukturell nicht in YAML-Frontmatter abbildbar
(z.B. Embedding-Vektoren, Graph-Topology-Scores, Multi-Document-Relationship-Trees)?
Wie soll das Python-Script damit umgehen?

**Restatement Checkpoint nach Step 6:**
Restiere Constraint Blocks 0–5 und alle fünf Methoden verbatim.

---

### Step 7 — Surviving-Branch Triangulation (cross-pollination from Category B)

*Dieser Step importiert eine Extraktionsdisziplin aus Category B. Eine Exploration die
mit einer „wahrscheinlichsten" Schema-Architektur endet, ohne die Evidenz unter dieser
Architektur zu triangulieren, hat eine Narrative produziert — kein Fundstück.*

Wenn der Hypothesenbaum aus Step 2 eine überlebende Architektur-Hypothese produziert
hat (eine die Falsifikationsversuche überlebt), führe folgendes aus:

**7.1 — Mini-Schema für die überlebende Architektur:**
- Claim: [Ein-Satz-Statement der überlebenden Hypothese]
- Key Evidence 1: [Quelle + Fundstück]
- Key Evidence 2: [Quelle + Fundstück]
- Key Evidence 3: [Quelle + Fundstück]
- Stärkstes Gegenbeispiel: [Quelle + Fundstück]
- Confidence: [NIEDRIG / MITTEL / HOCH]
- Was-würde-mich-überzeugen-umzustellen: [konkreter zukünftiger Befund]

**7.2 — Triangulation der Top-3-Evidenz-Items:**
Jeder der drei Key Evidence Items muss zu mindestens zwei unabhängigen Quellen
(Primär + Bestätigung) zurückverfolgt werden. Wenn ein Item Einzelquelle ist:
Architektur-Hypothese als **single-source-supported** flaggen, nicht als bestätigt.

**Restatement Checkpoint nach Step 7:**
Restiere Constraint Blocks 0–5 und alle Methoden verbatim.

---

### Step 8 — Hypothesis Half-Life Audit (cross-pollination from Category C)

*Dieser Step importiert eine Lifecycle-Disziplin aus Category C. Hypothesen die früh
in der Exploration stabilisiert wurden, werden oft implizit als Grundlagen später
Äste verwendet — ohne je re-getestet zu werden.*

**8.1 — Liste foundational hypotheses auf:**
Schreibe jeden impliziten Grundsatz auf den die aktuelle Analyse aufgebaut hat
(nicht die aktive Arbeitshypothese — die impliziten, die frühere Äste aufgelöst haben).

**8.2 — Decay-Test pro Hypothese:**
Format: *„Hypothese [H] decayed wenn eine Suche nach [QUERY] das Muster [PATTERN]
zurückgibt."*

**8.3 — Führe die Decay-Tests aus:**
Wenn ein Test feuert → halt den aktuellen Ast, re-öffne die Hypothese, re-führe
Falsifikation (M01) von Grund auf durch.

**8.4 — Logge den Audit** im finalen Output unter „Hypothesis Half-Life Audit"-Sektion.

**Pre-Synthesis-Reflektion (CONSTRAINT BLOCK 0):** Q1–Q5 nach Template.

**Restatement Checkpoint nach Step 8:**
Restiere Constraint Blocks 0–5 und alle fünf Methoden verbatim.

---

## E — Expectations (RISEN)

**Was ein erfolgreicher Output enthält:**

1. **Hypothesenbaum** (Steps 1–2): Vollständig sichtbar, mit allen drei Hypothesen
   (H1/H2/H3), Falsifikationsversuchen für jeden, und expliziter Bewertung welche
   überlebt hat und warum. Straw-Man-Einträge sichtbar.

2. **Metadaten-Ebenen-Matrix** (Step 3): Tabellarisch aufgestellt.
   - L0 Felder: vollständig, mit Obsidian-Typ und Verhaltensbeschreibung
   - L1 Pflicht-Felder: mit Konsumenten-Matrix (Obsidian / Mensch / Agent) und
     Begründung per Feld
   - L2 Domain-Namespacing-Konvention: mit Beispiel-Feldern pro Domain
   - L3 Agent-Only-Felder: mit Sidecar vs. Frontmatter-Abwägung

3. **Expansion-Pattern-Spec** (Step 4): Operationale Regeln in MUSS/KANN/DARF-NICHT
   Format. Auslöser-Bedingungen quantifiziert. Index-Node-Frontmatter-Template.
   Manifest-Datei-Template.

4. **Plugin-Linkliste** (Step 5): Plugins mit GitHub/Directory-Links, kurze
   Metadaten-Relevanz-Beschreibung, optional vs. optional-advanced Einordnung.

5. **Ontologie-Mapping-Guide** (Step 6): Mapping-Strategien mit Vor/Nachteilen
   per Konsumenten-Typ. Explizite Sektion zu Metadaten die nicht in Obsidian passen
   und wie das Python-Tool damit umgeht.

6. **Triangulations-Nachweis** (Step 7): Mini-Schema mit Evidence-Items.

7. **Query Expansion Log** (M13): Alle Expansionen mit Novel-Finding-Flag.

8. **Reflection History** (CONSTRAINT BLOCK 0): Alle Reflektions-Einträge.

9. **Contradiction Log** (M07 als implizit): Alle Widersprüche zwischen Quellen
   oder zwischen Ebenen, mit Auflösung oder explizitem „unresolved".

10. **Synthesis — Spec-Grundlage:** Ein abschließender Synthese-Abschnitt der
    direkt als Eingabe für eine Metadaten-Spec verwendbar ist. Format:
    YAML-Schema-Entwurf für L0+L1 als Minimal-Pflicht, kommentiert.
    Pseudo-Code für Python-Script-Logik (lesen, parsen, entscheiden).
    Entscheidungsbaum für Expansion-Pattern als ASCII-Diagramm oder Tabelle.

**Qualitätsstandards:**
- Jeder normative Claim (Muss/Kann/Darf-nicht) hat eine Quellenbelegung oder
  ist als `[SYNTHESE]` markiert.
- Kein evaluativer Claim ohne Contrast Class.
- Obsidian-Kompatibilitätspflicht (CONSTRAINT BLOCK 4) ist für jede Schema-
  Empfehlung geprüft und explizit bestätigt oder als inkompatibel markiert.
- Agentic-Konsumenten-Dualität (CONSTRAINT BLOCK 5) ist für jede Feld-Empfehlung
  geprüft.

---

## N — Narrowing (RISEN)

**Harte Scope-Grenzen:**

- Kein Plugin-Implementierungsdetail (wie entwickelt man ein Plugin). Nur was
  ein Plugin an Metadaten ermöglicht, als Linkliste.
- Kein Obsidian vs. andere-Tools-Vergleich es sei denn er informiert direkt eine
  Schema-Entscheidung.
- Kein Marketing-Material ohne technische Substanz.
- Temporal: 2020–2026 für PKM/Obsidian; 2022–2026 für agentic/LLM-spezifisch.
- Sprache: Synthese und Fließtext auf Deutsch. Schema-Definitionen, YAML-Keys,
  Code-Fragmente auf Englisch.
- Das Python-Script wird nicht implementiert — nur seine Logik und seine
  Input-Voraussetzungen werden aus den Metadaten-Erkenntnissen abgeleitet.
- Keine Empfehlungen die CONSTRAINT BLOCK 4 (Obsidian-Kompatibilitätspflicht)
  verletzen, außer sie sind explizit als „Obsidian-inkompatibel — Agent-Only"
  gekennzeichnet.

---

## PRE-SYNTHESIS INTEGRITY CHECK

Vor dem Schreiben der finalen Synthese, führe diese Verifikation schriftlich durch.
Jeder Punkt produziert eine geschriebene Zeile; „erledigt im Gedächtnis" gilt nicht.

1. **Restiere Constraint Blocks 0–5 verbatim.** Bestätige schriftlich: *„Ich habe
   jeden Constraint Block re-gelesen und sie alle sind weiterhin aktiv."*

2. **Restiere die Critical-Thinking-Methoden-Blocks.** Bestätige schriftlich:
   *„Jede Methode ist aktiv und ich habe sie angewandt: Falsification, First-Principles
   Decomposition, Steelmanning, Contrast Classes, Adversarial Query Expansion (M13)."*

3. **Reflection-Audit (CONSTRAINT BLOCK 0).** Zähle die geschriebenen
   Reflektions-Einträge. Bestätige: *„Ich habe [K] Reflektions-Einträge geschrieben
   an folgenden Checkpoints: [auflisten]."* Wenn K unter dem Minimum: schreibe die
   fehlenden Reflektionen jetzt, bevor du fortfährst.

4. **Query-Expansion-Audit (M13).** Bestätige schriftlich: *„Methode M13 Adversarial
   Query Expansion wurde [N] Mal über die vier Achsen invoked. Das Query Expansion Log
   enthält [M] Einträge, von denen [P] novel findings produziert haben die tentative
   Schlussfolgerungen modifiziert haben."* Wenn N = 0: Research ist unvollständig —
   führe mindestens einen Pass durch bevor du fortfährst.

5. **Cross-Pollination-Audit.** Bestätige schriftlich: *„Steps die aus den zwei
   Non-Primary-Kategorien importiert wurden, wurden folgendermaßen ausgeführt:
   Step 7 (Category B — Surviving-Branch Triangulation): [Ergebnis], Step 8
   (Category C — Hypothesis Half-Life Audit): [Ergebnis]."*

6. **Constraint-Compliance-Audit.** Für jeden Constraint Block (0–5): Nenne
   ein spezifisches Beispiel wie du ihn eingehalten hast. Wenn kein Beispiel
   nennbar: Flag als **not-demonstrably-honored**.

7. **Scope-Audit.** Bestätige: *„Alle Fundstücke liegen im temporalen Scope
   2020–2026 (PKM) / 2022–2026 (agentic)."*

8. **Exclusion-Audit.** Bestätige: *„Keines der Fundstücke oder Empfehlungen
   fällt in die Ausschluss-Liste aus CONSTRAINT BLOCK 3."*

Erst wenn alle acht Punkte schriftlich vollständig sind: beginne die Synthese.

---

## SYNTHESIS — Finaler Output

Fülle folgendes Schema aus:

```
# Obsidian Frontmatter & Agentic Navigation — Research Synthesis

## Executive Summary
[2–3 Absätze: Was ist das überlebende Schema-Modell? Was war die wichtigste
unerwartete Erkenntnis? Was ist die wichtigste Lücke die keine Quelle abgedeckt hat?]

## Hypothesenbaum
[Vollständige Darstellung H1/H2/H3 mit Falsifikations-Ergebnissen, Straw-Man-Tests,
und überlebender Architektur]

## Metadaten-Ebenen-Matrix
### L0 — Obsidian Default
[Tabellarisch: Key | Obsidian-Typ | Verhalten | Reserviert?]

### L1 — Vault Core (Pflicht)
[Tabellarisch: Key | Typ | Obsidian-Konsument | Mensch-Konsument | Agent-Konsument | Quelle/SYNTHESE]

### L2 — Domain Extension Namespacing
[Konvention + Beispiele pro Domain]

### L3 — Agent-Only
[Felder + Sidecar-vs-Frontmatter-Abwägung]

## Expansion-Pattern-Spec
[MUSS/KANN/DARF-NICHT Regeln. Auslöser-Bedingungen. Index-Node-Template. Manifest-Template.]

## Plugin-Linkliste
[Name | Link | Metadaten-Mehrwert | Optional / Optional-Advanced]

## Ontologie-Mapping-Guide
[Strategien mit Vor/Nachteilen. Metadaten die nicht in Obsidian passen.]

## Synthesis — Spec-Grundlage für Python-Script
[YAML-Schema-Entwurf L0+L1. Pseudocode für Script-Logik. Expansion-Entscheidungsbaum.]

## Contradiction Log
[Alle Widersprüche zwischen Quellen oder Ebenen — resolved oder unresolved]

## Hypothesis Half-Life Audit
[Einträge aus Step 8]

## Query Expansion Log
[Alle M13-Expansionen: Achse | Query | Novel Finding | Conclusion modified]

## Reflection History
[Alle Reflektions-Einträge Q1–Q5 in Reihenfolge]

## Open Questions / Unresolved
[Was die Research nicht klären konnte]

## Sources
[Strukturierte Quellliste — Primärquellen zuerst]

## Methodology Note
[Welche Methoden wurden angewandt, welche Findings wurden durch welche Methode
produziert, alle single-source Flags]
```

---

## SELF-VERIFICATION CHECKLIST FÜR DIE AUSFÜHRENDE KI (v2.1 · 11 Punkte)

Vor der Auslieferung der Synthese, verifiziere:

- [ ] Jeder Major Step begann mit einem verbatim Restatement Checkpoint.
- [ ] CONSTRAINT BLOCK 0 (Reflection Baseline) wurde an allen fünf definierten
      Checkpoints eingehalten; Reflektions-Einträge sind geschrieben, nicht implizit.
- [ ] Methode M13 (Adversarial Query Expansion) wurde entlang aller vier Achsen
      (adjacent / opposing / abstraction / orthogonal) mindestens einmal invoked, und
      das Query Expansion Log ist ausgefüllt.
- [ ] Beide cross-pollinierten Steps (Step 7 — Category B, Step 8 — Category C)
      wurden ausgeführt und geloggt.
- [ ] Jede aktive Critical-Thinking-Methode hat mindestens eine konkrete Anwendung
      in den Findings sichtbar.
- [ ] Jeder faktische Claim wurde trianguliert (≥ 2 unabhängige Quellen) oder ist
      als single-source oder `[SYNTHESE]` geflaggt.
- [ ] Der Contradiction Log ist ausgefüllt (auch wenn „keine Widersprüche" das Ergebnis ist).
- [ ] Alle Findings liegen im Temporal Scope.
- [ ] Kein Finding fällt in den Ausschluss-Bereich aus CONSTRAINT BLOCK 3.
- [ ] Der Pre-Synthesis Integrity Check wurde schriftlich ausgeführt (alle 8 Punkte).
- [ ] Reflection History, Query Expansion Log, und Cross-Pollination Log sind im
      Output als eigene Sektionen vorhanden.

Wenn ein Punkt scheitert → repariere vor der Auslieferung. Liefere keine Synthese
mit scheiternden Checks aus.

---

**Post-Synthesis-Reflektion (CONSTRAINT BLOCK 0):** Nach der Entwurfs-Synthese,
vor der Auslieferung, führe die Post-Synthesis-Reflektion aus (Q1–Q5 nach Template).

---

*Ende des Research Prompts. Beginne die Ausführung jetzt.*