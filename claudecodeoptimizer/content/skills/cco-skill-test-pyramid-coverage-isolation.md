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
- **Inadequate Test Coverage**: 60%+ of production bugs occur in untested code paths
- **Inverted Test Pyramid**: Slow e2e tests dominate, causing 10-30 minute CI runs instead of 2-5 minutes
- **Flaky Tests**: Non-isolated tests fail randomly, reducing developer trust to <50%
- **Missing Edge Cases**: Property testing catches 40%+ more bugs than example-based tests alone

**Impact**: Critical

---

## Principles Included

This skill loads the following P_ principles on-demand:

### P_TEST_PYRAMID
**Category**: Testing Architecture
**Why**: Fast unit tests (70%), moderate integration tests (20%), minimal e2e tests (10%)
**Triggers when**: Test strategy, CI performance, test suite design

### P_TEST_COVERAGE
**Category**: Test Quality
**Why**: Measure and enforce minimum coverage thresholds (typically 80%+)
**Triggers when**: Analyzing test gaps, reviewing PRs, quality gates

### P_TEST_ISOLATION
**Category**: Test Reliability
**Why**: Each test runs independently; no shared state causes 90%+ of flaky tests
**Triggers when**: Debugging flaky tests, test fixtures, parallelization

### P_PROPERTY_TESTING
**Category**: Advanced Testing
**Why**: Generative testing finds edge cases manual tests miss (40%+ additional coverage)
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
