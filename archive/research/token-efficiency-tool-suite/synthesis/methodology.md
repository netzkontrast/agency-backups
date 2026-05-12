# Methodology

This research applied the following rigorous methods:
- **M01 (Falsification):** Designed search axes to find specific structural implementations of token efficiency, discarding repos that only provided general prompt engineering advice.
- **M06 (First Principles):** Broke down "token efficiency" into its constituent parts: invocation cost (mandatory tools), budget constraints (token caps), output compression (structured JSON), and input pruning (context management).
- **M07 (Contradiction Log):** Identified the tension between the token overhead of JSON schemas and the token savings of blocked hallucination.
- **M13 (Adversarial Query Expansion):** Expanded searches across adjacent, opposing, abstract, and orthogonal dimensions to uncover failure modes (e.g., context overflow) and alternative paradigms (e.g., query planners).
