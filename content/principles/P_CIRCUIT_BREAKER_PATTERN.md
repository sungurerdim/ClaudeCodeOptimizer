---
id: P_CIRCUIT_BREAKER_PATTERN
title: Circuit Breaker Pattern
category: architecture
severity: medium
weight: 7
applicability:
  project_types: ['microservices', 'api']
  languages: ['all']
---

# P_CIRCUIT_BREAKER_PATTERN: Circuit Breaker Pattern 🟡

**Severity**: Medium

Fail fast on external failures, prevent cascade failures.

**Why**: Enables parallel development through isolated feature branches and clear merge strategy

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: microservices, api
**Languages**: all

**❌ Bad**:
```
# No circuit breaker, retries forever
```

**✅ Good**:
```
@circuit_breaker(failure_threshold=5, timeout=60)
def call_external_api():
```
