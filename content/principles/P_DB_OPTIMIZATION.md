---
id: P_DB_OPTIMIZATION
title: Database Query Optimization
category: performance
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_DB_OPTIMIZATION: Database Query Optimization 🔴

**Severity**: High

Proper indexing, N+1 prevention, query analysis.

**Why**: Prevents slow queries through proper database indexing and query optimization

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: all
**Languages**: all

**❌ Bad**:
```
SELECT * FROM large_table  # No index, full scan
```

**✅ Good**:
```
CREATE INDEX idx_user_id ON jobs(user_id)  # Indexed query
```
