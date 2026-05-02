# Brief

**Original user request (verbatim):**

> Analysiere repo mit /spec-skill und /research-prompt-optimizer und schreibe einen prompt im folder prompt (Folge folder spec) für den prompt Task, erzeuge ein prompt.md spec für die Arbeit an und mit prompts - und erzeuge einen prompt für ein Update des Research optimizer - so, das wenn ein hier landender Research-folder Anmerkungen, offene Fragen, oder ähnliches enthält, damit neue Research-prompts erzeugt werden können… analog zu Research.md

**Interpreted intent:**

Create a self-contained prompt that updates the research-prompt-optimizer capability: when given an existing `/research/<slug>/` folder containing annotations, open questions, [NOT-FOUND] markers, or friction-log improvement suggestions, the prompt enables an agent to extract those signals and generate new, fully-formed research prompts in the `research-prompt-optimizer v2.1.0` format — analogous to how `RESEARCH.md` governs the execution of a single research task.

**Target audience:** Any agent operating in this repository who encounters a research folder with unresolved questions after the primary research cycle is complete.

**Target model/agent:** Model-agnostic. Designed for Claude Code, Gemini Jules, or any ReAct-capable agent.

**Intended use:** Give the prompt verbatim to an agent, along with the path to the target research folder. The agent reads the folder, extracts annotation signals, and deposits new research prompts into `/prompt/<new-slug>/prompt.md`.

**Source skill:** research-prompt-optimizer v2.1.0 (referenced in `research/ncp-novel-co-authoring-spec/prompt.md`).

**Date:** 2026-05-02
