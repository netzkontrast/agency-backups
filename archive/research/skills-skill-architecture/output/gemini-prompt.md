# Deep Research Prompt: `skills-skill` Architecture

**For**: Google Gemini Deep Research
**Prepared by**: Claude Code agent, 2026-05-04
**Purpose**: Resolve architectural uncertainties for a git-backed skill-loader stub

---

## How to use this prompt

Copy the entire content of the **Research Task** section below into Google Gemini Deep Research as your research query. The prompt is self-contained — you do not need access to any external repository or prior documents to execute it.

Expected output: a PDF report answering R1-Q1 through R7-Q1, with citations where available. The PDF should be uploaded to `/research/skills-skill-architecture/workspace/gemini-deep-research.pdf` in the netzkontrast/agency repository for integration per `integration-plan.md`.

---

## Research Task

### Context (read before researching)

An AI assistant called "Claude" is used via two interfaces:
1. **claude.ai** — a web interface that supports "user skills": custom instruction files installed at a path called `/mnt/skills/user/<name>/SKILL.md` inside a per-session container. These files are loaded into the model's context when the user asks for help with a particular topic. The container is managed by Anthropic.
2. **Claude Code** — a CLI tool that supports the same skill concept, loading skills from `~/.claude/skills/<name>/SKILL.md` on the local filesystem.

Both use the same `SKILL.md` file format: a YAML frontmatter block followed by a Markdown instruction body.

The project: replace 14 individually-installed skills with a single stub skill called `skills-skill`. When activated, `skills-skill` clones a GitHub repository (github.com/netzkontrast/agency) and routes all skill requests to versioned skill bodies stored there under `/skills/`. The other 13 skills become repository content rather than installed entities.

The architecture is partially specified but has six unresolved questions (U1–U6) that require empirical research. This prompt asks you to research each one.

---

### R1-Q1 (Critical): Is `git` available in the claude.ai session container?

**Background**: The proposed architecture relies on the stub executing `git clone` and `git fetch` from within the claude.ai session. If `git` is not available as an executable in the container's `PATH`, the entire clone-based approach must be replaced.

**Research questions**:
1. Is the `git` binary available in claude.ai session containers? If yes, what version?
2. If `git` is not available, what alternative mechanisms does a claude.ai session have for fetching content from a GitHub repository? Candidates to evaluate:
   - GitHub REST API via `curl` or `wget` (if available)
   - GitHub MCP server (if registered as a connector in the session)
   - Python `requests` library (if Python is available in the container)
3. What is the complete list of shell utilities and runtimes available in a claude.ai session container (`bash`, `python3`, `curl`, `wget`, `jq`, etc.)?
4. Are there any Anthropic-documented ways to run shell commands from inside a claude.ai SKILL.md instruction, or does the skill only inject text into the model's context?

**Expected output**: A definitive answer to whether `git` is available, and if not, the best-supported alternative mechanism for HTTP-based file fetching from GitHub.

---

### R1-Q2 (High): How does claude.ai's host select which skill to activate?

**Background**: The stub `skills-skill` must be installed as the only (or one of very few) skills. We need to understand how claude.ai's skill-trigger mechanism decides which skill to inject into context for a given user message.

**Research questions**:
1. Does claude.ai use the SKILL.md frontmatter `description` field for skill selection? If so, what matching algorithm is used (keyword, semantic similarity, exact match)?
2. Can a user explicitly name a skill by name in their message (e.g., "use dramatica-theory skill")? If so, what naming convention does claude.ai use?
3. Does the host pass the user's original message to the skill as part of the context injection? Or does the skill see only a pre-processed intent signal?
4. If only one skill is installed (the stub), does the host always activate it regardless of the user's message? Or does the host still perform intent-matching before activating?
5. Is there a way to make a skill act as a "catch-all" that activates for any user message not matched by another skill?

**Expected output**: A clear description of the skill-activation flow from user message to skill body injection.

---

### R2-Q1 (Medium): Jules skill-loading conventions

**Background**: The project uses four agents — claude.ai, Claude Code, Jules (Google's agentic coding assistant), and gemini-cli. The architecture needs to serve skill content to all four. Claude Code uses `~/.claude/skills/<name>/SKILL.md`. The Jules convention is unknown.

**Research questions**:
1. Does Jules (labs.google.com/jules or equivalent) support a concept analogous to "user skills" — custom instruction files that are automatically loaded into context?
2. If yes: what is the file path convention, the file format, and how does Jules trigger skill loading?
3. If Jules does not have a native skill mechanism: what is the recommended way to provide persistent custom instructions to a Jules session? (e.g., a `.jules/` directory, a `AGENTS.md` file, a repository-level prompt file?)
4. Is the Jules skill/instruction format compatible with Claude's SKILL.md format (YAML frontmatter + Markdown body)? If not, what transformation is required?
5. Does Jules read any file from the repository at session start that could serve as a skill-loading hook?

**Expected output**: A description of Jules' instruction-loading mechanism sufficient to design a compatible adapter or confirm no adapter is needed.

---

### R2-Q2 (Medium): gemini-cli skill-loading conventions

**Background**: Same question as R2-Q1 but for gemini-cli (Google's command-line Gemini interface, available at github.com/google-gemini/gemini-cli).

**Research questions**:
1. Does gemini-cli support a concept analogous to "user skills" — custom instruction files?
2. If yes: what is the path convention, file format, and trigger mechanism?
3. Does gemini-cli read a `GEMINI.md` or similar repository-level file that could serve as a skill-loading hook?
4. Is the gemini-cli instruction format compatible with Claude's SKILL.md format? What transformation, if any, is needed?
5. What is the recommended way to provide persistent custom instructions that survive across gemini-cli sessions?

**Expected output**: A description of gemini-cli's instruction-loading mechanism sufficient to design a compatible adapter or confirm no adapter is needed.

---

### R5-Q1 (Low): git signing feasibility in the claude.ai container

**Background**: The trust model relies on the stub being in read-only `/mnt/skills/user/` (tamper-proof per session). A secondary layer would be git tag signing to detect repo-level tampering between sessions.

**Research questions**:
1. Is `gpg` or `ssh`-based git signing available in the claude.ai session container?
2. Can a skill stub verify a signed git tag using only tools available in the container?
3. If signing is not feasible in the container, are there alternative lightweight integrity checks for a shallow clone from a public GitHub repository (e.g., comparing the HEAD SHA against a known-good value stored in the stub)?
4. What is the attack vector if an agent with PR access pushes a malicious skill body that passes Michael's review? Is there a practical defense beyond PR review?

**Expected output**: A recommendation for the trust model's secondary layer (signing, SHA comparison, or accept current PR-review-only policy).

---

### R7-Q1 (High): claude.ai container filesystem persistence

**Background**: The pull-if-exists strategy (clone once, fetch on each session start) only saves latency if the clone persists between sessions. If the container is wiped on session end, every session is a full clone.

**Research questions**:
1. Does the claude.ai session container's filesystem persist between sessions for the same user? Specifically: does content written to `~/.claude/` (or any path outside `/mnt/skills/user/`) survive a session end and reappear in the next session?
2. If the filesystem is ephemeral per session: what is the typical time to shallow-clone a ~5 MB public GitHub repository from inside the container? Are there Anthropic-documented latency budgets for skill bootstrap?
3. Is there any Anthropic-documented persistent storage mechanism available to skills (beyond the read-only `/mnt/skills/user/` mount)?
4. If persistent storage is available: what path, what capacity, and what durability guarantees?

**Expected output**: A definitive answer to whether pull-if-exists is viable, and if not, the actual clone latency to inform the architecture.

---

### Synthesis Request

After researching the individual questions, please synthesize your findings into:

1. **Recommended bootstrap sequence** for `skills-skill` given what you've learned about container capabilities. Replace the `git`-based B1–B3 sequence in the preliminary spec with one that uses actually-available tools.

2. **Cross-agent compatibility matrix**: For each of the four agents (claude.ai, Claude Code, Jules, gemini-cli), state whether a native adapter is needed and what it looks like.

3. **Updated trust model**: Given the feasibility findings for R5-Q1, recommend the appropriate secondary trust layer.

4. **Latency budget**: Given the R7-Q1 findings, specify what the bootstrap sequence can guarantee about time-to-first-skill in both persistent and ephemeral container scenarios.

---

### Format requirements for the PDF report

Please structure the PDF report with these sections:
1. Executive Summary (1 page)
2. R1-Q1: git availability — findings and recommendation
3. R1-Q2: skill activation mechanism — findings and recommendation
4. R2-Q1: Jules compatibility — findings and recommendation
5. R2-Q2: gemini-cli compatibility — findings and recommendation
6. R5-Q1: signing feasibility — findings and recommendation
7. R7-Q1: container persistence — findings and recommendation
8. Synthesis: recommended bootstrap sequence
9. Synthesis: cross-agent compatibility matrix
10. Synthesis: updated trust model
11. Synthesis: latency budget
12. Open questions not resolved by this research
13. References / Citations
