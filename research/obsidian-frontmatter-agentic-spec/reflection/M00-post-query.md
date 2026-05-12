# Post-Query-Expansion-Reflektion

**Q1. Was glaube ich gerade tatsächlich, und wie confident bin ich?**
Ich bin sehr confident (hoch), dass das Expansion-Pattern nicht primär durch Dateigröße (Token-Limit), sondern durch "Semantic Divergence" getriggert werden muss.

**Q2. Was ist das stärkste Gegenbeispiel gegen meine aktuelle Überzeugung?**
Das stärkste Gegenbeispiel sind Agenten-Frameworks, die starre Chunker verwenden (z.B. "teile nach 500 Wörtern"), weil semantisches Splittern für LLMs fehleranfällig zu programmieren ist.

**Q3. Wo liege ich am wahrscheinlichsten falsch, und warum?**
Ich könnte falsch liegen in der Annahme, dass eine `README.md` Manifest-Datei im Expansion-Unterordner für Agenten leicht zu finden ist. Wenn sie die Ordner-Struktur nicht kennen, verfehlen sie das Manifest.

**Q4. Was würde ich anders machen wenn ich die Research von vorne beginnen würde mit dem Wissen das ich jetzt habe?**
Ich würde Zettelkasten-Literatur überspringen und direkt auf "File System manifest index parsing für LLM RAG" suchen.

**Q5. Was ist die einzige höchstwertige nächste Aktion?**
Die Heuristiken in harte Constraints (MUSS/KANN/DARF NICHT) zu gießen, um sie in Schritt 4 in der Spezifikation zu dokumentieren.
