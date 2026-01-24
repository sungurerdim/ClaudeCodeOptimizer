# Infrastructure
*Infrastructure as Code patterns*

## Docker (Infra:Docker)
**Trigger:** {container_files}

### Dockerfile Patterns
- **Multi-Stage**: Use multi-stage builds: `FROM node:20 AS builder` then `FROM node:20-slim`
- **Non-Root**: Add `USER nonroot` or `USER 1000` - never run as root
- **Layer-Order**: Copy package.json before source code for better layer caching
- **Cache-Mounts**: Use `--mount=type=cache,target=/root/.npm` for package managers
- **Secrets-Mount**: Use `--mount=type=secret,id=api_key` for build-time secrets
- **Healthcheck**: Add `HEALTHCHECK CMD curl -f http://localhost/health || exit 1`

### Base Image Priority

| Priority | Image Type | Example | Use Case |
|----------|------------|---------|----------|
| 1 | Distroless | `gcr.io/distroless/nodejs20` | Production (smallest attack surface) |
| 2 | Alpine | `node:20-alpine` | General use (small + shell) |
| 3 | Slim | `node:20-slim` | When Alpine incompatible |
| 4 | Full | `node:20` | Development only |

### Security
- **No-Latest**: Pin image versions: `node:20.10.0-slim` not `node:latest`
- **Drop-Capabilities**: In compose: `cap_drop: [ALL]` and `read_only: true`

### Image Scanning (Required in CI/CD)

```bash
# Trivy scan
trivy image --severity CRITICAL,HIGH --exit-code 1 myapp:1.0

# Docker Scout
docker scout cves --only-severity critical,high myapp:1.0
```

**Gate**: Block deployment on CRITICAL vulnerabilities

---

## Kubernetes (Infra:K8s)
**Trigger:** {k8s_dirs}, {k8s_configs}

### Pod Security Standards (v1.25+)

**Restricted** (Production workloads):
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  seccompProfile:
    type: RuntimeDefault
  capabilities:
    drop: [ALL]
```

**Baseline** (Standard workloads):
- No host network/ports
- No privileged containers
- Limited volume types (configMap, secret, emptyDir, PVC)

**Privileged** (Infrastructure only):
- System components only (CNI, storage drivers)
- NEVER for application workloads

### RBAC Requirements

**Service Account Rules**:
- NEVER use default service account
- Create single-purpose service accounts per application
- Disable auto-mounting: `automountServiceAccountToken: false`
- Use projected tokens with audiences when needed

**Role Binding Rules**:
- Prefer namespace-scoped `RoleBinding` over `ClusterRoleBinding`
- Grant minimum necessary permissions
- Audit bindings quarterly

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
automountServiceAccountToken: false
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: myapp-role
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
```

### Resource Limits
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "500m"
```

### Health Probes
- **Liveness**: `livenessProbe: httpGet: path: /healthz` - restart if failing
- **Readiness**: `readinessProbe: httpGet: path: /ready` - remove from service if failing
- **Startup**: `startupProbe` for slow-starting containers

### Network Policy (Default Deny)

**Apply to every namespace first**, then allow specific traffic:

```yaml
# Default deny all ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes:
  - Ingress
---
# Default deny all egress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
spec:
  podSelector: {}
  policyTypes:
  - Egress
---
# Allow specific ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-api
spec:
  podSelector:
    matchLabels:
      app: api
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - port: 8080
```

---

## Supply Chain Security (SLSA)

### SLSA Compliance Levels

| Level | Requirement | Implementation |
|-------|-------------|----------------|
| L1 | Provenance exists | Document build process |
| L2 | Signed provenance | Sign artifacts with cosign |
| L3 | Hardened builds | Isolated build environment |

### Required Artifacts

**SBOM Generation**:
```bash
# Generate SBOM
syft packages myapp:1.0 -o cyclonedx-json > sbom.json
```

**Artifact Signing**:
```bash
# Sign container image
cosign sign --key cosign.key myregistry/myapp:1.0
```

**Provenance Verification**:
```bash
# Verify artifact
slsa-verifier verify-artifact myapp.tar.gz \
  --provenance-path provenance.json \
  --source-uri github.com/org/repo
```

---

## Terraform (Infra:Terraform)
**Trigger:** {tf_files}

- **Variables-Type**: Add types: `variable "name" { type = string, description = "..." }`
- **Outputs**: Export needed values: `output "arn" { value = aws_instance.this.arn }`
- **Modules**: Extract reusable patterns into modules
- **Moved-Blocks**: Use `moved { from = ..., to = ... }` for refactoring
- **Import-Blocks**: Use `import { to = ..., id = ... }` for existing resources
- **State-Lock**: Enable state locking for team environments
- **Sensitive-Mark**: Mark sensitive outputs: `sensitive = true`

## Serverless (Infra:Serverless)
**Trigger:** {serverless_configs}

- **Timeout-Set**: Always set explicit timeout: `timeout: 30`
- **Memory-Size**: Right-size memory: `memorySize: 256`
- **Event-Validate**: Validate event payload at handler entry
- **Stateless**: No local state between invocations - use external storage
- **Cold-Start**: Minimize dependencies, use provisioned concurrency for latency-critical
- **VPC-Minimize**: Avoid VPC unless necessary (adds cold start latency)

---

## API Gateway (Infra:APIGateway)
**Trigger:** {api_gateway_config}, {api_gateway_deps}

- **Rate-Limit-Config**: Per-route rate limiting with burst allowance
- **Auth-Plugin**: Centralized authentication at gateway
- **Route-Versioning**: API version routing (header or path)
- **Circuit-Breaker-Route**: Per-upstream circuit breaker
- **Logging-Structured**: Structured request/response logging
- **CORS-Config**: Centralized CORS configuration
- **Timeout-Upstream**: Upstream timeout configuration

## Service Mesh (Infra:ServiceMesh)
**Trigger:** {service_mesh_config}, {service_mesh_deps}

- **mTLS-Enable**: Enable mutual TLS between services
- **Retry-Policy**: Service-level retry policies
- **Timeout-Budget**: Request timeout budgets
- **Traffic-Split**: Traffic splitting for canary deployments
- **Observability-Auto**: Auto-inject observability sidecars
- **Auth-Policy**: Service-to-service authorization policies

## Build Cache (Infra:BuildCache)
**Trigger:** {build_cache_config}

- **Cache-Key**: Deterministic cache key generation
- **Remote-Cache**: Enable remote cache for CI
- **Artifact-Share**: Share build artifacts across pipelines
- **Invalidation-Explicit**: Explicit cache invalidation rules
- **Size-Limit**: Cache size limits per project
- **TTL-Set**: Set cache TTL based on artifact type

---

## Ansible (Infra:Ansible)
**Trigger:** {ansible_config}, {ansible_patterns}

- **Inventory-Dynamic**: Use dynamic inventory for cloud resources
- **Role-Organization**: Organize playbooks into roles
- **Vault-Secrets**: Ansible Vault for sensitive data
- **Idempotency**: Ensure tasks are idempotent
- **Handler-Notify**: Use handlers for service restarts
- **Tags-Selective**: Tags for selective execution
- **Molecule-Testing**: Test roles with Molecule

## Consul (Infra:Consul)
**Trigger:** {consul_config}, {consul_patterns}

- **Service-Registration**: Auto-register services with health checks
- **KV-Store**: Use KV store for dynamic configuration
- **Service-Mesh**: Connect for service mesh
- **ACL-Policies**: ACL policies for security
- **Prepared-Queries**: Prepared queries for failover
- **Watch-Handlers**: Watches for configuration updates
- **Datacenter-Federation**: Multi-datacenter federation

## Vault (Infra:Vault)
**Trigger:** {vault_config}, {vault_patterns}

- **Secrets-Engines**: Use appropriate secrets engines
- **Authentication-Methods**: Configure auth methods per use case
- **Policies-Minimal**: Minimal policies (least privilege)
- **Dynamic-Secrets**: Dynamic secrets for databases
- **Token-TTL**: Short-lived tokens with renewal
- **Audit-Logging**: Enable audit logging
- **Seal-Unseal**: Secure seal/unseal procedures
- **Agent-Injection**: Vault Agent for Kubernetes injection
