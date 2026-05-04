# Notion-Schema — 3 Datenbanken

> Drei DBs unter einer User-Page (z.B. "Claude Drive Workspace"). Alle SQL DDL.
> RELATION zwischen Files-DB und Topics-DB als zwei-stufige Anlage (siehe unten).

## Datenbank 1 — `Claude Drive Files`

Pro Drive-File EIN Page-Entry. Original- und Curated-IDs getrennt sichtbar.

```sql
CREATE TABLE (
  -- Identität (5)
  "Filename"               TITLE       COMMENT 'Aktueller Drive-Filename des Originals.',
  "Original Drive ID"      RICH_TEXT   COMMENT 'Drive-fileId des Source-Originals. Stabiler Identifier.',
  "Curated Drive ID"       RICH_TEXT   COMMENT 'Drive-fileId der Kopie in /Claude/curated/. Leer wenn noch nicht kopiert oder Duplikat.',
  "Original Drive Link"    URL         COMMENT 'webViewLink zum Original.',
  "Curated Drive Link"     URL         COMMENT 'webViewLink zur Kopie in /curated/.',

  -- Drive-Metadaten (4)
  "MIME"                   SELECT('Doc':blue, 'Sheet':green, 'Slide':orange, 'PDF':red, 'Image':purple, 'Audio':pink, 'Video':yellow, 'Folder':gray, 'Other':default) COMMENT 'Drive mimeType-Kategorie.',
  "Created"                DATE        COMMENT 'Drive createdTime des Originals (RFC-3339).',
  "Modified"               DATE        COMMENT 'Drive modifiedTime des Originals.',
  "MD5 Checksum"           RICH_TEXT   COMMENT 'Nur befüllt für Binary-Files (PDF, Image, etc). Google Docs haben kein md5.',

  -- Klassifikation (5)
  "Language"               SELECT('de':blue, 'en':green, 'mixed':yellow, 'unknown':gray) COMMENT 'Erkannte Sprache.',
  "Topic"                  SELECT('kohaerenz-protokoll':blue, 'dramatica-theory':purple, 'agency-system-design':pink, 'agentic-architecture':orange, 'llm-wiki-agent':yellow, 'research-prompt-optimizer':green, 'music-production':red, 'trauma-dis-material':brown, 'dkt-physik':default, 'visual-design':gray, 'misc':default) COMMENT 'Primary Topic-Slug. Sync mit Topics-DB.',
  "Suggested Topics"       MULTI_SELECT('kohaerenz-protokoll':blue, 'dramatica-theory':purple, 'agency-system-design':pink, 'agentic-architecture':orange, 'llm-wiki-agent':yellow, 'research-prompt-optimizer':green, 'music-production':red, 'trauma-dis-material':brown, 'dkt-physik':default, 'visual-design':gray, 'misc':default) COMMENT 'Bei Multi-Match: alle Kandidaten.',
  "Confidence"             SELECT('high':green, 'medium':yellow, 'low':orange, 'none':gray, 'manual':blue) COMMENT 'Klassifikations-Sicherheit.',
  "Match Reason"           RICH_TEXT   COMMENT 'Audit-Trail: matched keyword(s), score, etc.',

  -- Workflow (4)
  "Sort Status"            STATUS('pending':default, 'copied':blue, 'indexed':green, 'in-inbox':yellow, 'duplicate':gray, 'archived':gray, 'pinned':purple) COMMENT 'Lifecycle-Phase.',
  "Run ID"                 RICH_TEXT   COMMENT 'Welcher Skill-Run hat dieses File verarbeitet (Format: run-YYYYMMDD-HHMMSS).',
  "Sub-Page Link"          URL         COMMENT 'Direktlink zur Sub-Page in Topics-DB falls indexed.',
  "Inbox Page Link"        URL         COMMENT 'Direktlink zum Inbox-Eintrag falls in-inbox.',

  -- User-Touch (3)
  "Sensitive"              CHECKBOX    COMMENT 'trauma-relevant — kein Content-Read, keine Sub-Page mit Inhalt.',
  "Pinned"                 CHECKBOX    COMMENT 'Skill rührt nicht mehr an, auch nicht bei Repair.',
  "Notes"                  RICH_TEXT   COMMENT 'Frei-Annotationen User. Wird von Claude NICHT überschrieben.'
)
```

**21 Properties.** Identität (5) + Drive-Meta (4) + Klassifikation (5) + Workflow (4) + User (3).

## Datenbank 2 — `Claude Topics`

Eine Page pro Topic. Children dieser Page = Sub-Pages mit File-Inhalten (Auszug).

```sql
CREATE TABLE (
  "Topic Name"      TITLE       COMMENT 'Display-Name (Mensch-lesbar).',
  "Slug"            RICH_TEXT   COMMENT 'Maschinen-Slug. Sync mit Files-DB Topic-Select-Option.',
  "Sensitive"       CHECKBOX    COMMENT 'Wenn true: keine Content-Sub-Pages, nur Metadaten.',
  "Keywords"        RICH_TEXT   COMMENT 'Komma-separierte Match-Keywords (lowercased, normalisiert).',
  "File Count"      NUMBER      COMMENT 'Cached Anzahl der Files in diesem Topic. Wird beim Sweep aktualisiert.',
  "Description"     RICH_TEXT   COMMENT 'Optional: Topic-Beschreibung für Mensch.',
  "Files"           RELATION('FILES_DS_ID', DUAL 'Topic') COMMENT 'Reverse-Relation: alle Files mit diesem Topic.'
)
```

**Hinweis zur RELATION:** `RELATION('FILES_DS_ID', ...)` braucht die echte data_source_id der Files-DB. Diese kennt man erst NACH Anlage der Files-DB. Daher zwei-stufiges Setup:

1. Erst Files-DB anlegen → `data_source_id_files` extrahieren
2. Topics-DB mit `RELATION('<data_source_id_files>', DUAL 'Topic')` anlegen
3. ALTER COLUMN auf Files-DB: `Topic`-SELECT bleibt wie ist, aber zusätzliche Property "Topic Relation" könnte als RELATION zu Topics-DB hinzukommen — **aktuell NICHT**, weil Topic als SELECT-Slug in Files-DB ausreicht und wir bidirektionale Sync vermeiden.

**Kompromiss-Entscheidung:** Topic in Files-DB bleibt SELECT (Slug), Files in Topics-DB bleibt RELATION-leer. Cross-Lookup erfolgt via Notion-Search by Topic-Slug. Vorteil: keine RELATION-Sync-Komplexität. Roadmap v0.6 plant bidirektionale RELATION.

**Vereinfachte Topics-DB-DDL:**

```sql
CREATE TABLE (
  "Topic Name"      TITLE,
  "Slug"            RICH_TEXT,
  "Sensitive"       CHECKBOX,
  "Keywords"        RICH_TEXT,
  "File Count"      NUMBER,
  "Description"     RICH_TEXT
)
```

**6 Properties.** Files werden NICHT als RELATION gehalten — stattdessen:
- File-Sub-Pages werden als **Page-Children** unter der Topic-Page angelegt
- Files-DB hat `Topic`-Slug als SELECT für schnelle Filter

Damit sehen User in Notion: Topic-Page öffnen → Children-Liste = alle indexierten Files mit Auszug.

## Datenbank 3 — `Claude Topic Inbox`

Eine Page pro Vorschlag für neuen Topic. Awaits askuser-Approve.

```sql
CREATE TABLE (
  "Vorschlag"           TITLE       COMMENT 'Display-Name des Vorschlags.',
  "Suggested Slug"      RICH_TEXT   COMMENT 'Vorgeschlagener Topic-Slug (lowercase-normalisiert).',
  "Sample File IDs"     RICH_TEXT   COMMENT 'Komma-separierte Drive-IDs der Sample-Files die diesen Vorschlag triggern.',
  "Sample File Count"   NUMBER      COMMENT 'Wie viele Files diesen Vorschlag stützen.',
  "Suggested Keywords"  RICH_TEXT   COMMENT 'Top-Token-Häufigkeiten aus Sample-Files.',
  "Status"              STATUS('pending-review':yellow, 'approved':green, 'rejected':red, 'merged':gray) COMMENT 'Workflow-Status.',
  "Decision Notes"      RICH_TEXT   COMMENT 'User-Annotationen zur Entscheidung.',
  "Merged Into"         RICH_TEXT   COMMENT 'Wenn Status=merged: Slug des Existing-Topics.',
  "Created"             CREATED_TIME COMMENT 'Wann Vorschlag entstand.'
)
```

**9 Properties.**

## Setup-Sequenz

```
1. notion-create-database (Files-DB) — siehe DDL oben
   → extract data_source_id_files aus <data-source url="collection://..."> Tag

2. notion-create-database (Topics-DB) — vereinfachte DDL ohne RELATION
   → extract data_source_id_topics

3. notion-create-database (Inbox-DB) — DDL oben
   → extract data_source_id_inbox

4. notion-create-view 4x für Files-DB:
   - "📥 Inbox"      table  FILTER "Sort Status" = "pending"; SORT BY "Created" DESC
   - "📂 By Topic"   board  GROUP BY "Topic"
   - "❓ Uncategorized" table FILTER "Sort Status" = "in-inbox"; SORT BY "Modified" DESC
   - "🧠 Indexed"    table  FILTER "Sort Status" = "indexed"; SORT BY "Modified" DESC

5. notion-create-view 1x für Topics-DB:
   - "📚 All Topics" table  SORT BY "File Count" DESC

6. notion-create-view 2x für Inbox-DB:
   - "⚠️ Pending Review" table FILTER "Status" = "pending-review"; SORT BY "Created" DESC
   - "📜 History" table FILTER "Status" != "pending-review"; SORT BY "Created" DESC

7. Speichere alle 3 data_source_ids in einer kleinen lokalen Datei
   (z.B. /tmp/gdrive-curator-state.json) für nachfolgende Runs:
   {
     "files_ds_id":  "...",
     "topics_ds_id": "...",
     "inbox_ds_id":  "..."
   }

8. Topics-DB initial befüllen aus assets/topics-config.yaml:
   notion-create-pages mit allen 11 Topics (siehe references/topics-initial.md)
```

## Property-Update-Format-Cheatsheet

| Type | Update-Format |
|---|---|
| TITLE, RICH_TEXT, URL | normaler String |
| SELECT | exakt option-name als String |
| MULTI_SELECT | comma-separated String |
| DATE | `"date:Created:start": "2026-05-02T10:00:00Z"`, `"date:Created:is_datetime": 1` |
| CHECKBOX | `"__YES__"` oder `"__NO__"` |
| STATUS | exakt option-name |
| NUMBER | JavaScript number |

## Schema-Migration über Zeit

Wenn topics-config.yaml neue Topics bekommt:
- ALTER COLUMN "Topic" SET SELECT(...) auf Files-DB mit kompletter neuer Liste
- ALTER COLUMN "Suggested Topics" SET MULTI_SELECT(...) gleich
- Neue Page in Topics-DB für jeden neuen Slug

**Achtung:** ALTER COLUMN überschreibt Optionen-Liste komplett. Immer alle Optionen mitgeben (alte + neue).
