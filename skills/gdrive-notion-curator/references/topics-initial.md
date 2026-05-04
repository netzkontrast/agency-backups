# Topics-DB Initial-Befüllung

> Beim `setup`: Topics-DB wird mit den 11 Topics aus `assets/topics-config.yaml` befüllt. Eine Page pro Topic.

## Ablauf

1. `assets/topics-config.yaml` lesen
2. Pro Topic eine Page in Topics-DB anlegen via `notion-create-pages`
3. Page-Inhalt: Topic-Beschreibungs-Markdown (siehe Templates unten)

## Notion-Create-Pages Aufruf

```
notion-create-pages
  parent: { data_source_id: <topics_ds_id> }
  pages: [
    { properties: {...}, content: "..." },
    { properties: {...}, content: "..." },
    ...
  ]
```

Pro Page-Objekt:

```json
{
  "properties": {
    "Topic Name":  "Kohärenz Protokoll",
    "Slug":        "kohaerenz-protokoll",
    "Sensitive":   "__NO__",
    "Keywords":    "kohaerenz, kohärenz protokoll, aegis, kael, juna, dramatica, hard-sf",
    "File Count":  0,
    "Description": "Hard-SF/Philosophical Horror Novel-Projekt"
  },
  "content": "<Markdown-Beschreibung — siehe Template>"
}
```

## Page-Templates pro Topic

### kohaerenz-protokoll (Sensitive: false)

```markdown
# Kohärenz Protokoll

Hard-SF/Philosophical Horror Novel-Projekt.

**Hauptcharaktere:** Kael (DIS-modelliert), AEGIS (KI-Entität), Juna, fünf Guardians.
**Struktur:** 39 Kapitel, drei Akte.
**Themen:** Kohärenz als state variable, fragmentation, AEGIS-Bewusstsein.

Children dieser Page = Sub-Pages pro indexiertem File mit Auszug + Drive-Links.
```

### dramatica-theory (Sensitive: false)

```markdown
# Dramatica Theory

Story-Strukturanalyse via Dramatica-Methodologie.

**Themen:** Storyform, Quad-Modell, Character-Throughlines, Thematic-Argument.

Children dieser Page = Sub-Pages pro indexiertem File mit Auszug + Drive-Links.
```

### agency-system-design (Sensitive: false)

```markdown
# Agency System Design

Darkwave/industrial Triptych Konzeptalbum-Projekt.

**Alben:** A1 "Together We Confide" (released 2024), A2 "Moment der Klarheit", A3 "Gegenüber".
**Themen:** corporate mimicry, IFS-informed polyphony, cybernetische Metaphern, 120 BPM industrial-darkwave.

Children dieser Page = Sub-Pages pro indexiertem File mit Auszug + Drive-Links.
```

### agentic-architecture (Sensitive: false)

```markdown
# Agentic Architecture

Multi-Agent-Orchestrations- und JANUS-System.

**Themen:** Planner-Executor, dual-cognition, System-1/System-2-Logic, Skills-Hierarchie.

Children dieser Page = Sub-Pages pro indexiertem File mit Auszug + Drive-Links.
```

### llm-wiki-agent (Sensitive: false)

```markdown
# LLM Wiki Agent

LLM-assistierter Novel-Writing Pipeline mit strukturierter Wiki-Wissens-Schicht.

**Themen:** wiki-Layer (knowledge/narrative/reader_state/meta), self-adaptive ingest, canon-diff.

Children dieser Page = Sub-Pages pro indexiertem File mit Auszug + Drive-Links.
```

### research-prompt-optimizer (Sensitive: false)

```markdown
# Research Prompt Optimizer

Skill für Deep-Research-Prompt-Generierung (Gemini, Perplexity, Claude Research).

**Themen:** intent capture, planning gates, audit, prompt versioning.

Children dieser Page = Sub-Pages pro indexiertem File mit Auszug + Drive-Links.
```

### music-production (Sensitive: false)

```markdown
# Music Production

Suno-basierte Tracks und Skill-Hierarchie für Songtext-Generierung.

**Themen:** Suno-Prompts, Lyric-Writing, Sound Engineering, Track-DNA, vocal tags.

Children dieser Page = Sub-Pages pro indexiertem File mit Auszug + Drive-Links.
```

### trauma-dis-material (Sensitive: TRUE — Sub-Pages enthalten KEINEN Inhalt)

```markdown
# trauma-dis-material

⚠️ **Sensitive Topic.** Files werden Title-only klassifiziert. Inhalte sind nicht in Notion indexiert.

Sub-Pages dieser Page enthalten nur Metadaten und Drive-Links — keinen inhaltlichen Auszug.

Direkter Zugriff erfolgt über die Drive-Links in den Sub-Pages.

Behandlung: keine Auto-Konsolidierung, keine Vorschläge zur Umstrukturierung, kein Content-Read.
```

### dkt-physik (Sensitive: false)

```markdown
# DKT Physik

DKT (Dynamische Kohärenz-Theorie) — physikalische und philosophische Modellierung.

**Themen:** Thermodynamische Epistemologie, Kohärenz als state variable analog zu Entropie.

Children dieser Page = Sub-Pages pro indexiertem File mit Auszug + Drive-Links.
```

### visual-design (Sensitive: false)

```markdown
# Visual Design

ASDLS (Agency System Design Language Spec) und visuelle Asset-Generierung.

**Themen:** Atelier-System, Cluster-Architektur, Cover-Artworks, Illustrations-Spec.

Children dieser Page = Sub-Pages pro indexiertem File mit Auszug + Drive-Links.
```

### misc (Sensitive: false)

```markdown
# Misc

Catch-all für Files die explizit "misc" zugewiesen wurden (manuell oder via Inbox-Reject).

Children dieser Page = Sub-Pages pro indexiertem File mit Auszug + Drive-Links.
```

## Idempotenz

Vor dem Anlegen jeder Page: prüfen ob Topic-Page mit gleichem Slug schon existiert (Notion-Search by Slug-Property). Wenn ja: skip, nicht überschreiben.

## Update-Path bei Topic-Erweiterung

Wenn `review-inbox` einen neuen Topic approved:
1. Neue Page in Topics-DB anlegen mit User-eingegebenen Properties
2. Files-DB ALTER COLUMN auf `Topic` und `Suggested Topics` mit erweiterter Optionen-Liste
3. Hinweis an User: `assets/topics-config.yaml` lokal updaten falls gewünscht (für Reproducibility)

## Stopword-Liste für Suggested-Slug-Generierung

Wenn ein File keinen Topic matcht und ein Inbox-Vorschlag generiert wird, soll der Suggested Slug aus dem Title gebildet werden — aber Stopwords ignoriert.

```python
STOPWORDS_DE = {
    "der","die","das","ein","eine","einen","und","oder","aber","wenn","dann","als","auch","noch","nur","schon","doch","mit","von","zu","auf","im","in","an","bei","aus","für","über","unter","durch",
    "ist","sind","war","waren","wird","werden","wurde","wurden","hat","haben","hatte","hatten","sein","kann","könnte","sollte","müsste","würde",
    "kapitel","notes","draft","entwurf","version","kopie","copy","new","neu","alt","old","final","temp","backup",
    "doc","document","datei","file","page","seite",
    "zum","zur","des","den","dem","ich","du","er","sie","es","wir","ihr","mich","dich","sich"
}

STOPWORDS_EN = {
    "the","a","an","and","or","but","if","then","as","also","only","just","yet","still",
    "is","are","was","were","will","would","could","should","might","been","being","have","has","had",
    "of","in","on","at","by","for","from","to","with","about",
    "chapter","notes","draft","version","copy","new","old","final","temp","backup",
    "doc","document","file","page",
    "i","you","he","she","it","we","they","me","him","her","us","them"
}
```

Suggested-Slug-Algorithm:
1. Title slugify
2. Tokens splitten
3. Stopwords entfernen (DE+EN)
4. Erste 2-3 Tokens nehmen
5. Mit `-` joinen
