# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records documenting key architectural decisions made in the ClaudeCodeOptimizer project.

## What is an ADR?

An Architecture Decision Record (ADR) captures an important architectural decision made along with its context and consequences. ADRs help teams understand why certain decisions were made and provide valuable context for future development.

## Index

- [ADR-001: Marker-based CLAUDE.md System](001-marker-based-claude-md.md)
- [ADR-002: Zero Pollution Design](002-zero-pollution-design.md)
- [ADR-003: Progressive Skill Loading](003-progressive-skill-loading.md)

## ADR Template

When creating a new ADR, use the following template:

```markdown
# ADR-XXX: Title

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
What is the issue we're seeing that is motivating this decision or change?
Include:
- Current situation
- Forces at play (technical, business, user needs)
- Constraints

## Decision
What is the change that we're proposing and/or doing?
- Clear statement of the decision
- Key implementation details

## Consequences
What becomes easier or more difficult to do because of this change?

### Positive
- Benefit 1
- Benefit 2

### Negative
- Trade-off 1
- Trade-off 2

### Neutral
- Impact 1
- Impact 2

## Alternatives Considered
What other options were considered and why were they rejected?

### Alternative 1: [Name]
- Description
- Why rejected

### Alternative 2: [Name]
- Description
- Why rejected

## Implementation Notes
- Key technical details
- Migration considerations
- Testing approach

## References
- Related ADRs
- External documentation
- Discussion threads
```

## Naming Convention

ADRs are numbered sequentially with zero-padded three digits:
- `001-marker-based-claude-md.md`
- `002-zero-pollution-design.md`
- `003-progressive-skill-loading.md`

## Lifecycle

1. **Proposed**: Under discussion, not yet implemented
2. **Accepted**: Approved and implemented
3. **Deprecated**: No longer recommended but still in use
4. **Superseded**: Replaced by a newer ADR (link to replacement)

## Best Practices

1. **One Decision Per ADR**: Keep each ADR focused on a single decision
2. **Write in Past Tense**: Decisions are statements of fact
3. **Be Specific**: Include concrete details and examples
4. **Document Trade-offs**: Honest assessment of pros and cons
5. **Link Related ADRs**: Create a web of related decisions
6. **Update Status**: Keep ADR status current
7. **Immutability**: Don't edit old ADRs - create new ones that supersede them

## Contributing

When making significant architectural decisions:

1. Create a new ADR using the template
2. Number it sequentially
3. Fill in all sections
4. Submit as part of your PR
5. Update this index

## Questions?

For questions about ADRs or architectural decisions, refer to:
- [Project Architecture Documentation](../ARCHITECTURE.md) (if it exists)
- [CONTRIBUTING.md](../../CONTRIBUTING.md) (if it exists)
- GitHub Issues/Discussions
