# Partial — Language Warning Block (Q1 v1.1)

> Prepended to the Plan-View in Phase 2.8 when `intent.language != "en"`.
>
> Also injected as a callout into the rendered research prompt itself
> (Phase 3) so the executing AI is aware of the EN/DE mix it will see.

---

## When Injected

`if intent.language != "en"`. For `intent.language == "en"`, this
partial is skipped entirely.

## Slot Definition

```yaml
slots:
  user_language:
    type: fill_from
    fill_from: "intent.language"
    description: "ISO-639-1 code, e.g. 'de'"
```

---

## Plan-View Rendering (in Phase 2.8)

```markdown
⚠ LANGUAGE NOTE — Plan View

Templates in this skill are English-only in v3.0. Your `intent.language`
is `{{user_language}}`, so the rendered research prompt will mix:

  · {{user_language_full}} prose: research objective, framing, your
    custom Constraint Block content, audience descriptions
  · English template anchors: method names ("Method: Falsification"),
    framework section headers ("R — Role", "I — Input"), self-
    verification checklist items, ReAct loop template ("Reason →
    Act → Observe")

This mix is intentional — English template anchors prevent semantic
drift in restatement loops (Replication Mechanism M2). Translation of
anchor names would break their cross-reference reliability.

If you want a fully {{user_language_full}}-language prompt, abort
Phase 2 and request DE-template support in a future iteration of this
skill (v3.1+ plan).

To proceed with the EN/DE mix as documented: choose "Approve" in the
upcoming Plan-View approval question.
```

`{{user_language_full}}` is a derived slot Phase 2 maps from the ISO
code: `de → German · fr → French · es → Spanish · it → Italian · ...`.
For unknown codes, fall back to the literal code.

---

## Render Prompt Rendering (in Phase 3)

When the rendered research prompt is composed, include a brief callout
just under the title (Phase 3 assembly order step 2):

```markdown
> **Note for the executing agent:** This prompt mixes {{user_language_full}}
> prose with English method/framework anchors (e.g. "Method:
> Falsification", "R — Role"). This is intentional — keep English
> anchor strings verbatim in restatement checkpoints. Translate
> prose freely; never translate anchor names.
```

---

## Why This Exists

User mandate Q1 (v1.1): **EN templates only**. The DE warning is the
honesty gate — the user sees up front that they will get a mixed-
language prompt, and the executing agent sees a directive to keep
anchors verbatim.

This is cheaper than building a parallel `modules-de/` tree (Q1
option b) and more reliable than render-time translation (Q1 option
c), and it preserves the v2.1 strength of language-stable method
names across runs.
