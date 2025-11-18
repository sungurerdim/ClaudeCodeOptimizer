---
name: observability-metrics-slo
description: Implement OpenTelemetry-based observability with SLO-driven alerting to detect issues before user impact. Includes metrics (Counter, Gauge, Histogram), health checks (liveness, readiness, startup), SLO/SLI/SLA frameworks, error budgets, and Prometheus/Grafana dashboards.
keywords: [observability, metrics, monitoring, alerts, SLO, SLI, SLA, Prometheus, Grafana, health check, error budget, telemetry, OpenTelemetry, golden signals]
category: observability
related_commands:
  action_types: [audit, generate, optimize]
  categories: [observability]
pain_points: [9, 10]
---

# Observability - Metrics, Alerts, SLOs

## Domain
Production observability: metrics, traces, logs, health checks, SLOs/SLIs, error budgets, actionable alerts.

## Purpose
Implement OpenTelemetry-based observability with SLO-driven alerting to detect issues before user impact.

## Core Techniques

### OpenTelemetry Metrics
- **Counter**: Monotonic (requests, errors) - `create_counter()`
- **Gauge**: Point-in-time (CPU, memory) - `create_up_down_counter()`
- **Histogram**: Distributions (latency) - `create_histogram()`
- Export: Prometheus (metrics), Jaeger (traces), Loki (logs)

### Health Checks (3 Types)
- **Liveness** (`/health/live`): Service running? Restart if fails
- **Readiness** (`/health/ready`): Accept traffic? Check DB/cache
- **Startup** (`/health/startup`): Initialized? Check migrations

### SLO/SLI/SLA Framework
- **SLI**: Measurement (99% requests <200ms)
- **SLO**: Target (99.9% availability)
- **SLA**: Contract (99.5% uptime, penalties)
- **Error Budget**: Allowed failure (0.1% = 43min/month @ 99.9%)

### Error Budget Policy
```
Burn rate > 1.0 → Budget exhausted → Freeze features
Burn rate < 1.0 → Budget healthy → Ship faster
```

### Golden Signals
1. **Latency**: p50, p95, p99
2. **Traffic**: Requests/sec
3. **Errors**: 4xx, 5xx rate
4. **Saturation**: CPU, memory, disk, connections

## Patterns

### OpenTelemetry Setup
```python
from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader

reader = PrometheusMetricReader()
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

# Counter
requests = meter.create_counter("http_requests_total")

# Histogram
duration = meter.create_histogram("http_duration_seconds")

# Usage
def handle_request(req):
    start = time.time()
    try:
        resp = process(req)
        requests.add(1, {"status": resp.status})
        return resp
    finally:
        duration.record(time.time() - start)
```

### Health Endpoints
```python
@app.get("/health/live")
def liveness():
    return {"status": "alive"}

@app.get("/health/ready")
def readiness():
    checks = {"db": check_db(), "redis": check_redis()}
    all_ok = all(checks.values())
    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={"status": "ready" if all_ok else "not_ready", "checks": checks}
    )
```

### SLO Definition
```yaml
slos:
  - name: "API Availability"
    sli: "success_rate"
    target: 99.9%
    window: 30d
    error_budget: 0.1%  # 43min/month

  - name: "API Latency"
    sli: "p95_duration"
    target: 200ms
    window: 30d
```

### Error Budget Tracking
```promql
# Burn rate (1h)
(sum(rate(http_requests{status=~"5.."}[1h])) / sum(rate(http_requests[1h]))) / (1 - 0.999)

# Remaining budget (30d)
1 - (sum(increase(http_requests{status=~"5.."}[30d])) / sum(increase(http_requests[30d]))) / 0.001
```

### Alert Rules
```yaml
groups:
  - name: slo_alerts
    rules:
      - alert: HighErrorBudgetBurn
        expr: (sum(rate(http_requests{status=~"5.."}[1h])) / sum(rate(http_requests[1h]))) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error budget burning 10x faster"
          runbook: "https://wiki/runbooks/high-error-rate"

      - alert: HighLatencyP95
        expr: histogram_quantile(0.95, rate(http_duration_bucket[5m])) > 0.2
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "p95 latency > 200ms"
```

### Kubernetes Probes
```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5

startupProbe:
  httpGet:
    path: /health/startup
    port: 8080
  failureThreshold: 30  # 150s max
```

## Checklist

### Metrics Implementation
- [ ] OpenTelemetry SDK configured
- [ ] Counter for requests (by method, status)
- [ ] Histogram for latency (p50, p95, p99)
- [ ] Gauge for active connections/resources
- [ ] Prometheus exporter endpoint (/metrics)

### Health Checks
- [ ] Liveness probe (always returns 200)
- [ ] Readiness probe (checks dependencies)
- [ ] Startup probe (checks initialization)
- [ ] Kubernetes probes configured

### SLO/SLI
- [ ] SLIs defined (availability, latency)
- [ ] SLO targets set (99.9%, 200ms)
- [ ] Error budgets calculated
- [ ] Burn rate tracking implemented

### Alerting
- [ ] Alert on SLO violations (not individual errors)
- [ ] Runbook links in annotations
- [ ] Severity levels (critical, warning)
- [ ] Escalation policy defined
- [ ] Alert fatigue prevention (thresholds tuned)

### Dashboards
- [ ] Golden signals visualized
- [ ] Error budget remaining displayed
- [ ] Latency percentiles (p50, p95, p99)
- [ ] Error rate by endpoint

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for this skill's domain
action_types: [audit, generate, optimize]
keywords: [observability, metrics, SLO, health check, monitoring, alerts]
category: observability
pain_points: [9, 10]
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*[pattern]` in frontmatter
2. Match `category: observability`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.
