#!/usr/bin/env python3
"""
validate_prosody.py — Prosodie-Validator für Agency-System-Lyrics.

Nutzung:
    python3 validate_prosody.py <pfad-zur-lyric-datei>
    python3 validate_prosody.py -   (liest von stdin)

Prüft:
  1. Silbenzahl pro Zeile (grobe Heuristik für Deutsch)
  2. Symmetrie zwischen parallelen Verses (Verse 1 vs Verse 2)
  3. Reimschema pro Section (konstant AABB oder ABAB oder AABA etc.)

Output:
  PASS | FAIL mit Diagnose-Zeilen.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from dataclasses import dataclass, field


VOWEL_GROUPS = re.compile(r"[aeiouäöüy]+", re.IGNORECASE)
SECTION_TAG = re.compile(r"^\s*\[([^\]]+)\]\s*$")


def count_syllables_de(line: str) -> int:
    """Grobe Silbenschätzung für Deutsch: Zählt Vokalgruppen pro Wort."""
    text = re.sub(r"[^a-zA-ZäöüÄÖÜß\s]", " ", line)
    total = 0
    for word in text.split():
        groups = VOWEL_GROUPS.findall(word)
        total += max(1, len(groups))
    return total


def last_sound(line: str) -> str:
    """Reim-Signatur: letzte Vokalgruppe + Endkonsonanten."""
    text = re.sub(r"[^a-zA-ZäöüÄÖÜß]", "", line.lower())
    if not text:
        return ""
    # Nimm die letzten 4 Zeichen als Näherung der Reimendung
    return text[-4:]


def rhyme_scheme(lines: list[str]) -> str:
    """Weist jeder Zeile einen Reim-Buchstaben zu (A, B, C, ...)."""
    if not lines:
        return ""
    sounds = [last_sound(l) for l in lines]
    scheme = []
    mapping: dict[str, str] = {}
    next_letter = ord("A")
    for s in sounds:
        # Fuzzy-Match: gleiche letzte 2 Zeichen = gleicher Reim
        key = s[-2:] if len(s) >= 2 else s
        if key not in mapping:
            mapping[key] = chr(next_letter)
            next_letter += 1
        scheme.append(mapping[key])
    return "".join(scheme)


@dataclass
class Section:
    name: str
    lines: list[str] = field(default_factory=list)

    @property
    def syllables(self) -> list[int]:
        return [count_syllables_de(l) for l in self.lines]

    @property
    def scheme(self) -> str:
        return rhyme_scheme(self.lines)


def parse(text: str) -> list[Section]:
    sections: list[Section] = []
    current: Section | None = None
    for raw in text.splitlines():
        m = SECTION_TAG.match(raw)
        if m:
            if current and current.lines:
                sections.append(current)
            current = Section(name=m.group(1).strip())
        elif raw.strip() and current is not None:
            current.lines.append(raw.strip())
    if current and current.lines:
        sections.append(current)
    return sections


def check_symmetry(sections: list[Section]) -> list[str]:
    """Prüft Silbensymmetrie zwischen Verse 1 und Verse 2 (und weitere Paare)."""
    issues: list[str] = []
    verses = [s for s in sections if s.name.lower().startswith("verse")]
    if len(verses) < 2:
        return issues
    ref = verses[0]
    for v in verses[1:]:
        if len(v.lines) != len(ref.lines):
            issues.append(
                f"FAIL: {v.name} hat {len(v.lines)} Zeilen, "
                f"{ref.name} hat {len(ref.lines)}."
            )
            continue
        for i, (a, b) in enumerate(zip(ref.syllables, v.syllables), 1):
            if abs(a - b) > 1:
                issues.append(
                    f"FAIL: {ref.name} Z{i}={a} Silben, "
                    f"{v.name} Z{i}={b} Silben (Δ>1)."
                )
    return issues


def check_scheme_stability(sections: list[Section]) -> list[str]:
    """Pro Section muss das Reimschema eine der erlaubten Formen haben."""
    allowed = {"AABB", "ABAB", "AABA", "ABBA", "AAAA"}
    issues: list[str] = []
    for s in sections:
        if len(s.lines) < 2:
            continue
        scheme = s.scheme
        # Wir prüfen nur die ersten 4 Zeilen als Schema-Indikator
        head = scheme[:4]
        if len(head) == 4 and head not in allowed:
            issues.append(
                f"WARN: Section [{s.name}] Schema '{head}' "
                f"nicht in {sorted(allowed)}."
            )
    return issues


def main() -> int:
    if len(sys.argv) < 2:
        print("Nutzung: validate_prosody.py <datei|->", file=sys.stderr)
        return 2

    src = sys.argv[1]
    text = sys.stdin.read() if src == "-" else Path(src).read_text(encoding="utf-8")

    sections = parse(text)
    if not sections:
        print("FAIL: Keine Sections gefunden (erwarte [Verse 1], [Chorus] etc.).")
        return 1

    print(f"Gefundene Sections: {[s.name for s in sections]}")
    for s in sections:
        print(f"  [{s.name}] Silben={s.syllables}  Schema={s.scheme}")

    issues = check_symmetry(sections) + check_scheme_stability(sections)

    if not issues:
        print("\nPASS")
        return 0

    print("\nDiagnose:")
    for i in issues:
        print(f"  {i}")
    fails = [i for i in issues if i.startswith("FAIL")]
    print("\n" + ("FAIL" if fails else "PASS_WITH_WARNINGS"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
