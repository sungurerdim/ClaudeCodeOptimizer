---
id: P_PRIVACY_COMPLIANCE
title: Privacy Compliance
category: security_privacy
severity: high
weight: 9
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_PRIVACY_COMPLIANCE: Privacy Compliance 🔴

**Severity**: High

Comply with GDPR, CCPA, and other privacy regulations

**Why**: Avoids regulatory fines through comprehensive privacy compliance

**Enforcement**: Skills required - verification_protocol, root_cause_analysis

**Project Types**: all
**Languages**: all

**Rules**:
- **Data Minimization**: Collect only necessary data
- **Right To Deletion**: Support automated data deletion

**❌ Bad**:
```
# Collect everything, no deletion support
```

**✅ Good**:
```
@app.delete('/user/{id}/data')
def delete_user_data(id):
    # GDPR Article 17
```
