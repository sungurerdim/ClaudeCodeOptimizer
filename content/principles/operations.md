# Operational Excellence Principles

**Generated**: 2025-11-09
**Principle Count**: 10

---

### P031: Minimal Responsibility (Zero Maintenance) 🟠

**Severity**: High

Manual admin tasks = 0. Every process auto-manages lifecycle.

**❌ Bad**:
```
# Cron job: python cleanup.py  # Manual!
```

**✅ Good**:
```
redis.setex(key, ttl, value)  # Auto-expires
```

---

### P032: Configuration as Code 🟠

**Severity**: High

All config versioned, validated, environment-aware, never hardcoded.

**Rules**:
- No hardcoded IPs/hosts

**❌ Bad**:
```
DB_HOST = 'localhost'  # Hardcoded!
```

**✅ Good**:
```
class Settings(BaseSettings):\n    DB_HOST: str = Field(..., env='DB_HOST')
```

---

### P033: Infrastructure as Code + GitOps 🟠

**Severity**: High

IaC (Terraform/Pulumi) + GitOps (ArgoCD/Flux) for declarative, version-controlled infrastructure with automated reconciliation.

**Rules**:
- Infrastructure code versioned in Git
- Use GitOps for deployments (ArgoCD, Flux)
- Declarative K8s manifests (no imperative kubectl)
- Detect and reconcile infrastructure drift

**❌ Bad**:
```
# Manual kubectl apply
```

**✅ Good**:
```
# IaC - Terraform
```

---

### P034: Observability with OpenTelemetry 🟠

**Severity**: High

Use OpenTelemetry (OTel) for unified metrics, traces, logs, and profiles. Vendor-neutral instrumentation.

**Project Types**: api, microservices

**Rules**:
- Use OpenTelemetry SDK for all instrumentation
- Structured JSON logs with trace context
- Distributed tracing with W3C Trace Context
- RED metrics (Rate, Errors, Duration) for services

**❌ Bad**:
```
# No instrumentation, plain text logs
```

**✅ Good**:
```
# OpenTelemetry instrumentation
```

---

### P035: Health Checks & Readiness Probes 🟠

**Severity**: High

Kubernetes-compatible health endpoints, dependency checks.

**Project Types**: api, microservices

**❌ Bad**:
```
# No health endpoint
```

**✅ Good**:
```
@app.get('/health')\ndef health():\n    return {'status': 'healthy', 'dependencies': check_deps()}
```

---

### P036: Graceful Shutdown 🟡

**Severity**: Medium

Handle SIGTERM, finish in-flight requests before exit.

**Project Types**: api, microservices

**❌ Bad**:
```
# No signal handling, abrupt termination
```

**✅ Good**:
```
signal.signal(signal.SIGTERM, graceful_shutdown)
```

---

### P059: GitOps Practices 🟡

**Severity**: Medium

Infrastructure and application deployment through Git-based workflows

**Rules**:
- Git is single source of truth

**❌ Bad**:
```
kubectl apply -f manifest.yaml  # Manual apply
```

**✅ Good**:
```
# Commit to Git, ArgoCD auto-syncs
```

---

### P060: Incident Response Readiness 🟠

**Severity**: High

Prepare for security incidents with runbooks, logging, and recovery procedures

**Rules**:
- Document incident response plan
- Log security events for SIEM

**❌ Bad**:
```
# No incident plan, minimal logging
```

**✅ Good**:
```
# docs/incident-response.md exists\n# Security logs to SIEM\n# DR tested quarterly
```

---

### P065: Compliance as Code 🟡

**Severity**: Medium

Automate compliance checks through policy as code

**Rules**:
- Use OPA/Kyverno for policies

**❌ Bad**:
```
# Manual compliance checks
```

**✅ Good**:
```
# policies/require-labels.rego\n# Automated compliance reports
```

---

### P069: Incremental Safety Patterns 🟠

**Severity**: High

Implement safety checkpoints (git stash, backups, tests) before and after changes with automatic rollback on failure

**Rules**:
- Git stash before risky changes
- Test after every change
- Automatic rollback on failure

**❌ Bad**:
```
# Make breaking changes directly\nrefactor_everything()\n# No backup, no tests, no rollback
```

**✅ Good**:
```
# Safety-first approach\ngit stash\ngit checkout -b refactor-backup\n\nrefactor_module()\npytest tests/\n\nif tests_fail:\n    git reset --hard
```

---

---

**Loading**: These principles load automatically when running relevant commands

**Reference**: Use `@PRINCIPLES.md` to load core principles, or reference this file directly