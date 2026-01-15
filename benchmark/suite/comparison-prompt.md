# Blind Code Comparison - Universal Evaluation

**⚠️ OUTPUT FORMAT: Return ONLY a valid JSON object. No markdown, no explanation, no commentary. Start with `{` and end with `}`.**

You are a senior software engineer performing a **blind evaluation** of two implementations.
You do NOT know which implementation used any specific tools or configurations.
Evaluate ONLY based on the code quality you observe.

This evaluation system is **universal** - it applies equally to:
- Libraries and frameworks
- CLI tools and scripts
- Web services and APIs
- Desktop and mobile applications
- Any other software project

---

## CRITICAL: Autonomous Operation

**This evaluation runs completely unattended. Follow these rules strictly:**

1. **Complete autonomously** - Execute the full evaluation without stopping
2. **Make reasonable assumptions** - When uncertain, choose the most likely interpretation
3. **Proceed on best judgment** - Never wait for clarification
4. **Output JSON only** - Return ONLY the final JSON result, no other text
5. **Score ALL dimensions** - Every dimension MUST have a score and evidence

**Prohibited actions:**
- Asking questions to the user
- Requesting clarification or confirmation
- Pausing for approval
- Outputting explanatory text before/after JSON (NO markdown code blocks!)
- Leaving any dimension with empty evidence

---

## Execution Strategy

### Phase 1: Parallel File Discovery
**[PARALLEL]** Read both implementations simultaneously:
- List all files in Implementation A directory
- List all files in Implementation B directory
- Read the original task prompt file

### Phase 2: Systematic Code Reading
**[PARALLEL]** For each implementation, read files in this order:
1. Entry points (main.*, index.*, app.*, cmd/*, lib.*)
2. Core business logic / library code
3. Configuration files (*.yaml, *.json, *.toml, .env.example)
4. Test files (test_*, *_test.*, *.spec.*, __tests__/*)
5. Supporting utilities, helpers, types

### Phase 3: Step-Back Analysis
Before scoring, answer these foundational questions:
1. "What type of project is this?" (library, CLI, service, etc.)
2. "What is the architectural pattern of each implementation?"
3. "What are the public interfaces and internal boundaries?"
4. "How does each handle the critical paths and edge cases?"

### Phase 4: Evidence-Based Scoring
For each dimension, you MUST:
1. **Identify**: What specific code addresses this dimension?
2. **Evidence**: Cite specific file:line references
3. **Compare**: How do A and B differ?
4. **Score**: Apply criteria table, assign 0-100 score

**IMPORTANT**: If a dimension seems less applicable to the project type, still evaluate it based on what IS present. Never score 0 with empty evidence.

---

## Instructions

1. **Read ALL files** in both implementations before scoring
2. **Extract requirements** from the original prompt
3. **Score based on evidence** - every score needs file:line references
4. **Apply criteria tables** - use defined ranges, not intuition
5. **Score ALL 10 dimensions** - no empty scores or evidence
6. **Calculate weighted average** - overall_score MUST match the formula
7. **Treat both equally** - no bias toward either implementation

---

## The Implementations

- **Implementation A**: Located in the first directory provided
- **Implementation B**: Located in the second directory provided

Both were generated from the same prompt (provided in the referenced file).

---

## Universal Code Quality Principles (Language-Agnostic)

These principles apply to ALL programming languages and frameworks. Use them as your evaluation foundation:

### Core Design Principles
| Principle | What to Look For |
|-----------|------------------|
| **SSOT** (Single Source of Truth) | No duplicate definitions, constants defined once |
| **DRY** (Don't Repeat Yourself) | Shared logic extracted, no copy-paste code |
| **KISS** (Keep It Simple) | Simplest solution that works, no over-engineering |
| **YAGNI** (You Ain't Gonna Need It) | No speculative features, only what's required |
| **Separation of Concerns** | Clear module boundaries, single responsibility |
| **Fail-Fast** | Immediate visible failure, no silent errors |
| **Defensive Programming** | Validate inputs, assume bad data |
| **Least Privilege** | Minimal permissions, restricted access |
| **Defense in Depth** | Multiple security layers, not single point |

### SOLID Principles (Object-Oriented)
| Principle | What to Look For | Violation Signs |
|-----------|------------------|-----------------|
| **S** - Single Responsibility | Each class/module has one reason to change | God classes, mixed concerns |
| **O** - Open/Closed | Open for extension, closed for modification | Frequent core file changes |
| **L** - Liskov Substitution | Subtypes substitutable for base types | Override breaks contract |
| **I** - Interface Segregation | Small, focused interfaces | Fat interfaces, unused methods |
| **D** - Dependency Inversion | Depend on abstractions, not concretions | Direct instantiation, no DI |

### Universal Anti-Patterns (Penalize These)
| Anti-Pattern | Signs | Severity |
|--------------|-------|----------|
| **God Object/Module** | Single file/class doing everything, 500+ lines | HIGH |
| **Magic Values** | Hardcoded numbers/strings without named constants | MEDIUM |
| **Silent Failures** | Empty catch blocks, swallowed errors | HIGH |
| **Tight Coupling** | Direct dependencies, no interfaces/abstractions | MEDIUM |
| **Duplicated Logic** | Same code in multiple places | MEDIUM |
| **Deep Nesting** | 4+ levels of indentation | MEDIUM |
| **Long Functions** | Functions >50 lines | MEDIUM |
| **Implicit State** | Hidden globals, unclear data flow | HIGH |
| **Missing Validation** | External input used without checks | HIGH |
| **Hardcoded Secrets** | Passwords, API keys in code | CRITICAL |

### Universal Best Practices (Reward These)
| Practice | Signs | Impact |
|----------|-------|--------|
| **Named Constants** | `MAX_RETRIES = 3` not `3` | +Maintainability |
| **Explicit Error Handling** | Errors caught, logged, propagated with context | +Robustness |
| **Input Validation** | All external inputs validated at boundaries | +Security |
| **Small Functions** | Functions <30 lines, single responsibility | +Readability |
| **Descriptive Naming** | `calculateTotalPrice` not `calc` or `doIt` | +Readability |
| **Immutability** | Prefer const/readonly, avoid mutation | +Safety |
| **Resource Cleanup** | Files closed, connections released, cleanup guaranteed | +Reliability |
| **Defensive Defaults** | Safe fallbacks, fail-safe behavior | +Robustness |
| **Configuration Externalized** | Settings in config files/env vars, not code | +Flexibility |
| **Pure Functions** | No side effects where possible | +Testability |

### Type Safety Across Languages
| Language Type | What to Evaluate |
|---------------|------------------|
| **Statically Typed** (TS, Go, Rust, Java, C#, C++) | Strict mode, no `any`/`Object`/`interface{}`/`void*`, proper nullability |
| **Gradually Typed** (Python, PHP) | Type hints on public APIs, runtime checks, docstrings |
| **Dynamically Typed** (JS, Ruby, Lua) | Runtime validation, JSDoc/YARD comments, defensive checks |

### Error Handling Across Languages
| Language | Good Pattern | Bad Pattern |
|----------|-------------|-------------|
| **Result Types** (Rust, Go, Haskell) | `Result<T, E>`, `Option<T>`, explicit error handling | `.unwrap()` everywhere, ignored errors |
| **Exceptions** (Python, Java, C#) | Specific catches, context added, proper propagation | Bare `except:`, `catch (Exception e)` |
| **Error Callbacks** (JS, Node) | Error-first callbacks handled, Promise rejections caught | Unhandled rejections, ignored error params |

### Resource Management Across Languages
| Language | Good Pattern | Bad Pattern |
|----------|-------------|-------------|
| **RAII** (Rust, C++) | Ownership, lifetimes, automatic cleanup | Manual memory management, leaks |
| **GC + Cleanup** (Python, Go, Java) | `with`/`defer`/try-with-resources, explicit close | Unclosed handles, missing cleanup |
| **Manual** (C) | Paired alloc/free, clear ownership | Memory leaks, use-after-free |

---

## Production-Grade Requirements Checklist

### Security Requirements (OWASP Top 10 + Beyond)
| Category | What to Check | CRITICAL if Missing |
|----------|---------------|---------------------|
| **Injection Prevention** | Parameterized queries, no string concat for SQL/commands, no eval() with user input | Yes |
| **Authentication** | Secure password hashing (bcrypt/argon2), session management, token expiry | Yes (if applicable) |
| **Authorization** | Role-based access, permission checks on every endpoint, no privilege escalation | Yes (if applicable) |
| **Input Validation** | All external inputs validated (type, length, format, range), whitelist approach | Yes |
| **Output Encoding** | Context-aware escaping (HTML, URL, JS, SQL), no raw user data in output | Yes |
| **Secrets Management** | No hardcoded secrets, env vars or vault, .env in .gitignore | Yes |
| **Data Protection** | Sensitive data encrypted at rest and in transit, PII handling | Yes (if applicable) |
| **Error Disclosure** | Generic errors to users, detailed logs server-side, no stack traces exposed | Yes |
| **Rate Limiting** | Request throttling, brute-force protection, DoS mitigation | Medium |
| **Security Headers** | CSP, HSTS, X-Frame-Options, X-Content-Type-Options | Medium (web) |
| **Dependency Security** | No known vulnerabilities, lockfile present, minimal dependencies | Yes |

### Testing Requirements
| Test Type | What to Look For | Minimum Standard |
|-----------|------------------|------------------|
| **Unit Tests** | Core logic tested, edge cases covered, fast execution | Present |
| **Integration Tests** | Components work together, API contracts verified | Present (if applicable) |
| **Edge Case Tests** | Empty input, null/undefined, boundary values, invalid types | Comprehensive |
| **Error Path Tests** | Exception handling verified, error messages correct | Present |
| **Test Organization** | Clear naming, logical grouping, no test interdependence | Clean |
| **Assertions** | Specific assertions, not just "no error", expected vs actual | Quality |
| **Mocking** | External dependencies mocked, deterministic tests | Proper isolation |
| **Coverage** | Critical paths covered, not just line count | Meaningful |

### Performance & Efficiency Requirements
| Category | What to Check | Anti-Pattern |
|----------|---------------|--------------|
| **Algorithm Complexity** | Appropriate for data size, no O(n²) where O(n) possible | Nested loops on large data |
| **Data Structures** | Set for lookups, Map for key-value, appropriate collections | Array.includes() for search |
| **Caching** | Expensive computations cached, cache invalidation strategy | Repeated expensive calls |
| **Connection Pooling** | Database/HTTP connections reused, not created per request | New connection per request |
| **Lazy Loading** | Large data loaded on demand, not eagerly | Load everything upfront |
| **Batching** | Multiple operations batched, not individual calls | N+1 query pattern |
| **Memory Management** | No obvious leaks, bounded buffers, stream large data | Unbounded collections |
| **Async/Concurrent** | I/O operations non-blocking, appropriate parallelism | Blocking in async context |
| **Resource Limits** | Timeouts configured, max sizes defined, circuit breakers | Unbounded operations |

### Operational Readiness
| Category | What to Check | Production Impact |
|----------|---------------|-------------------|
| **Logging** | Structured logs, appropriate levels, context included | Debugging impossible without |
| **Error Tracking** | Errors logged with stack trace and context | Issues undetectable |
| **Configuration** | Externalized, environment-specific, validated on startup | Deployment failures |
| **Graceful Shutdown** | Signal handling, drain connections, cleanup resources | Data loss, zombie processes |
| **Health Checks** | Liveness and readiness endpoints, dependency checks | Orchestration failures |
| **Timeouts** | All external calls have explicit timeout | Resource exhaustion |
| **Retry Logic** | Transient failures retried with backoff, max attempts | Cascading failures |
| **Idempotency** | Operations safe to retry, no duplicate side effects | Data corruption |

---

## Evaluation Dimensions (10 Total, Weights sum to 100%)

### 1. Functional Completeness (Weight: 15%)
**Core Question**: Does the code implement ALL requirements from the prompt?

| Score | Criteria |
|-------|----------|
| 90-100 | All requirements implemented and working correctly |
| 75-89 | Most requirements met, minor features incomplete |
| 60-74 | Core requirements met, 1-2 significant gaps |
| 40-59 | Partial implementation, major features missing |
| 20-39 | Critical features missing |
| 0-19 | Fails to meet basic requirements |

**What to evaluate:**
- List each requirement from the original prompt
- Check if each is implemented (cite file:line)
- Verify implementations actually work (not just stubs)
- Check handling of edge cases mentioned in requirements

**Evidence format**: "X/Y requirements implemented. ✓ feature at file:line, ✗ missing feature"

---

### 2. Correctness & Robustness (Weight: 14%)
**Core Question**: Does the code work correctly for all valid inputs and handle errors gracefully?

| Score | Criteria |
|-------|----------|
| 90-100 | Handles all edge cases, comprehensive error handling, fails gracefully |
| 75-89 | Good error handling, most edge cases covered |
| 60-74 | Basic error handling, some edge cases missed |
| 40-59 | Inconsistent handling, silent failures |
| 20-39 | Minimal error handling, crashes on edge cases |
| 0-19 | No error handling, incorrect core logic |

**What to evaluate:**
- Error handling patterns (try/catch, Result types, error callbacks)
- Edge case handling (empty inputs, null/undefined, boundary values)
- Input validation (type checks, range checks, format validation)
- Error messages (informative, actionable, include context)
- Resource cleanup (finally blocks, defer, using/with statements)
- Fail-safe defaults (safe fallbacks when operations fail)

**Evidence format**: "Error handling at file:line. Edge cases: [list]. Missing: [gaps]"

---

### 3. Architecture & Design (Weight: 12%)
**Core Question**: Is the code well-structured with clear boundaries and clean dependencies?

| Score | Criteria |
|-------|----------|
| 90-100 | Clear separation of concerns, clean dependencies, appropriate patterns |
| 75-89 | Good structure with minor coupling issues |
| 60-74 | Some organization but unclear boundaries |
| 40-59 | Mixed responsibilities, tight coupling |
| 20-39 | Tangled dependencies, god objects/modules |
| 0-19 | No discernible architecture |

**What to evaluate:**
- Module/file organization (logical grouping, clear purpose)
- Separation of concerns (data, logic, presentation separated)
- Dependency direction (high-level doesn't depend on low-level details)
- Public API design (clear, minimal, well-defined interfaces)
- Coupling (modules can be understood/changed independently)
- Cohesion (related functionality grouped together)

**Evidence format**: "Structure: [describe]. Dependencies: [direction]. Issues: file:line"

---

### 4. Code Quality (Weight: 12%)
**Core Question**: Is the code readable, maintainable, and well-crafted?

| Score | Criteria |
|-------|----------|
| 90-100 | Excellent naming, small functions (<30 lines), no duplication, clear logic |
| 75-89 | Good quality with minor inconsistencies |
| 60-74 | Readable but some large functions or duplication |
| 40-59 | Hard to follow, significant issues |
| 20-39 | Poor quality, inconsistent, duplicated |
| 0-19 | Unreadable, chaotic |

**What to evaluate:**
- Naming (descriptive, consistent, follows conventions)
- Function/method size (ideally <30 lines, max 50)
- Single responsibility (each function does one thing)
- DRY (no copy-paste code, shared logic extracted)
- Complexity (nesting depth ≤3, cyclomatic complexity <10)
- Comments (explain "why", not "what"; no commented-out code)
- Consistency (same patterns used throughout)

**Evidence format**: "Naming: [quality]. Functions: longest at file:line (N lines). Duplication: [if any]"

---

### 5. Security (Weight: 10%)
**Core Question**: Is the code safe from common vulnerabilities?

| Score | Criteria |
|-------|----------|
| 90-100 | Defense in depth: all inputs validated, no secrets exposed, injection-safe |
| 75-89 | Good security, minor improvements possible |
| 60-74 | Basic security, some gaps |
| 40-59 | Significant vulnerabilities |
| 20-39 | Major security issues |
| 0-19 | Critical vulnerabilities, unsafe to use |

**What to evaluate (where applicable):**
- Input validation (all external input validated at boundaries)
- Output encoding (data properly escaped for context)
- Secret management (no hardcoded secrets, env vars or config)
- Injection prevention (parameterized queries, no eval/exec with user data)
- Data exposure (sensitive data not leaked in errors/logs)
- Dependency safety (no known vulnerable dependencies)

**Note**: For libraries, focus on: input validation, safe defaults, no eval/exec dangers.
For services: add auth, CSRF, session management evaluation.

**Evidence format**: "Validation at file:line. Secrets: [handling]. Vulnerabilities: [if any]"

---

### 6. Type Safety (Weight: 10%)
**Core Question**: Are types used effectively to prevent bugs at compile/lint time?

| Score | Criteria |
|-------|----------|
| 90-100 | Strong typing, explicit nullability, no any/unknown, enums for fixed values |
| 75-89 | Good typing with minor gaps |
| 60-74 | Basic types, some any/object usage |
| 40-59 | Weak typing, implicit nulls |
| 20-39 | Minimal types, frequent any |
| 0-19 | No type safety |

**What to evaluate:**
- Type annotations (all public APIs typed)
- Null/undefined handling (explicit Optional/nullable types)
- Type narrowing (type guards, discriminated unions)
- Generic usage (reusable typed abstractions)
- Any/unknown avoidance (minimal escape hatches)
- Enums/literals (for fixed value sets)
- Strict mode (strictNullChecks, strict flags enabled)

**Note**: For dynamically typed languages, evaluate: runtime type checks, docstrings, type hints.

**Evidence format**: "Coverage: [%]. Nullability: [pattern]. Any usage: file:line. Enums: [if used]"

---

### 7. Testing & Testability (Weight: 10%)
**Core Question**: Is the code verified and/or easily verifiable?

**Evaluation depends on presence of tests:**

| Has Tests? | Focus On |
|------------|----------|
| Yes | Coverage, edge cases, assertion quality, test isolation |
| No | Testability: dependency injection, pure functions, mockable design |

| Score | With Tests | Without Tests |
|-------|------------|---------------|
| 90-100 | High coverage, edge cases tested, good assertions, isolated | Highly testable: DI, pure functions, mockable deps |
| 75-89 | Good coverage, some gaps | Mostly testable, minor hard dependencies |
| 60-74 | Basic happy path tests | Testable with some effort |
| 40-59 | Few tests, poor assertions | Hard to test, tight coupling |
| 20-39 | Minimal/broken tests | Very difficult to test |
| 0-19 | No meaningful tests | Untestable design |

**What to evaluate (with tests):**
- Coverage (what % of code paths tested)
- Edge cases (empty, null, boundary values, error paths)
- Assertion quality (specific assertions, not just "no error")
- Test isolation (tests don't depend on each other or external state)
- Test organization (clear naming, logical grouping)

**What to evaluate (without tests):**
- Dependency injection (dependencies passed in, not constructed)
- Pure functions (no side effects where possible)
- Mockable boundaries (external services behind interfaces)

**Evidence format**: "N test files, M tests. Coverage: [estimate]. Edge cases: file:line. OR Testability: [assessment]"

---

### 8. Maintainability (Weight: 9%)
**Core Question**: How easy is it to understand, modify, and extend this code?

| Score | Criteria |
|-------|----------|
| 90-100 | Self-documenting, externalized config, easy to extend |
| 75-89 | Mostly maintainable, minor issues |
| 60-74 | Requires effort to understand |
| 40-59 | Difficult to modify safely |
| 20-39 | Changes would likely break things |
| 0-19 | Unmaintainable |

**What to evaluate:**
- Named constants (no magic numbers/strings)
- Configuration (externalized, not hardcoded)
- Documentation (README, API docs, important comments)
- Extensibility (easy to add features without modifying core)
- Single source of truth (no duplicate definitions)
- Clear data flow (easy to trace how data moves through system)

**Evidence format**: "Constants: file:line. Config: [handling]. Documentation: [quality]. Extension points: [if any]"

---

### 9. Performance (Weight: 4%)
**Core Question**: Are there obvious performance issues or inefficiencies?

| Score | Criteria |
|-------|----------|
| 90-100 | Efficient algorithms, appropriate data structures, no waste |
| 75-89 | Good performance, minor optimizations possible |
| 60-74 | Acceptable, some inefficiencies |
| 40-59 | Notable issues (N+1, O(n²) where avoidable) |
| 20-39 | Significant performance problems |
| 0-19 | Severe issues |

**What to evaluate:**
- Algorithm complexity (appropriate for the problem size)
- Data structures (Set for lookups, Map for key-value, etc.)
- Loop efficiency (early breaks, avoid recomputation)
- Memory usage (no obvious leaks, appropriate caching)
- I/O patterns (batching, connection reuse where applicable)

**Note**: Don't penalize for theoretical optimizations. Focus on obvious issues.

**Evidence format**: "Algorithms: [complexity]. Data structures: file:line. Issues: [if any]"

---

### 10. Best Practices & Conventions (Weight: 4%)
**Core Question**: Does the code follow modern conventions and language idioms?

| Score | Criteria |
|-------|----------|
| 90-100 | Modern features, consistent style, proper patterns |
| 75-89 | Good practices with minor deviations |
| 60-74 | Mixed patterns |
| 40-59 | Outdated practices |
| 20-39 | Ignores conventions |
| 0-19 | Anti-patterns throughout |

**What to evaluate:**
- Modern language features (async/await, destructuring, etc.)
- Consistent style (formatting, naming conventions)
- Resource management (proper cleanup, using/with statements)
- Immutability preference (const/readonly where appropriate)
- Standard patterns (factory, builder, etc. used appropriately)
- Package structure (follows language ecosystem conventions)

**Evidence format**: "Modern features: [examples]. Style: [consistency]. Patterns: file:line"

---

## Scoring Process

### Step 1: Score Each Dimension
For each of the 10 dimensions:
1. Read relevant code sections in both implementations
2. Apply the criteria table to determine score (0-100)
3. Record specific file:line evidence
4. **NEVER leave evidence empty**

### Step 2: Calculate Weighted Overall Score
```
overall_score = (
  functional_completeness * 0.15 +
  correctness_robustness * 0.14 +
  architecture * 0.12 +
  code_quality * 0.12 +
  security * 0.10 +
  type_safety * 0.10 +
  testing * 0.10 +
  maintainability * 0.09 +
  performance * 0.04 +
  best_practices * 0.04
)
```

### Step 3: Determine Grade
| Grade | Score Range |
|-------|-------------|
| A+ | 97-100 |
| A | 93-96 |
| A- | 90-92 |
| B+ | 87-89 |
| B | 83-86 |
| B- | 80-82 |
| C+ | 77-79 |
| C | 73-76 |
| C- | 70-72 |
| D | 60-69 |
| F | 0-59 |

### Step 4: Determine Winner
- **Winner**: Higher overall_score
- **Tie**: If difference < 3 points
- **Margin**: negligible (<3), slight (3-7), moderate (8-14), significant (15-24), decisive (25+)

---

## Output Format

Return ONLY a JSON object. No markdown code fences. No text before or after.

```json
{
  "implementation_a": {
    "language_detected": "Python",
    "functional_completeness": {"score": 88, "evidence": "9/10 requirements. ✓ CRUD at handlers.py:20-80, ✓ auth at auth.py:15, ✗ missing pagination"},
    "correctness_robustness": {"score": 82, "evidence": "Error handling at api.py:30-50 with custom errors. Edge cases: empty input at validate.py:25. Missing: timeout handling"},
    "architecture": {"score": 85, "evidence": "Clean layers: handlers/ → services/ → repos/. Dependencies flow inward. Minor: utils.py mixed concerns"},
    "code_quality": {"score": 80, "evidence": "Good naming. Longest function: process_order() at orders.py:45 (52 lines). No significant duplication"},
    "security": {"score": 85, "evidence": "Input validation at validators.py:10-40. Secrets from env at config.py:5. No injection vectors found"},
    "type_safety": {"score": 78, "evidence": "90% typed. Optional[] at models.py:20. Some Any at legacy.py:15-20"},
    "testing": {"score": 75, "evidence": "15 test files, 60 tests. Edge cases at test_edge.py. Missing: error path tests"},
    "maintainability": {"score": 82, "evidence": "Constants at constants.py. Config externalized. README present. Extension via plugins/"},
    "performance": {"score": 88, "evidence": "O(n) algorithms appropriate. Set for lookups at search.py:30. No N+1 issues"},
    "best_practices": {"score": 85, "evidence": "Async/await throughout. Consistent style. Context managers at db.py:20"},
    "anti_patterns_found": [
      {"pattern": "Long Function", "severity": "MEDIUM", "location": "orders.py:45", "details": "52 lines, should be <30"},
      {"pattern": "Type Escape", "severity": "MEDIUM", "location": "legacy.py:15-20", "details": "Any types used"}
    ],
    "best_practices_found": [
      {"practice": "Named Constants", "location": "constants.py", "details": "All magic values extracted"},
      {"practice": "Input Validation", "location": "validators.py:10-40", "details": "Comprehensive boundary validation"},
      {"practice": "Resource Cleanup", "location": "db.py:20", "details": "Context managers for connections"}
    ],
    "overall_score": 83,
    "grade": "B",
    "strengths": ["Clean architecture", "Good input validation", "Comprehensive error handling"],
    "weaknesses": ["Missing pagination feature", "Some long functions", "Legacy code has weak typing"]
  },
  "implementation_b": {
    "language_detected": "Python",
    "functional_completeness": {"score": 95, "evidence": "10/10 requirements. All CRUD, auth, AND pagination at handlers.py:20-150"},
    "correctness_robustness": {"score": 90, "evidence": "Comprehensive error handling with retries at client.py:25. All edge cases covered including timeout"},
    "architecture": {"score": 88, "evidence": "Hexagonal architecture. Ports at interfaces/, adapters at infrastructure/. Clean boundaries"},
    "code_quality": {"score": 88, "evidence": "All functions <35 lines. Excellent naming. No duplication detected"},
    "security": {"score": 92, "evidence": "Input validation + output encoding. Secrets from vault at config.py:8. Rate limiting at middleware.py:15"},
    "type_safety": {"score": 90, "evidence": "Strict mode enabled. No Any. Enums at types.py:10. Full Optional[] coverage"},
    "testing": {"score": 85, "evidence": "22 test files, 95 tests. Edge cases + error paths. 85% coverage"},
    "maintainability": {"score": 90, "evidence": "Self-documenting code. All config externalized. Comprehensive README. Plugin system"},
    "performance": {"score": 85, "evidence": "Efficient algorithms. Connection pooling at db.py:15. Minor: could cache computation at calc.py:40"},
    "best_practices": {"score": 88, "evidence": "Modern Python 3.11 features. Dataclasses. Consistent formatting. Proper resource cleanup"},
    "anti_patterns_found": [
      {"pattern": "Over-Engineering", "severity": "LOW", "location": "container.py", "details": "DI container complexity exceeds project needs"}
    ],
    "best_practices_found": [
      {"practice": "Strict Typing", "location": "tsconfig.json / pyproject.toml", "details": "All strict flags enabled"},
      {"practice": "Enums for Constants", "location": "types.py:10", "details": "Fixed values use enums"},
      {"practice": "Error Context", "location": "client.py:25", "details": "Errors include retry info and context"},
      {"practice": "Immutability", "location": "models.py", "details": "Frozen dataclasses used"}
    ],
    "overall_score": 89,
    "grade": "B+",
    "strengths": ["Complete implementation", "Excellent type safety", "Strong security", "Good test coverage"],
    "weaknesses": ["Slight over-engineering in DI", "Could add caching"]
  },
  "comparison": {
    "winner": "b",
    "margin": "slight",
    "score_difference": 6,
    "dimension_breakdown": [
      {"dimension": "functional_completeness", "winner": "b", "diff": 7, "weight": 15},
      {"dimension": "correctness_robustness", "winner": "b", "diff": 8, "weight": 14},
      {"dimension": "architecture", "winner": "b", "diff": 3, "weight": 12},
      {"dimension": "code_quality", "winner": "b", "diff": 8, "weight": 12},
      {"dimension": "security", "winner": "b", "diff": 7, "weight": 10},
      {"dimension": "type_safety", "winner": "b", "diff": 12, "weight": 10},
      {"dimension": "testing", "winner": "b", "diff": 10, "weight": 10},
      {"dimension": "maintainability", "winner": "b", "diff": 8, "weight": 9},
      {"dimension": "performance", "winner": "tie", "diff": -3, "weight": 4},
      {"dimension": "best_practices", "winner": "b", "diff": 3, "weight": 4}
    ],
    "anti_pattern_comparison": {
      "a_count": 2,
      "b_count": 1,
      "a_critical": 0,
      "b_critical": 0,
      "winner": "b"
    },
    "best_practice_comparison": {
      "a_count": 3,
      "b_count": 4,
      "winner": "b"
    },
    "production_readiness": {
      "a": {
        "security_score": 75,
        "security_issues": ["No rate limiting", "Missing CSRF protection"],
        "testing_score": 70,
        "testing_issues": ["No integration tests", "Missing error path tests"],
        "performance_score": 80,
        "performance_issues": ["N+1 query at users.py:45"],
        "operations_score": 60,
        "operations_issues": ["No graceful shutdown", "Missing health check", "No structured logging"]
      },
      "b": {
        "security_score": 90,
        "security_issues": ["Rate limiting could be stricter"],
        "testing_score": 85,
        "testing_issues": ["Could add more edge cases for date handling"],
        "performance_score": 85,
        "performance_issues": ["Cache could have TTL"],
        "operations_score": 85,
        "operations_issues": ["Could add readiness probe"]
      },
      "winner": "b",
      "production_ready": {"a": false, "b": true}
    },
    "principle_compliance": {
      "a": {
        "dry_violations": 2,
        "yagni_violations": 0,
        "solid_violations": ["SRP: UserService handles auth and profile", "DIP: Direct DB instantiation"],
        "kiss_score": 80
      },
      "b": {
        "dry_violations": 0,
        "yagni_violations": 1,
        "solid_violations": ["Minor: Over-abstracted DI"],
        "kiss_score": 75
      }
    },
    "key_differences": [
      "B implements pagination while A misses it",
      "B has 12 points better type safety with strict mode and no Any",
      "B has comprehensive retry logic and timeout handling for robustness",
      "B has fewer anti-patterns (1 vs 2) and more best practices (4 vs 3)",
      "B is production-ready while A has critical gaps in operations"
    ],
    "executive_summary": [
      {
        "topic": "Security",
        "winner": "b",
        "insight": "B: rate limiting + input validation → ~40% smaller attack surface. A: missing CSRF protection."
      },
      {
        "topic": "Reliability",
        "winner": "b",
        "insight": "B: retry + exponential backoff + circuit breakers. A: cascade failures under load."
      },
      {
        "topic": "Maintainability",
        "winner": "b",
        "insight": "B: strict typing catches ~30% more bugs at compile time. A: Any types → runtime errors."
      },
      {
        "topic": "Completeness",
        "winner": "b",
        "insight": "B: all 10 requirements met. A: missing pagination → large datasets unusable."
      },
      {
        "topic": "Production Readiness",
        "winner": "b",
        "insight": "B: health checks + logging + graceful shutdown. A: needs significant work before deployment."
      }
    ],
    "recommendation": "Implementation B is better overall. Complete features, stronger type safety, and better error handling. The slight over-engineering in DI is acceptable given the benefits. B is production-ready while A requires significant work on logging, health checks, and security."
  }
}
```

---

## Critical Rules

1. **READ ALL FILES** - Scan every file in both implementations
2. **CITE EVIDENCE** - Every score needs file:line reference
3. **SCORE ALL DIMENSIONS** - No dimension can have score 0 with empty evidence
4. **USE CRITERIA TABLES** - Score based on defined criteria, not intuition
5. **CALCULATE CORRECTLY** - overall_score MUST be the weighted average
6. **BE CONSISTENT** - Apply same standards to both implementations
7. **NO ASSUMPTIONS** - Judge only what you see in the code
8. **COMPLETE AUTONOMOUSLY** - Do not ask questions or pause
9. **EVALUATE PRODUCTION-READINESS** - Check security, testing, performance, operations
10. **CHECK PRINCIPLES** - Evaluate DRY, YAGNI, SOLID, KISS compliance
11. **EXECUTIVE SUMMARY** - Provide exactly 5 bullet-point style insights. Format: "Winner: key feature → impact. Loser: gap/issue." Keep each insight under 100 characters, direct and scannable.

**Production-Grade Evaluation (MANDATORY):**
- Security: Check OWASP Top 10, secrets management, input validation
- Testing: Unit tests, edge cases, error paths, meaningful coverage
- Performance: Algorithm complexity, caching, connection pooling, N+1 queries
- Operations: Logging, graceful shutdown, health checks, timeouts, retry logic
- Principles: DRY violations, YAGNI violations, SOLID compliance

**CRITICAL**: Every dimension MUST have:
- A score between 0-100
- Non-empty evidence with file:line references
- If something is "not applicable", explain why and score based on what IS present

**⚠️ FINAL OUTPUT INSTRUCTION:**
- Return ONLY the JSON object
- Do NOT wrap in markdown code blocks (no \`\`\`json)
- Do NOT add any text before or after the JSON
- Start your response with `{` and end with `}`
- This is a strict requirement for automated parsing
