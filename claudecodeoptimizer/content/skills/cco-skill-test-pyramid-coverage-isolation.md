---
name: cco-skill-test-pyramid-coverage-isolation
description: |
  Use this skill when testing strategy, test quality, or test architecture is mentioned:
  - test, testing, tests, test suite, test strategy, test pyramid
  - coverage, test coverage, code coverage, branch coverage, line coverage
  - unit test, integration test, e2e test, end-to-end test, functional test
  - test isolation, test independence, flaky test, test reliability
  - property testing, generative testing, fuzz testing, randomized testing
  - test framework, pytest, jest, junit, mocha, rspec
  - Files: *test*.py, *spec.ts, *test.js, test_*.py, *_test.go

  Triggers: test, testing, coverage, unit, integration, e2e, pyramid, isolation, property, flaky, mock, stub, fixture
---

# Skill: Testing Strategy - Test Pyramid, Coverage & Isolation

## Purpose

Prevent production defects, flaky tests, and inadequate test coverage through comprehensive testing strategies.

**Solves**:
- **Inadequate Test Coverage**: Most production bugs occur in untested code paths
- **Inverted Test Pyramid**: Slow e2e tests dominate, causing slow CI runs
- **Flaky Tests**: Non-isolated tests fail randomly, reducing developer trust
- **Missing Edge Cases**: Property testing catches significantly more bugs than example-based tests alone

**Impact**: Critical

---

## Principles Included

This skill loads the following P_ principles on-demand:

### P_TEST_PYRAMID
**Category**: Testing Architecture
**Why**: Fast unit tests (majority), moderate integration tests, minimal e2e tests
**Triggers when**: Test strategy, CI performance, test suite design

### P_TEST_COVERAGE
**Category**: Test Quality
**Why**: Measure and enforce minimum coverage thresholds (high coverage target)
**Triggers when**: Analyzing test gaps, reviewing PRs, quality gates

### P_TEST_ISOLATION
**Category**: Test Reliability
**Why**: Each test runs independently; shared state causes most flaky tests
**Triggers when**: Debugging flaky tests, test fixtures, parallelization

### P_PROPERTY_TESTING
**Category**: Advanced Testing
**Why**: Generative testing finds edge cases manual tests miss (significant additional coverage)
**Triggers when**: Testing complex algorithms, data validation, invariant checking

### P_INTEGRATION_TESTS
**Category**: Testing Strategy
**Why**: Verify component interactions without full system overhead
**Triggers when**: API integrations, database interactions, multi-module workflows

**Note**: These principles are loaded into context only when this skill activates.

---

## Automatic Activation

This skill auto-loads when Claude detects:
- **Keywords**: test, testing, coverage, unit test, integration test, e2e, flaky, isolation, property, mock, fixture
- **User intent**: "improve test coverage", "fix flaky tests", "test strategy review"
- **File context**: `*test*.py`, `*_test.go`, `*.spec.ts`, `test_*.py`, `*Test.java`

**No manual invocation needed** - Claude autonomously decides based on context.

---

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for this skill's domain
action_types: [audit, fix, generate]
keywords: [tests, coverage, unit tests, integration tests, pytest, test pyramid, isolation]
category: testing
pain_points: [4]
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*test` in frontmatter
2. Match `category: testing`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.

---

## Related Skills

Skills that work well together:
- **cco-skill-code-quality-refactoring-complexity**: Testing drives refactoring
- **cco-skill-cicd-gates-deployment-automation**: Test pyramid determines CI gate thresholds

---

## Examples

### Example 1: Slow Test Suite
```
User: "Our test suite takes 20 minutes to run. How can we speed it up?"
       ↓
Skill: cco-skill-test-pyramid-coverage-isolation auto-loads (detects "test suite")
       ↓
Principles: P_TEST_PYRAMID, P_TEST_ISOLATION active
       ↓
Result: Analyzes test distribution, identifies inverted pyramid, recommends e2e → unit refactor
```

### Example 2: Flaky Tests
```
User: "Why do our tests fail randomly?"
       ↓
Skill: cco-skill-test-pyramid-coverage-isolation (detects "flaky test" intent)
       ↓
Principles: P_TEST_ISOLATION active
       ↓
Result: Identifies shared state, non-deterministic dependencies, parallelization issues
```

### Example 3: File Context
```
User opens: test_auth.py
       ↓
Skill: cco-skill-test-pyramid-coverage-isolation (detects "test_*.py" pattern)
       ↓
Principles: P_TEST_ISOLATION, P_TEST_COVERAGE active
       ↓
Result: Checks isolation violations, coverage gaps, property-based opportunities
```

---

## Test Analysis Patterns (Claude Executes)

When auditing test coverage or quality, use these analysis patterns:

### Find Untested Code

```bash
# Find Python files without corresponding tests
find . -name "*.py" -path "*/src/*" -o -name "*.py" -path "*/${PROJECT}/*" | \
  while read f; do
    base=$(basename "${f%.py}")
    if ! find tests/ -name "*${base}*test*.py" -o -name "test_*${base}*.py" 2>/dev/null | grep -q .; then
      echo "Untested: $f"
    fi
  done

# Coverage analysis with threshold
pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# List functions and check for tests
# Create safe temp directory (sandboxed)
mkdir -p .tmp
grep -rhn "^def \|^async def " --include="*.py" src/ | \
  sed 's/.*def \([a-zA-Z_][a-zA-Z0-9_]*\).*/\1/' | sort -u > .tmp/funcs.txt
grep -rh "def test_" --include="*.py" tests/ | \
  sed 's/.*def test_\([a-zA-Z_][a-zA-Z0-9_]*\).*/\1/' | sort -u > .tmp/tested.txt
echo "Potentially untested functions:"
comm -23 .tmp/funcs.txt .tmp/tested.txt
```

### Flaky Test Detection

```bash
# Time-dependent tests (potential flakiness)
grep -rn "random\|time.sleep\|datetime.now\|time.time\|uuid" --include="*test*.py" .

# Shared state indicators
grep -rn "global \|cls\.\|self\.__class__\|setUpModule\|tearDownModule" --include="*test*.py" .

# Network calls in tests (should be mocked)
grep -rn "requests\.\|urllib\|http\.client\|aiohttp" --include="*test*.py" . | grep -v "mock\|patch\|@responses"

# Database without fixtures
grep -rn "\.save()\|\.create()\|\.delete()" --include="*test*.py" . | grep -v "factory\|fixture"
```

### Test Pyramid Analysis

```bash
# Count test types
echo "Unit tests (test_*.py in tests/unit/):"
find tests/unit -name "test_*.py" 2>/dev/null | wc -l

echo "Integration tests (tests/integration/):"
find tests/integration -name "test_*.py" 2>/dev/null | wc -l

echo "E2E tests (tests/e2e/):"
find tests/e2e -name "test_*.py" 2>/dev/null | wc -l

# Ideal ratio: 70% unit, 20% integration, 10% e2e
```

### Test Quality Indicators

```bash
# Tests with no assertions (likely incomplete)
grep -L "assert\|pytest.raises\|self.assert" tests/**/test_*.py 2>/dev/null

# Tests with too many assertions (should be split)
grep -c "assert" tests/**/test_*.py 2>/dev/null | awk -F: '$2 > 10 {print "Too many assertions:", $1, $2}'

# Mock overuse (>5 mocks in one test)
grep -c "@patch\|@mock\|MagicMock\|Mock(" tests/**/test_*.py 2>/dev/null | awk -F: '$2 > 5 {print "Mock overuse:", $1, $2}'
```
