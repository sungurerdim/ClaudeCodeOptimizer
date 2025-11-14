---
id: P_MINIMAL_RESPONSIBILITY
title: Minimal Responsibility (Zero Maintenance)
category: project-specific
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_MINIMAL_RESPONSIBILITY: Minimal Responsibility (Zero Maintenance) 🔴

**Severity**: High

Manual admin tasks = 0. Every process auto-manages lifecycle.

**Why**: Reduces operational burden by automating all manual maintenance tasks

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: all
**Languages**: all

**❌ Bad**:
```
# Cron job: python cleanup.py  # Manual!
```

**✅ Good**:
```
redis.setex(key, ttl, value)  # Auto-expires
```
