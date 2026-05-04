# Workflow — 4 Operations

> v0.4.0 ersetzt die alten Phasen 0/A/B/C/E durch vier explizite Operations: **setup**, **routine**, **review-inbox**, **repair**. Setup ist die Kombi aus altem Phase-0 + Phase-A. Routine ersetzt das alte Phase-B.

## Inhalts-Verzeichnis

- [setup](#setup) — One-time, full Source-Listing paginated, alle Files verarbeiten
- [routine](#routine) — Incremental, Filter `> newest_in_last_run`, cap 50 ASC, Status-Report
- [review-inbox](#review-inbox) — askuser-driven, on-demand, eigene Operation
- [repair](#repair) — Drift-Check zwischen Drive `/curated/` und Notion, on-demand

---

## Verarbeitungs-Loop (gemeinsam für setup + routine)

Beide Operations nutzen denselben Pro-File-Loop. Unterscheidung nur in:
- **Source-Filter** (kein Filter / `createdTime > newest_in_last_run`)
- **File-Cap** (unbegrenzt / 50)
- **Sortierung** (irrelevant / ASC)

### Schritte pro File

**A. Skip-Checks (in dieser Reihenfolge):**

| Check | Aktion bei Hit |
|---|---|
| `Original Drive ID` schon in `notion_state.original_drive_ids` | **Skip komplett** — File war schon dran |
| Title ist `_pending.yml`, `index.yml`, oder beginnt mit `.` | **Skip** — System-File |
| MIME = Folder | **Skip** — wir traversieren nicht |
| Duplikat-Regel triggert (siehe `duplicate-handling.md`) | Files-DB-Entry mit `Status=duplicate`, kein Copy, **continue** |

**B. Sensitive-Check vorab (Title-only):**

Lade `assets/topics-config.yaml`, finde Topics mit `sensitive: true`, prüfe ob Title irgendein sensitive-Keyword matcht. Wenn ja: Sensitive-Flag merken, **kein Content-Read in Schritt G**. Siehe `sensitive-handling.md`.

**C. Slug-Filename generieren:**

```bash
python3 scripts/slug.py "<original-title>"
```

Output: slug-filename mit Extension. Beispiel: `Kohärenz Protokoll - Notes.md` → `kohaerenz-protokoll-notes.md`

**D. Copy nach /curated/:**

```
Google Drive:copy_file
  fileId:    <original-id>
  parentId:  <curated_folder_id>
  title:     <slug-filename>
```

→ `Curated Drive ID` aus Response.

**E. Files-DB-Entry anlegen (initial mit Status=copied):**

```
Notion:notion-create-pages
  parent: { data_source_id: <files_ds_id> }
  pages: [{
    properties: {
      "Filename":             "<original-title>",
      "Original Drive ID":    "<original-id>",
      "Curated Drive ID":     "<copied-id>",
      "Original Drive Link":  "<webViewLink>",
      "Curated Drive Link":   "<copy-webViewLink>",
      "MIME":                 "Doc",
      "date:Created:start":   "<original-createdTime>",
      "date:Created:is_datetime": 1,
      "date:Modified:start":  "<original-modifiedTime>",
      "date:Modified:is_datetime": 1,
      "MD5 Checksum":         "<md5 oder leer>",
      "Sort Status":          "copied",
      "Run ID":               "<run-id>",
      "Sensitive":            "<__YES__ wenn sensitive sonst __NO__>",
      "Pinned":               "__NO__"
    }
  }]
```

→ `Files-Page-ID` aus Response merken.

**F. Bei sensitive: STOP HIER.** Topic-Klassifikation rein nach Title via Sensitive-Topic-Match. Sub-Page wird mit nur Metadaten angelegt (kein Inhalt). Files-DB-Entry kriegt:
- `Topic` = sensitive-Topic-Slug
- `Confidence` = high
- `Sort Status` = indexed

Siehe `sensitive-handling.md` für Sub-Page-Template.

**G. Bei non-sensitive: Content lesen** (cap auf erste ~3000 Wörter):

```
Google Drive:download_file_content
  fileId: <original-id>
  exportMimeType: "text/plain"  # für Google Docs
```

Bei sehr großen Files (>50k chars): nur erste 50k.

**H. Sprache erkennen:**

```bash
python3 scripts/language_detect.py "<content-first-2000-chars>"
```

Output: `de`, `en`, `mixed`, oder `unknown`.

**I. Klassifikation:**

```bash
python3 scripts/classify.py \
  --title "<title>" \
  --content "<content-first-3000-chars>" \
  --topics-yaml assets/topics-config.yaml
```

Output: JSON `{topic: slug-or-null, confidence: high|medium|low|none, suggested: [slugs], reason: text}`.

**J. Routing nach Confidence:**

Bei `high` oder `medium`:
1. **Sub-Page in Topics-DB anlegen** als Child der Topic-Page (Topic-Page-ID via Notion-Search nach Slug, dann `notion-create-pages` mit `parent: {page_id: <topic-page-id>}`)
2. Inhalt: Auszug ~500 Wörter + Metadaten + Drive-Links (Template unten)
3. **Files-DB updaten**: `Topic`, `Suggested Topics`, `Confidence`, `Match Reason`, `Language`, `Sort Status=indexed`, `Sub-Page Link`

Bei `low` oder `none`:
1. **Inbox-DB-Entry anlegen** ODER bestehenden ergänzen wenn Suggested Slug schon existiert
2. **Files-DB updaten**: `Suggested Topics`, `Confidence`, `Match Reason`, `Language`, `Sort Status=in-inbox`, `Inbox Page Link`

### Sub-Page-Template (in Topics-DB)

```
# <Filename>

**Original:** [<title>](<original-drive-link>)
**Curated:** [<slug-filename>](<curated-drive-link>)
**Sprache:** <de/en/mixed>
**Erstellt:** <created-date>
**Run:** <run-id>

## Auszug

<erste 500-1000 Wörter des Contents>

[...gekürzt — vollständiger Inhalt im Drive]

---

**Topic:** <topic-slug>
**Match Reason:** <reason>
**Confidence:** <high/medium>
```

### Sub-Page-Template (sensitive)

```
# <Filename>

**Original:** [<title>](<original-drive-link>)
**Curated:** [<slug-filename>](<curated-drive-link>)
**Sprache:** unbekannt (sensitive — kein Content-Read)
**Erstellt:** <created-date>

⚠️ **Sensitive Topic — Inhalt wird nicht von Claude indexiert.**
Zugriff nur via Drive-Links oben.

---

**Topic:** <sensitive-topic-slug>
**Match:** Title-only
```

---

## setup

**Wann:** Erstes Skill-Run im Workspace, oder Wiederherstellung nach Container-Restart wenn `/tmp/gdrive-curator-state.json` weg ist.

**Idempotenz:** setup re-triggern ist sicher — Skip-Regel via `Original Drive ID` filtert schon-verarbeitete Files. Bei Crash mid-run also einfach nochmal `setup` aufrufen.

### Voraussetzungen

- User hat eine Notion-Page als Workspace-Parent (z.B. "Claude Drive Workspace")
- User kennt die ID der Source-Folder in Drive (z.B. "Inbox" oder "Ablage")
- User kennt die ID des `/Claude/`-Roots in Drive

### Sequenz

#### Schritt 1: Setup-IDs erfragen / lesen

Wenn `/tmp/gdrive-curator-state.json` existiert: Setup-IDs daraus lesen, Schritt 2-5 überspringen.

Sonst askuser:
- Notion-Parent-Page-ID
- Drive-Source-Folder-ID
- Drive-Claude-Root-ID

#### Schritt 2: `/Claude/curated/` Folder anlegen (idempotent)

Erst prüfen:
```
Google Drive:search_files
  query: "parentId = '<claude_root>' and title='curated' and mimeType='application/vnd.google-apps.folder' and trashed=false"
```

Wenn nicht vorhanden:
```
Google Drive:create_file
  title: "curated"
  parentId: <claude_root>
  contentMimeType: "application/vnd.google-apps.folder"
```

Curated-Folder-ID merken.

#### Schritt 3: Notion-DBs anlegen

Wenn noch nicht da: 3 DBs anlegen mit DDL aus `assets/ddl-statements.sql`. Schema-Detail in `references/notion-schema.md`.

- `Claude Drive Files` → `data_source_id_files`
- `Claude Topics` → `data_source_id_topics`
- `Claude Topic Inbox` → `data_source_id_inbox`

Wenn vorhanden (idempotenter Setup-Re-Run): existierende `data_source_id`s aus Notion-Search holen.

#### Schritt 4: Views anlegen (4 + 1 + 2 — siehe notion-schema.md)

Idempotent: existierende Views überspringen.

#### Schritt 5: Topics-DB initial befüllen aus `assets/topics-config.yaml`

11 Pages anlegen, eine pro Topic. Pro Page: Topic Name, Slug, Sensitive, Keywords, File Count=0. Siehe `references/topics-initial.md`.

Idempotent: existierende Topic-Slugs überspringen.

#### Schritt 6: Setup-State speichern

`/tmp/gdrive-curator-state.json`:
```json
{
  "skill_version": "0.4.0",
  "claude_root_folder_id": "...",
  "curated_folder_id": "...",
  "source_folder_ids": ["..."],
  "files_ds_id": "...",
  "topics_ds_id": "...",
  "inbox_ds_id": "...",
  "notion_workspace_page_id": "..."
}
```

#### Schritt 7: State aus Notion holen

Siehe `resume-logic.md`. Bei erstem Setup leer; bei Re-Trigger nicht-leer.

#### Schritt 8: Komplett-Listing Source-Folder paginated

```
Google Drive:search_files
  query: "parentId = '<source>' and trashed=false"
  pageSize: 100
```

Bei `nextPageToken` paginieren bis leer. Alle Resultate in einer Liste sammeln.

**Sortierung:** Nicht nötig für setup (wir verarbeiten alle).

#### Schritt 9: Run-ID generieren

`run-YYYYMMDD-HHMMSS-setup` (Zeitstempel + Mode-Suffix für klare Unterscheidung in Notion).

#### Schritt 10: Pro File Verarbeitungs-Loop

Für jedes File aus dem Listing: Schritte A-J aus dem [Verarbeitungs-Loop](#verarbeitungs-loop-gemeinsam-für-setup--routine).

#### Schritt 11: Run-Übersicht an User

Markdown-Tabelle: copied / indexed / in-inbox / duplicate / skipped (already-in-db). Hinweis wenn Inbox-Einträge vorhanden: "review-inbox empfohlen".

### Backlog-Strategie bei riesigen Source-Foldern

Bei >500 Files im Source: Token-Cost wird beachtlich (siehe Budget in SKILL.md). Strategien:
1. **Naiv:** setup einmal triggern, dann auf Token-Limit warten, Crash, setup nochmal triggern. Skip-Regel filtert Verarbeitete. Idempotent.
2. **Geplant:** User askuser-Pause-Punkte einbauen — Skill verarbeitet 100 Files, askt "weiter?", verarbeitet 100 weitere. (Nicht implementiert in v0.4.0; bei Bedarf hinzufügen.)
3. **Alternative:** Source-Folder vorab manuell in Sub-Folder splitten (≤200 Files), Setup pro Sub-Folder.

---

## routine

**Wann:** Routine-Trigger (z.B. täglich). Findet neue Files seit letztem completed Run.

**Cap:** 50 Files pro Run, ASC by createdTime (ältester der neuen zuerst — FIFO bei Backlog, kein Verlust).

### Sequenz

#### Schritt 1: State aus Notion holen

Siehe `resume-logic.md`. Result:
- `last_run_id`
- `newest_in_last_run` (createdTime des jüngsten Files im letzten Run)
- `original_drive_ids`, `titles_in_db`, `md5_checksums` (für Duplicate-Check)

Wenn `last_run_id == None`: Skill ist im "leeren" State — askuser ob `setup` gemeint war.

#### Schritt 2: Drive-Listing flat mit Filter

```
Google Drive:search_files
  query: "parentId = '<source>' and trashed=false and createdTime > '<newest_in_last_run>'"
  pageSize: 100
```

Bei `nextPageToken`: paginieren bis komplett ODER bis 200 Files (Safety-Limit, sollte nie erreicht werden bei daily-Trigger).

#### Schritt 3: Client-side Sort ASC by createdTime

Drive-MCP hat keinen `orderBy` für `search_files`. Daher: alle Resultate gesammelt, dann lokal sortieren:

```python
results.sort(key=lambda f: f.createdTime)  # ASC, oldest-of-new first
```

#### Schritt 4: Cap auf 50

`to_process = results[:50]`. Den Rest merken: `overflow = len(results) - 50`.

#### Schritt 5: Run-ID generieren

`run-YYYYMMDD-HHMMSS-routine`.

#### Schritt 6: Pro File Verarbeitungs-Loop

Schritte A-J aus dem Verarbeitungs-Loop oben.

#### Schritt 7: Status-Report

```markdown
## Routine-Run <run-id>

- **Verarbeitet:** N Files (cap 50)
  - Indexed: N
  - In-Inbox: N
  - Duplicate: N
- **Skipped (already in DB):** N

[Wenn overflow > 0:]
⚠️ **Backlog:** Es sind noch X Files mit createdTime > `<newest_in_last_run>` übrig, die nicht ins 50er-Cap gepasst haben. Bitte routine nochmal triggern.

[Sonst:]
✅ Alle neuen Files seit `<last_run_id>` sind durch.

[Wenn Inbox-Einträge vorhanden:]
📥 N neue Inbox-Einträge — review-inbox empfohlen.
```

### Edge Cases

**Kein newest_in_last_run** (allererste routine ohne vorherigen setup): Skill askuser ob setup gemeint war. Sollte Skill nicht heimlich auto-konvertieren.

**newest_in_last_run älter als 7 Tage:** Skill warnt User: "Letzter Run war vor X Tagen, möglicher Backlog. Ggf mehrfach triggern oder repair zur Drift-Sicherung."

**0 Files gefunden:** Status-Report sagt "Keine neuen Files seit `<last_run_id>`. Nichts zu tun." Kein Run-ID-Eintrag in Notion (sonst füllt sich die DB mit leeren Runs).

---

## review-inbox

**Wann:** On-demand. Wird NICHT automatisch nach routine getriggert (Operation 4 ist orthogonal).

### Sequenz

1. **Notion-Query Inbox-DB**: alle Pages mit `Status=pending-review`, sortiert nach `Sample File Count DESC` (häufigste zuerst — wahrscheinlich Topic-Kandidaten)
2. Pro Eintrag mit `ask_user_input_v0`:
   - Anzeige: Vorschlag-Title, Suggested Slug, Sample-File-Count, Top-Keywords
   - Optionen: `Approve neuer Topic`, `Merge in <existing-slug>`, `Reject`, `Skip`

3. **Bei Approve:**
   - Topics-DB neue Page anlegen (Slug, Keywords, Sensitive=false)
   - Files-DB Topic-Property: SELECT-Optionen erweitern + Suggested-Topics-MULTI_SELECT erweitern
   - Re-Klassifizierung der Sample-Files: Topic gesetzt, Sub-Pages anlegen, Status=indexed
   - Inbox-Eintrag: Status=approved
   - User-Hinweis: "Bitte `assets/topics-config.yaml` updaten" (User macht manuell)

4. **Bei Merge:**
   - Sample-Files: Topic auf Existing-Slug setzen, Sub-Pages anlegen, Status=indexed
   - Inbox-Eintrag: Status=merged, Merged Into=<slug>

5. **Bei Reject:**
   - Sample-Files: Status bleibt in-inbox ODER User entscheidet "set to misc"
   - Inbox-Eintrag: Status=rejected

6. **Bei Skip:** Nichts ändern, später wieder vorschlagen.

### Empfehlung

review-inbox sollte ungefähr alle 2-4 routines getriggert werden, sonst wächst die Inbox unnötig. Skill kann am Ende einer routine erinnern: "📥 N Einträge in der Inbox — review-inbox empfohlen."

---

## repair

Detail in `references/repair-consistency.md`. Kurzform:

1. Drive-Listing `/curated/` flat, paginated bis komplett → `drive_curated_set`
2. Notion-Query Files-DB mit `Curated Drive ID` gesetzt, paginated → `notion_curated_set`
3. Diff-Klassifikation:
   - **Drift A — Orphan in Drive:** in `/curated/` aber nicht in Notion
   - **Drift B — Ghost in Notion:** in Notion aber nicht in Drive
   - **Drift C — Source Original gone** (optional, teurer): Original-Drive-ID 404
   - **Drift D — Status-Inkonsistenz:** Sort Status=indexed aber Sub-Page Link leer
4. Pro Diff: askuser mit Repair-Optionen, kein automatisches Reparieren
5. Repair-Aktionen werden als Notion-Updates angewendet, NIE als Drive-Mutationen (Tool-Limitation).

---

## Token-Budget pro Operation

| Operation | Token-Cost (geschätzt) |
|---|---|
| setup, leer (DBs anlegen, 0 Source-Files) | ~10k |
| setup, 100 Files Source | ~150-300k |
| setup, 500 Files Source | ~750k-1.5M |
| routine, 0 neue Files | ~5-10k |
| routine, 50 Files | ~80-150k |
| review-inbox, 10 Einträge | ~5-10k |
| repair, 100 Files curated, ~5 Findings | ~30-50k |
| repair, 500 Files curated, ~30 Findings | ~100-180k |
