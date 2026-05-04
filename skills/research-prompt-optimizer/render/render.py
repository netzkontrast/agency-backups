#!/usr/bin/env python3
"""
research-prompt-optimizer · Phase 3 — Render

Reads an approved meta-prompt.yaml + the skill's catalog.yaml + module
files, and emits the final research-prompt_<slug>.md file the user
hands to an external research agent.

Pure stdlib + pyyaml. No Jinja, no string templating engine — slot
substitution uses a simple regex replacer that respects the v3.0
four-type slot system:

  - phase2_fill         → resolved here from meta-prompt.slot_fills
  - phase2_fill_or_runtime → resolved if value present, else preserved
  - agent_runtime_fill  → ALWAYS preserved as {{slot}} for executing agent
  - fill_from           → computed by deterministic per-slot handlers

Usage (CLI):

    python3 render.py meta-prompt.yaml \
        --skill-root /path/to/skill \
        --output-dir /mnt/user-data/outputs

Or programmatically:

    from render import render_meta_prompt
    out_path = render_meta_prompt(
        meta_prompt_yaml=Path("meta-prompt.yaml"),
        skill_root=Path("."),
        output_dir=Path("/mnt/user-data/outputs"),
    )

Author: Michael Schimmer + Claude (research-prompt-optimizer v3.2.0)
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# =============================================================================
# CONSTANTS
# =============================================================================

SCHEMA_VERSION_SUPPORTED = ("2.0", "2.1")
SLOT_PATTERN = re.compile(r"\{\{([a-z_][a-z0-9_]*)\}\}")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
FENCED_RE = re.compile(r"```(?:markdown|yaml)\n(.*?)\n```", re.DOTALL)

# Heading patterns that mark "this is the render template" sections
RENDER_HEADING_RE = re.compile(
    r"^##\s+(Rendered Block|Rendered Output Template|Render Prompt Rendering|Render Output|Rendered Output).*$",
    re.MULTILINE,
)

CATEGORY_FULL_NAMES = {
    "A": "Exploration",
    "B": "Extraction",
    "C": "Lifecycle",
}

LANGUAGE_FULL_NAMES = {
    "en": "English",
    "de": "German",
    "fr": "French",
    "es": "Spanish",
    "it": "Italian",
    "nl": "Dutch",
    "pt": "Portuguese",
}

# Standard partials that are always rendered (regardless of slot_fills)
STANDARD_PARTIALS = [
    "frontmatter-template",
    "meta-header",
    "react-loop-anchored",
    "synthesis-schema",
]


# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class Module:
    """A loaded module: frontmatter + extracted render template."""
    id: str
    type: str  # category | method | framework | replication | cross-pollination | partial | verification
    file_path: Path
    frontmatter: dict
    template: str  # the render template (extracted from fenced block)
    raw_body: str  # full body (after frontmatter) — kept for partials w/o fenced templates


@dataclass
class RenderContext:
    """Everything the renderer needs to know about this run."""
    meta_prompt: dict
    catalog: dict
    skill_root: Path
    modules: dict[str, Module] = field(default_factory=dict)  # id → Module
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


# =============================================================================
# 1. LOADING & PARSING
# =============================================================================


def load_yaml_file(path: Path) -> dict:
    with path.open() as f:
        return yaml.safe_load(f) or {}


def _yaml_inline(value: object) -> str:
    """Serialize a single value for inline YAML use in the frontmatter block.

    Lists render flow-style; strings render double-quoted; numbers
    render bare. Used by the v3.2 provenance frontmatter prefix.
    """
    if isinstance(value, list):
        items = ", ".join(_yaml_inline(v) for v in value)
        return f"[{items}]"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if value is None:
        return "null"
    s = str(value)
    # Quote if the string contains special chars that would change YAML meaning
    if any(c in s for c in ":#[]{},&*!|>'\"%@`") or s != s.strip():
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return f'"{s}"'


def parse_module_file(path: Path) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_text) for a module file."""
    text = path.read_text()
    m = FRONTMATTER_RE.match(text)
    if not m:
        # Partials may have no frontmatter
        return {}, text
    fm = yaml.safe_load(m.group(1)) or {}
    body = text[m.end():]
    return fm, body


def extract_render_template(body: str, module_id: str) -> str:
    """
    Extract the render template from a module body.

    Strategy: look for a `## Rendered ...` H2 heading; if found, take
    the first fenced ```markdown or ```yaml block after it. If no
    rendering heading is found, take the first fenced block in the
    body. If no fenced block exists, return the body as-is (e.g. some
    partials are pure inline templates).
    """
    heading_match = RENDER_HEADING_RE.search(body)
    if heading_match:
        # Slice body from the heading onward
        post_heading = body[heading_match.end():]
        fenced = FENCED_RE.search(post_heading)
        if fenced:
            return fenced.group(1).strip()
        # heading found but no fenced block underneath — fallback
    # Fallback 1: first fenced block anywhere
    fenced = FENCED_RE.search(body)
    if fenced:
        return fenced.group(1).strip()
    # Fallback 2: body as-is (no fenced template, e.g. partials with
    # frontmatter-only content)
    return body.strip()


def load_module(skill_root: Path, rel_path: str, module_id: str) -> Module:
    """Load a module file and parse it into a Module dataclass."""
    full = skill_root / rel_path
    if not full.exists():
        raise FileNotFoundError(f"Module file missing: {rel_path}")
    fm, body = parse_module_file(full)
    template = extract_render_template(body, module_id)
    mtype = fm.get("type", "unknown")
    if rel_path.startswith("modules/partials/"):
        mtype = "partial"
    elif rel_path.startswith("modules/verification/"):
        mtype = "verification"
    elif rel_path.startswith("modules/categories/"):
        mtype = "category"
    elif rel_path.startswith("modules/cross-pollination/"):
        mtype = "cross-pollination"
    return Module(
        id=module_id,
        type=mtype,
        file_path=full,
        frontmatter=fm,
        template=template,
        raw_body=body,
    )


def resolve_module_path(catalog: dict, module_id: str) -> str | None:
    """Find the file path for a module ID by walking the catalog."""
    # Modules block
    modules = catalog.get("modules", {})
    if module_id in modules:
        entry = modules[module_id]
        if isinstance(entry, dict) and "file" in entry:
            return entry["file"]
    # Partials block
    partials = catalog.get("partials", {})
    if module_id in partials:
        entry = partials[module_id]
        if isinstance(entry, dict) and "file" in entry:
            return entry["file"]
    # Verification block
    verif = catalog.get("verification", {})
    if module_id in verif:
        entry = verif[module_id]
        if isinstance(entry, dict) and "file" in entry:
            return entry["file"]
    # Categories block
    cats = catalog.get("categories", {})
    if module_id in cats:
        cat_entry = cats[module_id]
        if isinstance(cat_entry, dict):
            ibm = cat_entry.get("inline_block_module")
            if ibm:
                return f"modules/{ibm}.md"
    # Cross-pollination — files under modules/cross-pollination/<id>.md
    candidate = f"modules/cross-pollination/{module_id}.md"
    if (Path("modules/cross-pollination") / f"{module_id}.md").parent.exists():
        return candidate
    return None


# =============================================================================
# 2. SLOT RESOLUTION
# =============================================================================


def substitute_slots(template: str, slot_values: dict[str, str]) -> str:
    """Replace {{slot_name}} with slot_values[slot_name]; preserve unfilled."""
    def repl(match: re.Match) -> str:
        key = match.group(1)
        if key in slot_values:
            return str(slot_values[key])
        return match.group(0)  # preserve {{slot}} for agent_runtime_fill
    return SLOT_PATTERN.sub(repl, template)


def resolve_phase2_fill_slots(module: Module, ctx: RenderContext) -> dict[str, str]:
    """
    Walk the module's slot definitions and look up phase2_fill values
    in meta-prompt.slot_fills.<module_id>.
    """
    slot_fills = ctx.meta_prompt.get("slot_fills", {}) or {}
    # The meta-prompt sometimes uses module IDs as-is, sometimes lowercased.
    # Try both.
    module_fills = slot_fills.get(module.id) or slot_fills.get(module.id.lower()) or {}
    if not isinstance(module_fills, dict):
        module_fills = {}

    out: dict[str, str] = {}
    slots = module.frontmatter.get("slots") or {}
    if not isinstance(slots, dict):
        return out

    for slot_name, slot_spec in slots.items():
        if not isinstance(slot_spec, dict):
            continue
        slot_type = slot_spec.get("type")
        if slot_type == "phase2_fill":
            if slot_name in module_fills:
                out[slot_name] = str(module_fills[slot_name]).rstrip()
            else:
                # Not filled but required → record as warning
                if slot_spec.get("required"):
                    ctx.warnings.append(
                        f"phase2_fill slot '{slot_name}' in {module.id} required but not filled"
                    )
        elif slot_type == "phase2_fill_or_runtime":
            if slot_name in module_fills:
                out[slot_name] = str(module_fills[slot_name]).rstrip()
            # else: preserve as {{slot}} for runtime
        # agent_runtime_fill: always preserve → don't add to out
        # fill_from: handled separately below
    return out


# =============================================================================
# 3. fill_from HANDLERS — deterministic computed slots
# =============================================================================


def fillfrom_active_method_anchors(ctx: RenderContext) -> str:
    """
    Render the active method anchor table (used by react.md and
    react-loop-anchored.md). Returns a Markdown table.
    """
    methods = ctx.meta_prompt.get("modules", {}).get("methods", []) or []
    rows = ["| Anchor   | Method                          | When to choose                        |",
            "|----------|---------------------------------|---------------------------------------|"]
    for mid in methods:
        mod = ctx.modules.get(mid)
        if not mod:
            continue
        full = mod.frontmatter.get("full_name", mid)
        # Strip parenthetical from full_name for cleaner display
        full_short = re.sub(r"\s*\(.*\)\s*$", "", full)
        anchor = mod.frontmatter.get("short_anchor", mid).split("-")[0]
        when = mod.frontmatter.get("when_to_choose_short", "—")
        rows.append(f"| [{anchor}] | {full_short:<31} | {when:<37} |")
    return "\n".join(rows)


def fillfrom_cb_restatement_block(ctx: RenderContext) -> str:
    """Render the CB restatement bullet list (m2-restatement)."""
    cbs = ctx.meta_prompt.get("constraint_blocks", []) or []
    bullets = []
    for cb in cbs:
        cb_id = cb.get("id")
        title = cb.get("title", "")
        bullets.append(
            f"- **CONSTRAINT BLOCK {cb_id} — {title}:** "
            f"[Paste the full text of the block here. Do not paraphrase.]"
        )
    return "\n".join(bullets)


def fillfrom_method_restatement_block(ctx: RenderContext) -> str:
    """Render the method restatement bullet list (m2-restatement). M13 first."""
    methods = ctx.meta_prompt.get("modules", {}).get("methods", []) or []
    # Reorder: M13 always first
    ordered = ["M13"] + [m for m in methods if m != "M13"]
    bullets = []
    for mid in ordered:
        mod = ctx.modules.get(mid)
        if not mod:
            continue
        full = mod.frontmatter.get("full_name", mid)
        full_short = re.sub(r"\s*\(.*\)\s*$", "", full)
        bullets.append(
            f"- **Method: {full_short}** — "
            f"[Paste the \"How to apply\" bullet list verbatim.]"
        )
    return "\n".join(bullets)


def fillfrom_components_render_block(ctx: RenderContext) -> str:
    """Bespoke synthesis: render component bullets from `components` slot."""
    components = (
        ctx.meta_prompt.get("slot_fills", {}).get("bespoke", {}).get("components")
        or ctx.meta_prompt.get("modules", {}).get("bespoke_components")
        or []
    )
    if not isinstance(components, list):
        return ""
    bullets = []
    for c in components:
        if not isinstance(c, dict):
            continue
        letter = c.get("letter", "?")
        name = c.get("name", "?")
        defn = c.get("definition", "?")
        bullets.append(f"- **{letter} — {name}**: {defn}")
    return "\n".join(bullets)


def fillfrom_provenance_render_block(ctx: RenderContext) -> str:
    """Bespoke synthesis: render provenance lines from `components`."""
    components = (
        ctx.meta_prompt.get("slot_fills", {}).get("bespoke", {}).get("components")
        or ctx.meta_prompt.get("modules", {}).get("bespoke_components")
        or []
    )
    if not isinstance(components, list):
        return ""
    lines = []
    for c in components:
        if not isinstance(c, dict):
            continue
        letter = c.get("letter", "?")
        src = c.get("source_framework", "?")
        lines.append(f"- Component {letter} is adapted from the {src} framework.")
    return "\n".join(lines)


def fillfrom_active_constraint_blocks_list(ctx: RenderContext) -> str:
    """Numbered list of active CB titles for meta-header."""
    cbs = ctx.meta_prompt.get("constraint_blocks", []) or []
    lines = []
    for cb in cbs:
        lines.append(f"  {cb.get('id')}. {cb.get('title', '')}")
    return "\n".join(lines)


def fillfrom_active_methods_list(ctx: RenderContext) -> str:
    """Markdown table of active methods (for meta-header)."""
    return fillfrom_active_method_anchors(ctx)


def fillfrom_methods_list_indented(ctx: RenderContext) -> str:
    """YAML-indented list of methods for the rendered prompt's frontmatter."""
    methods = ctx.meta_prompt.get("modules", {}).get("methods", []) or []
    lines = []
    for mid in methods:
        mod = ctx.modules.get(mid)
        full = mod.frontmatter.get("full_name", mid) if mod else mid
        full_short = re.sub(r"\s*\(.*\)\s*$", "", full)
        lines.append(f'  - "{mid} {full_short}"')
    return "\n".join(lines)


def fillfrom_constraint_blocks_list_indented(ctx: RenderContext) -> str:
    cbs = ctx.meta_prompt.get("constraint_blocks", []) or []
    lines = []
    for cb in cbs:
        lines.append(f'  - "{cb.get("id")} — {cb.get("title", "")}"')
    return "\n".join(lines)


def fillfrom_cross_pollination_list_indented(ctx: RenderContext) -> str:
    cps = ctx.meta_prompt.get("modules", {}).get("cross_pollination", []) or []
    lines = []
    for i, cp in enumerate(cps):
        if not isinstance(cp, dict):
            continue
        src = cp.get("source_category", "?")
        mod = cp.get("module", "?")
        title = cp.get("injected_step_title", "")
        lines.append(f'  - source_category: "{src}"')
        lines.append(f'    module: "{mod}"')
        if title:
            lines.append(f'    title: "{title}"')
    return "\n".join(lines)


def fillfrom_bespoke_provenance_indented(ctx: RenderContext) -> str:
    """Only emits content if framework_structural == 'bespoke'."""
    fs = ctx.meta_prompt.get("modules", {}).get("framework_structural")
    if fs != "bespoke":
        return ""
    components = ctx.meta_prompt.get("modules", {}).get("bespoke_components") or []
    if not components:
        return ""
    lines = ["bespoke_framework_provenance: |"]
    for c in components:
        if not isinstance(c, dict):
            continue
        letter = c.get("letter", "?")
        src = c.get("source_framework", "?")
        lines.append(f"  Component {letter} is adapted from the {src} framework.")
    return "\n".join(lines)


def fillfrom_items_render_block(ctx: RenderContext) -> str:
    """m3-batch: render numbered list of batch items."""
    items = (
        ctx.meta_prompt.get("slot_fills", {})
        .get("m3-batch", {})
        .get("items")
    )
    if isinstance(items, str):
        return items  # already pre-formatted
    if isinstance(items, list):
        return "\n".join(f"{i+1}. {it}" for i, it in enumerate(items))
    return ""


def fillfrom_iteration_steps_render_block(ctx: RenderContext) -> str:
    """m3-batch: render iteration steps as numbered list."""
    steps = (
        ctx.meta_prompt.get("slot_fills", {})
        .get("m3-batch", {})
        .get("iteration_steps")
    )
    if isinstance(steps, str):
        return steps
    if isinstance(steps, list):
        return "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))
    return ""


def fillfrom_output_schema_render_block(ctx: RenderContext) -> str:
    """m3-batch: render output-schema fields as bullets w/ [...] placeholders."""
    schema = (
        ctx.meta_prompt.get("slot_fills", {})
        .get("m3-batch", {})
        .get("output_schema_per_iteration")
    )
    if isinstance(schema, str):
        return schema
    if isinstance(schema, list):
        return "\n".join(f"- {field}: [...]" for field in schema)
    return ""


def fillfrom_category_specific_main_body(ctx: RenderContext) -> str:
    """
    Synthesis schema's category-specific section header. Returns
    the heading text the agent fills under.
    """
    cat = ctx.meta_prompt.get("routing", {}).get("category", "B")
    return {
        "A": "Hypothesis Tree (Category A — Exploration)",
        "B": "Output Matrix (Category B — Extraction)",
        "C": "Periodic Brief (Category C — Lifecycle)",
    }.get(cat, "Main Findings")


def fillfrom_category_specific_directive(ctx: RenderContext) -> str:
    """Brief instruction to the agent for the category-specific section."""
    cat = ctx.meta_prompt.get("routing", {}).get("category", "B")
    return {
        "A": (
            "Render the surviving hypothesis tree from your exploration. "
            "For each top-level hypothesis: confidence band, supporting "
            "evidence, falsification attempts, and open child hypotheses."
        ),
        "B": (
            "Render the comparison/extraction matrix per the Expectations "
            "section. Every row gets the full per-iteration schema; gaps "
            "marked explicitly as 'not found — [reason]' rather than "
            "silently omitted."
        ),
        "C": (
            "Render the periodic brief: state-of-the-question this session, "
            "what changed since last session (cross-session diff), "
            "world-change events distinct from source-disagreement events, "
            "decayed assumptions, and the next-session roadmap."
        ),
    }.get(cat, "Render the main findings.")


def fillfrom_world_change_log_section_or_empty(ctx: RenderContext) -> str:
    """Conditional: only Cat-C renders the World-Change Log section."""
    cat = ctx.meta_prompt.get("routing", {}).get("category", "B")
    if cat != "C":
        return ""
    return (
        "### World-Change Log (Category C only)\n\n"
        "Distinct from contradictions: events where the *world itself* "
        "moved between sessions. Each entry: date observed, what changed, "
        "evidence source, downstream conclusions affected.\n"
    )


# Registry: slot name → handler function
FILL_FROM_HANDLERS: dict[str, callable] = {
    "active_method_anchors": fillfrom_active_method_anchors,
    "active_methods_list": fillfrom_active_methods_list,
    "active_methods_table": fillfrom_active_method_anchors,  # alias
    "active_constraint_blocks_list": fillfrom_active_constraint_blocks_list,
    "cb_restatement_block": fillfrom_cb_restatement_block,
    "method_restatement_block": fillfrom_method_restatement_block,
    "components_render_block": fillfrom_components_render_block,
    "provenance_render_block": fillfrom_provenance_render_block,
    "methods_list_indented": fillfrom_methods_list_indented,
    "constraint_blocks_list_indented": fillfrom_constraint_blocks_list_indented,
    "cross_pollination_list_indented": fillfrom_cross_pollination_list_indented,
    "bespoke_provenance_indented": fillfrom_bespoke_provenance_indented,
    "category_specific_main_body": fillfrom_category_specific_main_body,
    "category_specific_main_body_content_directive": fillfrom_category_specific_directive,
    "world_change_log_section_or_empty": fillfrom_world_change_log_section_or_empty,
    "items_render_block": fillfrom_items_render_block,
    "iteration_steps_render_block": fillfrom_iteration_steps_render_block,
    "output_schema_render_block": fillfrom_output_schema_render_block,
}


def resolve_fill_from_slots(ctx: RenderContext) -> dict[str, str]:
    """Compute all fill_from slots once, cached for global substitution."""
    out = {}
    for slot_name, handler in FILL_FROM_HANDLERS.items():
        try:
            out[slot_name] = handler(ctx)
        except Exception as e:
            ctx.warnings.append(f"fill_from handler '{slot_name}' raised: {e}")
            out[slot_name] = f"<<error: {slot_name}>>"
    return out


# =============================================================================
# 4. CONTEXT-WIDE SLOTS (computed from intent + meta-prompt globals)
# =============================================================================


def collect_all_phase2_fills(ctx: RenderContext) -> dict[str, str]:
    """
    Flatten every phase2_fill value across all modules into a single
    dict. This makes per-module fills visible to other modules that
    reference the same slot name (e.g. M13.orthogonal_lens needed
    inside final-checklist).
    """
    out: dict[str, str] = {}
    slot_fills = ctx.meta_prompt.get("slot_fills", {}) or {}
    if not isinstance(slot_fills, dict):
        return out
    for module_id, fills in slot_fills.items():
        if not isinstance(fills, dict):
            continue
        for slot_name, value in fills.items():
            if value is None:
                continue
            # First-write-wins for cross-module collisions; warn if
            # we see a divergent re-fill.
            sval = str(value).rstrip()
            if slot_name in out and out[slot_name] != sval:
                ctx.warnings.append(
                    f"slot '{slot_name}' has divergent values across modules "
                    f"(keeping first-seen)"
                )
                continue
            out.setdefault(slot_name, sval)
    return out


def compute_global_slots(ctx: RenderContext) -> dict[str, str]:
    """
    Slots that don't belong to a specific module — they're filled from
    the meta-prompt's global fields (intent_ref-derived, routing, etc.).
    """
    mp = ctx.meta_prompt
    intent_topic = (
        mp.get("slot_fills", {}).get("frontmatter", {}).get("topic")
        or mp.get("topic")
        or "Untitled Research"
    )
    category = mp.get("routing", {}).get("category", "?")
    cat_label = mp.get("routing", {}).get(
        "category_label", CATEGORY_FULL_NAMES.get(category, "?")
    )
    fs = mp.get("modules", {}).get("framework_structural", "risen")
    fs_label = fs.upper() if fs != "bespoke" else "Bespoke Synthesis"
    language = mp.get("language", "en")
    lang_full = LANGUAGE_FULL_NAMES.get(language, language)

    return {
        "topic": intent_topic,
        "slug": mp.get("slug", "untitled"),
        "research_category": category,
        "research_category_label": cat_label,
        "category_label": cat_label,
        "framework_structural": fs,
        "framework_structural_label": fs_label,
        "language": language,
        "user_language": language,
        "user_language_full": lang_full,
        "created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        # research_question and unpacked_question (for meta-header)
        "research_question": (
            mp.get("slot_fills", {}).get("frontmatter", {}).get("research_question")
            or mp.get("research_question")
            or intent_topic
        ),
        "unpacked_question": (
            mp.get("slot_fills", {}).get("frontmatter", {}).get("unpacked_question", "")
        ),
        "output_format_directive": (
            mp.get("slot_fills", {}).get("frontmatter", {}).get(
                "output_format_directive", "(see Synthesis schema)"
            )
        ),
    }


# =============================================================================
# 5. COMPOSITION — assemble the final markdown
# =============================================================================


def render_module(module: Module, ctx: RenderContext, global_slots: dict[str, str]) -> str:
    """
    Render a single module's template by resolving its slots.
    """
    phase2_slots = resolve_phase2_fill_slots(module, ctx)
    fill_from_slots = resolve_fill_from_slots(ctx)
    # Merge precedence: global < fill_from < phase2_fill < module_specific_overrides
    merged = {}
    merged.update(global_slots)
    merged.update(fill_from_slots)
    merged.update(phase2_slots)
    return substitute_slots(module.template, merged)


def compose_frontmatter(ctx: RenderContext, global_slots: dict[str, str]) -> str:
    """
    Compose the rendered prompt's YAML frontmatter.

    Note: the frontmatter-template module body contains Jinja-style
    `{% if bespoke_provenance %}` blocks for clarity — Phase 3 handles
    the conditional in code rather than via a templating engine.
    """
    mod = ctx.modules.get("frontmatter-template")
    if not mod:
        return "---\nerror: frontmatter-template module missing\n---\n"
    rendered = render_module(mod, ctx, global_slots)
    # Strip Jinja conditional markers; emit bespoke_provenance line only
    # when framework_structural == 'bespoke'.
    fs = ctx.meta_prompt.get("modules", {}).get("framework_structural")
    if fs == "bespoke":
        # Strip just the {% %} markers, keep the inner block content
        rendered = re.sub(r"\{%\s*if\s+bespoke_provenance\s*%\}\n?", "", rendered)
        rendered = re.sub(r"\{%\s*endif\s*%\}\n?", "", rendered)
    else:
        # Drop the entire conditional block including content
        rendered = re.sub(
            r"\{%\s*if\s+bespoke_provenance\s*%\}.*?\{%\s*endif\s*%\}\n?",
            "",
            rendered,
            flags=re.DOTALL,
        )
    return rendered


def compose_language_warning(ctx: RenderContext, global_slots: dict[str, str]) -> str:
    """Compose the language warning block (empty if language=='en')."""
    if ctx.meta_prompt.get("language", "en") == "en":
        return ""
    mod = ctx.modules.get("language-warning")
    if not mod:
        return ""
    # Use the second fenced block (Phase 3 render variant)
    blocks = FENCED_RE.findall(mod.raw_body)
    template = blocks[-1].strip() if blocks else mod.template
    return substitute_slots(template, global_slots)


def compose_meta_header(ctx: RenderContext, global_slots: dict[str, str]) -> str:
    """
    The meta-header is itself a partial that pulls in 4 sub-blocks:
    language-warning (conditional), category, react, structural.
    Resolve them in advance and inject as slots.
    """
    mod = ctx.modules.get("meta-header")
    if not mod:
        return "<!-- meta-header partial missing -->"
    # Sub-block resolution
    cat = ctx.meta_prompt.get("routing", {}).get("category", "B")
    cat_module_id_map = {"A": "A", "B": "B", "C": "C"}
    cat_id = cat_module_id_map.get(cat, "B")
    cat_module = ctx.modules.get(cat_id)
    cat_block = render_module(cat_module, ctx, global_slots) if cat_module else ""
    react_module = ctx.modules.get("react")
    react_block = render_module(react_module, ctx, global_slots) if react_module else ""
    fs = ctx.meta_prompt.get("modules", {}).get("framework_structural", "risen")
    structural_module = ctx.modules.get(fs)
    structural_block = (
        render_module(structural_module, ctx, global_slots) if structural_module else ""
    )
    lang_warning_block = compose_language_warning(ctx, global_slots)

    sub_slots = {
        "category_block": cat_block,
        "react_block": react_block,
        "structural_block": structural_block,
        "language_warning_block_or_empty": lang_warning_block,
    }
    merged = {**global_slots, **sub_slots}
    return substitute_slots(mod.template, merged)


def compose_constraint_blocks(ctx: RenderContext, global_slots: dict[str, str]) -> str:
    """
    Render CB-0 (from m0-reflection module) + CB-1..N (from
    meta-prompt.constraint_blocks authored content).
    """
    parts = ["## Constraint Blocks", ""]
    cbs = ctx.meta_prompt.get("constraint_blocks", []) or []

    for cb in cbs:
        cb_id = cb.get("id")
        title = cb.get("title", "")
        source = cb.get("source", "authored")
        if source == "module":
            module_ref = cb.get("module_ref")
            mod = ctx.modules.get(module_ref) if module_ref else None
            if mod:
                parts.append(render_module(mod, ctx, global_slots))
            else:
                parts.append(f"<!-- CB {cb_id} module {module_ref} missing -->")
        else:
            content = cb.get("content", "").rstrip()
            parts.append(f"### CONSTRAINT BLOCK {cb_id} — {title}\n\n{content}")
        parts.append("")  # blank line between

    return "\n".join(parts).rstrip() + "\n"


def compose_methods_section(ctx: RenderContext, global_slots: dict[str, str]) -> str:
    """Render each active method's body block."""
    methods = ctx.meta_prompt.get("modules", {}).get("methods", []) or []
    parts = ["## Critical-Thinking Methods (Always Active)", ""]
    for mid in methods:
        mod = ctx.modules.get(mid)
        if not mod:
            parts.append(f"<!-- method {mid} missing -->")
            continue
        parts.append(render_module(mod, ctx, global_slots))
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def compose_replication_section(ctx: RenderContext, global_slots: dict[str, str]) -> str:
    """
    Render the replication blocks: M2 restatement template + M3 batch
    framing (if active) + cross-pollination blocks.
    """
    rep = ctx.meta_prompt.get("modules", {}).get("replication", []) or []
    cps = ctx.meta_prompt.get("modules", {}).get("cross_pollination", []) or []

    parts = ["## Steps and Replication Mechanisms", ""]

    # M2 restatement template
    m2 = ctx.modules.get("m2-restatement-checkpoint")
    if m2:
        parts.append("### Per-Step Restatement Checkpoint Template")
        parts.append("")
        parts.append(
            "Apply this template at the start of every step / iteration:"
        )
        parts.append("")
        parts.append(render_module(m2, ctx, global_slots))
        parts.append("")

    # M3 batch (if present)
    if "m3-batch" in rep:
        m3 = ctx.modules.get("m3-batch")
        if m3:
            parts.append("### Batch Procedures")
            parts.append("")
            parts.append(render_module(m3, ctx, global_slots))
            parts.append("")

    # Cross-pollination blocks
    if cps:
        parts.append("### Cross-Pollination Steps")
        parts.append("")
        for cp in cps:
            if not isinstance(cp, dict):
                continue
            mid = cp.get("module")
            mod = ctx.modules.get(mid)
            if not mod:
                parts.append(f"<!-- cross-pollination {mid} missing -->")
                continue
            parts.append(render_module(mod, ctx, global_slots))
            parts.append("")

    return "\n".join(parts).rstrip() + "\n"


def compose_pre_synthesis(ctx: RenderContext, global_slots: dict[str, str]) -> str:
    mod = ctx.modules.get("m4-pre-synthesis")
    if not mod:
        return "<!-- m4-pre-synthesis missing -->"
    return render_module(mod, ctx, global_slots)


def compose_synthesis(ctx: RenderContext, global_slots: dict[str, str]) -> str:
    mod = ctx.modules.get("synthesis-schema")
    if not mod:
        return "<!-- synthesis-schema missing -->"
    return render_module(mod, ctx, global_slots)


def compose_final_checklist(ctx: RenderContext, global_slots: dict[str, str]) -> str:
    mod = ctx.modules.get("final-checklist")
    if not mod:
        return "<!-- final-checklist missing -->"
    return render_module(mod, ctx, global_slots)


# =============================================================================
# 6. MAIN RENDER PIPELINE
# =============================================================================


def collect_active_module_ids(meta_prompt: dict) -> list[tuple[str, str]]:
    """
    Return list of (module_id, role) for every module that needs loading.
    Roles are informational; the renderer handles each role specifically.
    """
    out: list[tuple[str, str]] = []
    mods = meta_prompt.get("modules", {})

    # Frameworks
    if mods.get("framework_agentic_spine"):
        out.append((mods["framework_agentic_spine"], "framework_agentic"))
    if mods.get("framework_structural"):
        fs = mods["framework_structural"]
        if fs == "bespoke":
            out.append(("synthesis", "framework_structural"))
        else:
            out.append((fs, "framework_structural"))

    # Methods
    for m in mods.get("methods", []) or []:
        out.append((m, "method"))

    # Replication
    for r in mods.get("replication", []) or []:
        out.append((r, "replication"))

    # Cross-pollination
    for cp in mods.get("cross_pollination", []) or []:
        if isinstance(cp, dict) and cp.get("module"):
            out.append((cp["module"], "cross_pollination"))

    # Category block
    cat = meta_prompt.get("routing", {}).get("category")
    if cat:
        out.append((cat, "category"))

    # CB-0 module (from constraint_blocks where source=='module')
    for cb in meta_prompt.get("constraint_blocks", []) or []:
        if cb.get("source") == "module" and cb.get("module_ref"):
            out.append((cb["module_ref"], "constraint_block_module"))

    # Standard partials
    for p in STANDARD_PARTIALS:
        out.append((p, "partial"))

    # Verification
    out.append(("final-checklist", "verification"))

    # Language warning (conditional)
    if meta_prompt.get("language", "en") != "en":
        out.append(("language-warning", "partial"))

    # Dedupe preserving order
    seen = set()
    deduped = []
    for mid, role in out:
        if mid not in seen:
            seen.add(mid)
            deduped.append((mid, role))
    return deduped


def load_all_modules(ctx: RenderContext) -> None:
    """Load every module referenced by the meta-prompt."""
    targets = collect_active_module_ids(ctx.meta_prompt)
    for mid, role in targets:
        rel = resolve_module_path(ctx.catalog, mid)
        if not rel:
            ctx.errors.append(f"Module not found in catalog: {mid} (role: {role})")
            continue
        try:
            mod = load_module(ctx.skill_root, rel, mid)
            ctx.modules[mid] = mod
        except Exception as e:
            ctx.errors.append(f"Failed to load {mid} ({rel}): {e}")


def validate(ctx: RenderContext) -> None:
    """Pre-render integrity check. Append issues to ctx.errors."""
    mp = ctx.meta_prompt

    # Schema version
    sv = str(mp.get("schema_version", ""))
    if sv not in SCHEMA_VERSION_SUPPORTED:
        ctx.errors.append(
            f"Unsupported schema_version '{sv}' (expected one of {SCHEMA_VERSION_SUPPORTED})"
        )

    # Approval gate
    if not mp.get("approved"):
        ctx.errors.append("meta-prompt.approved != true — render refused")

    # Mandatories
    expected_mandatories = (
        mp.get("verification", {}).get("mandatories_present", [])
        or ["react", "m0-reflection", "m1-constraint-blocks",
            "m2-restatement-checkpoint", "m4-pre-synthesis", "M13"]
    )
    all_active = []
    mods = mp.get("modules", {})
    if mods.get("framework_agentic_spine"):
        all_active.append(mods["framework_agentic_spine"])
    if mods.get("framework_structural") and mods["framework_structural"] != "bespoke":
        all_active.append(mods["framework_structural"])
    all_active.extend(mods.get("methods", []) or [])
    all_active.extend(mods.get("replication", []) or [])
    for m in expected_mandatories:
        if m not in all_active:
            ctx.errors.append(f"Mandatory module missing: {m}")

    # Cross-pollination count
    cps = mods.get("cross_pollination", []) or []
    if len(cps) != 2:
        ctx.warnings.append(
            f"Cross-pollination count = {len(cps)} (Phase-2 spec expects exactly 2)"
        )


def assemble_final_document(ctx: RenderContext, global_slots: dict[str, str]) -> str:
    """Compose the full research-prompt.md per Schema 3 ordering."""
    sections = []

    # 1. YAML frontmatter
    fm = compose_frontmatter(ctx, global_slots)
    if not fm.startswith("---"):
        fm = "---\n" + fm
    if not fm.rstrip().endswith("---"):
        fm = fm.rstrip() + "\n---\n"
    sections.append(fm.rstrip() + "\n")

    # 2. Title + executing-AI callout (lives inside meta-header partial)
    # 3. Meta-Header (composes 1+2 already)
    sections.append(compose_meta_header(ctx, global_slots))

    # 4. Research Objective (fits inside meta-header in v3.0)
    # — handled by meta-header

    # 5. Constraint Blocks
    sections.append(compose_constraint_blocks(ctx, global_slots))

    # 6. Methods section
    sections.append(compose_methods_section(ctx, global_slots))

    # 7. Structural framework body — already in meta-header

    # 8-10. Steps + replication + batch
    sections.append(compose_replication_section(ctx, global_slots))

    # 11. Pre-Synthesis Integrity Check
    sections.append(compose_pre_synthesis(ctx, global_slots))

    # 12. Synthesis schema
    sections.append(compose_synthesis(ctx, global_slots))

    # 13. Self-verification checklist
    sections.append(compose_final_checklist(ctx, global_slots))

    # 14. End marker
    sections.append("---\n\n*End of research prompt — generated by "
                    f"research-prompt-optimizer v3.2.0 at {global_slots['created']}.*")

    # Join with double-newline for clean section separation
    return "\n\n".join(s.rstrip() for s in sections) + "\n"


def post_render_check(rendered: str, ctx: RenderContext) -> None:
    """Final integrity check on the rendered document."""
    # Find unfilled {{slot}} placeholders
    unfilled = SLOT_PATTERN.findall(rendered)
    # Filter out agent_runtime_fill slots (legitimate to remain unfilled).
    # We track which slots are agent_runtime by walking active modules.
    runtime_slots = set()
    for mod in ctx.modules.values():
        slots = mod.frontmatter.get("slots") or {}
        if isinstance(slots, dict):
            for sk, sv in slots.items():
                if isinstance(sv, dict) and sv.get("type") == "agent_runtime_fill":
                    runtime_slots.add(sk)
    leaked = [s for s in unfilled if s not in runtime_slots]
    if leaked:
        unique_leaked = sorted(set(leaked))
        ctx.warnings.append(
            f"Unfilled non-runtime slots in rendered output: {unique_leaked}"
        )


def auto_fill_m3_batch_from_batches(ctx: RenderContext) -> None:
    """
    Convenience: if slot_fills.m3-batch is empty/missing but the
    meta-prompt declares a domain batch in batches[], auto-fill the
    m3-batch slots from that batch entry. Phase 2 may emit either form.
    """
    slot_fills = ctx.meta_prompt.setdefault("slot_fills", {})
    if not isinstance(slot_fills, dict):
        return
    existing = slot_fills.get("m3-batch") or {}
    if isinstance(existing, dict) and existing:
        return  # already populated by Phase 2
    batches = ctx.meta_prompt.get("batches", []) or []
    domain_batches = [b for b in batches if isinstance(b, dict) and not b.get("standard")]
    if not domain_batches:
        return
    db = domain_batches[0]
    items = db.get("items") or []
    schema = db.get("output_schema_per_iteration") or []
    iteration_steps = [
        "Apply M13 Adversarial Query Expansion to the item.",
        "Apply each category-default method (M06, M07, M08, M12 etc.) "
        "to the item per its protocol.",
        "Populate the per-iteration output schema below.",
    ]
    slot_fills["m3-batch"] = {
        "batch_name": db.get("name", "Per-Item Analysis"),
        "cardinality": db.get("cardinality", "?"),
        "items": items,                       # native list — handler renders
        "iteration_steps": iteration_steps,   # native list — handler renders
        "output_schema_per_iteration": schema,  # native list — handler renders
    }


def render_meta_prompt(
    meta_prompt_yaml: Path,
    skill_root: Path,
    output_dir: Path,
) -> Path:
    """Render a meta-prompt.yaml to a research-prompt_<slug>.md file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    meta_prompt = load_yaml_file(meta_prompt_yaml)
    catalog = load_yaml_file(skill_root / "catalog.yaml")
    ctx = RenderContext(
        meta_prompt=meta_prompt, catalog=catalog, skill_root=skill_root
    )

    validate(ctx)
    if ctx.errors:
        msg = "Render aborted due to validation errors:\n"
        for e in ctx.errors:
            msg += f"  ✗ {e}\n"
        raise ValueError(msg)

    load_all_modules(ctx)
    if ctx.errors:
        msg = "Render aborted due to module-load errors:\n"
        for e in ctx.errors:
            msg += f"  ✗ {e}\n"
        raise ValueError(msg)

    # Phase-2 → Phase-3 bridge: derive m3-batch slot_fills from
    # batches[] if Phase 2 didn't write them explicitly.
    auto_fill_m3_batch_from_batches(ctx)

    global_slots = compute_global_slots(ctx)
    # Cross-module phase2_fill flatten — makes e.g. M13.orthogonal_lens
    # visible to final-checklist.md
    cross_module_fills = collect_all_phase2_fills(ctx)
    global_slots.update(cross_module_fills)
    rendered = assemble_final_document(ctx, global_slots)
    post_render_check(rendered, ctx)

    # K6: append-only versioning. Resolve next free path; if a previous
    # rendered file exists, link it via previous_version in the
    # frontmatter provenance block we prepend below.
    slug = meta_prompt.get("slug", "untitled")
    try:
        # Local import keeps render.py functional without io_helpers
        # for environments that haven't installed the helper module.
        from io_helpers import next_versioned_path, make_provenance
        out_path, rev_count, prev = next_versioned_path(
            output_dir, slug, "rendered", "md"
        )
        # Prepend a v3.2 provenance frontmatter block. The body
        # already carries module-level frontmatter via the
        # frontmatter-template module; this v3.2 block sits ABOVE
        # that one and carries the normalised provenance fields.
        from datetime import datetime, timezone
        now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
        upstream_prov = meta_prompt.get("provenance", {}) or {}
        prov = make_provenance(
            timestamp=now_iso,
            skill_version=upstream_prov.get("skill_version", "3.2.0"),
            phase="phase3",
            slug=slug,
            output_filename=out_path.name,
            category_signal=upstream_prov.get("category_signal"),
            selected_methods=upstream_prov.get("selected_methods"),
            selected_framework_structural=upstream_prov.get("selected_framework_structural"),
            cross_pollination_pair=upstream_prov.get("cross_pollination_pair"),
            previous_version=prev.name if prev is not None else None,
            revision_count=rev_count,
        )
        prov["intent_ref"] = meta_prompt.get("intent_ref")
        prov["meta_prompt_ref"] = meta_prompt_yaml.name
        # Drop None values to keep the frontmatter clean
        prov = {k: v for k, v in prov.items() if v is not None}
        prov_block = (
            "---\n"
            "schema_version: \"3.1\"\n"
            "schema: research-prompt-render\n"
            "provenance:\n"
            + "\n".join(f"  {k}: {_yaml_inline(v)}" for k, v in prov.items())
            + "\n"
            f"language: {_yaml_inline(meta_prompt.get('language', 'en'))}\n"
            "target_agent: model-agnostic\n"
            "---\n\n"
        )
        rendered = prov_block + rendered
    except ImportError:
        # io_helpers not on path — fall back to non-versioned single-file
        # write. Surface as warning so caller knows provenance is missing.
        out_path = output_dir / f"research-prompt_{slug}.md"
        ctx.warnings.append(
            "io_helpers unavailable; rendered without v3.2 provenance frontmatter "
            "and without versioning"
        )

    out_path.write_text(rendered)

    # Print warnings to stderr for visibility
    if ctx.warnings:
        sys.stderr.write("Render warnings:\n")
        for w in ctx.warnings:
            sys.stderr.write(f"  ⚠ {w}\n")

    return out_path


# =============================================================================
# CLI
# =============================================================================


def cli() -> None:
    parser = argparse.ArgumentParser(
        description="Render an approved meta-prompt.yaml to a final research-prompt.md."
    )
    parser.add_argument("meta_prompt", type=Path, help="Path to meta-prompt.yaml")
    parser.add_argument(
        "--skill-root",
        type=Path,
        default=Path.cwd(),
        help="Path to skill root (containing catalog.yaml + modules/)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("/mnt/user-data/outputs"),
        help="Output directory for the rendered research-prompt.md",
    )
    args = parser.parse_args()

    out = render_meta_prompt(
        meta_prompt_yaml=args.meta_prompt,
        skill_root=args.skill_root,
        output_dir=args.output_dir,
    )
    print(f"Rendered: {out}")


if __name__ == "__main__":
    cli()
