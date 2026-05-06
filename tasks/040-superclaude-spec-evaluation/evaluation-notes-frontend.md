---
type: note
status: draft
slug: superclaude-spec-evaluation-frontend-notes
summary: "Frontend-architect lens evaluation of the Gemini SuperClaude spec — operator/agent UX, command-surface accuracy, persona-invocation syntax, flag matrix, AGENTS.md onboarding impact."
created: 2026-05-06
updated: 2026-05-06
---

# Task 040 — Evaluation Notes (frontend-architect lens — operator/agent UX)

> **Scope.** This note evaluates the Gemini "SuperClaude Orchestration & Meta-Governance Specification"
> (`research/gemini/superclaude-agency-orchestration-spec/superclaude-agency-orchestration-spec.md`)
> from the perspective of the *operator-CLI / agent-interaction-UX* surface — i.e. the parts of the
> spec a new agent or human encounters when they sit down at the prompt and try to *do something* in
> this repo. It is the companion to the backend-architect lens (separate file).

---

## §F. Command-surface accuracy matrix

The Gemini spec asserts (in its summary and §10) "thirty distinct slash commands". The actual count it
*lists* is 22 distinct `/sc:*` names plus one mis-formatted `sc-document` (see §F.note below). The
table below tracks every cited command against the actual repo and against the upstream SuperClaude
Framework reference cited at `AGENTS.md:76`
(`https://github.com/netzkontrast/SuperClaude_Framework/blob/main/src/superclaude/commands/`).

**Local-skill test.** The repo's local `skills/` directory (verified by `ls /home/user/agency/skills/`)
contains zero `sc:*` skills. The only `sc:` command actually wired into AGENTS.md is `/sc:createPR`
(`AGENTS.md:16, 76, 80–86, 98, 105–107`), and even that one is sourced upstream, not local. Every
other `/sc:*` command in the Gemini spec is therefore "exists upstream / not locally installed" at
best — a meaningful UX distinction the spec elides.

| Gemini cites | Actual local skill | Upstream SuperClaude command | Status | Note |
|---|---|---|---|---|
| `/sc:pm` (§1.1) | none | likely exists | external | Gemini's "omnipresent background orchestrator" framing is upstream marketing language; the actual `/sc:pm` is an explicit slash-command, not a daemon. The directive at SC.CMD.1.1 ("MUST prioritize AGENTS.md…upon any new session initialization") describes *agent behaviour*, not a real background process. |
| `/sc:agent` | none | unverified | external | Mentioned only in the §0 mapping table, never specified. Probably a stub. |
| `/sc:spawn` (§2.1) | none | exists upstream | external | Behavioural description plausible. |
| `/sc:task` (§2.2) | none | exists upstream | external | Plausible. |
| `/sc:workflow` (§2.3) | none | exists upstream | external | Plausible. |
| `/sc:brainstorm` (§3.1) | none | exists upstream | external | Description (Socratic dialogue, vague-prompt routing) is consistent with the *exemplar* `skills/research-prompt-optimizer/SKILL.md:65–96` (intent-capture loop with askuser gates), so the Gemini description is plausible even though the command itself is not local. |
| `/sc:research` (§3.2) | none | exists upstream | external | The "Tavily + Playwright + Sequential" claim is upstream-MCP-stack specific; this repo does not actually wire those servers. |
| `/sc:spec-panel` (§3.3) | none | unverified | likely external | The "scoring gate < 7.0 blocks merge" claim (§10) is hallucinated as a *repo* gate — the actual merge gate is `tools/check-governance.sh` (`AGENTS.md:31, 39`), which has no spec-panel hook. |
| `/sc:business-panel` | none | unverified | likely external | Same caveat. |
| `/sc:index-repo` (§1.2) | none | exists upstream | external | The "MUST run on every clone" mandate (SC.CMD.1.A.2) is asserted without reference to the local `tools/check-governance.sh`-style gate. **This is a high-cost UX claim** — see §I. |
| `/sc:load`, `/sc:save` | none | exist upstream | external | Tied to Serena MCP, which is not configured for this repo. |
| `/sc:design` (§4.1) | none | exists upstream | external | Plausible. |
| `/sc:implement` (§4.2) | none | exists upstream | external | Plausible. |
| `/sc:estimate` (§4.3) | none | exists upstream | external | Plausible. |
| `/sc:analyze` (§5.1) | none | exists upstream | external | Plausible. |
| `/sc:troubleshoot` (§5.2) | none | exists upstream | external | Plausible. |
| `/sc:test` (§5.3) | none | exists upstream | external | Plausible. |
| `/sc:reflect` (§6.1) | none | exists upstream | external | The "MUST execute /sc:reflect --type task --analyze before checking off a TASK.md node" mandate (SC.CMD.6.1) **conflicts** with the existing closing-run procedure (`AGENTS.md:80–86`), which mandates `/sc:createPR` — not `/sc:reflect` — as the binding final action. |
| `/sc:git` (§6.2) | none | exists upstream | external | See §G's commit-message UX analysis below — this directive collides with the repo's HEREDOC pattern. |
| `/sc:improve` (§8.1) | none | exists upstream | external | Plausible. |
| `/sc:cleanup` (§8.2) | none | exists upstream | external | Plausible. |
| `/sc:build` (§8.3) | none | exists upstream | external | Plausible. |
| `/sc:document` (§7.3) | none | exists upstream | external | The §7.3 "auto-generate formal in-line code documentation" mandate is plausible. **However the `sc-document` mention in §7.1 (same spec) is a different, fabricated entity** — see §F.note. |
| `/sc:explain` (§7.3) | none | exists upstream | external | The `--explain` flag claim is suspect — see §I/J. |
| `sc-document` (§0 table, §7.1, SC.CMD.7.1) | none | does not exist as written | **hallucinated / typo** | Written without `:`, with hyphen. Either (a) a typo for `/sc:document` (in which case the §7.1 "friction-log skill" framing is wrong: `/sc:document` is for code-doc generation, not friction logging), or (b) a fabricated "skill" that does not exist anywhere. **§F.note below.** |
| `/sc:createPR` | upstream (per `AGENTS.md:76`) | exists | **exists, in use** | Conspicuously *absent* from the Gemini spec. This is the one `/sc:*` command the repo actually depends on, and Gemini does not mention it. Major omission. |

### §F.note — The `sc-document` confusion

The spec uses three forms in three different places:

- §0 governance-table: `sc-document` (hyphen, no `/sc:` prefix).
- §7.1 heading: `(`sc-document`)` — same hyphenated form.
- §7.3 normative clause SC.CMD.7.5: `/sc:document` (proper slash-command form).

These are presented as **different commands with different jobs**: §7.1 says `sc-document` is the
"meta-cognitive diary" auto-invoked on Friction Level 1 events; §7.3 says `/sc:document` is the formal
in-line code-documentation generator. There is exactly one upstream command (`/sc:document`), and its
documented job is code-doc generation, not friction-log writing. So §7.1's mandate "the agent MUST
invoke the `sc-document` skill automatically and immediately whenever any command or external operation
fails unexpectedly (triggering a Friction Level 1 event)" is a **conflation**: it borrows the name of a
real code-doc command and reassigns it to a friction-log job already owned by `FRUSTRATED.md`
(`FRUSTRATED.md:30–32` — the actual mandate is "include a section named `## Frustration Log` in your
final PR description"). This is the single most operator-confusing claim in the entire spec.

---

## §G. Persona-invocation syntax

**Gemini cites** (SC.CMD.2.A.2, §1.1, §2.2):
- `@agent-security`
- `@agent-frontend-architect`
- `@agent-backend-architect`

**Actual repo syntax.** A `grep -rn "@agent-"` against `AGENTS.md`, `PROMPT.md`, `RESEARCH.md`, `TASK.md`
returns **zero hits**. There is no `.claude/agents/` directory. The repo's actual agent-invocation
mechanism is Claude Code's `Agent` tool with `subagent_type: <name>` — that is how this very evaluation
was dispatched (the parent task spawns `frontend-architect` and `backend-architect` subagents via the
SDK, not via an `@agent-*` slash-mention).

**Verdict.** The `@agent-*` syntax is **not a real surface in this repo**. It may exist upstream in
SuperClaude as a chat-interface convenience, but Gemini presents it as if it were the binding
invocation contract for this repository. It is not. A new operator who reads SC.CMD.2.A.2 and types
`/sc:task execute "auth-fix-jwt" --delegate` expecting "the system MUST dynamically assign the
`@agent-security` persona" will get nothing — there is no such routing layer wired into
`tools/check-governance.sh` or any other repo gate.

**Recommendation.** Reject the `@agent-*` syntax wholesale. If Task 040 wants to surface persona
invocation, document the actual `Agent` tool's `subagent_type` enum and the available agents
(`frontend-architect`, `backend-architect`, `security-engineer`, etc., wherever those are catalogued).

---

## §H. Flag matrix verification

The Gemini §9 flag matrix is unverifiable from inside this repo: there are no local `sc:*` skill briefs
to parse flags from. The closest thing to a "flag-parsing" skill is
`skills/research-prompt-optimizer/SKILL.md`, which uses YAML-driven phase gates, **not CLI flags**.
That said, here is what I can pin down:

| Gemini flag | Cited compatible commands | Verifiable? | Verdict |
|---|---|---|---|
| `--lean` | `/sc:implement`, `/sc:improve`, `/sc:cleanup` | not locally — no skill to test against | **plausible upstream**, unverified locally. The semantic ("eliminates verbosity, focuses on raw code delta") is reasonable. |
| `--parallel` | `/sc:spawn`, `/sc:task`, `/sc:workflow` | not locally | **plausible**. Aligns with how the parent Task 040 actually dispatches parallel subagents (this very lens runs in parallel with the backend-architect lens). |
| `--performance` | `/sc:analyze`, `/sc:implement`, `/sc:test` | not locally | **suspicious**. The semantic ("explicitly biases the LLM to optimize for execution speed over readability") is the kind of flag that sounds plausible but is rarely a real LLM control. Likely fabricated or aspirational. |
| `--readonly` | `/sc:troubleshoot`, `/sc:analyze`, `/sc:reflect` | not locally | **plausible**. Read-only diagnostic mode is a sound pattern. The spec contradicts itself slightly: SC.CMD.5.5 says `/sc:troubleshoot` "MUST operate in a strictly diagnostic, `--readonly` mode" *by default* — i.e. the flag is not needed unless overriding. So citing `--readonly` as an explicit flag in §9 is inconsistent with §5.2. |
| `--fix` | `/sc:troubleshoot` | not locally | **plausible**. Standard diagnostic-tool pattern. |
| `--think` | `/sc:analyze`, `/sc:research` | not locally | **partially fabricated**. The "deep multi-step reasoning" framing is real upstream-SuperClaude vocabulary. But §9 lists only 2 commands while SC.CMD.5.3 also mentions `--think-hard` (a third tier) without including it in the §9 matrix at all — the matrix is incomplete. |
| `--delegate` | `/sc:task` | not locally | **plausible**. |
| `--no-mcp` | "All implementation execution commands" | not locally | **plausible**. SC.CMD.4.4 is internally inconsistent: it says `--no-mcp` MUST be used "to conserve tokens on lightweight isolated tasks" — but `--no-mcp` disables Magic + Context7, which the same §4.2 says MUST be active "to prevent the agent from hallucinating outdated library methods". You cannot simultaneously MUST-have both. UX cost: an operator following both clauses is in a contradiction. |
| `--strategy` | `/sc:spawn`, `/sc:workflow`, `/sc:task` | not locally | **plausible** — `--strategy sequential\|parallel\|adaptive` is a standard pattern. |
| `--focus` | `/sc:analyze`, `/sc:test` | not locally | **plausible**. SC.CMD.5.2 enumerates valid args (`quality`, `security`, `performance`, `architecture`). |
| `--load` (SC.CMD.1.5) | implied on every persona handoff | not locally | **suspicious**. The clause "the `--load` flag MUST be appended to commands when executing a handoff between specialized agent personas" is asserted but `--load` does not appear in the §9 flag matrix at all. Either the matrix is wrong or the clause is wrong. |
| `--git` (SC.CMD.4.6) | `/sc:implement` | not locally | **suspicious**. Mandate "to enforce strict version control best practices, the `--git` flag MUST be appended to implementation commands to automatically stage and snapshot atomic changes". Not in the §9 matrix. Conflicts with `/sc:git` (§6.2) and with the repo's HEREDOC commit pattern. **Reject.** |
| `--explain` (SC.CMD.7.6) | `/sc:explain` | not locally | **likely fabricated** — see §J/K below. The flag name and the command name are the same; appending `--explain` to `/sc:explain` is suspiciously redundant. |

**Top-level UX problem.** Without local skill briefs to parse, an operator has no way to discover which
flags actually parse. The Gemini spec presents the matrix as if it were a contract; it is at best a
hopeful catalogue. Adopting it as binding governance would generate FL2 friction (per `FRUSTRATED.md:18–22`,
"conflicting instructions" or "tooling/dependency failures requiring substantial diagnostic effort") on
every operator who tries to use a flag that does not parse.

---

## §I. UX impact on AGENTS.md onboarding

A new Claude Code agent landing in this repo today reads `AGENTS.md` and follows a clean cognitive path:

1. Run `./install.sh` (`AGENTS.md:22`).
2. Run `tools/check-governance.sh` (`AGENTS.md:31`).
3. Decide task type via the routing table (`AGENTS.md:115–119`).
4. Apply L1 frontmatter (`AGENTS.md:201–215`).
5. At the end of the run, invoke `/sc:createPR` (`AGENTS.md:80`).

That is **five concrete actions, one of which is a slash-command**. Every action is mechanically
verifiable; every clause has a stable anchor (`SS.1`, `AG.1.1`, `CR.1`).

If we naively adopt Gemini's §1 directives, the cognitive load explodes:

- SC.CMD.1.1 — "MUST prioritize AGENTS.md as supreme config layer for `/sc:pm` background process" — **already true in spirit**; AGENTS.md is the entry point. But the framing of `/sc:pm` as a "background process" is misleading: there is no daemon. **Net: confusion (-)**.
- SC.CMD.1.2 — "`/sc:pm` MUST utilize the Serena MCP server" — Serena is not configured here. **Net: blocking onboarding error (---)**.
- SC.CMD.1.A.2 — "MUST independently run `/sc:index-repo`" on every clone — this would add a sixth setup step *that does not actually do anything in this repo* (no Serena, no semantic index store). **Net: pure friction (---)**.
- SC.CMD.1.5 — "`--load` MUST be appended on persona handoff" — handoffs in this repo are via the `Agent` tool, which has no `--load` flag. **Net: zero-info noise (-)**.
- SC.CMD.1.6 — "Upon session termination, MUST trigger `/sc:save`" — collides with `CR.1` (the actual mandated termination action is `/sc:createPR`). **Net: contradictory close-run procedure (---)**.

**Cognitive load delta: strongly negative.** Adopting §1 wholesale roughly **doubles the setup
checklist** and adds three slash-commands the operator has no way to verify, while replacing one
working close-run mandate (`/sc:createPR`) with a different one (`/sc:save`) for no clear gain.

What *would* help onboarding: a one-paragraph note in AGENTS.md saying "the SuperClaude `/sc:*`
namespace is partially available in Claude Code sessions; this repo binds only `/sc:createPR` (see
`§ Closing Run Procedure`); other `/sc:*` commands are upstream conveniences, not repo-mandated".
That clarifies the actual surface in ~50 words. The Gemini spec is the opposite: ~5000 words of
cross-referenced mandates whose enforceability ranges from "exists" to "fabricated".

---

## §J. Top 3 highest-leverage UX adoptions (my call)

1. **The Socratic-discovery framing of `/sc:brainstorm` (§3.1).** The mandate "vague single-sentence
   feature requests MUST be routed through `/sc:brainstorm`" is a genuinely good UX pattern, and it
   *already exists in this repo* — the canonical implementation is
   `skills/research-prompt-optimizer/SKILL.md:65–96` (Phase 1 — Intent Capture, askuser-gated loop
   until 100% slot clarity). The Gemini description (Socratic dialogue, latent-requirement extraction,
   updates `PROMPT.md` only — never writes code) maps cleanly onto how research-prompt-optimizer Phase
   1 works. **Adoption move:** add a `PROMPT.md §4` clause routing single-sentence prompt briefs through
   the research-prompt-optimizer's intent-capture phase. This formalizes a working pattern.

2. **Read-only-by-default diagnostics (`--readonly` semantics from §5.2).** SC.CMD.5.5 — "the
   `/sc:troubleshoot` command MUST operate in a strictly diagnostic, `--readonly` mode" — encodes a
   sound principle (diagnose before mutate) that the repo currently relies on convention for. **Adoption
   move:** lift this principle into a generic `MAINTENANCE.md` clause: "diagnostic skills MUST output a
   ranked-cause list and MUST NOT apply patches without explicit human confirmation". This is the
   safest, highest-leverage UX adoption.

3. **The friction-log auto-trigger pattern (§7.1, modulo the `sc-document` naming bug).** The clause
   "if a human operator issues a hard correction (`No, that's wrong…`, `Actually the API changed…`),
   the system MUST log this delta in `FRUSTRATED.md`" (SC.CMD.7.2) extends the existing FRUSTRATED.md
   FL1 trigger to a **conversational** signal, not just a tool-failure signal. That is a real UX gain.
   **Adoption move:** add a `FRUSTRATED.md` clause: "in addition to tool-failure FL1 triggers, an
   in-session human correction containing one of {`actually`, `no, that's wrong`, `you misunderstood`}
   MUST be logged as FL1+ in the friction log". Strip the `sc-document` naming entirely.

---

## §K. Top 3 highest-risk-to-UX rejections (my call)

1. **`/sc:git` as a mandatory commit wrapper (§6.2 / SC.CMD.6.3).** "All commits MUST be processed
   through the `/sc:git` wrapper to ensure context-aware smart commit messages." This **directly
   collides** with the working HEREDOC pattern documented in the system prompt and in
   `tools/check-governance.sh`-gated workflow:
   ```bash
   git commit -m "$(cat <<'EOF' ... EOF)"
   ```
   The HEREDOC pattern is: (a) inspectable before commit, (b) deterministic, (c) survives any
   slash-command-resolution failure. Mandating `/sc:git` adds a runtime dependency for what is
   currently a zero-dependency operation. **Reject.**

2. **`/sc:index-repo` mandatory on every clone (SC.CMD.1.A.2) + `/sc:save` mandatory on session close
   (SC.CMD.1.6).** Both pile bookkeeping onto an already-loaded session-bracket
   (`./install.sh` → `tools/check-governance.sh` → work → `/sc:createPR`). Without Serena MCP actually
   wired, the indexing call is a no-op; the save call collides with `/sc:createPR`. The
   FRUSTRATED.md "Structural Bloat / Micromanagement" trigger (`FRUSTRATED.md:28`) was *written* for
   this kind of administrative-overhead inflation. **Reject.**

3. **The `--explain` progressive-disclosure flag (SC.CMD.7.6).** "The human MAY invoke `/sc:explain`,
   optionally appending the `--explain` flag to trigger progressive disclosure." Putting the flag name
   identical to the command name is a strong tell of fabrication; the §9 flag matrix does not list
   `--explain` either. Even if upstream-SuperClaude has a real progressive-disclosure feature, the
   Gemini description is too thin to be actionable. **Reject as cited; revisit only if upstream docs
   confirm a real syntax.**

---

## Closing observation

The Gemini spec is fluent, plausible-sounding, and internally cross-referenced — i.e. it has all the
*surface* features of a binding governance document. But viewed through the operator-UX lens, it
fails the most basic test: **can a new agent actually do what the spec says?** The answer is: only for
`/sc:createPR`, the one command the spec does not mention. Every other mandate is at best aspirational
and at worst contradicts the working onboarding path. The right disposition for Task 040 is to lift
the three high-leverage *patterns* (§J above) into the actual repo specs (`PROMPT.md`, `MAINTENANCE.md`,
`FRUSTRATED.md`) **without** importing the `/sc:*` mandate-vocabulary, and to mark the rest of the
Gemini spec as "research input, not in-force governance".
