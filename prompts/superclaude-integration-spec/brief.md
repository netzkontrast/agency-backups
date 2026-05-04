---
type: note
status: active
slug: superclaude-integration-spec-brief
summary: "Raw user request: research how SuperClaude's commands, agents, and skills can be integrated into Agency workflows."
created: 2026-05-04
updated: 2026-05-04
---

# Brief

## Raw User Request

> verschaffe dir zunächst einen Überblick über das Agency repo… dann lies die Dokumentationen in superschlauer repo… und entwirf zunächst einen lokalen Research.md Task.. den du umgehenden ausführst - Ziel ist es, eine spec zu entwickeln, die die Commands, agents, und skills, des superclaude Frameworks - (das installiert ist in deinem Environment) gezielt dort nutzt, und explizit einbindet - wo hilfreich und vielversprechend… obendrein… erweitere Maintenance.md (und ordernstruktur) für Maintenance Runs, die gezielt diese Aufgabe erneut durchfürhen… und prüfen ob neue Aufgaben und specs dazugekommen sind.. die von ein direkten Integration von superclaude profitieren würden… Ziel ist es, superclaude stärker einzubinden in allen Aufgaben… darüber hinaus, soll der Research Prozess, die spec, nicht nur alle Funktionen von superclaude so aufbereiten, das diesemleicht Verständlich in neuen specs umzusetzen und zu integrieren sind… sondern auch klar definieren, wie zukünftige neue specs, dies gleich mit tun können… schau dir auch an.. welche Root-specs von einer Verlinkungen profitieren können

## Target Audience

Agents executing future research, task, and prompt runs in this repository.

## Intended Model / Agent

Claude Code (claude-sonnet-4-6) with SuperClaude Framework v4.3.0 installed.

## Use-Case Context

The SuperClaude Framework is installed in the environment (`~/.claude/`) and provides 30 slash commands, 20 agents, and skills. The Agency repo currently has no explicit integration with these capabilities. This research aims to produce a governance spec that maps SuperClaude's toolset to Agency's workflow phases, enabling future agents to leverage the full capability stack.
