# Core Rules
*Fundamental principles for all software projects - AI/human agnostic*

## Design Principles

- **SSOT**: Single source of truth for every piece of data/logic
- **DRY**: Extract common patterns, avoid repetition
- **YAGNI**: Add only requested features + robustness (validation, edge cases, error handling) - robustness is required, features are not
- **KISS**: Simplest solution that works correctly for all valid inputs
- **Separation-of-Concerns**: Distinct responsibilities per module
- **Composition**: Prefer composition over inheritance
- **Idempotent**: Same operation, same result, safe to retry
- **Least-Astonishment**: Behavior matches user expectations
- **Defensive-Default**: Assume bad input, validate anyway. Cost of validation << cost of bug

## Code Quality

- **Fail-Fast**: Immediate visible failure, propagate errors explicitly
- **Used-Only**: Keep only called functions and used imports
- **Type-Safe**: Full type annotations on all public APIs. Prefer stricter types (Literal, enums over strings)
- **Immutable**: Prefer immutable, mutate only when necessary
- **Complexity**: Cyclomatic <10 per function
- **Clean**: Meaningful names, single responsibility
- **Explicit**: Use named constants, clear intent
- **Scope**: Only requested changes, general solutions
- **Robust**: Handle all valid input variations (whitespace, case, empty, None, boundary values)

## File & Resource

- **Minimal-Touch**: Only files required for task
- **Request-First**: Create files only when explicitly requested
- **Paths**: Forward slash, relative, quote spaces
- **Cleanup**: Temp files, handles, connections
- **Skip**: VCS (.git, .svn), deps (node_modules, vendor, venv), build (dist, out, target), IDE (.idea, .vscode), generated (*.min.*, @generated)

## Efficiency

- **Parallel-Independent**: Run unrelated operations simultaneously
- **Sequential-Dependent**: Chain dependent operations
- **Lazy-Evaluation**: Defer work until needed
- **Cache-Reuse**: Cache results, reuse computations
- **Batch-Operations**: Group similar operations

## Security

- **Secrets**: Env vars or vault only
- **Input-Boundary**: Validate at system entry points
- **Least-Privilege**: Minimum necessary access
- **Deps-Audit**: Review before adding, keep updated
- **Defense-in-Depth**: Multiple layers, verify each control independently

## Testing

- **Coverage**: 60-90% context-adjusted
- **Isolation**: Independent tests, reproducible results
- **Integrity**: Fix code to pass tests, tests define expected behavior
- **Critical-Paths**: E2E for critical user workflows
- **Edge-Cases-Mandatory**: Always test: empty/None, whitespace-only, boundary values (0, 1, max, max+1), state combinations, invalid type coercion
- **Input-Variations**: Test normalized vs raw input (leading/trailing whitespace, case variations, unicode)
- **State-Matrix**: Test all valid state combinations where multiple states interact

## Error Handling

- **Catch-Context**: Log context, recover or propagate
- **Log-All**: Log all exceptions with context before handling
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
