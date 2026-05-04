# Repair-Consistency

> **Zweck:** Drive `/curated/` und Notion Files-DB konsistent halten. Read-only Diff + askuser-driven Repair. KEIN automatisches Reparieren.

## Wann nutzen

- User merkt: "habe in Drive manuell was getrasht/verschoben"
- Nach längerer Pause zwischen Sweeps
- Wenn Notion-DB-Entries verdächtig erscheinen
- Routinemässig 1x pro Monat

## Sequenz

### Schritt 1: Drive-Listing flat in /curated/

```
Google Drive:search_files
  query: "parentId = '<curated_folder_id>' and trashed=false"
  pageSize: 100
```

Bei mehr als 100: paginieren via `nextPageToken`.

Aufbau Set: `drive_curated_set = {file.id, file.title for file in results}`

### Schritt 2: Notion-Listing aller Files-DB-Entries mit Curated Drive ID

```
Notion-Search auf Files-DB:
  Filter: "Curated Drive ID" is not empty
  Properties: Filename, Original Drive ID, Curated Drive ID, Sort Status, Sub-Page Link
  Page-Size: 100, paginated
```

Aufbau Set: `notion_curated_set = {p.curated_drive_id, p.notion_page_id, p.sort_status for p in results}`

### Schritt 3: Diffs berechnen

```python
drive_only = {f.id for f in drive_curated_set} - {p.curated_drive_id for p in notion_curated_set}
notion_only = {p.curated_drive_id for p in notion_curated_set} - {f.id for f in drive_curated_set}
```

### Schritt 4: Auch Source-Originals prüfen (optional)

```
Notion-Query Files-DB:
  Filter: "Original Drive ID" is not empty AND "Sort Status" != "archived"
  Properties: Original Drive ID, Filename, Sort Status
```

Für jedes File: `Google Drive:get_file_metadata(file_id=Original Drive ID)`. Bei 404 oder `trashed=true`: Source-File getrasht.

**Achtung:** Das ist potentiell viele get_metadata-Calls. Für große DBs (>500 Files): Stichprobe oder askuser ob full check gewünscht.

## Diff-Klassifikation

### Drift-Typ A — Orphan in Drive

**Symptom:** File existiert in `/curated/` aber kein Files-DB-Entry mit dieser Curated Drive ID

**Mögliche Ursachen:**
- File manuell in /curated/ gezogen vom User
- Skill ist mid-run gecrasht NACH copy aber VOR Notion-create-page
- Test-Artefakte wie das `test-copy-from-mcp-2026-05-02.md` aus dem Reality-Test

**Repair-Optionen (askuser):**
- `Adopt to Notion` — Files-DB-Entry anlegen mit Status=copied, dann normal weiter klassifizieren
- `Mark as test artifact` — Entry mit Notes="manual test artifact, ignore", Sort Status=archived
- `Skip` — nicht anrühren

### Drift-Typ B — Ghost in Notion

**Symptom:** Notion-Entry mit Curated Drive ID, aber File in Drive nicht mehr da (getrasht/gelöscht)

**Mögliche Ursachen:**
- User hat File manuell getrasht in Drive
- Drive-Sync-Fehler

**Repair-Optionen (askuser):**
- `Set archived` — Sort Status=archived, behalte Entry für Historie
- `Delete from Notion` — Files-DB-Entry trashen via update_data_source mit in_trash=true (für Page selbst nicht nutzbar — User muss in Notion-UI machen)
- `Skip` — nicht anrühren

### Drift-Typ C — Source Original gone

**Symptom:** Notion-Entry hat Original Drive ID, aber Source-File ist 404 oder trashed

**Mögliche Ursachen:**
- User hat Original getrasht (was wir wollen — Curated-Copy ist canonical)
- Source-Folder wurde umstrukturiert

**Repair-Optionen (askuser):**
- `Confirm archived` — User bestätigt: alles gut, Curated-Copy ist canonical
  - Sort Status bleibt indexed/in-inbox, aber Sub-Page-Header wird mit "Original archived" annotiert
- `Restore from Trash` — User soll in Drive prüfen ob Trash leerbar ist
- `Skip`

### Drift-Typ D — Status-Inkonsistenz

**Symptom:** Files-DB-Entry hat `Sort Status=indexed` aber `Sub-Page Link` ist leer (oder `Sub-Page Link` zeigt auf gelöschte Notion-Page)

**Repair-Optionen (askuser):**
- `Re-create sub-page` — Topic-Page finden + Sub-Page neu anlegen + Sub-Page Link setzen
- `Set status to copied` — wenn Sub-Page nicht mehr nötig, Status zurücksetzen
- `Skip`

## Algorithmus

```python
def repair_consistency(notion, drive, state):
    print("Repair-Phase startet...")

    # 1. Drive curated/ listing
    drive_files = drive.list_in_folder(state.curated_folder_id)
    drive_ids = {f.id for f in drive_files}

    # 2. Notion files-db mit curated id
    notion_curated = notion.query(
        ds_id=state.files_ds_id,
        filter={"Curated Drive ID": {"is_not_empty": True}}
    )
    notion_curated_ids = {p.curated_drive_id for p in notion_curated}

    # 3. Diffs
    drive_only = drive_ids - notion_curated_ids
    notion_only = notion_curated_ids - drive_ids

    findings = []

    # Drift A — Orphan in Drive
    for drive_id in drive_only:
        f = next(x for x in drive_files if x.id == drive_id)
        findings.append(Finding(
            type="orphan",
            ref=drive_id,
            description=f"File in /curated/ but no Notion entry: {f.title}",
            options=["adopt", "mark-test-artifact", "skip"]
        ))

    # Drift B — Ghost in Notion
    for c_id in notion_only:
        page = next(p for p in notion_curated if p.curated_drive_id == c_id)
        findings.append(Finding(
            type="ghost",
            ref=c_id,
            description=f"Notion entry but no Drive file: {page.filename}",
            options=["set-archived", "delete-from-notion", "skip"]
        ))

    # Optional Drift C — Source Original gone (if requested)
    if check_source_originals:
        for page in notion.query(state.files_ds_id, filter={"Original Drive ID": {"is_not_empty": True}}):
            try:
                meta = drive.get_metadata(page.original_drive_id)
                if meta.trashed:
                    raise NotFound()
            except NotFound:
                findings.append(Finding(
                    type="source-gone",
                    ref=page.original_drive_id,
                    description=f"Original {page.filename} not in Drive anymore",
                    options=["confirm-archived", "restore-from-trash", "skip"]
                ))

    # Drift D — Status inconsistencies
    for page in notion.query(state.files_ds_id, filter={"Sort Status": "indexed"}):
        if not page.sub_page_link:
            findings.append(Finding(
                type="status-inconsistent",
                ref=page.id,
                description=f"Page indexed but no Sub-Page Link: {page.filename}",
                options=["recreate-sub-page", "set-copied", "skip"]
            ))

    # 4. Report
    print(f"Findings: {len(findings)} ({len([f for f in findings if f.type=='orphan'])} orphans, {len([f for f in findings if f.type=='ghost'])} ghosts, ...)")

    # 5. Pro Finding: askuser
    for finding in findings:
        choice = ask_user(finding.description, finding.options)
        apply_repair(finding, choice)
```

## Token-Budget

| Operation | Cost |
|---|---|
| Drive-Listing (100 Files) | ~3k |
| Notion-Query (100 Pages) | ~5k |
| Pro askuser-Finding | ~500 input + 100 output |
| Pro Repair-Aktion | ~1k |

Bei 10 Findings: ~20-30k. Bei 50 Findings: ~80-120k.

Mitigation: User kann sagen "stop" → Skill speichert Resume-Point in `/tmp/gdrive-curator-repair.json` und macht später weiter.

## Was Repair NICHT macht

- KEIN automatisches Trashen in Drive (Tool-Limitation + Sicherheit)
- KEIN automatisches Bulk-Delete in Notion
- KEIN Versuch, gelöschte Drive-Files zu "rekonstruieren" aus Notion-Daten
- KEINE Repair-Aktionen für Pinned-Entries
- KEIN Touch von User-Notes oder User-eigenen Properties
