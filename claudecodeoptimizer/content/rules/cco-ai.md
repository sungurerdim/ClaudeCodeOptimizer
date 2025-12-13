# AI Rules
*Portable across Claude/Codex/Gemini - AGENTS.md compatible*

## Context Optimization

- **Semantic-Density**: Concise over verbose
- **Structured**: Tables/lists over prose
- **Front-load**: Critical info first
- **Hierarchy**: H2 > H3 > bullets
- **Reference**: Cite by name, don't duplicate

## Execution Order [CRITICAL]

- **Read-First**: NEVER propose edits to unread files
- **Plan-Before-Act**: Understand full scope before any action
- **Incremental**: Complete one step fully before starting next
- **Verify**: Confirm changes match stated intent

## Decision Making

- **Challenge**: Question solutions that seem too perfect
- **Ask**: When uncertain, clarify before proceeding
- **Confidence**: State uncertainty level for non-obvious conclusions
- **No-Guessing**: Never guess file contents without reading
- **No-Assume**: Never assume user intent without confirmation

## Quality Control

- **Understand-First**: No vibe coding
- **Adapt**: Examples to context, don't copy blind
- **No-Hallucination**: Only existing APIs/features
- **Positive**: What to do, not what to avoid
- **Motivate**: Explain why behaviors matter

## Status Updates

- **Announce-Before**: State action before starting
- **Progress-Track**: Starting > In progress > Completed
- **Transitions**: Clear phase signals
- **Visible-State**: User always knows current state

## Multi-Model

- **Agnostic**: No model-specific syntax
- **Graceful**: Account for different capabilities
- **Portable**: Patterns work across models

## Output Standards

- **Error-Format**: `[SEVERITY] {What} in {file:line}`
- **Status-Values**: OK / WARN / FAIL
- **Accounting**: done + skip + fail = total
- **Structured**: JSON/table when needed
