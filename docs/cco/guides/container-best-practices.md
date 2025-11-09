# Container & Kubernetes Best Practices

**Load on-demand when:** Container operations, Docker/K8s tasks

---

## Overview

Best practices for containerized applications using Docker and Kubernetes.

---

## Dockerfile Optimization

### Multi-Stage Builds

**Purpose**: Smaller images, faster deployments

**❌ Bad** - Single stage (large image):
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install poetry
RUN poetry install  # Includes dev dependencies
CMD ["python", "app.py"]
# Result: 1.2GB image
```

**✅ Good** - Multi-stage (small image):
```dockerfile
# Build stage
FROM python:3.11 AS builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry export -o requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
CMD ["python", "app.py"]
# Result: 250MB image (5x smaller)
```

### Minimal Base Images

**Options**:
```dockerfile
# ✅ Best: Distroless (smallest, most secure)
FROM gcr.io/distroless/python3-debian11
# ~50MB, no shell, no package manager

# ✅ Good: Alpine (small, has shell)
FROM python:3.11-alpine
# ~150MB, apk package manager

# ⚠️ OK: Slim (larger, more compatible)
FROM python:3.11-slim
# ~250MB, apt package manager

# ❌ Avoid: Full image (too large)
FROM python:3.11
# ~1GB+, unnecessary tools
```

### Layer Caching Optimization

**Order matters for cache hits**:

**❌ Bad** - Cache invalidated often:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .  # ← Changes every commit, cache miss
RUN pip install -r requirements.txt  # ← Always re-runs
CMD ["python", "app.py"]
```

**✅ Good** - Optimized caching:
```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Copy only requirements first (rarely changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code last (changes often)
COPY app/ .
CMD ["python", "app.py"]
```

### Security Hardening

**Non-root user**:
```dockerfile
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app
COPY --chown=appuser:appuser . .

# Switch to non-root
USER appuser

CMD ["python", "app.py"]
```

**Read-only filesystem**:
```yaml
# docker-compose.yml
services:
  app:
    image: myapp:latest
    read_only: true
    tmpfs:
      - /tmp  # Allow writes only to /tmp
```

### Dependency Scanning

**Scan before deployment**:
```bash
# Scan for vulnerabilities
docker scan myapp:latest

# Or use Trivy
trivy image myapp:latest

# Or CCO command
/cco-optimize-docker --scan
```

**Fix vulnerabilities**:
```dockerfile
# Update base image regularly
FROM python:3.11.8-slim  # ← Specific version, not 'latest'

# Scan and fix during build
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

---

## Kubernetes Patterns

### Declarative Manifests

**❌ Bad** - Imperative commands:
```bash
# Don't do this
kubectl create deployment myapp --image=myapp:latest
kubectl expose deployment myapp --port=80
kubectl scale deployment myapp --replicas=3
```

**✅ Good** - Declarative manifests:
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v1.2.3  # ← Specific version
        ports:
        - containerPort: 80
```

### Resource Requests & Limits

**Why**: Prevents resource starvation, enables efficient scheduling

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        resources:
          requests:
            memory: "256Mi"  # Guaranteed
            cpu: "250m"      # Guaranteed
          limits:
            memory: "512Mi"  # Maximum
            cpu: "500m"      # Maximum
```

**Guidelines**:
- **Requests**: What app needs normally (~50% of limit)
- **Limits**: Maximum allowed (~2x requests)
- **Memory**: OOM if exceeded (pod killed)
- **CPU**: Throttled if exceeded (pod slowed)

### Health Checks

**Three types**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:latest

        # 1. Liveness: Is app alive? (restart if fails)
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          failureThreshold: 3

        # 2. Readiness: Is app ready for traffic? (remove from LB if fails)
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          failureThreshold: 3

        # 3. Startup: Has app started? (wait before liveness checks)
        startupProbe:
          httpGet:
            path: /health/startup
            port: 8080
          initialDelaySeconds: 0
          periodSeconds: 5
          failureThreshold: 30  # 30*5s = 150s max startup time
```

**Implement endpoints**:
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health/live')
def liveness():
    # Check: Can app respond? (basic check)
    return jsonify({"status": "alive"}), 200

@app.route('/health/ready')
def readiness():
    # Check: Can app handle requests? (DB connected, cache ready, etc.)
    if not db.is_connected():
        return jsonify({"status": "not ready"}), 503
    return jsonify({"status": "ready"}), 200

@app.route('/health/startup')
def startup():
    # Check: Has app finished initialization?
    if not app_initialized:
        return jsonify({"status": "starting"}), 503
    return jsonify({"status": "started"}), 200
```

### ConfigMaps & Secrets

**Never hardcode configuration**:

**❌ Bad**:
```python
# Hardcoded in code
DATABASE_URL = "postgres://user:pass@db:5432/mydb"
API_KEY = "sk-1234567890"
```

**✅ Good** - ConfigMaps for non-sensitive config:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  DATABASE_HOST: "postgres.default.svc.cluster.local"
  DATABASE_PORT: "5432"
  LOG_LEVEL: "info"
---
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: myapp
        envFrom:
        - configMapRef:
            name: myapp-config
```

**✅ Good** - Secrets for sensitive data:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
stringData:
  DATABASE_PASSWORD: "secretpass123"
  API_KEY: "sk-1234567890"
---
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: myapp
        envFrom:
        - secretRef:
            name: myapp-secrets
```

### Pod Security Policies

**Enforce security standards**:

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  # Prevent privileged containers
  privileged: false

  # Require non-root user
  runAsUser:
    rule: MustRunAsNonRoot

  # Read-only root filesystem
  readOnlyRootFilesystem: true

  # No host network/ports
  hostNetwork: false
  hostPorts: []

  # Drop all capabilities
  requiredDropCapabilities:
    - ALL

  # Allow only specific volume types
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'secret'
```

---

## GitOps Workflow

### Infrastructure as Code

**Benefits**:
- Version controlled
- Auditable changes
- Repeatable deployments
- Easy rollbacks

**Tools**:
```bash
# Terraform
terraform apply -var-file=prod.tfvars

# Pulumi
pulumi up --stack prod

# Helm
helm upgrade --install myapp ./chart -f values-prod.yaml
```

### Automated Reconciliation

**ArgoCD Example**:

```yaml
# application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo
    targetRevision: main
    path: k8s/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true     # Delete removed resources
      selfHeal: true  # Auto-sync on drift
```

**Benefits**:
- Git is source of truth
- Automatic drift detection
- Self-healing deployments
- Audit trail via Git history

### Drift Detection & Correction

**Manual check**:
```bash
# Check for drift
argocd app diff myapp

# Sync to desired state
argocd app sync myapp

# Or with kubectl
kubectl diff -f manifests/
kubectl apply -f manifests/
```

**Automated**:
```yaml
# Enable auto-sync in ArgoCD
syncPolicy:
  automated:
    selfHeal: true  # ← Auto-fix drift
```

---

## Best Practices Checklist

### Docker

- [ ] Multi-stage builds for smaller images
- [ ] Minimal base images (distroless/alpine/slim)
- [ ] Optimized layer caching (dependencies before code)
- [ ] Non-root user
- [ ] Read-only root filesystem where possible
- [ ] Specific version tags (not `latest`)
- [ ] Vulnerability scanning before deployment
- [ ] `.dockerignore` to exclude unnecessary files

### Kubernetes

- [ ] Declarative manifests (YAML) instead of imperative commands
- [ ] Resource requests and limits defined
- [ ] All three health checks (liveness, readiness, startup)
- [ ] ConfigMaps for config, Secrets for sensitive data
- [ ] Pod security policies enforced
- [ ] Horizontal Pod Autoscaler (HPA) configured
- [ ] Network policies for traffic isolation
- [ ] RBAC (Role-Based Access Control) configured

### GitOps

- [ ] All infrastructure in version control
- [ ] Automated reconciliation (ArgoCD/Flux)
- [ ] Drift detection enabled
- [ ] Separate environments (dev/staging/prod)
- [ ] CI/CD pipeline for deployments
- [ ] Rollback strategy defined

---

## CCO Commands

```bash
# Optimize Dockerfile
/cco-optimize-docker

# Scan for vulnerabilities
/cco-optimize-docker --scan

# Generate Kubernetes manifests
/cco-generate k8s

# Audit container best practices
/cco-audit ops --focus=containers
```

---

## Principle References

- **P059-P063**: Operational Excellence Principles
  - P059: Minimal Host Responsibility (containers)
  - P060: Infrastructure as Code
  - P061: Observability & Monitoring
  - P062: Automated Health Checks
  - P063: Config-as-Code

See: [@docs/cco/principles/operations.md](../principles/operations.md)

---

*Part of CCO Documentation System*
*Load when needed: @docs/cco/guides/container-best-practices.md*
