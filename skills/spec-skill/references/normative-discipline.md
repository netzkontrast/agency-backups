# Normative Discipline — Writing Statements That Hold Up

Most specs fail not because the schema is wrong but because the normative statements inside it are sloppy. This document covers the discipline that distinguishes a binding requirement from a wish.

## The BCP-14 keywords, briefly

| Keyword | Meaning | When to use |
| :--- | :--- | :--- |
| `MUST` / `REQUIRED` / `SHALL` | Absolute requirement | Violation breaks the system or invalidates downstream guarantees |
| `MUST NOT` / `SHALL NOT` | Absolute prohibition | The action causes harm, contradicts the system contract, or destroys evidence |
| `SHOULD` / `RECOMMENDED` | Strong default; deviation requires reason | The action is right in nearly all cases but edge cases exist |
| `SHOULD NOT` / `NOT RECOMMENDED` | Strong default against; deviation requires reason | Action is usually wrong but sometimes justified |
| `MAY` / `OPTIONAL` | Permitted, not required | The action is a legitimate choice the implementor makes |

The keywords only carry their BCP-14 meaning when they appear in **all caps**. Lowercase "must", "should", "may" are regular English and bind nothing. This is why §1 of every spec quotes the BCP-14 paragraph verbatim — it makes the convention enforceable.

## Statement structure

Every normative statement has three parts:

1. **Actor** — who is being constrained
2. **Modal verb** — the BCP-14 keyword
3. **Action with object** — what the actor does or doesn't do

```
A.4.1 — A planning prompt MUST explicitly request the agent to generate
        a step-by-step proposal before code execution begins.
```

- Actor: *A planning prompt*
- Modal: *MUST*
- Action: *explicitly request the agent to generate a step-by-step proposal before code execution begins*

If you can't identify all three parts in your draft statement, rewrite it.

## One claim per statement

The single biggest source of audit failures is the **and-bug** — two requirements joined into one statement.

```
BAD:  A.5.1 — An execution prompt MUST define acceptance criteria
              and the agent MUST run the test suite.
```

This is two statements. It looks like one because of the conjunction. Split:

```
GOOD: A.5.1 — An execution prompt MUST define acceptance criteria the
              agent can independently verify.
      A.5.2 — The system MUST run the project's test suite before
              marking the task complete.
```

The exception: when the second clause is a clarifying constraint on the first, not an independent requirement. "The agent MUST commit changes using the configured authorship mode" is fine — "using the configured authorship mode" qualifies the commit, it doesn't add a second action.

## Specify the actor

Vague actors break audits. "The system" is sometimes acceptable but often hides who's actually responsible.

```
BAD:  A.6.3 — The automated critique MUST NOT be used as a substitute
              for human security review.
```

Who's the actor here? The critique can't constrain itself. The actor is the user.

```
GOOD: A.6.3 — The user MUST NOT treat the automated critique as a full
              substitute for human-in-the-loop security audits.
```

Common actors: *the agent*, *the user*, *the developer*, *the system*, *the prompt*, *the planning module*, *the validation module*. Pick the one whose behavior the statement actually constrains.

## Make it testable

A normative statement that can't be checked is decoration. Before finalizing a statement, write the Gherkin scenario that would verify it. If you can't write one, the statement is too vague.

```
BAD:  A.5.3 — The agent SHOULD be efficient.
```

There's no scenario for this. Efficient relative to what? Measured how?

```
GOOD: A.5.3 — An implementation prompt SHOULD leverage environment
              snapshots to bypass redundant dependency installation.
```

This one is testable: a Gherkin scenario can check whether an environment snapshot was used, and whether dependency installation was skipped.

## Don't smuggle vendor surface details

Surface details — UI elements, button colors, version numbers, specific endpoint URLs — belong in **rationale**, not in normative statements. Surface details change. The statement shouldn't break when the UI gets a redesign.

```
BAD:  A.4.2 — A user MUST click the green "Approve" button in the
              planning panel to proceed.
```

```
GOOD: A.4.2 — A user MUST interact with the interactive planning
              interface to approve or reject the proposed file
              modifications.
```

The rationale paragraph for §4 can then say "the planning interface in the current product surfaces this as a green Approve button". When the button turns blue or moves, the statement still holds.

## MUST inflation

If every statement is MUST, none are. The keyword loses its weight. A healthy aspect block has roughly:

- 1–2 MUSTs (the things that genuinely break the system if violated)
- 2–3 SHOULDs (strong defaults with edge cases)
- 0–2 MAYs (legitimate options)
- 0–1 MUST NOT or SHOULD NOT (explicit prohibitions worth calling out)

If your draft is all MUSTs, force-rank them. The bottom half are probably SHOULDs.

## When to prefer prohibition

`MUST NOT` and `SHOULD NOT` statements often communicate something a positive statement can't: they call out a specific failure mode the author has seen.

```
A.7.5 — The agent MUST NOT blindly suppress error logs to force a CI
        build to pass.
```

This is more useful than the positive form ("MUST address the root cause") because it names the exact corner-cutting behavior the author has caught the agent doing. Use prohibitions when there's a known anti-pattern worth flagging by name.

## Statement IDs and renumbering

- IDs use the pattern `<PREFIX>.<SECTION>.<ORDINAL>`. The prefix is the spec letter (A, B, C). The section is the §-number (2 for system-level, 3–7 for aspects). The ordinal counts within the section.
- IDs are stable references. Once a statement has been published with ID `A.5.3`, do not reuse that ID for a different statement after deletion. If `A.5.3` is removed, leave the gap and note it in §8 or a change log, or renumber everything after explicitly.
- When inserting between existing statements, append at the end of the section rather than shifting all subsequent IDs. Order within a section is presentation, not semantics.

## The rewrite test

After drafting, re-read each statement and ask:

1. Could a reasonable engineer cite this statement to block a PR?
2. Could the author cite this statement to defend an architectural decision?
3. Could a tester convert this into a passing or failing scenario?

If the answer to all three is yes, the statement is doing its job. If any answer is no, rewrite or demote.
