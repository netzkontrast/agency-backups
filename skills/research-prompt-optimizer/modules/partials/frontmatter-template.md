# Partial — Frontmatter Template

> The YAML frontmatter at the top of the rendered research-prompt.md
> file. Phase 3 fills the slots from the approved meta-prompt.yaml.

---

## Slot Definitions

```yaml
slots:
  topic:
    type: phase2_fill
    fill_from: "intent.research_question"
    fill_strategy: "first_sentence_max_120_chars"
  slug:
    type: fill_from
    fill_from: "intent.slug"
  research_category:
    type: fill_from
    fill_from: "category"
  research_category_label:
    type: fill_from
    fill_from: "category_full_name"
  methods_list:
    type: fill_from
    fill_from: "selected_methods"
    renders_as: "yaml_list"
  framework_agentic:
    type: literal
    value: "ReAct"
  framework_structural:
    type: fill_from
    fill_from: "framework_structural"
  bespoke_provenance:
    type: fill_from
    fill_from: "bespoke_components"
    required_when: "framework_structural == 'bespoke'"
  cross_pollination_list:
    type: fill_from
    fill_from: "cross_pollination"
  constraint_blocks_list:
    type: fill_from
    fill_from: "constraint_blocks"
  language:
    type: fill_from
    fill_from: "intent.language"
  created:
    type: literal
    value: "{{ now_iso8601 }}"
```

---

## Rendered Output Template

```yaml
---
topic: "{{topic}}"
slug: "{{slug}}"
research_category: "{{research_category}}"
research_category_label: "{{research_category_label}}"
critical_thinking_methods:
{{methods_list_indented}}
prompt_engineering_framework_agentic_spine: "ReAct"
prompt_engineering_framework_structural: "{{framework_structural}}"
{% if bespoke_provenance %}
bespoke_framework_provenance: |
{{bespoke_provenance_indented}}
{% endif %}
cross_pollination:
{{cross_pollination_list_indented}}
constraint_blocks:
{{constraint_blocks_list_indented}}
language: "{{language}}"
target_agent: "model-agnostic"
created: "{{created}}"
version: "1.0"
source_skill: "research-prompt-optimizer v3.2.0"
---
```

Note: the `{% if %}` Jinja-style block is shown for clarity. The
actual render in `render.py` uses pure `str.format_map` (per Q-decision
phase1, no Jinja). Conditional inclusion handled by Python `if/else`
around the format call.
