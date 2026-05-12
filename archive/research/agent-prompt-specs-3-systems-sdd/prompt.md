---
topic: "Spec-Driven Best Practices for Research/Agent Prompts on Google Jules, Claude Code, and Gemini Deep Research"
slug: "agent-prompt-specs-3-systems-sdd"
research_category: "B"
research_category_label: "Extraction"
critical_thinking_methods:
  - "Source Triangulation"
  - "Contradiction Log"
  - "What Would Change My Mind (Pre-Commitment)"
  - "Steelmanning"
  - "Adversarial Query Expansion"   # M13 — always present in v2.1
prompt_engineering_framework_agentic_spine: "ReAct"
prompt_engineering_framework_structural: "RISE-DX"
bespoke_framework_provenance: |
  # RISE-DX is a bespoke synthesis. Provenance per component:
  # - R (Role)            adapted from RISEN
  # - I (Input)           adapted from RISEN
  # - S (Steps)           adapted from RISEN
  # - E (Expectations)    adapted from RISEN
  # - D (Do/Don't)        adapted from TIDD-EC (Do + Don't pair)
  # - X (eXamples)        adapted from TIDD-EC / CARE (worked examples)
  # Synthesis triggered because the user mandates Spec-Driven Development
  # output conventions (RFC 2119 normative grammar + Gherkin scenarios)
  # which require an explicit Do/Don't grammar layer AND a worked-example
  # layer that no single catalog framework cleanly expresses.
cross_pollination:
  - source_category: "A"
    step_id: "S6.a"
    description: "Hidden-Aspects + Schema-Gap Hypothesis Pass"
  - source_category: "C"
    step_id: "S7.c"
    description: "Pre-Batch and Mid-Batch World-Change Scan (system-version drift)"
constraint_blocks:
  - "0 — Reflection Baseline"
  - "1 — Source Priority Rules"
  - "2 — Temporal Scope"
  - "3 — Output Exclusions"
  - "4 — Spec-Driven Output Grammar (RFC 2119 + Gherkin)"
language: "en"
target_agent: "model-agnostic"
created: "2026-05-02"
version: "1.0"
source_skill: "research-prompt-optimizer v2.1.0"
---

# Research Prompt: Spec-Driven Best Practices for Agent/Research Prompts on Google Jules, Claude Code, and Gemini Deep Research

> **For the executing AI:** This prompt is self-contained. Every method, framework, and constraint you need is defined inline below. You do not need external context, prior training on specific methodologies, or knowledge of the skill that generated this prompt. Read the entire prompt before beginning. The output you produce is **three Specs** — one per target system — each defining what a good prompt looks like across at least five operational aspects, written in the Spec-Driven Development grammar pinned in CONSTRAINT BLOCK 4.

... (I will assume the prompt content is here since we are extracting from memory/prompt)
