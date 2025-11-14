---
id: P_SEPARATION_OF_CONCERNS
title: Separation of Concerns
category: architecture
severity: high
weight: 7
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_SEPARATION_OF_CONCERNS: Separation of Concerns 🔴

**Severity**: High

Each layer/service has ONE responsibility - no mixing.

**Why**: Makes systems scalable by breaking monoliths into independent, deployable services

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: all
**Languages**: all

**Rules**:
- **No Business Logic In Api**: No business logic in API layer

**❌ Bad**:
```
@app.post('/api')
def create(data):
    result = complex_calc(data)  # Business logic in API!
```

**✅ Good**:
```
@app.post('/api')
def create(data):
    return business_layer.process(data)  # Delegated
```
