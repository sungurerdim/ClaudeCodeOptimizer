---
name: cco-skill-observability
description: Production observability and incident management including OpenTelemetry metrics, SLO-driven alerting, health checks, incident response, on-call rotation, and blameless postmortems.
keywords: [observability, metrics, monitoring, alerts, SLO, SLI, Prometheus, health check, incident response, on-call, postmortem, MTTD, MTTR]
category: observability
pain_points: [4, 9, 10, 12]
---

# Skill: Observability and Incident Management

## Purpose
Implement comprehensive observability with SLO-driven alerting and structured incident response.

**Solves**: Blind production, alert fatigue, slow incident response, blame culture

## Guidance Areas
- Metrics - OpenTelemetry, Prometheus, Golden Signals
- Health Checks - Liveness, Readiness, Startup probes
- SLO/SLI/SLA - Error budgets, burn rate tracking
- Alerting - SLO-based alerts, runbook integration
- Incident Response - Severity classification, playbooks
- Postmortems - Blameless analysis, action tracking

## Part 1: Metrics

### Golden Signals
- Latency: p50, p95, p99
- Traffic: Requests/sec
- Errors: 4xx, 5xx rate
- Saturation: CPU, memory

## Part 2: Health Checks
- Liveness: Process running (K8s restarts if fails)
- Readiness: Accept traffic (K8s removes from LB)
- Startup: Initialization complete

## Part 3: SLO Framework
- SLI: Indicator (99 percent < 200ms)
- SLO: Objective (99.9 percent availability)
- Error Budget: 43 min/month at 99.9 percent

## Part 4: Incident Response

### Severity Levels
- P0: Site down (< 15 min response)
- P1: Major degradation (< 30 min)
- P2: Partial issue (< 4 hr)
- P3: Minor (< 24 hr)

## Part 5: Postmortems
Blameless analysis with action items and owners

## Checklist
- OpenTelemetry configured
- Golden signals instrumented
- Health probes implemented
- SLOs defined
- On-call rotation set
- Playbooks ready
- Postmortem template used


---

## Detailed Implementation

### OpenTelemetry Setup

from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader

reader = PrometheusMetricReader()
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

requests = meter.create_counter('http_requests_total')
latency = meter.create_histogram('http_request_duration_seconds')
connections = meter.create_up_down_counter('active_connections')

### Health Check Implementation

@app.get('/health/live')
def liveness():
    return {'status': 'alive'}

@app.get('/health/ready')
def readiness():
    checks = {'db': check_db(), 'redis': check_redis()}
    all_ok = all(checks.values())
    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={'status': 'ready' if all_ok else 'not_ready', 'checks': checks}
    )

### Kubernetes Probe Configuration

livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 3

startupProbe:
  httpGet:
    path: /health/startup
    port: 8080
  failureThreshold: 30

### SLO Definition Example

slos:
  - name: API Availability
    sli: success_rate
    target: 99.9%
    window: 30d
    error_budget: 43.2min

  - name: API Latency
    sli: p95_latency
    target: 200ms
    window: 30d

### Error Budget Tracking (PromQL)

burn_rate_1h:
  sum(rate(http_requests{status=~"5.."}[1h])) / sum(rate(http_requests[1h])) / (1 - 0.999)

remaining_budget_30d:
  1 - (sum(increase(http_requests{status=~"5.."}[30d])) / sum(increase(http_requests[30d]))) / 0.001

### Alert Rules Example

groups:
  - name: slo_alerts
    rules:
      - alert: SLOFastBurn
        expr: error_rate > 0.02
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: Fast error budget burn
          runbook: https://wiki/runbooks/slo-fast-burn

      - alert: HighLatencyP95
        expr: histogram_quantile(0.95, rate(http_duration_bucket[5m])) > 0.2
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: P95 latency exceeds 200ms

### Automated Severity Detection

def determine_severity(error_rate, response_p95, affected_pct, availability):
    # P0: Complete outage
    if availability < 50 or affected_pct > 80 or error_rate > 50:
        return 'P0'
    
    # P1: Major degradation
    if availability < 95 or affected_pct > 20 or error_rate > 10 or response_p95 > 5000:
        return 'P1'
    
    # P2: Partial degradation
    if error_rate > 5 or response_p95 > 2000 or affected_pct > 5:
        return 'P2'
    
    # P3: Minor issue
    return 'P3'

### On-Call Rotation

schedule:
  name: API On-Call
  rotation: weekly
  handoff: Monday 09:00
  
  tiers:
    - name: primary
      escalation_delay: 5m
      members: [alice, bob, charlie]
    
    - name: secondary
      escalation_delay: 10m
      members: [david, eve]
    
    - name: incident_commander
      escalation_delay: 15m
      members: [manager_1]

### Incident Playbook Template

# Playbook: {INCIDENT_TYPE}

## Symptoms
- Error rate spike on dashboard
- User reports in support channel
- Alert: {ALERT_NAME}

## Diagnosis Steps
1. Check error rate dashboard
2. Review recent deployments
3. Check dependency health
4. Review logs

## Mitigation

### Immediate (stop bleeding)
kubectl rollout undo deployment/api -n production

### Scale if traffic spike
kubectl scale deployment/api --replicas=10 -n production

## Communication
- Internal: Post in incidents channel
- External: Update status page
- Cadence: P0 every 30min, P1 every 1hr

## Escalation
- If not mitigated in 30min - escalate to secondary
- If database issue - page DBA on-call

### Blameless Postmortem Template

# Postmortem: {INCIDENT_TITLE}

Date: {DATE}
Severity: P{X}
Duration: {DURATION}
Author: {AUTHOR}

## Summary
1-2 sentence summary of what happened and impact

## Timeline
| Time | Event |
|------|-------|
| 14:05 | Alert triggered |
| 14:08 | On-call acknowledged |
| 14:15 | Root cause identified |
| 14:20 | Mitigation applied |
| 14:35 | Incident resolved |

## Root Cause
Detailed technical explanation

## Impact
- Users affected: {NUMBER}
- Revenue impact: {AMOUNT}
- Error budget consumed: {PERCENTAGE}

## What Went Well
- Alert triggered within 2 minutes
- Clear runbook available
- Team collaboration effective

## What Went Wrong
- Code review missed issue
- No monitoring for specific metric
- Recovery took longer than expected

## Action Items
| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P0 | Add monitoring alert | @alice | {DATE} |
| P0 | Fix root cause | @bob | {DATE} |
| P1 | Update code review | @charlie | {DATE} |

## Lessons Learned
1. Always monitor resource pools
2. Code reviews need specific checklist

### Status Page Integration

async def create_incident(name, impact, message):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'https://api.statuspage.io/v1/pages/{PAGE_ID}/incidents',
            headers={'Authorization': f'OAuth {API_KEY}'},
            json={'incident': {
                'name': name,
                'status': 'investigating',
                'impact_override': impact,
                'body': message
            }}
        )
        return response.json()

### Key Performance Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| MTTD (Mean Time to Detect) | < 5 min | > 10 min |
| MTTR (Mean Time to Resolve) | P0: < 30 min | +50% |
| False Positive Rate | < 10% | > 20% |
| Error Budget Remaining | > 25% | < 25% |
| Postmortem Completion | 100% P0/P1 | Any missing |

---

## Complete Checklist

### Metrics
- [ ] OpenTelemetry SDK configured
- [ ] Golden signals instrumented (latency, traffic, errors, saturation)
- [ ] Prometheus endpoint exposed (/metrics)
- [ ] Grafana dashboards created

### Health Checks
- [ ] Liveness probe implemented
- [ ] Readiness probe with dependency checks
- [ ] Startup probe for slow initialization
- [ ] Kubernetes probes configured

### SLOs
- [ ] SLIs defined and measured
- [ ] SLO targets documented
- [ ] Error budgets calculated
- [ ] Burn rate alerts configured

### Incident Response
- [ ] Severity levels defined with SLAs
- [ ] On-call rotation configured
- [ ] Playbooks for top 10 incident types
- [ ] Status page integrated
- [ ] Communication templates ready

### Postmortems
- [ ] Blameless culture established
- [ ] Template used for P0/P1
- [ ] Action items tracked with owners
- [ ] Monthly incident review scheduled

