---
id: P_API_VERSIONING_STRATEGY
title: API Versioning Strategy
category: architecture
severity: high
weight: 9
applicability:
  project_types: ['api', 'library']
  languages: ['all']
---

# P_API_VERSIONING_STRATEGY: API Versioning Strategy 🔴

**Severity**: High

Support N and N-1 versions, never break existing clients.

**Why**: Prevents breaking existing clients by supporting multiple API versions simultaneously

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: api, library
**Languages**: all

**❌ Bad**:
```
# No versioning, changes break clients
```

**✅ Good**:
```
/api/v1/resource  # Old version
/api/v2/resource  # New version
```
