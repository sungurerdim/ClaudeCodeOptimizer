---
id: P_PRIVACY_FIRST
title: Privacy-First by Default
category: security_privacy
severity: critical
weight: 9
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_PRIVACY_FIRST: Privacy-First by Default 🔴

**Severity**: Critical

PII explicitly managed, cleaned from memory after use.

**Why**: Protects sensitive data by encrypting it at rest and in transit

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: all
**Languages**: all

**Rules**:
- **No Pii Without Cleanup**: PII variables must have cleanup

**❌ Bad**:
```
data = load_pii()
process(data)  # Lingers in memory!
```

**✅ Good**:
```
data = load_pii()
try:
    process(data)
finally:
    secure_zero(data)
```
