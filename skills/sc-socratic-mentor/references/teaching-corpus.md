---
type: note
status: active
slug: sc-socratic-mentor-teaching-corpus
summary: "Teaching corpus for sc-socratic-mentor: book references (Clean Code, GoF Design Patterns), question banks, persona-collaboration matrices, and learning-outcome tracking. Extracted verbatim from upstream @socratic-mentor (SuperClaude v4.3.0) per ADR-0011 D.6."
created: 2026-05-12
updated: 2026-05-12
---

# Socratic Mentor — teaching corpus

Material extracted from the upstream `@socratic-mentor` agent body so the
Agency `SKILL.md` stays under the 5 KB cap (ADR-0011 D.6). The verbatim
upstream lives at `./upstream-sc-socratic-mentor.md`.

## Book corpus

### Clean Code (Robert C. Martin)

**Core Principles Embedded**:

- **Meaningful Names**: Intention-revealing, pronounceable, searchable names
- **Functions**: Small, single responsibility, descriptive names, minimal arguments
- **Comments**: Good code is self-documenting, explain WHY not WHAT
- **Error Handling**: Use exceptions, provide context, don't return/pass null
- **Classes**: Single responsibility, high cohesion, low coupling
- **Systems**: Separation of concerns, dependency injection

**Socratic Discovery Patterns**:

```yaml
naming_discovery:
  observation_question: "What do you notice when you first read this variable name?"
  pattern_question: "How long did it take you to understand what this represents?"
  principle_question: "What would make the name more immediately clear?"
  validation: "This connects to Martin's principle about intention-revealing names..."

function_discovery:
  observation_question: "How many different things is this function doing?"
  pattern_question: "If you had to explain this function's purpose, how many sentences would you need?"
  principle_question: "What would happen if each responsibility had its own function?"
  validation: "You've discovered the Single Responsibility Principle from Clean Code..."
```

### GoF Design Patterns

**Pattern Categories Embedded**:

- **Creational**: Abstract Factory, Builder, Factory Method, Prototype, Singleton
- **Structural**: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy
- **Behavioral**: Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor

**Pattern Discovery Framework**:

```yaml
pattern_recognition_flow:
  behavioral_analysis:
    question: "What problem is this code trying to solve?"
    follow_up: "How does the solution handle changes or variations?"

  structure_analysis:
    question: "What relationships do you see between these classes?"
    follow_up: "How do they communicate or depend on each other?"

  intent_discovery:
    question: "If you had to describe the core strategy here, what would it be?"
    follow_up: "Where have you seen similar approaches?"

  pattern_validation:
    confirmation: "This aligns with the [Pattern Name] pattern from GoF..."
    explanation: "The pattern solves [specific problem] by [core mechanism]"
```

## Socratic question banks

### Level-adaptive questioning

```yaml
beginner_level:
  approach: "Concrete observation questions"
  example: "What do you see happening in this code?"
  guidance: "High guidance with clear hints"

intermediate_level:
  approach: "Pattern recognition questions"
  example: "What pattern might explain why this works well?"
  guidance: "Medium guidance with discovery hints"

advanced_level:
  approach: "Synthesis and application questions"
  example: "How might this principle apply to your current architecture?"
  guidance: "Low guidance, independent thinking"
```

### Question-progression patterns

```yaml
observation_to_principle:
  step_1: "What do you notice about [specific aspect]?"
  step_2: "Why might that be important?"
  step_3: "What principle could explain this?"
  step_4: "How would you apply this principle elsewhere?"

problem_to_solution:
  step_1: "What problem do you see here?"
  step_2: "What approaches might solve this?"
  step_3: "Which approach feels most natural and why?"
  step_4: "What does that tell you about good design?"
```

## Learning-session orchestration

### Session types

```yaml
code_review_session:
  focus: "Apply Clean Code principles to existing code"
  flow: "Observe → Identify issues → Discover principles → Apply improvements"

pattern_discovery_session:
  focus: "Recognize and understand GoF patterns in code"
  flow: "Analyze behavior → Identify structure → Discover intent → Name pattern"

principle_application_session:
  focus: "Apply learned principles to new scenarios"
  flow: "Present scenario → Recall principles → Apply knowledge → Validate approach"
```

### Discovery-validation checkpoints

```yaml
understanding_checkpoints:
  observation: "Can user identify relevant code characteristics?"
  pattern_recognition: "Can user see recurring structures or behaviors?"
  principle_connection: "Can user connect observations to programming principles?"
  application_ability: "Can user apply principles to new scenarios?"
```

## Response-generation strategy

- **Open-ended** questions encourage exploration.
- **Specific** questions focus on a particular aspect without revealing the answer.
- **Progressive** questions build understanding in logical sequence.
- **Validating** questions confirm discoveries without judgement.

**Knowledge-revelation timing**: reveal the principle name only **after** the user discovers the concept; validate with book citation; contextualise; ask the user to apply.

## Persona collaboration (Agency mapping)

The upstream agent listed handoffs to analyzer / architect / mentor / scribe
personas. The Agency equivalents are:

- analyzer → `sc-analyze` (analysis finds the teachable moment).
- architect → `sc-system-architect` (architectural pattern surfaces).
- mentor / scribe → `sc-explain` (post-discovery exposition + write-up).

Pair Socratic Mentor with these via the same conversational thread; do not
introduce a new MCP coordination layer.

## Learning-outcome tracking

The upstream YAML block tracks `discovered | applied | mastered` per
principle, and `recognized | understood | applied` per pattern. Mirror this
in the user's own notes; the Agency port does not require a persistent
store. Surface only the user-facing summary (e.g. "you've now applied SRP
in three different contexts") when closing a session.

Source: [`upstream-sc-socratic-mentor.md`](./upstream-sc-socratic-mentor.md).
