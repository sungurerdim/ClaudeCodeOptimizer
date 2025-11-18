---
name: kubernetes-security
description: Secure K8s clusters and containers via pod security standards, RBAC, network policies, secrets management, image scanning with Trivy, and runtime monitoring with Falco
keywords: [kubernetes, container security, RBAC, network policy, pod security, secrets management, Trivy, Falco, distroless, OPA Gatekeeper]
category: infrastructure
related_commands:
  action_types: [audit, fix, generate]
  categories: [infrastructure, security]
pain_points: [3, 5, 7]
---

# Skill: Kubernetes Security & Container Hardening
**Domain**: Container Orchestration
**Purpose**: Secure K8s clusters and containers via defense-in-depth: pod security standards, RBAC, network policies, secrets management, image scanning, and runtime monitoring.

## Core Techniques

- **Minimal Images**: Use distroless/scratch bases, multi-stage builds, non-root users
- **Image Scanning**: Trivy for vulnerabilities, Cosign for signing
- **Pod Security**: Restricted profiles, non-root, read-only root filesystem, drop ALL capabilities
- **RBAC**: Least-privilege service accounts, disable automountServiceAccountToken
- **Network Policies**: Default-deny, explicit allowlists for ingress/egress
- **Secrets Management**: External stores (AWS Secrets Manager), encryption at rest, mount as files
- **Runtime Security**: Falco for threat detection, alert on unauthorized processes

## Patterns

### ✅ Minimal Dockerfile
```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /build
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-w -s" -o app .

FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /build/app /app
USER 65534:65534
ENTRYPOINT ["/app"]
```
**Why**: Minimal attack surface, no shell, non-root

### ❌ Bloated Dockerfile
```dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3
COPY . /app
CMD ["python3", "app.py"]
```
**Why**: Large image, many vulnerabilities, runs as root

### ✅ Secure Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: myapp:v1.0.0
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: [ALL]
      resources:
        requests: {memory: "128Mi", cpu: "250m"}
        limits: {memory: "256Mi", cpu: "500m"}
  hostNetwork: false
  automountServiceAccountToken: false
```
**Why**: Non-root, read-only, no capabilities, resource-limited

### ❌ Insecure Pod
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: app
      securityContext:
        privileged: true
```
**Why**: Privileged containers enable breakouts

### ✅ RBAC Least-Privilege
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list"]
    resourceNames: ["app-config"]
```
**Why**: Scoped to specific resources only

### ✅ Network Policy Default-Deny
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```
**Why**: Deny-all baseline, explicit allowlist

### ✅ Secrets as Files
```yaml
volumeMounts:
  - name: secrets
    mountPath: /etc/secrets
    readOnly: true
volumes:
  - name: secrets
    secret:
      secretName: db-secret
      defaultMode: 0400
```
**Why**: Not visible in pod spec or env vars

### ❌ Secrets as Env Vars
```yaml
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: db-secret
        key: password
```
**Why**: Visible in pod spec, logs, crashes

## Checklist

- [ ] Images: Distroless/scratch, non-root (UID > 1000), Trivy scan zero HIGH/CRITICAL
- [ ] Pods: runAsNonRoot, readOnlyRootFilesystem, drop ALL capabilities, seccomp
- [ ] RBAC: Minimal service accounts, automountServiceAccountToken: false
- [ ] Network: Default-deny policies, explicit ingress/egress allowlists
- [ ] Secrets: External store (AWS/Vault), encryption at rest, mount as files
- [ ] Runtime: Falco installed, alerts for unauthorized processes/privilege escalation
- [ ] Admission: OPA Gatekeeper blocks privileged pods
- [ ] Scanning: Trivy in CI/CD, image signing with Cosign

---

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for Kubernetes security domain
action_types: [audit, fix, generate]
keywords: [kubernetes, container, RBAC, network policy, pod security, Trivy, Falco]
category: infrastructure
pain_points: [3, 5, 7]
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*[pattern]` in frontmatter
2. Match `category: infrastructure` or `category: security`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.
