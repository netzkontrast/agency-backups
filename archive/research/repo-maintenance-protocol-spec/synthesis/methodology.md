# Methodology & Triangulation (M06)

## M06 Source Triangulation

**Topic: LLM Agent Automated Repository Maintenance & Technical Debt Delegation**

**Query 1:** "LLM agent automated repository maintenance"
- *Synthesis:* Existing systems often fail to keep metadata updated during active coding tasks because context limits encourage short-term reasoning. We must offload the maintenance of metadata into a specialized "Nightly Maintenance Run" decoupled from active product tasks.
- *Confidence:* Synthesized (no exact prior art found for this specific multi-agent structure).

**Query 2:** "Dynamic documentation state machines in multi-agent systems"
- *Synthesis:* Documentation in multi-agent systems (like `/readme.md` files) must stop being a simple table of contents and become an executable State Machine. The "Readmes as State Machines" paradigm ensures agents immediately load the operational status of a folder into context.
- *Confidence:* Synthesized.

**Query 3:** "Technical debt delegation for autonomous AI"
- *Synthesis:* Autonomous agents generate "frustration logs" when encountering systemic friction. These logs are unstructured. They must be transformed into isolated, executable `prompt.md` items in a centralized `/todo/` pipeline for future execution. This prevents the current agent from getting distracted by yak shaving.
- *Confidence:* Synthesized.

## M08 What Would Change My Mind (Pre-Commitment)
- I believe maintenance agents should only modify state (`readme.md`) and delegation files (`/todo/`), but *not* system architectures (`FOLDERS.md` or `RESEARCH.md`).
- *What would change my mind:* If a T1 source proves that agents cannot accurately delegate tasks unless they also update the structural rules governing those tasks. Or if it's proven that maintaining separate architectures inevitably leads to rapid drift that cron jobs cannot fix.
