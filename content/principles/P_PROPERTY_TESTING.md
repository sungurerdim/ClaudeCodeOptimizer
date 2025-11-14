---
id: P_PROPERTY_TESTING
title: Property-Based Testing
category: testing
severity: low
weight: 5
applicability:
  project_types: ['all']
  languages: ['python', 'haskell']
---

# P_PROPERTY_TESTING: Property-Based Testing 🟢

**Severity**: Low

Use Hypothesis/QuickCheck for complex logic, edge cases.

**Why**: Catches regressions through integration tests that verify component interactions

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: all
**Languages**: python, haskell

**❌ Bad**:
```
# Only example-based tests
```

**✅ Good**:
```
@given(st.integers())
def test_property(x):
    assert reverse(reverse(x)) == x
```
