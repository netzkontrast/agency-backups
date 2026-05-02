# ReAct Trace and Logs

## Restatements

**Research Objective:** Identify, triangulate, and codify documented best practices for writing prompts on three agent systems (Google Jules, Claude Code, Gemini Deep Research) across 5 aspects (Explore, Plan, Implement, Review, Validate), outputting three Specs using RFC 2119 and Gherkin.

**Constraint Blocks:**
*   **0 — Reflection Baseline:** Reflection is mandatory at defined checkpoints using a 5-question template.
*   **1 — Source Priority Rules:** Use sources in priority: 1) Primary vendor docs, 2) Vendor engineering blogs, 3) Vendor GitHub repos, 4) Independent reproductions, 5) Aggregators (low-confidence).
*   **2 — Temporal Scope:** Jan 1, 2025 - today (hard), Jul 1, 2024 - Dec 31, 2024 (soft).
*   **3 — Output Exclusions:** Exclude pricing, quotas, unannounced features, comparative rankings, model version strings, personal context.
*   **4 — Spec-Driven Output Grammar (RFC 2119 + Gherkin):** MUST use RFC 2119 keywords correctly, MUST use Gherkin scenarios for examples, MUST use specific identifiers, rationale paragraphs MUST NOT have all-caps keywords.

**Role:** Senior Prompt-Engineering Research Analyst specialized in autonomous agents and Spec-Driven Development. I write objective Specs grounded in evidence, distinguishing MUST/SHOULD/MAY rigorously.

**Do / Don't (Internalized):**
*   **Do:** Use one RFC 2119 keyword per statement, self-contained Gherkin scenarios (use Background if ≥3 share setup), annotate single-source claims, preserve original statements if world-changed, include anchor comments, separate system-level from aspect-level conventions, cite sources properly, halt/flag priority-1 contradictions.
*   **Don't:** Use lowercase RFC 2119 keywords normatively, use all-caps keywords in rationale, use multiple keywords per statement, write non-executable Gherkin scenarios, write assert-only scenarios (only Then), embed exclusions (pricing/versions/rankings), silently merge contradictions, invent ungrounded statements.

## Kickoff Reflection (CONSTRAINT BLOCK 0 checkpoint #1)
**Q1. What do I actually believe right now, and how confident?** I believe that while Claude Code has robust documentation, Google Jules and Gemini Deep Research may have sparser public docs since they are newer or have less established public best practices; I am highly confident.
**Q2. What is the strongest piece of evidence against my current belief?** Google often releases extensive whitepapers or cookbook examples when launching new agentic tools, which might provide ample documentation for Jules and Gemini DR.
**Q3. Where am I most likely wrong, and why?** I might be wrong in assuming Claude Code is perfectly documented; its community discourse could contradict the official docs due to rapid updates.
**Q4. What would I do differently if I restarted the research from scratch knowing what I know now?** I would prioritize GitHub repos and community reproductions immediately, as vendor docs often lag behind real-world behavior for CLI agents.
**Q5. What is the single highest-value next action?** Build the seed query set (Step S1) and begin searching for primary vendor docs (Step S2).
