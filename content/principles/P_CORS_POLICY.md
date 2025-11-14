---
id: P_CORS_POLICY
title: CORS Policy
category: security_privacy
severity: high
weight: 7
applicability:
  project_types: ['api', 'web']
  languages: ['all']
---

# P_CORS_POLICY: CORS Policy 🔴

**Severity**: High

Principle of least privilege - only allow required origins.

**Why**: Protects APIs from abuse through rate limiting and request throttling

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: api, web
**Languages**: all

**❌ Bad**:
```
CORS(app, origins='*')  # Allows anyone!
```

**✅ Good**:
```
CORS(app, origins=['https://example.com'])
```
