# Testing
**Coverage, isolation, test pyramid, integration, CI gates**

**Total Principles:** 6

---

## P037: Test Coverage Targets

**Severity:** HIGH

Minimum 80% line coverage, 100% for critical paths.

### Examples

**✅ Good:**
```
# pytest-cov shows 85% coverage
```

**❌ Bad:**
```
# 30% coverage
```

**Why:** Catches integration issues early by running full test suite on every commit

---

## P038: Test Isolation

**Severity:** HIGH

No shared state between tests, each test independent.

### Examples

**✅ Good:**
```
@pytest.fixture
def state():
    return {}  # Fresh per test
```

**❌ Bad:**
```
global_state = {}  # Shared between tests!
```

**Why:** Ensures quality by blocking deploys when tests fail or coverage drops

---

## P039: Integration Tests for Critical Paths

**Severity:** HIGH

Test service-to-service workflows end-to-end.

### Examples

**✅ Good:**
```
def test_job_workflow():
    # POST /jobs -> Queue -> Worker -> Result
```

**❌ Bad:**
```
# Only unit tests, no integration
```

**Why:** Validates production health by running smoke tests after every deployment

---

## P040: Test Pyramid

**Severity:** MEDIUM

70% unit, 20% integration, 10% e2e - fast feedback loop.

### Examples

**✅ Good:**
```
# 70% unit (fast), 20% integration, 10% e2e
```

**❌ Bad:**
```
# 90% e2e tests (slow!)
```

**Why:** Prevents bugs through isolated unit tests that don't depend on external systems

---

## P041: CI Gates

**Severity:** HIGH

All PRs must pass CI (lint, test, coverage) before merge.

### Examples

**✅ Good:**
```
# GitHub Actions: lint -> test -> coverage check
```

**❌ Bad:**
```
# No CI, manual testing
```

**Why:** Balances test coverage through unit, integration, and E2E testing pyramid

---

## P042: Property-Based Testing

**Severity:** LOW

Use Hypothesis/QuickCheck for complex logic, edge cases.

### Examples

**✅ Good:**
```
@given(st.integers())
def test_property(x):
    assert reverse(reverse(x)) == x
```

**❌ Bad:**
```
# Only example-based tests
```

**Why:** Catches regressions through integration tests that verify component interactions

---
