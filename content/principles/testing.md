# Testing Principles

**Generated**: 2025-11-09
**Principle Count**: 6

---

### P037: Test Coverage Targets 🟠

**Severity**: High

Minimum 80% line coverage, 100% for critical paths.

**❌ Bad**:
```
# 30% coverage
```

**✅ Good**:
```
# pytest-cov shows 85% coverage
```

---

### P038: Test Isolation 🟠

**Severity**: High

No shared state between tests, each test independent.

**❌ Bad**:
```
global_state = {}  # Shared between tests!
```

**✅ Good**:
```
@pytest.fixture\ndef state():\n    return {}  # Fresh per test
```

---

### P039: Integration Tests for Critical Paths 🟠

**Severity**: High

Test service-to-service workflows end-to-end.

**Project Types**: api, microservices

**❌ Bad**:
```
# Only unit tests, no integration
```

**✅ Good**:
```
def test_job_workflow():\n    # POST /jobs -> Queue -> Worker -> Result
```

---

### P040: Test Pyramid 🟡

**Severity**: Medium

70% unit, 20% integration, 10% e2e - fast feedback loop.

**❌ Bad**:
```
# 90% e2e tests (slow!)
```

**✅ Good**:
```
# 70% unit (fast), 20% integration, 10% e2e
```

---

### P041: CI Gates 🟠

**Severity**: High

All PRs must pass CI (lint, test, coverage) before merge.

**❌ Bad**:
```
# No CI, manual testing
```

**✅ Good**:
```
# GitHub Actions: lint -> test -> coverage check
```

---

### P042: Property-Based Testing 🟢

**Severity**: Low

Use Hypothesis/QuickCheck for complex logic, edge cases.

**Languages**: python, haskell

**❌ Bad**:
```
# Only example-based tests
```

**✅ Good**:
```
@given(st.integers())\ndef test_property(x):\n    assert reverse(reverse(x)) == x
```

---

---

**Loading**: These principles load automatically when running relevant commands

**Reference**: Use `@PRINCIPLES.md` to load core principles, or reference this file directly