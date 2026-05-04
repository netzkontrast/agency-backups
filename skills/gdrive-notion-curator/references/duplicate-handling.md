# Duplicate-Handling

> **Hard Rule:** Files NIE doppelt nach `/curated/` kopieren. Drive ist write-once-additive — wir vermeiden Müll.

## Mehrstufige Duplikat-Erkennung

Pro File aus Source-Listing wird vor dem Copy geprüft. ERSTE Regel die triggert gewinnt.

### Regel 1 — Bereits in Notion-DB (sicherster Skip)

```
if file.id in notion.original_drive_ids:
    skip(reason="already-in-files-db")
```

`original_drive_ids` ist das Set aller `Original Drive ID`-Werte aus der Files-DB, einmal beim Skill-Start geholt.

**Wichtig:** Das ist die zuverlässigste Skip-Regel — sie verhindert dass abgebrochene Runs zu Doppel-Kopien führen.

### Regel 2 — Title-Pattern "Kopie/Copy"

```python
title_lower = title.lower()
if title_lower.startswith("kopie von ") or title_lower.startswith("copy of "):
    create_files_db_entry(status="duplicate", reason="title-prefix-copy")
    skip()
```

### Regel 3 — Title-Pattern Numeriert

```python
import re
# Matches " (1).md", " (2)", " (Kopie)", " (copy)"
if re.search(r'\s\((\d+|kopie|copy)\)(\.\w+)?$', title_lower):
    base_title = re.sub(r'\s\((\d+|kopie|copy)\)(\.\w+)?$', r'\2', title)
    if base_title in notion.titles_in_db:
        create_files_db_entry(status="duplicate", reason="numbered-copy-of-existing")
        skip()
```

### Regel 4 — MD5-Checksum (nur Binary-Files)

```python
if file.md5Checksum:  # nur PDFs, Images, etc. — Google Docs haben kein md5
    if file.md5Checksum in notion.md5_checksums:
        create_files_db_entry(status="duplicate", reason=f"md5-match")
        skip()
```

**Achtung:** Google Docs (`mimeType=application/vnd.google-apps.document`), Sheets, Slides haben **kein md5Checksum**-Feld. Diese Regel ist nur für Binary-MIME-Types relevant.

### Regel 5 — Title+Size-Heuristik (für Google Docs)

Google Docs haben kein md5, aber size:

```python
if file.mimeType.startswith("application/vnd.google-apps.") and file.size:
    # Suche existierenden Notion-Entry mit gleichem Title und ähnlicher Size
    candidates = notion.find_by_title_and_size(file.title, file.size, tolerance=0.05)
    if candidates:
        # NICHT skip — könnte legitime Variante sein
        create_files_db_entry(
            status="copied",
            manual_action="Verify: similar file exists",
            notes=f"Similar to existing: {candidates[0].id}"
        )
        # → User entscheidet manuell ob Duplikat
```

Diese Regel **skippt nicht**, sondern markiert für User-Review. Begründung: gleicher Title + gleiche Größe ist verdächtig, aber nicht eindeutig (z.B. revidierte Version).

## Duplikat-Status in Files-DB

Wenn Regel 2-4 triggern: Files-DB-Entry wird trotzdem angelegt mit:
- `Original Drive ID` = die Drive-ID des duplikaten Originals
- `Curated Drive ID` = leer (nicht kopiert)
- `Sort Status` = `duplicate`
- `Match Reason` = warum als Duplikat erkannt
- `Notes` = vom Skill geschrieben mit Verweis auf Original-Entry

Das hilft beim Repair-Call, Duplikate nachvollziehen zu können ohne nochmal zu probieren.

## Algorithmus

```python
def check_duplicate(file, notion_state):
    # Regel 1: schon in DB
    if file.id in notion_state.original_drive_ids:
        return DuplicateResult(skip=True, reason="already-in-db", create_entry=False)

    # Regel 2: Kopie/Copy-Prefix
    title_lower = file.title.lower()
    if title_lower.startswith("kopie von ") or title_lower.startswith("copy of "):
        return DuplicateResult(skip=True, reason="title-prefix-copy", create_entry=True)

    # Regel 3: Numerierter Suffix
    import re
    m = re.search(r'\s\((\d+|kopie|copy)\)(\.\w+)?$', title_lower)
    if m:
        ext = m.group(2) or ""
        base = re.sub(r'\s\((\d+|kopie|copy)\)' + re.escape(ext) + r'$', ext, file.title, flags=re.IGNORECASE)
        if base.lower() in {t.lower() for t in notion_state.titles_in_db}:
            return DuplicateResult(skip=True, reason="numbered-copy", create_entry=True)

    # Regel 4: MD5-Match (nur Binary)
    if hasattr(file, 'md5Checksum') and file.md5Checksum:
        if file.md5Checksum in notion_state.md5_checksums:
            return DuplicateResult(skip=True, reason="md5-match", create_entry=True)

    # Regel 5: Title+Size für Google Docs
    if file.mimeType.startswith("application/vnd.google-apps.") and file.size:
        for existing in notion_state.find_by_title(file.title):
            if existing.size and abs(existing.size - file.size) / max(existing.size, file.size) < 0.05:
                return DuplicateResult(
                    skip=False,
                    reason=f"title-size-similar-to-{existing.id}",
                    create_entry=False,
                    manual_action="Verify duplicate"
                )

    # Kein Duplikat
    return DuplicateResult(skip=False, reason=None, create_entry=False)
```

`scripts/duplicate_check.py` implementiert die Regeln 2-5 als CLI-Tool. Regel 1 ist Notion-Lookup und passiert direkt im MCP-Workflow ohne Python.

## Notion-State-Vorbereitung

Vor jedem Sweep: Cache der relevanten Notion-Daten holen.

```
Notion-Search auf Files-DB:
  Filter: alle Pages
  Properties: Original Drive ID, Filename, MD5 Checksum
  → in-memory Sets:
      - original_drive_ids: Set[str]
      - titles_in_db: Set[str]
      - md5_checksums: Set[str]
```

Bei sehr großer DB (>1000 Files): paginiert holen. Per Page-Cap 100, mehrere Notion-Queries.
