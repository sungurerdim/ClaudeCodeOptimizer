# Operational Excellence
**Minimal responsibility, config as code, IaC, observability**

**Total Principles:** 10

---

## P031: Minimal Responsibility (Zero Maintenance)

**Severity:** HIGH

Manual admin tasks = 0. Every process auto-manages lifecycle.

### Examples

**✅ Good:**
```
redis.setex(key, ttl, value)  # Auto-expires
```

**❌ Bad:**
```
# Cron job: python cleanup.py  # Manual!
```

**Why:** Reduces operational burden by automating all manual maintenance tasks

---

## P032: Configuration as Code

**Severity:** HIGH

All config versioned, validated, environment-aware, never hardcoded.

### Examples

**✅ Good:**
```
class Settings(BaseSettings):
    DB_HOST: str = Field(..., env='DB_HOST')
```

**❌ Bad:**
```
DB_HOST = 'localhost'  # Hardcoded!
```

**Why:** Makes configuration reproducible by versioning all config files in git

---

## P033: Infrastructure as Code + GitOps

**Severity:** HIGH

IaC (Terraform/Pulumi) + GitOps (ArgoCD/Flux) for declarative, version-controlled infrastructure with automated reconciliation.

### Examples

**✅ Good:**
```
# IaC - Terraform
```
```
resource "aws_eks_cluster" "main" {
```
```
  name     = var.cluster_name
```
```
  role_arn = aws_iam_role.cluster.arn
```
```
}
```
```

```
```
# GitOps - ArgoCD Application
```
```
apiVersion: argoproj.io/v1alpha1
```
```
kind: Application
```
```
metadata:
```
```
  name: myapp
```
```
spec:
```
```
  source:
```
```
    repoURL: https://github.com/org/repo
```
```
    targetRevision: HEAD
```
```
    path: k8s/
```
```
  destination:
```
```
    server: https://kubernetes.default.svc
```
```
    namespace: production
```
```
  syncPolicy:
```
```
    automated:
```
```
      prune: true
```
```
      selfHeal: true
```

**❌ Bad:**
```
# Manual kubectl apply
```
```
kubectl apply -f deployment.yaml
```
```

```
```
# No version control
```
```
# Infrastructure changes made via console/CLI
```

**Why:** Enables reproducible infrastructure with Git as single source of truth and automated drift correction

---

## P034: Observability with OpenTelemetry

**Severity:** HIGH

Use OpenTelemetry (OTel) for unified metrics, traces, logs, and profiles. Vendor-neutral instrumentation.

### Examples

**✅ Good:**
```
# OpenTelemetry instrumentation
```
```
from opentelemetry import trace, metrics
```
```
tracer = trace.get_tracer(__name__)
```
```
meter = metrics.get_meter(__name__)
```
```

```
```
with tracer.start_as_current_span('process_request') as span:
```
```
    span.set_attribute('user.id', user_id)
```
```
    request_counter.add(1, {'endpoint': '/api/users'})
```
```
    logger.info('Request processed', extra={'trace_id': span.get_span_context().trace_id})
```

**❌ Bad:**
```
# No instrumentation, plain text logs
```
```
print('User logged in')
```
```
# No trace context propagation
```

**Why:** Enables fast debugging through centralized, structured, searchable logs

---

## P035: Health Checks & Readiness Probes

**Severity:** HIGH

Kubernetes-compatible health endpoints, dependency checks.

### Examples

**✅ Good:**
```
@app.get('/health')
def health():
    return {'status': 'healthy', 'dependencies': check_deps()}
```

**❌ Bad:**
```
# No health endpoint
```

**Why:** Detects anomalies early through comprehensive metrics and alerting

---

## P036: Graceful Shutdown

**Severity:** MEDIUM

Handle SIGTERM, finish in-flight requests before exit.

### Examples

**✅ Good:**
```
signal.signal(signal.SIGTERM, graceful_shutdown)
```

**❌ Bad:**
```
# No signal handling, abrupt termination
```

**Why:** Enables quick problem diagnosis through distributed request tracing

---

## P059: GitOps Practices

**Severity:** MEDIUM

Infrastructure and application deployment through Git-based workflows

### Examples

**✅ Good:**
```
# Commit to Git, ArgoCD auto-syncs
```

**❌ Bad:**
```
kubectl apply -f manifest.yaml  # Manual apply
```

**Why:** Makes infrastructure changes auditable and reversible through Git history

---

## P060: Incident Response Readiness

**Severity:** HIGH

Prepare for security incidents with runbooks, logging, and recovery procedures

### Examples

**✅ Good:**
```
# docs/incident-response.md exists
# Security logs to SIEM
# DR tested quarterly
```

**❌ Bad:**
```
# No incident plan, minimal logging
```

**Why:** Reduces incident impact through prepared response procedures and logging

---

## P065: Compliance as Code

**Severity:** MEDIUM

Automate compliance checks through policy as code

### Examples

**✅ Good:**
```
# policies/require-labels.rego
# Automated compliance reports
```

**❌ Bad:**
```
# Manual compliance checks
```

**Why:** Makes compliance auditable and enforceable through automated policy checks

---

## P069: Incremental Safety Patterns

**Severity:** HIGH

Implement safety checkpoints (git stash, backups, tests) before and after changes with automatic rollback on failure

### Examples

**✅ Good:**
```
# Safety-first approach
git stash
git checkout -b refactor-backup

refactor_module()
pytest tests/

if tests_fail:
    git reset --hard
```

**❌ Bad:**
```
# Make breaking changes directly
refactor_everything()
# No backup, no tests, no rollback
```

**Why:** Prevents data loss and enables quick recovery through systematic safety checkpoints

---
