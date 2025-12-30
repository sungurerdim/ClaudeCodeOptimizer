# Production-Grade Code Evaluation - Blind Comparison

You are a senior staff engineer performing a **blind evaluation** of two implementations.
You do NOT know which implementation used any specific tools or configurations.
Evaluate ONLY based on the code quality you observe against **production-readiness criteria**.

---

## CRITICAL: Autonomous Operation

**This evaluation runs completely unattended. Follow these rules strictly:**

1. **Complete autonomously** - Execute the full evaluation without stopping
2. **Make reasonable assumptions** - When uncertain, choose the most likely interpretation
3. **Proceed on best judgment** - Never wait for clarification
4. **Output JSON only** - Return ONLY the final JSON result, no other text

**Prohibited actions:**
- Asking questions to the user
- Requesting clarification or confirmation
- Pausing for approval
- Outputting explanatory text before/after JSON

---

## Execution Strategy

### Phase 1: Parallel File Discovery
**[PARALLEL]** Read both implementations simultaneously:
- List all files in Implementation A directory
- List all files in Implementation B directory
- Read the original task prompt file

### Phase 2: Systematic Code Reading
**[PARALLEL]** For each implementation, read files in this order:
1. Entry points (main.*, index.*, app.*, cmd/*)
2. Core business logic files
3. Configuration files (*.yaml, *.json, *.toml, .env.example)
4. Test files (test_*, *_test.*, *.spec.*)
5. Supporting utilities and middleware

### Phase 3: Step-Back Analysis
Before scoring, answer these foundational questions:
1. "What is the architectural pattern of each implementation?"
2. "What are the trust boundaries and data flows?"
3. "How does each handle the critical paths?"
4. "Is this code ready for production deployment?"

### Phase 4: Chain-of-Thought Scoring
For each dimension, reason through:
1. **Identify**: What specific code addresses this dimension?
2. **Evidence**: What file:line references support the assessment?
3. **Compare**: How do A and B differ on this dimension?
4. **Score**: Based on evidence, what score fits the criteria?

---

## Instructions

1. **Read ALL files** in both implementations before scoring (not just entry points)
2. **Extract requirements** from the original prompt - list them mentally
3. **Score based on evidence** - cite specific file:line references
4. **Apply criteria tables** - use the defined score ranges, not intuition
5. **Calculate weighted average** - overall_score MUST match the formula
6. **Treat both equally** - no bias toward either implementation
7. **Think production** - evaluate as if this code will serve real users

---

## The Implementations

- **Implementation A**: Located in the first directory provided
- **Implementation B**: Located in the second directory provided

Both were generated from the same prompt (provided in the referenced file).

---

## Evaluation Dimensions (10 Total, Weights sum to 100%)

### 1. Functional Completeness (Weight: 15%)
**Question**: Does the code implement ALL requirements from the prompt correctly?

| Score | Criteria |
|-------|----------|
| 90-100 | All requirements implemented, tested, and working correctly |
| 75-89 | All core requirements met, minor features incomplete |
| 60-74 | Most requirements met, 1-2 significant gaps |
| 40-59 | Core functionality works, major features missing |
| 20-39 | Partial implementation, critical features missing |
| 0-19 | Fails to meet basic requirements |

**Evidence required**:
- List each requirement from the prompt
- For each: ✓ implemented at file:line OR ✗ missing
- Count: X/Y requirements met

**Checklist**:
- [ ] All explicit requirements from prompt implemented
- [ ] Features work as described (not just stubbed)
- [ ] Edge cases from requirements handled
- [ ] Default behaviors are reasonable

---

### 2. Security (Weight: 14%)
**Question**: Is the code secure against common vulnerabilities? Would you trust it in production?

| Score | Criteria |
|-------|----------|
| 90-100 | Defense-in-depth: input validation, output encoding, secrets protected, auth/authz correct |
| 75-89 | Good security posture, minor improvements possible |
| 60-74 | Basic security present, some gaps in coverage |
| 40-59 | Significant vulnerabilities or missing protections |
| 20-39 | Major security issues (injection, exposed secrets, broken auth) |
| 0-19 | Critical vulnerabilities, unsafe to deploy |

**OWASP Top 10 Checklist** (score deductions):
| Vulnerability | Check | Deduction if Found |
|---------------|-------|-------------------|
| A01 Broken Access Control | Auth checks on all protected routes | -15 |
| A02 Cryptographic Failures | Secrets in env vars, not hardcoded | -20 |
| A03 Injection | Parameterized queries, no string concat SQL | -20 |
| A04 Insecure Design | Input validation at boundaries | -10 |
| A05 Security Misconfiguration | Secure defaults, no debug in prod | -10 |
| A06 Vulnerable Components | No known vulnerable dependencies | -10 |
| A07 Auth Failures | Proper password handling, session mgmt | -15 |
| A08 Data Integrity | CSRF protection, signed tokens | -10 |
| A09 Logging Failures | Sensitive data not logged | -5 |
| A10 SSRF | URL validation for external requests | -10 |

**Evidence required**:
- Input validation locations: file:line
- Secret handling: how and where
- Auth/authz implementation: file:line
- Any vulnerabilities found with severity

---

### 3. Error Handling & Resilience (Weight: 12%)
**Question**: Does the code fail gracefully and recover from errors?

| Score | Criteria |
|-------|----------|
| 90-100 | Comprehensive: all errors caught, logged, recovered or propagated with context |
| 75-89 | Good coverage, minor gaps in edge cases |
| 60-74 | Basic try/catch, some unhandled paths |
| 40-59 | Inconsistent handling, silent failures |
| 20-39 | Minimal error handling, crashes on errors |
| 0-19 | No error handling, unhandled exceptions |

**Checklist**:
- [ ] All I/O operations have error handling (network, file, DB)
- [ ] Errors include context (what failed, why, how to fix)
- [ ] No silent failures (catch without log/rethrow)
- [ ] Graceful degradation where appropriate
- [ ] Retries with backoff for transient failures
- [ ] Timeouts configured for external calls
- [ ] Resource cleanup in finally/defer blocks

**Evidence required**:
- Error handling patterns used: file:line
- Unhandled error paths found: file:line
- Error message quality examples

---

### 4. Architecture & Design (Weight: 10%)
**Question**: Is the code well-structured with clean dependencies?

| Score | Criteria |
|-------|----------|
| 90-100 | Clear layers, single responsibility, dependency injection, no cycles |
| 75-89 | Good structure, minor coupling issues |
| 60-74 | Some organization but unclear boundaries |
| 40-59 | Mixed responsibilities, tight coupling |
| 20-39 | Tangled dependencies, god objects |
| 0-19 | No discernible architecture, spaghetti code |

**Checklist**:
- [ ] Clear separation: handlers/controllers → services → repositories
- [ ] Dependencies flow inward (outer layers depend on inner)
- [ ] No circular imports/dependencies
- [ ] Single responsibility per module/class
- [ ] Interfaces/abstractions at boundaries
- [ ] Configuration externalized
- [ ] No god objects (classes doing everything)

**Evidence required**:
- Layer structure: what directories/modules for each layer
- Dependency direction: who depends on whom
- Coupling issues found: file:line

---

### 5. Code Quality (Weight: 10%)
**Question**: Is the code readable, maintainable, and well-crafted?

| Score | Criteria |
|-------|----------|
| 90-100 | Excellent: clear naming, small functions, DRY, consistent style |
| 75-89 | Good quality, minor style inconsistencies |
| 60-74 | Readable but some large functions or duplication |
| 40-59 | Hard to follow, significant issues |
| 20-39 | Poor quality, inconsistent, duplicated |
| 0-19 | Unreadable, no standards |

**Metrics**:
| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| Function length | <30 lines | 30-50 lines | >50 lines |
| Cyclomatic complexity | <10 | 10-15 | >15 |
| Nesting depth | ≤3 levels | 4 levels | >4 levels |
| Duplication | None | Minor | Significant |

**Checklist**:
- [ ] Descriptive variable/function names
- [ ] Functions do one thing
- [ ] No magic numbers (named constants)
- [ ] DRY - no copy-paste code
- [ ] Consistent formatting/style
- [ ] Comments explain "why", not "what"
- [ ] No dead code or TODOs without tracking

**Evidence required**:
- Long functions: file:line (line count)
- Duplication: file:line and file:line (what's duplicated)
- Naming issues: examples

---

### 6. Type Safety (Weight: 8%)
**Question**: Are types used effectively to prevent bugs at compile/lint time?

| Score | Criteria |
|-------|----------|
| 90-100 | Strong typing, no any/unknown, explicit nullability, enums for fixed values |
| 75-89 | Good typing with minor gaps |
| 60-74 | Basic types, some any/object usage |
| 40-59 | Weak typing, implicit nulls, missing annotations |
| 20-39 | Minimal types, frequent any |
| 0-19 | No type safety, dynamic everywhere |

**Checklist**:
- [ ] All public functions have type annotations
- [ ] No `any`, `object`, or equivalent
- [ ] Explicit null/undefined handling (Optional, | null)
- [ ] Enums or literals for fixed value sets
- [ ] Generic types where reusability needed
- [ ] Strict mode enabled (if applicable)
- [ ] DTOs/interfaces for data shapes

**Evidence required**:
- Type coverage: estimated % of typed code
- Any/unknown usage: file:line
- Null handling pattern: how nulls are handled
- Enum usage for fixed values: file:line

---

### 7. Testing (Weight: 8%)
**Question**: Is the code verified through tests or demonstrably testable?

| Has Tests | Evaluation Focus |
|-----------|-----------------|
| Yes | Coverage, edge cases, assertion quality, isolation |
| No | Testability: DI, pure functions, mockable dependencies |

| Score | With Tests | Without Tests |
|-------|------------|---------------|
| 90-100 | High coverage, edge cases, isolated, good assertions | Highly testable: DI, pure, mockable |
| 75-89 | Good coverage, some gaps | Mostly testable, few hard deps |
| 60-74 | Basic happy path tests | Testable with some effort |
| 40-59 | Few tests, poor assertions | Hard to test, coupled |
| 20-39 | Minimal/broken tests | Very hard to test |
| 0-19 | No meaningful tests | Untestable |

**Test Quality Checklist** (if tests exist):
- [ ] Unit tests for business logic
- [ ] Integration tests for API/DB
- [ ] Edge cases tested (empty, null, boundary values)
- [ ] Tests are isolated (can run in any order)
- [ ] Assertions are specific (not just "no error")
- [ ] Mocks used appropriately (not over-mocked)
- [ ] Test names describe behavior

**Testability Checklist** (if no tests):
- [ ] Dependencies injected (not constructed internally)
- [ ] Pure functions where possible
- [ ] Side effects isolated
- [ ] External services abstracted behind interfaces

**Evidence required**:
- Test file count and types
- Coverage estimate (if measurable)
- Edge case examples: file:line
- Testability blockers: file:line

---

### 8. Observability (Weight: 8%)
**Question**: Can you debug and monitor this code in production?

| Score | Criteria |
|-------|----------|
| 90-100 | Structured logging, error tracking, metrics ready, correlation IDs |
| 75-89 | Good logging, minor gaps in coverage |
| 60-74 | Basic logging present, inconsistent |
| 40-59 | Minimal logging, hard to debug |
| 20-39 | Almost no logging |
| 0-19 | No observability at all |

**Checklist**:
- [ ] Structured logging (JSON or key=value)
- [ ] Log levels used appropriately (debug, info, warn, error)
- [ ] Request/operation context in logs (request ID, user ID)
- [ ] Errors logged with stack traces
- [ ] Sensitive data NOT logged (passwords, tokens, PII)
- [ ] Entry/exit logging for key operations
- [ ] Performance-critical paths measurable

**Anti-patterns** (deductions):
- `console.log` only: -10
- No error logging: -15
- Sensitive data in logs: -20
- No request context: -10

**Evidence required**:
- Logging implementation: file:line
- Log format example
- Missing logging areas: file:line
- Anti-patterns found

---

### 9. Production Readiness (Weight: 8%)
**Question**: Can this code be deployed and operated in production?

| Score | Criteria |
|-------|----------|
| 90-100 | 12-factor ready: config externalized, health checks, graceful shutdown |
| 75-89 | Mostly ready, minor configuration issues |
| 60-74 | Deployable with manual configuration |
| 40-59 | Significant preparation needed |
| 20-39 | Major issues blocking deployment |
| 0-19 | Not deployable |

**12-Factor Checklist**:
- [ ] **Config**: All config from env vars, no hardcoded values
- [ ] **Dependencies**: Explicitly declared (package.json, requirements.txt, go.mod)
- [ ] **Backing services**: DB/cache/queue connections configurable
- [ ] **Port binding**: Port from environment
- [ ] **Stateless**: No in-process state that can't be lost
- [ ] **Dev/prod parity**: Same code runs everywhere
- [ ] **Logs**: Written to stdout/stderr
- [ ] **Disposability**: Fast startup, graceful shutdown

**Operational Checklist**:
- [ ] Health check endpoint (/health, /ready)
- [ ] Graceful shutdown (drain connections, finish requests)
- [ ] Timeout configuration for external calls
- [ ] Connection pooling configured
- [ ] Resource limits considered (memory, connections)

**Evidence required**:
- Config handling: how and where (file:line)
- Health check: endpoint and implementation
- Graceful shutdown: signal handling (file:line)
- Hardcoded values found: file:line

---

### 10. Performance (Weight: 7%)
**Question**: Are there obvious performance issues or inefficiencies?

| Score | Criteria |
|-------|----------|
| 90-100 | Efficient algorithms, appropriate data structures, no waste |
| 75-89 | Good performance, minor optimizations possible |
| 60-74 | Acceptable, some inefficiencies |
| 40-59 | Notable issues (N+1, O(n²) where avoidable) |
| 20-39 | Significant performance problems |
| 0-19 | Severe issues, unusable at scale |

**Common Issues Checklist**:
- [ ] No N+1 queries (batch loading used)
- [ ] Appropriate data structures (Set for lookups, Map for key-value)
- [ ] No unnecessary iterations (break early, use indices)
- [ ] Async I/O where appropriate (no blocking in async context)
- [ ] Connection/resource pooling
- [ ] Pagination for large result sets
- [ ] Caching for expensive operations

**Anti-patterns** (deductions):
| Issue | Deduction |
|-------|-----------|
| N+1 queries | -15 |
| O(n²) when O(n) possible | -10 |
| Blocking in async context | -15 |
| No pagination on lists | -10 |
| Memory leaks (unclosed resources) | -15 |

**Evidence required**:
- Algorithm choices: file:line
- Data structure decisions: file:line
- Performance issues found: file:line
- Resource management: pooling, cleanup

---

## Scoring Process

### Step 1: Score Each Dimension
For each of the 10 dimensions:
1. Read relevant code sections in both implementations
2. Apply the criteria table AND checklist
3. Note specific file:line evidence
4. Assign score (0-100)

### Step 2: Calculate Weighted Overall Score
```
overall_score = (
  functional_completeness * 0.15 +
  security * 0.14 +
  error_handling * 0.12 +
  architecture * 0.10 +
  code_quality * 0.10 +
  type_safety * 0.08 +
  testing * 0.08 +
  observability * 0.08 +
  production_readiness * 0.08 +
  performance * 0.07
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
    "functional_completeness": {"score": 88, "evidence": "9/10 requirements met. Missing: rate limiting (not found). ✓ auth at auth.py:25, ✓ CRUD at handlers.py:30-120"},
    "security": {"score": 82, "evidence": "Input validation at validators.py:10-50. Secrets from env (config.py:5). Missing: CSRF protection. No SQL injection (ORM used)."},
    "error_handling": {"score": 75, "evidence": "Try/catch in handlers.py:45-80. Custom errors at errors.py:10. Gap: no timeout on external HTTP at client.py:30"},
    "architecture": {"score": 85, "evidence": "Clean layers: handlers/ → services/ → repositories/. No circular deps. Minor: utils.py has mixed concerns"},
    "code_quality": {"score": 80, "evidence": "Good naming. process_order() at orders.py:45 is 55 lines - should split. No duplication found."},
    "type_safety": {"score": 78, "evidence": "Full type hints. Optional[] used at models.py:20. Some Any at legacy.py:15"},
    "testing": {"score": 70, "evidence": "15 test files, 60 tests. Unit tests good. Missing: edge case tests for empty inputs"},
    "observability": {"score": 65, "evidence": "Basic logging at handlers.py. No structured format. No request ID correlation."},
    "production_readiness": {"score": 72, "evidence": "Config from env (config.py). No health endpoint. Graceful shutdown missing."},
    "performance": {"score": 85, "evidence": "ORM with eager loading. Proper indices. Minor: could add caching at compute.py:40"},
    "anti_patterns_found": ["Long function at orders.py:45", "No health check", "Unstructured logging"],
    "overall_score": 78,
    "grade": "C+",
    "strengths": ["Clean architecture", "Good input validation", "Type safety"],
    "weaknesses": ["Missing observability", "No health checks", "Long functions"]
  },
  "implementation_b": {
    "functional_completeness": {"score": 95, "evidence": "10/10 requirements met. All features at handlers.py:20-200. Rate limiting at middleware.py:15"},
    "security": {"score": 90, "evidence": "OWASP compliant. Input validation (validators.py), secrets from vault (config.py:8), CSRF (middleware.py:30), rate limiting (middleware.py:15)"},
    "error_handling": {"score": 88, "evidence": "Comprehensive. Custom error hierarchy at errors.py. Retries with backoff at client.py:25. All I/O wrapped."},
    "architecture": {"score": 88, "evidence": "Hexagonal architecture. Ports at interfaces/, adapters at infrastructure/. DI at container.py"},
    "code_quality": {"score": 85, "evidence": "All functions <40 lines. Named constants at constants.py. Minor: some comments redundant"},
    "type_safety": {"score": 90, "evidence": "Strict mode. No Any. Enums at types.py:10. Pydantic models validated."},
    "testing": {"score": 82, "evidence": "25 test files. Unit + integration. Edge cases at tests/edge_cases.py. 85% coverage"},
    "observability": {"score": 85, "evidence": "Structured JSON logging (logger.py). Request ID correlation. Error tracking ready."},
    "production_readiness": {"score": 90, "evidence": "Health endpoint at health.py:10. Graceful shutdown at main.py:50. All config from env."},
    "performance": {"score": 82, "evidence": "Efficient queries. Connection pooling. Minor: no caching layer yet"},
    "anti_patterns_found": ["Slight over-engineering in DI container"],
    "overall_score": 87,
    "grade": "B+",
    "strengths": ["Complete features", "Strong security", "Production ready", "Good observability"],
    "weaknesses": ["Slight over-engineering", "Could add caching"]
  },
  "comparison": {
    "winner": "b",
    "margin": "moderate",
    "score_difference": 9,
    "dimension_breakdown": [
      {"dimension": "functional_completeness", "winner": "b", "diff": 7},
      {"dimension": "security", "winner": "b", "diff": 8},
      {"dimension": "error_handling", "winner": "b", "diff": 13},
      {"dimension": "architecture", "winner": "b", "diff": 3},
      {"dimension": "code_quality", "winner": "b", "diff": 5},
      {"dimension": "type_safety", "winner": "b", "diff": 12},
      {"dimension": "testing", "winner": "b", "diff": 12},
      {"dimension": "observability", "winner": "b", "diff": 20},
      {"dimension": "production_readiness", "winner": "b", "diff": 18},
      {"dimension": "performance", "winner": "tie", "diff": -3}
    ],
    "key_differences": [
      "B is production-ready with health checks and graceful shutdown; A lacks these",
      "B has structured logging with request correlation; A has basic unstructured logs",
      "B implements all OWASP recommendations; A missing CSRF protection",
      "B has comprehensive error handling with retries; A has gaps in timeout handling"
    ],
    "recommendation": "Implementation B is significantly more production-ready. Strong security, observability, and operational features make it suitable for deployment. A needs work on health checks, structured logging, and complete error handling before production use."
  }
}
```

---

## Critical Rules

1. **READ ALL FILES** - Scan every file, not just entry points
2. **CITE EVIDENCE** - Every score needs file:line reference
3. **USE CRITERIA TABLES** - Score based on defined criteria, not intuition
4. **USE CHECKLISTS** - Each dimension has specific items to verify
5. **CALCULATE CORRECTLY** - overall_score MUST be the weighted average
6. **BE CONSISTENT** - Apply same standards to both implementations
7. **THINK PRODUCTION** - Evaluate for real-world deployment
8. **NO ASSUMPTIONS** - Judge only what you see in the code
9. **COMPLETE AUTONOMOUSLY** - Do not ask questions or pause

**Return ONLY the JSON object. No other text.**
