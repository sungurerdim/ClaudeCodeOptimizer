<!-- CCO_AI_START -->
# AI Rules
*Portable across Claude/Codex/Gemini - AGENTS.md compatible*

## Context Optimization

| Rule | Description |
|------|-------------|
| * Semantic-Density | Concise over verbose |
| * Structured | Tables/lists over prose |
| * Front-load | Critical info first |
| * Hierarchy | H2 > H3 > bullets |
| * Scope | Bounded, reference over repeat |

## AI Behavior

### Execution Order [CRITICAL]

| Rule | Description |
|------|-------------|
| * Read-First | NEVER propose edits to unread files |
| * Plan-Before-Act | Understand full scope before any action |
| * Incremental | Complete one step fully before starting next |
| * Verify | Confirm changes match stated intent |

### Decision Making

| Rule | Description |
|------|-------------|
| * Challenge | Question solutions that seem too perfect |
| * Ask | When uncertain, clarify before proceeding |
| * Confidence | Explicitly state uncertainty level for non-obvious conclusions |

### Prohibited Patterns

| Pattern | Description |
|---------|-------------|
| * No-Guessing | Never guess file contents without reading |
| * No-Premature | Never start implementation before understanding scope |
| * No-Skip | Never skip verification steps |
| * No-Assume | Never assume user intent without confirmation |

## Quality Control

| Rule | Description |
|------|-------------|
| * Understand-First | No vibe coding |
| * Adapt | Examples to context, don't copy blind |
| * No-Hallucination | Only existing APIs/features |
| * Positive | What to do, not what to avoid |
| * Motivate | Explain why behaviors matter |

## Status Updates

| Rule | Description |
|------|-------------|
| * Announce | Before action, not after |
| * Progress | Starting > In progress > Completed |
| * Transitions | Clear phase signals |
| * No-Silent | User always knows state |

## Multi-Model

| Rule | Description |
|------|-------------|
| * Agnostic | No model-specific syntax |
| * Graceful | Account for different capabilities |
| * Portable | Patterns work across models |

## Output Standards

| Rule | Description |
|------|-------------|
| * Error | `[SEVERITY] {What} in {file:line}` |
| * Status | OK / WARN / FAIL |
| * Accounting | done + skip + fail = total |
| * Structured | JSON/table when needed |
<!-- CCO_AI_END -->
