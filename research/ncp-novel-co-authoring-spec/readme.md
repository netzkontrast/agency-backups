---
type: index
status: completed
slug: ncp-novel-co-authoring-spec
summary: "Research index for the Narrative Context Protocol specification enabling AI-agent-driven novel co-authoring."
created: 2026-05-04
updated: 2026-05-04
research_phase: complete
research_executes_prompt: ""
research_friction_level: FL0
---

# NCP Novel Co-Authoring Spec

**What is this folder?** The main task directory for the NCP/Dramatica research prompt.
**Why is it here?** To compartmentalize the specific inputs, workspaces, and outputs associated strictly with the NCP specification task, ensuring isolated and reproducible research.

## Contents
- [prompt.md](./prompt.md): The initial locked prompt provided by the user. Retained to verify adherence to constraints.
- [workspace/](./workspace/): The scratchpad directory. Exists to capture raw data, logs, and traces without polluting the synthesis layers.
- [synthesis/](./synthesis/): The logic assembly directory. Exists to process the raw workspace data into structured, arguable conclusions.
- [reflection/](./reflection/): The meta-analysis directory. Exists to apply critical thinking methods and track task friction, ensuring the agent did not hallucinate or lock into bad assumptions.
- [output/](./output/): The deliverable directory. Exists to hold the final `SPEC.md` isolated from the messy process files.
