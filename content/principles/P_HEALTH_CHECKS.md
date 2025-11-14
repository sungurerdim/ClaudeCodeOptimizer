---
id: P_HEALTH_CHECKS
title: Health Checks & Readiness Probes
category: project-specific
severity: high
weight: 8
applicability:
  project_types: ['api', 'microservices']
  languages: ['all']
---

# P_HEALTH_CHECKS: Health Checks & Readiness Probes 🔴

**Severity**: High

Kubernetes-compatible health endpoints, dependency checks.

**Why**: Detects anomalies early through comprehensive metrics and alerting

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: api, microservices
**Languages**: all

**❌ Bad**:
```
# No health endpoint
```

**✅ Good**:
```
@app.get('/health')
def health():
    return {'status': 'healthy', 'dependencies': check_deps()}
```
