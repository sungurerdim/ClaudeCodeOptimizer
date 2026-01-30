# Infrastructure
*Specific configurations and security requirements*

**Trigger:** {dockerfile}, {terraform_files}, {cloud_configs}

## Docker [CRITICAL]

### Base Image Priority

| Priority | Type | Example | Use Case |
|----------|------|---------|----------|
| 1 | Distroless | `gcr.io/distroless/nodejs20` | Production |
| 2 | Alpine | `node:20-alpine` | General |
| 3 | Slim | `node:20-slim` | Alpine incompatible |
| 4 | Full | `node:20` | Development only |

### Security Requirements

```dockerfile
# REQUIRED: Non-root user
USER 1000

# REQUIRED: Pin versions
FROM node:20.10.0-slim

# RECOMMENDED: Read-only filesystem
# In compose: read_only: true, cap_drop: [ALL]
```

### CI/CD Gate (Required)

```bash
# Block on CRITICAL vulnerabilities
trivy image --severity CRITICAL,HIGH --exit-code 1 myapp:1.0
```

---

## Kubernetes [CRITICAL]

### Pod Security (Production)

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: [ALL]
```

### RBAC Requirements

- NEVER use default service account
- `automountServiceAccountToken: false`
- Prefer `RoleBinding` over `ClusterRoleBinding`

### Resource Limits (Required)

```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "500m"
```

### Network Policy (Default Deny First)

```yaml
# Apply to EVERY namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```

---

## Supply Chain Security

### SLSA Levels

| Level | Requirement |
|-------|-------------|
| L1 | Provenance documented |
| L2 | Signed with cosign |
| L3 | Isolated build environment |

### Required Commands

```bash
# SBOM generation
syft packages myapp:1.0 -o cyclonedx-json > sbom.json

# Image signing
cosign sign --key cosign.key myregistry/myapp:1.0

# Verification
slsa-verifier verify-artifact myapp.tar.gz --provenance-path provenance.json
```

---

## Terraform

- **Variables**: Always add `type` and `description`
- **Refactoring**: Use `moved { from, to }` blocks
- **Import**: Use `import { to, id }` blocks
- **Sensitive**: Mark outputs `sensitive = true`
- **State**: Enable state locking for teams

---

## Serverless

| Setting | Requirement |
|---------|-------------|
| Timeout | Always explicit (e.g., 30s) |
| Memory | Right-size (start 256MB) |
| VPC | Use only when explicitly needed (cold start) |
| State | External only (no local state) |
