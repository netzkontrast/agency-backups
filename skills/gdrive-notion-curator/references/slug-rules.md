# Slug-Regeln

> File-Slug für Filename in `/curated/`. Topic-Keywords BLEIBEN drin (Pfad ist nicht mehr Topic-Referenz).

## Algorithmus

```python
def file_slug(title: str, max_len: int = 80) -> str:
    """
    Beispiele:
      "Kohärenz Protokoll - Notes.md"          → "kohaerenz-protokoll-notes.md"
      "Research_Prompt: Agentic Workflows.md"  → "research-prompt-agentic-workflows.md"
      "(My English Notes).pdf"                 → "my-english-notes.pdf"
      "Kapitel 1 — Außenstelle.docx"           → "kapitel-1-aussenstelle.docx"
      "übung mit Sonderzeichen!?@#.txt"        → "uebung-mit-sonderzeichen.txt"
      ".hidden-file"                           → "hidden-file"  (no leading dot)
      ""                                       → "untitled-<hash>"
    """

    # 1. Endung extrahieren
    base, ext = split_extension(title)

    # 2. Leerstrings handlen
    if not base.strip():
        return f"untitled-{short_hash(title)}{ext}"

    # 3. Lowercase
    s = base.lower()

    # 4. Umlaut-Normalize
    s = s.translate({
        ord('ä'): 'ae', ord('ö'): 'oe', ord('ü'): 'ue', ord('ß'): 'ss',
        ord('Ä'): 'ae', ord('Ö'): 'oe', ord('Ü'): 'ue',
    })

    # 5. Unicode-Combining-Marks entfernen (é → e, etc.)
    import unicodedata
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))

    # 6. Non-alphanumeric → "-"
    import re
    s = re.sub(r'[^a-z0-9]+', '-', s)

    # 7. Mehrfach-"-" zu einzelnem "-" collapse
    s = re.sub(r'-+', '-', s)

    # 8. Leading/Trailing "-" strippen
    s = s.strip('-')

    # 9. Truncate (max_len gilt für slug ohne extension)
    s = s[:max_len].rstrip('-')

    # 10. Fallback bei leerem Resultat
    if not s:
        return f"untitled-{short_hash(title)}{ext}"

    # 11. Extension wieder anhängen
    return s + ext
```

## Bekannte Extensions

```python
KNOWN_EXTENSIONS = (
    '.md', '.docx', '.txt', '.pdf', '.html', '.rtf', '.odt',
    '.m4a', '.mp3', '.wav', '.flac',
    '.png', '.jpg', '.jpeg', '.gif', '.webp',
    '.csv', '.tsv', '.json', '.yaml', '.yml',
    '.py', '.js', '.ts', '.html', '.css',
    '.zip', '.tar', '.gz',
)
```

Wenn Title keine bekannte Extension hat: kein ext, slug ohne extension.

Google Doc native MIME hat keine Extension im Title — daraus wird beim Copy `.gdoc`? Nein, Google Docs bleiben als Doc-Type. Filename in /curated/ hat dann keine Extension.

## Disambiguation bei Duplikat-Filename in /curated/

Sehr selten — könnte passieren wenn zwei verschiedene Original-Files den gleichen Slug ergeben.

```python
def disambiguate(desired_slug: str, existing_in_curated: set[str]) -> str:
    if desired_slug not in existing_in_curated:
        return desired_slug

    base, ext = split_extension(desired_slug)
    i = 2
    while f"{base}-{i}{ext}" in existing_in_curated:
        i += 1
    return f"{base}-{i}{ext}"
```

Vor jedem Copy: Drive-Listing in /curated/ holen oder cachen, Disambiguation prüfen.

**Pragmatisch:** Bei Skill-Start einmal `/curated/`-Listing holen, in-memory `existing_curated_titles` Set halten, nach jedem Copy ergänzen.

## CLI-Tool

`scripts/slug.py`:

```bash
python3 scripts/slug.py "Kohärenz Protokoll - Notes.md"
# Output: kohaerenz-protokoll-notes.md

python3 scripts/slug.py "$TITLE" --max-len 60
```

## Tests

| Input | Erwartete Output |
|---|---|
| `"Kohärenz Protokoll - Notes.md"` | `"kohaerenz-protokoll-notes.md"` |
| `"Research_Prompt: Agentic Workflows.md"` | `"research-prompt-agentic-workflows.md"` |
| `"(My English Notes).pdf"` | `"my-english-notes.pdf"` |
| `"Kapitel 1 — Außenstelle.docx"` | `"kapitel-1-aussenstelle.docx"` |
| `"übung mit Sonderzeichen!?@#.txt"` | `"uebung-mit-sonderzeichen.txt"` |
| `""` | `"untitled-<hash>"` |
| `"   "` | `"untitled-<hash>"` |
| `"---only-dashes---"` | `"only-dashes"` |
| `"a"` | `"a"` |
| 100 Zeichen mit max_len=60 | erste 60 Zeichen, kein trailing dash |
