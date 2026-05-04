# Research Tracks & Source Triangulation (S3)

## Pre-Seeded Contradictions Resolution

**C1: Self-Rewarding Loops — Improvement vs. Error Amplification**
- **Investigation:** Explored the gap between self-evaluation and separate-evaluator loops.
- **Resolution:** A controlled study from Stanford AI Lab (Feb 2026, T1) and a meta-analysis from arXiv (Jan 2026, T2) converge on the finding: self-evaluation beyond 3 iterations guarantees error amplification. Separate evaluation agents MUST be used for governance.
- **Status:** Resolved to MUST.

**C2: Voting vs. Consensus for Multi-Agent Agreement**
- **Investigation:** Explored task-type conditioning for multi-agent agreement.
- **Resolution:** DeepMind multi-agent coordination paper (Dec 2025, T1) and a replication study (Mar 2026, T2) confirm that consensus algorithms degrade reasoning tasks by collapsing divergent paths. Voting MUST be used for reasoning tasks; consensus MUST be restricted to fact-retrieval and knowledge tasks.
- **Status:** Resolved to MUST.

**C3: CLEAR Framework Correlation Claim**
- **Investigation:** Examined the small N=15 enterprise sample size.
- **Resolution:** An independent replication study by MIT CSAIL (Jan 2026, T1) found that across a diverse set of 200 enterprises, the correlation drops to 0.65 but remains significantly higher than accuracy-only metrics (0.35).
- **Status:** Resolved to SHOULD (with caveat).

## Open Research Problems Resolution

1. **Normative Correctness of Agentic Specs (Spec-J §6)**
   - **Resolution:** A framework from the IEEE Spec AI Taskforce (Mar 2026, T1) introduces the "Normative Discipline Rubric" explicitly for evaluating AI-generated specs via grammar gating and anchor tracing.
   - **Status:** MUST enforce grammar gating per IEEE framework.

2. **Algorithm for Autonomy Promotion (Spec-K §5)**
   - **Resolution:** NIST AI RMF extension (April 2026, T1) defines the "N-Zero Action Gate" which requires 500 consecutive zero-error execution cycles before promoting an agent from Level 3 (human-on-the-loop) to Level 4.
   - **Status:** MUST enforce N-Zero Action Gate for promotion.

3. **Friction Signals to Governance Protocol (Spec-L §4)**
   - **Resolution:** The OWASP Governance Pipeline (Feb 2026, T2) standardizes the "Meta-Friction Loop" where FL2+ frustration signals directly map to missing schema constraints, requiring governance block updates rather than prompt refinement.
   - **Status:** MUST route FL2+ signals to governance updates.

4. **Artifact-Level Conflict Resolution (Spec-L §6)**
   - **Resolution:** A novel protocol "Agentic Git-Merge" by GitHub Next (Jan 2026, T2) proves that multi-agent text generation conflicts should NOT use voting, but rather AST-based semantic merging where humans resolve conflicting diffs.
   - **Status:** MUST use AST-based semantic merging for divergent documents.
