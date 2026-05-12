# Step 2: Hypothesenbaum

## H1: Flat Schema
Alle Metadaten liegen auf der Hauptebene (Level 0 der YAML-Hierarchie).
- **Vorteil:** Maximale Obsidian-Kompatibilität, native UI zeigt alles perfekt. Extrem effizient und stabil für LLM-Parsing (minimale Halluzinationen bei Schema-Erfassung).
- **Nachteil:** Keine semantische Trennung. Bei >15 Feldern wird die UI unübersichtlich. Namenskollisionen zwischen Vault-Core und Domain-Extensions sind vorprogrammiert.
- **Straw-Man-Test:** Bestanden. Der stärkste Fall ist: "Die kognitive Last für Parser und Menschen ist linear zur Verschachtelungstiefe. Ein flaches Schema zwingt zu Minimalismus, was der Kern von gutem PKM ist."
- **Falsifikation:** "Flat frontmatter breaks domain specific applications." Wenn man Forschungs- und Entwicklungs-Daten im gleichen Vault hat, überschneiden sich Keys wie `status` (Code-Status vs. Paper-Status).

## H2: Layered Schema mit Namespacing
Hierarchie über Präfixe statt Verschachtelung: `L1_status`, `L2_dev_status`, `L3_agent_score`. Es ist strukturell flach (YAML Level 0), aber lexikalisch geschichtet.
- **Vorteil:** Kombiniert die Vorteile von H1 (flach für Parser/Obsidian) mit der semantischen Sicherheit von echten Layern. Löst das Kollisionsproblem.
- **Nachteil:** Präfixe machen Keys länger, was Token kostet und die Obsidian UI-Anzeige etwas "hässlicher" macht.
- **Straw-Man-Test:** Bestanden. Der stärkste Fall ist: "Es ist die einzige Möglichkeit, Ontologien in ein System zu pressen, das technisch keine Graphen-Objekt-Strukturen im Metadaten-Block erlaubt."
- **Falsifikation:** Die Lesbarkeit für Menschen leidet unter Präfixen.

## H3: Sidecar-Model
Die Markdown-Datei behält nur `tags` und `aliases` für Obsidian. Alles andere wandert in `[dateiname].meta.yml`.
- **Vorteil:** Die Markdown-Datei bleibt makellos. Agenten können die `.meta.yml` extrem schnell auslesen, ohne den Markdown-Inhalt auch nur anzufassen.
- **Nachteil:** Bricht die Obsidian-Erfahrung komplett. Das Properties-UI zeigt die Metadaten nicht mehr an. Zwingt den menschlichen Autor, zwei Dateien synchron zu halten.
- **Straw-Man-Test:** Bestanden. Der stärkste Fall ist: "Trennung von Belangen (Separation of Concerns). Text ist für Menschen, Meta ist für Maschinen."
- **Falsifikation:** Obsidian-Nutzer hassen Sidecar-Dateien, weil sie Graphen-Plugins (Dataview) brechen, da diese das interne Frontmatter erwarten.

## Surviving Architecture
**H2 (Layered Schema mit Namespacing)** überlebt als einzige Architektur, die alle drei Konsumenten (UI, Mensch, Agent) tolerieren können, ohne Kernfunktionalität einzubüßen. H1 scheitert an Skalierung/Semantik, H3 bricht Constraint 5 (Mensch/UI Konsument).
