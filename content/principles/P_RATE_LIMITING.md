---
id: P_RATE_LIMITING
title: Rate Limiting & Throttling
category: security_privacy
severity: high
weight: 8
applicability:
  project_types: ['api', 'web']
  languages: ['all']
---

# P_RATE_LIMITING: Rate Limiting & Throttling 🔴

**Severity**: High

Prevent abuse with rate limiting on all public endpoints.

**Why**: Prevents injection attacks by using parameterized queries instead of string concatenation

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: api, web
**Languages**: all

**❌ Bad**:
```
@app.post('/api')  # No rate limiting
```

**✅ Good**:
```
@limiter.limit('100/minute')
@app.post('/api')
```
