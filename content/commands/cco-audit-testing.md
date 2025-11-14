---
description: Test coverage, test quality, flaky tests, CI/CD audit
category: audit
cost: 2
principles: ['P_TEST_COVERAGE', 'P_TEST_ISOLATION', 'P_INTEGRATION_TESTS', 'P_TEST_PYRAMID', 'P_CI_GATES', 'P_PROPERTY_TESTING', 'U_TEST_FIRST']
---

# cco-audit-testing - Test Coverage & Quality Audit

**Comprehensive test coverage analysis, quality assessment, and CI/CD validation.**

---

## Architecture & Model Selection

**Data Gathering**: Haiku (Explore agent, medium)
- Test coverage analysis
- Flaky test detection
- Slow test identification
- Cost-effective for test metrics

**Analysis**: Sonnet (Plan agent)
- Test gap analysis by business impact
- Test quality recommendations
- Test strategy planning

**Execution Pattern**:
1. Launch 2 parallel Haiku agents:
   - Agent 1: Coverage analysis (what's tested, what's not)
   - Agent 2: Test quality (flaky tests, slow tests, isolation)
2. Aggregate with Sonnet for test strategy
3. Generate prioritized test generation plan

**Model Requirements**:
- Haiku for scanning (15-20 seconds)
- Sonnet for test strategy

---

## Action

Use Task tool to launch parallel test audit agents.

### Step 1: Parallel Test Scans

**CRITICAL**: Launch BOTH agents in PARALLEL in a SINGLE message.

#### Agent 1: Test Coverage Analysis

**Agent 1 Prompt:**
```
Subagent Type: Explore
Model: haiku
Description: Test coverage analysis

MUST LOAD FIRST:
1. @CLAUDE.md (Testing section)
2. @~/.cco/principles/testing.md
3. Print: "✓ Loaded 2 docs (~2,100 tokens)"

Audit principles:
- P_TEST_COVERAGE: Test Coverage Targets (80%+ for critical paths)
- P_TEST_PYRAMID: Test Pyramid (more unit than integration)
- P_INTEGRATION_TESTS: Integration Tests for Critical Paths
- U_TEST_FIRST: Test-First Development

Scan for:
- Overall test coverage percentage (line, branch, function)
- Files with 0% coverage (critical files untested)
- Critical paths without tests (payment, auth, data integrity)
- Test pyramid violations (too many E2E tests, not enough unit tests)
- Missing integration tests (API endpoints, database interactions)
- Coverage gaps by module/directory

Run coverage tools:
- Python: pytest --cov --cov-report=term-missing
- JavaScript: jest --coverage
- Go: go test -cover ./...
- Rust: cargo tarpaulin

Report with:
- Overall coverage percentage
- Files with 0% coverage (prioritize critical files)
- Coverage by category (unit, integration, E2E)
- Business impact for each gap
```

#### Agent 2: Test Quality Analysis

**Agent 2 Prompt:**
```
Subagent Type: Explore
Model: haiku
Description: Test quality analysis

MUST LOAD FIRST:
1. @CLAUDE.md (Testing section)
2. @~/.cco/principles/testing.md
3. Print: "✓ Loaded 2 docs (~2,100 tokens)"

Audit principles:
- P_TEST_ISOLATION: Test Isolation (tests don't affect each other)
- P_CI_GATES: CI Gates (tests must pass before merge)
- P_PROPERTY_TESTING: Property-Based Testing (where applicable)

Scan for:
- Flaky tests (non-deterministic, pass/fail randomly)
- Slow tests (>5 seconds for unit, >30 seconds for integration)
- Test isolation issues (tests depend on each other, shared state)
- Missing assertions (tests that don't check anything)
- Weak assertions (assertTrue only, no specific checks)
- Missing test documentation (unclear what's being tested)
- CI/CD configuration (are tests required before merge?)

Run test tools:
- Python: pytest --durations=10 (find slow tests)
- JavaScript: jest --verbose (test details)
- Flaky tests: Run tests 10 times, check for failures

Report with:
- Flaky test count and names
- Slow test count and durations
- Test isolation violations
- CI/CD gate status
```

### Step 2: Test Strategy & Recommendations

**After both agents complete**, use Sonnet Plan agent:

**Agent 3 Prompt:**
```
Subagent Type: Plan
Model: sonnet
Description: Test strategy analysis

Task: Analyze test findings and provide test generation strategy.

Input:
- Agent 1 findings (coverage analysis)
- Agent 2 findings (test quality)

Analysis steps:
1. Merge all test findings
2. Assess business impact of test gaps
   - Critical: Payment, auth, data integrity
   - High: API endpoints, user flows
   - Medium: Business logic
   - Low: Utilities
3. Prioritize by: Business Impact × Risk × Effort
4. Provide specific test generation commands
5. Calculate test debt (hours to 80% coverage)
6. Recommend test strategy (unit vs integration vs E2E)

Output format:
- Findings by business impact (CRITICAL > HIGH > MEDIUM > LOW)
- Each finding includes: principle, file, coverage gap, business risk, fix command
- Master test generation plan with priority tiers
- Test debt estimate (total hours)

Focus on pragmatic, high-value testing.
```

---

## Output Format

Report test coverage and quality issues with business impact:

```
Test Audit Results
==================

Coverage: 67% (target: 80%, gap: 13%)

CRITICAL (no tests):
  - src/payment.py - 0% coverage
    Business Risk: Payment processing bugs go undetected
    Impact: Financial loss, fraud vulnerability
    Command: /cco-generate tests --file src/payment.py --focus critical-path

  - src/auth.py - 0% coverage
    Business Risk: Authentication bypass possible
    Impact: Security breach, unauthorized access
    Command: /cco-generate tests --file src/auth.py --focus security

HIGH (insufficient coverage):
  - src/api.py - 45% coverage (23/51 functions untested)
    Missing: Error handling, edge cases, validation
    Business Risk: API failures in production
    Command: /cco-generate tests --file src/api.py --focus error-handling,edge-cases

  - src/database.py - 60% coverage
    Missing: Transaction rollback, connection pool edge cases
    Business Risk: Data corruption, connection leaks
    Command: /cco-generate tests --file src/database.py --focus transactions,rollback

MEDIUM (quality issues):
  - tests/test_user.py - 5 flaky tests detected
    Failures: test_concurrent_login (intermittent)
    Impact: CI unreliability, false positives
    Command: /cco-fix tests --type flaky --file tests/test_user.py

  - tests/test_integration.py - 3 slow tests (>10s each)
    Slowest: test_full_workflow (23.4s)
    Impact: Developer productivity (slow feedback)
    Command: /cco-fix tests --type slow --threshold 5s --file tests/test_integration.py

LOW (minor gaps):
  - src/utils.py - 85% coverage
    Missing: Error path in format_date()
    Impact: Minor edge case handling
    Command: /cco-generate tests --file src/utils.py --focus edge-cases
```

---

## Recommended Actions

**Analyze test gaps and provide impact-driven prioritization:**

```
🧪 Test Generation Plan (Business Impact Priority)
===================================================

IMMEDIATE (Production Blockers):
─────────────────────────────────
1. Add payment processing tests
   Command: /cco-generate tests --file src/payment.py --focus critical-path
   Impact: CRITICAL - Prevents financial bugs
   Coverage: 0% → 85% (target critical paths)
   Effort: 4 hours

2. Add authentication tests
   Command: /cco-generate tests --file src/auth.py --focus security
   Impact: CRITICAL - Prevents auth bypass
   Coverage: 0% → 80% (target security flows)
   Effort: 3 hours

THIS WEEK (High Risk):
─────────────────────
3. Expand API test coverage
   Command: /cco-generate tests --file src/api.py --focus error-handling,edge-cases
   Impact: HIGH - Catches production errors early
   Coverage: 45% → 80%
   Effort: 3.5 hours

4. Add database transaction tests
   Command: /cco-generate tests --file src/database.py --focus transactions,rollback
   Impact: HIGH - Prevents data corruption
   Coverage: 60% → 85%
   Effort: 2 hours

THIS SPRINT (Quality):
─────────────────────
5. Fix flaky tests
   Command: /cco-fix tests --type flaky --file tests/test_user.py
   Impact: MEDIUM - Improves CI reliability
   Flaky: 5 → 0
   Effort: 2 hours

6. Optimize slow tests
   Command: /cco-fix tests --type slow --threshold 5s --file tests/test_integration.py
   Impact: MEDIUM - Faster feedback loop
   Time: 23.4s → <5s (use mocking)
   Effort: 1.5 hours

BACKLOG (Minor Gaps):
────────────────────
7. Add edge case tests
   Command: /cco-generate tests --file src/utils.py --focus edge-cases
   Impact: LOW - Completeness
   Coverage: 85% → 95%
   Effort: 0.5 hours

Test Debt: 16.5 hours | Coverage: 67% → 82% | Risk Reduction: 90%
```

**Command Generation Logic:**
1. **Business Impact = Criticality × Exposure × Failure Cost**
   - Criticality: Payment, auth, data integrity > API > utilities
   - Exposure: Public APIs > internal > helpers
   - Failure Cost: Financial loss > security > UX > dev productivity

2. **Priority Tiers:**
   - IMMEDIATE: No tests for critical business logic (fix today)
   - THIS WEEK: <50% coverage on high-traffic code (fix this week)
   - THIS SPRINT: Flaky/slow tests, 50-80% coverage (fix this sprint)
   - BACKLOG: >80% coverage, minor utilities (fix when convenient)

3. **Command Features:**
   - Focus areas: `--focus critical-path`, `--focus error-handling`, `--focus security`
   - Fix types: `--type flaky`, `--type slow`
   - Coverage targets: Show before → after
   - Effort estimates: Realistic time based on file complexity

4. **Test Strategy:**
   - Critical files: Unit + integration + edge cases
   - High-traffic files: Unit + integration
   - Utilities: Unit only
   - Flaky tests: Isolate, mock external dependencies
   - Slow tests: Mock I/O, use in-memory DBs

---

## Related Commands

- `/cco-generate tests` - Generate missing tests automatically
- `/cco-fix tests` - Fix flaky/slow tests
- `/cco-audit-code-quality` - Code quality audit
- `/cco-audit-comprehensive` - Full comprehensive audit
