# Core Rules
*Fundamental principles for all software projects - AI/human agnostic*

## Design Principles

- **SSOT**: Single source of truth for every piece of data/logic
- **DRY**: Don't repeat yourself, extract common patterns
- **YAGNI**: Only build what's needed now, not hypotheticals
- **KISS**: Simplest solution that works
- **Separation-of-Concerns**: Distinct responsibilities per module
- **Composition**: Prefer composition over inheritance
- **Idempotent**: Same operation, same result, safe to retry
- **Least-Astonishment**: Behavior matches user expectations

## Code Quality

- **Fail-Fast**: Immediate visible failure, no silent fallbacks
- **No-Orphans**: Every function called, every import used
- **Type-Safe**: Annotations where supported
- **Immutable**: Prefer immutable, mutate only when necessary
- **Complexity**: Cyclomatic <10 per function
- **Clean**: Meaningful names, single responsibility
- **Explicit**: No magic values, clear intent
- **Scope**: Only requested changes, general solutions
- **Defensive**: Validate assumptions, handle edge cases

## File & Resource

- **Minimal-Touch**: Only files required for task
- **No-Unsolicited**: Never create files unless requested
- **Paths**: Forward slash, relative, quote spaces
- **Cleanup**: Temp files, handles, connections
- **Skip**: VCS (.git, .svn), deps (node_modules, vendor, venv), build (dist, out, target), IDE (.idea, .vscode), generated (*.min.*, @generated)

## Efficiency

- **Parallel-Independent**: Run unrelated operations simultaneously
- **Sequential-Dependent**: Chain dependent operations
- **Lazy-Evaluation**: Defer work until needed
- **Cache-Reuse**: Don't recompute, cache results
- **Batch-Operations**: Group similar operations

## Security

- **Secrets**: Env vars or vault only
- **Input-Boundary**: Validate at system entry points
- **Least-Privilege**: Minimum necessary access
- **Deps-Audit**: Review before adding, keep updated
- **Defense-in-Depth**: Multiple layers, don't trust single control

## Testing

- **Coverage**: 60-90% context-adjusted
- **Isolation**: No inter-test deps, reproducible
- **Integrity**: Never edit tests to pass code
- **Critical-Paths**: E2E for critical workflows

## Error Handling

- **Catch-Context**: Log context, recover or propagate
- **No-Swallow**: Never swallow exceptions silently
- **User-Actionable**: Clarity + next steps for users
- **Logs-Technical**: Technical details only in logs
- **Rollback-State**: Consistent state on failure

## Analysis

- **Architecture-First**: Before fixing symptoms, understand system design
- **Dependency-Mapping**: Trace impact through component relationships
- **Root-Cause-Hunt**: Ask "why does this pattern exist?" not just "what's wrong?"
- **Cross-Cutting-Concerns**: Check for issues that span multiple modules
- **Systemic-Patterns**: Identify recurring problems indicating design flaws

## Documentation

- **README**: Description, setup, usage
- **CHANGELOG**: Versions with breaking changes
- **Comments-Why**: Explain why, not what
- **Examples**: Working, common use cases

## Workflow

- **Match-Conventions**: Follow existing patterns
- **Reference-Integrity**: Find ALL refs, update, verify
- **Decompose**: Break complex tasks into steps
- **SemVer**: MAJOR.MINOR.PATCH

## UX/DX

- **Minimum-Friction**: Fewest steps to goal
- **Maximum-Clarity**: Unambiguous output
- **Predictable**: Consistent behavior
- **Fast-Feedback**: Progress indicators, incremental results
