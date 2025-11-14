---
id: P_COMPLIANCE_AS_CODE
title: Compliance as Code
category: project-specific
severity: medium
weight: 7
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_COMPLIANCE_AS_CODE: Compliance as Code 🟡

**Severity**: Medium

Automate compliance checks through policy as code

**Why**: Makes compliance auditable and enforceable through automated policy checks

**Enforcement**: Skills required - verification_protocol

**Project Types**: all
**Languages**: all

**Rules**:
- **Policy As Code**: Use OPA/Kyverno for policies

**❌ Bad**:
```
# Manual compliance checks
```

**✅ Good**:
```
# policies/require-labels.rego
# Automated compliance reports
```
