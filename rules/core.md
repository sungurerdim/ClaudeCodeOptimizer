# Core Rules
*Fundamental principles for all software projects - AI/human agnostic*

## Design Principles

- **SSOT**: Single source of truth for every piece of data/logic
- **DRY**: Extract common patterns, avoid repetition
- **YAGNI**: Add only requested features + robustness (validation, edge cases, error handling) - robustness is required, features are not
- **KISS**: Simplest solution that works correctly for all valid inputs
- **3-Question-Guard**: Before adding code/feature, ask: (1) Does absence break something? (2) Does absence confuse users? (3) Is adding worth complexity cost? All NO → don't add
- **Separation-of-Concerns**: Distinct responsibilities per module
- **Composition**: Prefer composition over inheritance
- **Idempotent**: Same operation, same result, safe to retry
- **Least-Astonishment**: Behavior matches user expectations
- **Defensive-Default**: Assume bad input, validate anyway. Cost of validation << cost of bug
- **Depend-Abstract**: High-level modules depend on abstractions, not implementations. Enables testing and flexibility
- **Single-Instance**: For shared state (config, connection pools, caches), use single instance per process. Not universal—apply only when state must be globally shared

## Code Quality

- **Fail-Fast**: Immediate visible failure, propagate errors explicitly
- **Used-Only**: Keep only called functions and used imports
- **Type-Safe**: Full type annotations on all public APIs. Prefer stricter types (Literal, enums over strings)
- **Immutable**: Prefer immutable, mutate only when necessary
- **Clean**: Meaningful names, single responsibility
- **Explicit**: Use named constants, clear intent
- **Scope**: Only requested changes, general solutions
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
| Nesting Depth | ≤ 3 | 4 | 5+ |
| Parameters | ≤ 4 | 5-7 | 8+ |

### Maintainability Index

| Score | Rating | Action |
|-------|--------|--------|
| 85-100 | Green | Maintain |
| 65-84 | Yellow | Monitor |
| 20-64 | Orange | Refactor |
| 0-19 | Red | Critical priority |

**Target**: MI >= 65 minimum, >= 85 ideal

### Code Duplication

| Duplication | Status | Action |
|-------------|--------|--------|
| 0-5% | Excellent | Maintain |
| 5-10% | Good | Monitor |
| 10-15% | Review | Extract common |
| 15%+ | Refactor | Required |

**Detection**: Minimum 10 LOC, 75% similarity threshold

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

*Based on OWASP Top 10:2025*

### Access Control (OWASP A01)
- **Access-Control-Enforce**: Deny by default, require explicit grants. Verify permissions server-side on every request
- **Least-Privilege**: Minimum necessary access for users and services
- **RBAC-Implement**: Role-based access control with principle of least privilege
- **SSRF-Prevent**: Validate URLs, block internal IPs (10.x, 172.16.x, 192.168.x, 127.x), use allowlists

### Configuration Security (OWASP A02)
- **Safe-Defaults**: Production defaults must be secure: debug off, verbose errors off, restrictive CORS, no wildcard origins
- **Secrets**: Env vars or vault only, never in code or version control
- **Error-Disclosure**: Show generic error messages to users. Keep stack traces, internal paths, system details server-side
- **Security-Headers**: X-Frame-Options (DENY), HSTS (max-age>=31536000), CSP, X-Content-Type-Options (nosniff)

### Supply Chain Security (OWASP A03)
- **Lockfile-Required**: Use dependency lockfile, pin versions, no floating ranges
- **Deps-Audit**: Review dependencies before adding, prefer well-maintained packages
- **Deps-Minimal**: Minimize dependencies, avoid unnecessary packages

### Input & Output (OWASP A04, A05)
- **Input-Boundary**: Validate ALL user input at system entry points. Use schema validation
- **Defense-in-Depth**: Multiple layers, verify each control independently
- **Output-Encode**: Encode output based on context (HTML, URL, JS, CSS)
- **Deserialize-Safe**: Deserialize only trusted data using safe formats (JSON). Never pickle/yaml.load/eval

### Authentication (OWASP A07)
- **Session-Security**: Secure + HttpOnly + SameSite=Lax/Strict cookies, token TTL with refresh strategy, logout invalidates server-side
- **Password-Security**: Store passwords with bcrypt/argon2/scrypt using appropriate cost factor. Salt per-password
- **MFA-Support**: Support TOTP/WebAuthn for sensitive accounts. Don't rely on SMS alone
- **Auth-Identical-Errors**: Use identical auth failure messages (prevents user enumeration)

### Logging & Monitoring (OWASP A09)
- **Audit-Log**: Immutable logging for security-critical actions. Include who, what, when, from-where
- **Redact-Sensitive**: Redact/mask secrets, tokens, credentials, PII in all output
- **Alert-On-Anomaly**: Alert on suspicious patterns (failed logins, unusual access patterns)

### Error Handling (OWASP A10)
- **Error-Graceful**: Handle exceptional conditions gracefully, fail secure (deny access on error)
- **Error-No-Leak**: Never expose internal state, paths, or stack traces to users
- **Fail-Closed**: On security-related errors, default to deny access

### Data Protection
- **Data-Minimization**: Collect and store only necessary data. Each field requires justification
- **Encrypt-Transit**: TLS 1.2+ for all network communication
- **Encrypt-Rest**: AES-256-GCM for sensitive data at rest
- **Timeout-Required**: All external calls must have explicit timeout. Prevent resource exhaustion

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
- **80/20-Priority**: Prioritize by impact × effort: Quick Win (high impact, low effort) → Moderate (high impact, medium effort) → Complex (medium impact) → Major (low impact or high effort)

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
- **Diff-Before-Destruct**: Show diff before delete/overwrite operations
- **Error-Actionable**: Errors include file:line AND suggested fix

## Functional Completeness

- **Complete-CRUD**: Every entity MUST have Create, Read, Update, Delete operations
- **List-Pagination**: Collection endpoints MUST support pagination (offset/limit or cursor)
- **Filter-Support**: List endpoints SHOULD support filtering on indexed fields
- **Sort-Support**: List endpoints SHOULD support sorting with sensible defaults
- **Soft-Delete**: Prefer soft delete (is_deleted flag) over hard delete for audit trail
- **Empty-Input**: Handle empty strings, empty lists, empty dicts explicitly
- **Boundary-Values**: Test and handle min, max, 0, 1, max+1 values
- **Whitespace-Only**: Treat whitespace-only strings as empty (strip + check)
- **Null-vs-Empty**: Distinguish None (absent) from empty (present but empty)
- **Not-Found-Explicit**: Return 404 with clear message when resource not found
- **Conflict-Handling**: Return 409 when duplicate/conflict occurs with explanation
- **Validation-Detailed**: Return 400 with field-level validation errors
- **Auth-Distinction**: Distinguish 401 (not authenticated) from 403 (not authorized)
- **State-Machine-Documented**: Document valid states and transitions
- **Transition-Validation**: Reject invalid state transitions with clear error
- **Concurrent-Safe**: Use optimistic locking or versioning for concurrent updates
- **Health-Check**: Include /health or /healthz endpoint
- **Referential-Integrity**: Foreign keys enforced at database level
- **Transaction-Boundaries**: Database operations grouped in transactions appropriately

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
- **Connect-vs-Read**: Separate connection timeout from read timeout
- **Timeout-Configurable**: Timeouts should be configurable (env var or config)
- **Close-Always**: Resources MUST be closed in finally block or using with/using statement
- **Pool-Connections**: Use connection pools for database/http connections
- **Limit-Concurrent**: Limit concurrent connections to prevent resource exhaustion
- **Race-Condition-Prevent**: Identify and prevent race conditions
- **Deadlock-Prevent**: Acquire locks in consistent order
- **Config-Validate**: Validate configuration at startup, fail fast
- **Env-Required-Check**: Check required environment variables at startup
