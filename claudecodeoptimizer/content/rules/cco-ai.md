# AI Rules
*Portable across Claude/Codex/Gemini - AGENTS.md compatible*

## Context Optimization

- **Semantic-Density**: Concise over verbose
- **Structured**: Tables/lists over prose
- **Front-load**: Critical info first
- **Hierarchy**: H2 > H3 > bullets
- **Reference**: Cite by name, don't duplicate

## Execution Order [CRITICAL]

- **Read-First**: Read files completely before proposing any edits
- **Plan-Before-Act**: Understand full scope before any action
- **Incremental**: Complete one step fully before starting next
- **Verify**: Confirm changes match stated intent

## Decision Making

- **Challenge**: Question solutions that seem too perfect
- **Ask**: When uncertain, clarify before proceeding
- **Confidence**: State uncertainty level for non-obvious conclusions
- **Read-To-Know**: Read file contents before referencing them
- **Confirm-Intent**: Confirm user intent before making assumptions

## Reasoning Strategies

### Step-Back Prompting (Complex Tasks)

Before diving into specifics, ask the broader question first:

| Task Type | Step-Back Question |
|-----------|-------------------|
| Refactoring | "What is the architectural pattern here?" |
| Bug fix | "What is the expected behavior of this system?" |
| Security audit | "What are the trust boundaries in this codebase?" |
| Performance | "What are the critical paths in this flow?" |

### Chain of Thought (Critical Decisions)

For P0-P1 severity decisions, explicitly reason through steps:

```
1. Identify: What exactly is the issue?
2. Impact: Who/what is affected?
3. Evidence: What confirms this assessment?
4. Severity: Based on evidence, what's the appropriate level?
```

### Self-Consistency (P0 Decisions Only)

For CRITICAL severity findings, validate with multiple reasoning paths:

1. **Path A**: Analyze from attacker perspective
2. **Path B**: Analyze from system design perspective
3. **Consensus**: If both paths agree → confirm P0. If disagree → downgrade to P1

## Quality Control

- **Understand-First**: Comprehend code logic before modifying
- **Adapt**: Adjust examples to context, verify before applying
- **Verify-APIs**: Use only documented, existing APIs and features
- **Positive**: State what to do, not what to avoid
- **Motivate**: Explain why behaviors matter

## Code Generation [CRITICAL]

- **Validation-First**: Add input validation for all public APIs. Validate at boundaries, trust internals
- **Bounds-Always**: Set min/max limits on strings (max_length), numbers (ge/le), collections (max_items)
- **Whitespace-Normalize**: Strip/normalize string inputs in validators. Whitespace-only is usually invalid
- **State-Complete**: Handle all valid state combinations, not just happy path
- **Enum-Prefer**: Use enums/Literal types over raw strings for fixed values
- **Optional-Explicit**: Distinguish None (absent) vs empty string/list (present but empty)
- **Coercion-Document**: If auto-coercing types, document behavior. Prefer explicit over magic
- **Error-Rich**: Validation errors should be specific, actionable, field-level
- **Test-Edge**: Generate tests for: empty, None, whitespace, boundaries, state combinations

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
- **Accounting**: done + declined + fail = total
- **Structured**: JSON/table when needed

### Output Examples

**Error reporting:**
```
[{severity}] {issue_description} in {file_path}:{line_number}
```

**Status summary:**
```
Status: {status} | Applied: {n} | Declined: {n} | Failed: {n} | Total: {n}
```
