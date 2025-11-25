---
name: cco-skill-containers
description: Comprehensive Kubernetes and container security including pod security standards, RBAC, network policies, Zero Trust (mTLS), KSPM, runtime monitoring with Falco/Tetragon, image scanning, CIS benchmarks, and admission control (2025 best practices)
keywords: [kubernetes, container security, RBAC, network policy, pod security, secrets management, Trivy, Falco, Tetragon, distroless, OPA Gatekeeper, Zero Trust, mTLS, KSPM, CIS benchmark, runC CVE, eBPF]
category: infrastructure
related_commands:
  action_types: [audit, fix, generate]
  categories: [infrastructure, security]
pain_points: [6, 10]
---

# Kubernetes Security & Container Hardening

> **Standards:** Format defined in [cco-standards.md](../cco-standards.md)  
> **Discovery:** See [cco-standards.md](../cco-standards.md#18-command-discovery-protocol)


Comprehensive K8s and container security via defense-in-depth, Zero Trust, KSPM, and runtime monitoring.
---

---

## Domain

Container orchestration, Kubernetes clusters, microservices security, cloud-native infrastructure.

---

## Purpose

**2025 Critical Updates:**
- **KSPM (Kubernetes Security Posture Management)** - Continuous compliance automation
- **Zero Trust Architecture** - mTLS, service mesh, identity-based access
- **Runtime CVEs** - runC CVE-2024-21626, containerd vulnerabilities
- **eBPF Security** - Tetragon, enhanced Falco with kernel-level visibility
- **Pod Security Admission** - PSP deprecated, new admission controllers
- **Supply Chain for K8s** - Image signing, artifact verification, admission gates

**Why These Matter:**
- 90% of K8s breaches involve misconfigurations (CIS 2025)
- Zero Trust prevents lateral movement after initial compromise
- eBPF provides kernel-level visibility without performance overhead
- KSPM catches 80%+ of security issues before deployment

---

## Core Techniques

### 1. Pod Security Standards & Admission

**Pod Security Admission (PSA - replaces deprecated PSP):**
```yaml
# Namespace-level enforcement
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

**Restricted Pod (compliant):**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
  namespace: production
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: myapp:v1.0.0@sha256:abc123...
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: [ALL]
        runAsNonRoot: true
        runAsUser: 1000
      resources:
        requests:
          memory: "128Mi"
          cpu: "250m"
        limits:
          memory: "256Mi"
          cpu: "500m"
  automountServiceAccountToken: false
  hostNetwork: false
  hostPID: false
  hostIPC: false
```

**Detection Pattern:**
```python
def detect_pod_security_issues(manifest: dict) -> List[dict]:
    """Find pod security violations"""
    issues = []

    spec = manifest.get('spec', {})

    # Check security context
    sec_ctx = spec.get('securityContext', {})

    if not sec_ctx.get('runAsNonRoot'):
        issues.append({
            'type': 'pod_security',
            'subtype': 'missing_run_as_non_root',
            'severity': 'HIGH',
            'message': 'Pod missing runAsNonRoot: true'
        })

    # Check containers
    for container in spec.get('containers', []):
        container_sec = container.get('securityContext', {})

        # Privileged containers
        if container_sec.get('privileged'):
            issues.append({
                'type': 'pod_security',
                'subtype': 'privileged_container',
                'severity': 'CRITICAL',
                'container': container['name'],
                'message': f"Container {container['name']} is privileged"
            })

        # Missing readOnlyRootFilesystem
        if not container_sec.get('readOnlyRootFilesystem'):
            issues.append({
                'type': 'pod_security',
                'subtype': 'writable_root_fs',
                'severity': 'MEDIUM',
                'container': container['name'],
                'message': f"Container {container['name']} has writable root filesystem"
            })

        # Capability check
        caps = container_sec.get('capabilities', {})
        if 'ALL' not in caps.get('drop', []):
            issues.append({
                'type': 'pod_security',
                'subtype': 'capabilities_not_dropped',
                'severity': 'HIGH',
                'container': container['name'],
                'message': f"Container {container['name']} doesn't drop ALL capabilities"
            })

    # Host namespaces
    if spec.get('hostNetwork'):
        issues.append({
            'type': 'pod_security',
            'subtype': 'host_network',
            'severity': 'CRITICAL',
            'message': 'Pod uses hostNetwork: true'
        })

    if spec.get('hostPID'):
        issues.append({
            'type': 'pod_security',
            'subtype': 'host_pid',
            'severity': 'CRITICAL',
            'message': 'Pod uses hostPID: true'
        })

    return issues
```

---

### 2. RBAC Least Privilege

**Minimal Service Account:**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
automountServiceAccountToken: false  # Don't auto-mount unless needed
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list"]
    resourceNames: ["app-config"]  # Specific resource only
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-binding
subjects:
  - kind: ServiceAccount
    name: app-sa
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
```

**Detection Pattern:**
```python
def detect_rbac_issues(manifest: dict) -> List[dict]:
    """Find RBAC security issues"""
    issues = []

    kind = manifest.get('kind')

    if kind == 'Role' or kind == 'ClusterRole':
        rules = manifest.get('rules', [])

        for rule in rules:
            # Wildcard resources
            if '*' in rule.get('resources', []):
                issues.append({
                    'type': 'rbac',
                    'subtype': 'wildcard_resources',
                    'severity': 'HIGH',
                    'message': 'Role grants access to all resources (*)'
                })

            # Wildcard verbs
            if '*' in rule.get('verbs', []):
                issues.append({
                    'type': 'rbac',
                    'subtype': 'wildcard_verbs',
                    'severity': 'HIGH',
                    'message': 'Role grants all verbs (*)'
                })

            # Dangerous verbs
            dangerous_verbs = ['create', 'delete', 'deletecollection', 'patch', 'update']
            granted_dangerous = [v for v in rule.get('verbs', []) if v in dangerous_verbs]

            if granted_dangerous and 'secrets' in rule.get('resources', []):
                issues.append({
                    'type': 'rbac',
                    'subtype': 'secrets_write_access',
                    'severity': 'CRITICAL',
                    'verbs': granted_dangerous,
                    'message': f'Role can modify secrets: {granted_dangerous}'
                })

    # Check ServiceAccount automount
    if kind == 'ServiceAccount':
        if manifest.get('automountServiceAccountToken', True):  # Defaults to true
            issues.append({
                'type': 'rbac',
                'subtype': 'automount_service_account',
                'severity': 'MEDIUM',
                'message': 'ServiceAccount auto-mounts token (should be false unless needed)'
            })

    return issues
```

---

### 3. Network Policies (Zero Trust)

**Default Deny + Explicit Allow:**
```yaml
# 1. Default deny all
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
---
# 2. Allow specific ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
---
# 3. Allow DNS egress (required)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns-egress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: UDP
          port: 53
```

**Detection Pattern:**
```python
def detect_network_policy_gaps(namespace_manifests: List[dict]) -> dict:
    """Check if namespace has default-deny network policies"""
    has_default_deny_ingress = False
    has_default_deny_egress = False

    network_policies = [
        m for m in namespace_manifests
        if m.get('kind') == 'NetworkPolicy'
    ]

    for policy in network_policies:
        spec = policy.get('spec', {})
        pod_selector = spec.get('podSelector', {})

        # Empty podSelector {} means all pods
        if not pod_selector or pod_selector == {}:
            policy_types = spec.get('policyTypes', [])

            # Default deny if no ingress/egress rules defined
            if 'Ingress' in policy_types and not spec.get('ingress'):
                has_default_deny_ingress = True
            if 'Egress' in policy_types and not spec.get('egress'):
                has_default_deny_egress = True

    issues = []
    if not has_default_deny_ingress:
        issues.append({
            'type': 'network_policy',
            'subtype': 'missing_default_deny_ingress',
            'severity': 'HIGH',
            'message': 'No default-deny ingress policy (all pods accept traffic)'
        })

    if not has_default_deny_egress:
        issues.append({
            'type': 'network_policy',
            'subtype': 'missing_default_deny_egress',
            'severity': 'MEDIUM',
            'message': 'No default-deny egress policy (pods can call anywhere)'
        })

    return {
        'has_default_deny': has_default_deny_ingress and has_default_deny_egress,
        'policy_count': len(network_policies),
        'issues': issues
    }
```

---

### 4. Zero Trust with Service Mesh (mTLS)

**Istio Strict mTLS:**
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT  # Enforce mTLS for all traffic
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
## Checklist

### Pod Security
- [ ] Pod Security Admission enforced (restricted level)
- [ ] runAsNonRoot: true
- [ ] readOnlyRootFilesystem: true
- [ ] Capabilities dropped: ALL
- [ ] Seccomp profile: RuntimeDefault
- [ ] No hostNetwork/hostPID/hostIPC
- [ ] automountServiceAccountToken: false

### RBAC
- [ ] Least-privilege service accounts
- [ ] No wildcard (*) in roles
- [ ] No secrets write access unless required
- [ ] ServiceAccount token auto-mount disabled

### Network Security
- [ ] Default-deny network policies (ingress + egress)
- [ ] Explicit allow policies for required traffic
- [ ] DNS egress allowed
- [ ] Service mesh mTLS (Istio/Linkerd)

### Secrets Management
- [ ] External Secrets Operator configured
- [ ] Secrets mounted as files, not env vars
- [ ] Encryption at rest enabled
- [ ] Secret rotation automated

### Container Images
- [ ] Distroless or scratch base images
- [ ] Multi-stage builds
- [ ] Images pinned by digest (@sha256)
- [ ] Non-root USER directive
- [ ] Trivy scan: 0 CRITICAL/HIGH CVEs
- [ ] Images signed (Cosign)

### Runtime Security
- [ ] Falco installed and configured
- [ ] Tetragon tracing policies active
- [ ] Alerts for unauthorized processes
- [ ] Alerts for privilege escalation
- [ ] Runtime behavior monitoring

### KSPM & Compliance
- [ ] CIS Kubernetes Benchmark > 90%
- [ ] OPA Gatekeeper admission control
- [ ] Regular security posture scans
- [ ] Compliance dashboards configured

---

---

## References
