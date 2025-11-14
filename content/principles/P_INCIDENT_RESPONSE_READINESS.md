---
id: P_INCIDENT_RESPONSE_READINESS
title: Incident Response Readiness
category: project-specific
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_INCIDENT_RESPONSE_READINESS: Incident Response Readiness 🔴

**Severity**: High

Prepare for security incidents with runbooks, logging, and recovery procedures

**Why**: Reduces incident impact through prepared response procedures and logging

**Enforcement**: Skills required - verification_protocol, root_cause_analysis

**Project Types**: all
**Languages**: all

**Rules**:
- **Incident Plan**: Document incident response plan
- **Security Logging**: Log security events for SIEM

**❌ Bad**:
```
# No incident plan, minimal logging
```

**✅ Good**:
```
# docs/incident-response.md exists
# Security logs to SIEM
# DR tested quarterly
```
