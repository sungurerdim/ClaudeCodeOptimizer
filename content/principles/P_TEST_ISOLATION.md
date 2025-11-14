---
id: P_TEST_ISOLATION
title: Test Isolation
category: testing
severity: high
weight: 7
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_TEST_ISOLATION: Test Isolation 🔴

**Severity**: High

No shared state between tests, each test independent.

**Why**: Ensures quality by blocking deploys when tests fail or coverage drops

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: all
**Languages**: all

**❌ Bad**:
```
global_state = {}  # Shared between tests!
```

**✅ Good**:
```
@pytest.fixture
def state():
    return {}  # Fresh per test
```
