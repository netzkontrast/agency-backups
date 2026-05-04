# Resume-Logic — State aus Notion

> **Hard Rule:** Notion ist State-Source. Skill-Start zieht alle nötigen Infos aus Notion. Kein lokaler State-File ausser den statischen Setup-IDs in `/tmp/gdrive-curator-state.json`.

## Warum kein lokaler State

- Setup läuft in Claude Web — der Container kann zwischen Sessions verschwinden
- User kann zwischen Sessions in Notion direkt korrigieren (Topic ändern, Entries pinnen)
- Wenn Skill auf mehreren Maschinen genutzt wird: Notion synct automatisch

`/tmp/gdrive-curator-state.json` enthält NUR die statischen IDs aus dem Setup (Drive-Folder-IDs + 3 Notion-data_source_ids). Alles andere ist in Notion.

## Was beim Skill-Start aus Notion geholt wird

### Schritt 1: Setup-State lesen

```bash
cat /tmp/gdrive-curator-state.json
```

Falls nicht vorhanden: User muss `setup` triggern (oder askuser nach den fehlenden IDs für Wiederherstellung).

### Schritt 2: Letzten Run-State aus Notion ziehen

Nur relevant für **routine** und **repair**, nicht für **setup** (setup liest sowieso alles).

```
Notion-Search auf Files-DB:
  Filter: "Run ID" is not empty
  Sort: "Created" DESC
  Properties: "Run ID", "Original Drive ID", "Created"
  Page-Size: 100
```

In-Memory-Verarbeitung:
- `last_run_id` = max("Run ID") sortiert lexikographisch (Format `run-YYYYMMDD-HHMMSS-<mode>`)
- `last_run_files` = alle Pages mit `Run ID == last_run_id`
- **`newest_in_last_run`** = `max("Created")` aus `last_run_files`
  - Das ist die createdTime des **jüngsten** Files das in dem letzten Run verarbeitet wurde
  - Wird in routine als Filter benutzt: `createdTime > newest_in_last_run`

### Schritt 3: Volles Notion-Set für Duplicate-Check

Für die Duplicate-Regeln (siehe `duplicate-handling.md`):

```
Notion-Search auf Files-DB (paginated):
  Filter: alle Pages
  Properties: "Original Drive ID", "Filename", "MD5 Checksum"
  Page-Size: 100
```

Aufbau:
- `original_drive_ids: Set[str]`
- `titles_in_db: Set[str]`
- `md5_checksums: Set[str]`

Bei großen DBs (>1000 Files): mehrere paginierte Queries via Notion-Search mit cursor.

### Schritt 4: Source-Filter berechnen

| Operation | Source-Filter |
|---|---|
| **setup** | kein Filter — alle Files in Source-Folder |
| **routine** | `createdTime > newest_in_last_run` |
| **repair** | irrelevant (listet `/curated/`, nicht Source) |

## Warum `>` und nicht `>=`?

Frühere Skill-Versionen nutzten `>= oldest_in_last_run`. Das ist defensiv — fängt Files die im selben Sekunden-Bucket wie das oldest-File des Vorgänger-Runs liegen — aber bei einem normalen routine-Run ist der oldest-of-last-run schon längst verarbeitet, und Skip-Regel filtert ihn raus. Das produziert pro Run unnötige Skip-Checks gegen die ganze DB.

In v0.4.0 nutzen wir `> newest_in_last_run`. Logik:
- routine cap=50 ASC verarbeitet die **ältesten 50 der neuen** zuerst
- `newest_in_last_run` ist die createdTime des 50. Files (oder weniger, wenn weniger gefunden)
- Nächste routine filtert `> newest_in_last_run` → sieht nur Files mit jüngerer createdTime
- Bei strengem `>` und gleichzeitigen createdTimes (rare bei Sekunden-Auflösung): Edge-Case, akzeptabel weil sehr selten

**Edge-Case:** Wenn zwei Files exakt dieselbe createdTime haben und Skill genau bei dem ersten cappt, würde der zweite mit `>` übersprungen. Mitigation:
- Skip-Regel filtert ihn beim **nächsten** routine-Run nicht mehr automatisch (er hat höheren oder gleichen createdTime, kommt nicht mehr ins Filter-Set)
- → User sollte ggf einen `repair` ausführen, der per Drift-Detection den Orphan im Source erkennen würde
- ODER: Skill nimmt am Ende der routine die createdTime des **vorletzten** Files (=50.) als `effective_newest`, und nutzt `>=` für genau den Sekunden-Bucket

In v0.4.0 ist die Wahl: einfache `> newest_in_last_run`-Logik, Edge-Case via repair fangbar.

## Resume bei Crash mid-Run

### Szenario A: setup crasht

setup ist idempotent. User triggert `setup` nochmal:
1. State aus Notion (Schritt 1-3 oben)
2. `original_drive_ids` enthält bereits alle schon-verarbeiteten Files
3. setup listet komplett, Skip-Regel filtert die schon-verarbeiteten
4. Skill verarbeitet die restlichen Files weiter

Keine spezielle Resume-Logic nötig.

### Szenario B: routine crasht

User triggert `routine` nochmal:
1. Letzte routine vor Crash hat möglicherweise schon X Files verarbeitet (mit `Run ID = run-...-routine`)
2. `newest_in_last_run` aus dieser **abgebrochenen** Run-ID = createdTime des jüngsten verarbeiteten Files
3. Nächste routine filtert `> newest_in_last_run` → findet die Files die createdTime > X haben
4. Files mit createdTime ≤ X die in dem Crash-Run nicht verarbeitet wurden, werden **nicht** wieder gesehen

**Verlust-Analyse:** Kein Verlust, weil ASC-Sortierung garantiert dass die verarbeiteten Files die niedrigste createdTime haben.

Beispiel — routine sortiert ASC, cap 50, Crash bei File #25:
- Files 1-25 in Notion mit `Run ID = R_crash` (createdTime aufsteigend)
- `newest_in_last_run` nach Crash = createdTime von File #25
- Nächste routine filter `> createdTime(#25)` → findet Files #26-#50 + alle neueren
- Skill verarbeitet weiter, neue Run-ID `R_resume`

Voraussetzung dafür: routine schreibt File-by-File in Notion (kein Batch). v0.4.0 macht das so — siehe Verarbeitungs-Loop in `workflow-phases.md`.

### Szenario C: Container-Restart, /tmp/-State weg

`/tmp/gdrive-curator-state.json` ist nicht persistent. Bei Container-Restart:
1. setup mit `claude_root_folder_id`, `source_folder_ids`, `notion_workspace_page_id` askuser
2. Skill findet existierende DBs in Notion (via notion-search nach Title) → liest data_source_ids
3. State-File wird neu geschrieben
4. Restliches setup läuft idempotent durch

User-Friction: 3 IDs nochmal eingeben. Mitigation in zukünftiger v0.5.0: Setup-IDs in einer Notion-`_meta`-Page speichern (Single-Source-of-Truth Notion).

## Pseudo-Code

```python
def get_state_from_notion(notion_client, files_ds_id):
    # 1. Setup-State (statische IDs)
    with open('/tmp/gdrive-curator-state.json') as f:
        setup = json.load(f)

    # 2. Letzten Run finden
    last_run_query = notion_client.search(
        data_source=files_ds_id,
        filter={"Run ID": {"is_not_empty": True}},
        sort={"Created": "desc"},
        properties=["Run ID", "Original Drive ID", "Created"],
        limit=100
    )

    if not last_run_query:
        return State(
            **setup,
            last_run_id=None,
            newest_in_last_run=None,
            original_drive_ids=set(),
            titles_in_db=set(),
            md5_checksums=set()
        )

    last_run_id = max(p.run_id for p in last_run_query)
    last_run_files = [p for p in last_run_query if p.run_id == last_run_id]
    newest_in_last_run = max(p.created for p in last_run_files)

    # 3. Volles Set für Duplicate-Check (paginated)
    all_files = notion_client.search_all(
        data_source=files_ds_id,
        properties=["Original Drive ID", "Filename", "MD5 Checksum"]
    )
    original_drive_ids = {p.original_drive_id for p in all_files}
    titles_in_db = {p.filename for p in all_files}
    md5_checksums = {p.md5_checksum for p in all_files if p.md5_checksum}

    return State(
        **setup,
        last_run_id=last_run_id,
        newest_in_last_run=newest_in_last_run,
        original_drive_ids=original_drive_ids,
        titles_in_db=titles_in_db,
        md5_checksums=md5_checksums
    )
```

## Edge Cases

### Keine Files in DB (allererster Run)

`last_run_id=None`, `newest_in_last_run=None`. Bei `routine`-Trigger: askuser ob `setup` gemeint war. Bei `setup`: läuft normal ohne Filter.

### Nur Topics-DB ist leer (nach DB-Reset)

`/tmp/gdrive-curator-state.json` zeigt auf eine Topics-DB die User manuell geleert hat. Skill detektiert beim ersten Sweep dass keine Topics-Pages existieren → askuser: "Topics-DB neu befüllen aus topics-config.yaml?"

### `/tmp/gdrive-curator-state.json` weg

Container-Restart, Setup-State weg. askuser: "Setup-IDs erneut erfragen oder `setup` wiederholen?" (siehe Szenario C oben)

### Zwei parallele Skill-Sessions

Wenn User in zwei Tabs gleichzeitig Skill triggert: beide ziehen gleichen `last_run_id`, generieren neue Run-IDs, processen potentiell überlappende Files. Skip-Regel 1 (Original Drive ID schon in Notion) verhindert Doppel-Copy weil zweite Session beim Anlegen sieht dass Erste schon den Entry erstellt hat — **aber Race Condition möglich** zwischen Notion-Lookup und Notion-Create.

**Mitigation:** User soll nur eine Skill-Session gleichzeitig triggern. Doku in README.

### Notion-DB hat >1000 Pages

Pre-Load des Duplicate-Sets via paginated Search wird teuer (10+ Notion-Queries pro Skill-Start). Bei DB-Größe >5000 würde Per-File-Lookup günstiger werden. In v0.4.0 nicht implementiert; bei Bedarf in v0.5.0 nachziehen.
