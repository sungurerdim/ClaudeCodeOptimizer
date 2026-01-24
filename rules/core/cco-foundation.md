# Foundation Rules
*Core principles for all software projects - forms the base context*

## Design Principles

- **SSOT**: Single source of truth for every piece of data/logic
- **DRY**: Extract common patterns, avoid repetition
- **YAGNI**: Add only requested features + robustness (validation, edge cases, error handling) - robustness is required, features are not
- **KISS**: Simplest solution that works correctly for all valid inputs
- **3-Question-Guard**: Before adding code/feature, ask: (1) Does absence break something? (2) Does absence confuse users? (3) Is adding worth complexity cost? All NO = don't add
- **Separation-of-Concerns**: Distinct responsibilities per module
- **Composition**: Prefer composition over inheritance
- **Idempotent**: Same operation, same result, safe to retry
- **Least-Astonishment**: Behavior matches user expectations
- **Defensive-Default**: Assume bad input, validate anyway. Cost of validation << cost of bug
- **Depend-Abstract**: High-level modules depend on abstractions, not implementations

## Code Quality

- **Fail-Fast**: Immediate visible failure, propagate errors explicitly
- **Used-Only**: Keep only called functions and used imports
- **Type-Safe**: Full type annotations on all public APIs. Prefer stricter types (Literal, enums over strings)
- **Immutable**: Prefer immutable, mutate only when necessary
- **Clean**: Meaningful names, single responsibility
- **Explicit**: Use named constants, clear intent
- **Robust**: Handle all valid input variations (whitespace, case, empty, None, boundary values)
- **Async-Await**: Use async/await for I/O operations, keep async context non-blocking
- **Graceful-Shutdown**: Handle termination signals, drain connections before exit

### Complexity Thresholds

| Metric | Good | Review | Refactor |
|--------|------|--------|----------|
| Cyclomatic Complexity | 1-10 | 11-15 | 16+ |
| Cognitive Complexity | < 15 | 15-20 | 21+ |
| Method Lines | < 50 | 50-100 | 100+ |
| File Lines | < 500 | 500-1000 | 1000+ |
| Nesting Depth | <= 3 | 4 | 5+ |
| Parameters | <= 4 | 5-7 | 8+ |

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

## Robustness

- **Validate-Boundaries**: All public APIs MUST validate input at entry point
- **Type-Check-Explicit**: Verify types explicitly, don't rely on implicit coercion
- **Range-Bounds**: Numeric inputs MUST have min/max limits defined
- **String-Length-Limit**: String inputs MUST have max length limit
- **Collection-Size-Limit**: Array/list inputs MUST have max items limit
- **Explicit-Null-Check**: Check for None/null explicitly before use
- **Optional-Defaults**: Provide sensible defaults for optional parameters
- **Early-Return-Null**: Return early when null check fails
- **Graceful-Degradation**: System continues with reduced functionality on partial failure
- **Retry-Transient**: Retry transient errors (network, timeout) with exponential backoff
- **Circuit-Breaker**: Implement circuit breaker for external service calls
- **Timeout-Required**: ALL external calls MUST have explicit timeout
- **Close-Always**: Resources MUST be closed in finally block or using with/using statement
- **Pool-Connections**: Use connection pools for database/http connections

## Error Handling

- **Catch-Context**: Log context, recover or propagate
- **Log-All**: Log all exceptions with context before handling
- **User-Actionable**: Clarity + next steps for users
- **Logs-Technical**: Technical details only in logs
- **Rollback-State**: Consistent state on failure

## Documentation

- **README**: Description, setup, usage
- **CHANGELOG**: Versions with breaking changes
- **Comments-Why**: Explain why, not what
- **Examples**: Working, common use cases

## Refactoring Safety

- **Delete-Impact**: Before deleting function/class/file, identify ALL callers and dependents
- **Rename-Cascade**: Rename operation = find refs + update ALL + verify builds
- **Move-Imports**: When moving code between files, update all import statements
- **Signature-Propagate**: Changing function signature requires updating all call sites
- **Type-Cascade**: Type changes must propagate to all consumers

## UX/DX

- **Minimum-Friction**: Fewest steps to goal
- **Maximum-Clarity**: Unambiguous output
- **Predictable**: Consistent behavior
- **Fast-Feedback**: Progress indicators, incremental results
- **Step-Progress**: Multi-step operations show "Step 2/5: Building..."
- **Summary-Final**: End with summary: "Changed 3 files, added 2 tests"
- **Impact-Explain**: Show why: "This reduces bundle size by 15%"
- **Error-Actionable**: Errors include file:line AND suggested fix

## Team Collaboration

- **PR-Review**: Async code review on all changes
- **ADR**: Architecture Decision Records for significant decisions
- **CODEOWNERS**: Clear ownership via CODEOWNERS file (6+ team)
- **Branch-Protection**: Require reviews before merge (6+ team)
