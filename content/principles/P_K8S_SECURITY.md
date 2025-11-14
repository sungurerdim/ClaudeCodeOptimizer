---
id: P_K8S_SECURITY
title: Kubernetes Security
category: project-specific
severity: high
weight: 9
applicability:
  project_types: ['microservice', 'cloud']
  languages: ['all']
---

# P_K8S_SECURITY: Kubernetes Security 🔴

**Severity**: High

Harden Kubernetes clusters with RBAC, network policies, and admission control

**Why**: Hardens Kubernetes against attacks through defense-in-depth controls

**Enforcement**: Skills required - verification_protocol, root_cause_analysis

**Project Types**: all
**Languages**: all

**Rules**:
- **Rbac Enabled**: Use RBAC with least privilege
- **Network Policies**: Define network policies
- **Pod Security**: Use Pod Security Standards (restricted)

**❌ Bad**:
```
# No RBAC, no network policies, root containers
```

**✅ Good**:
```
apiVersion: policy/v1
kind: PodSecurityPolicy
spec:
  runAsUser:
    rule: MustRunAsNonRoot
```
