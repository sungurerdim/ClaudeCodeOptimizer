# SLA-Based Observability
*Observability requirements based on SLA commitments*

**Trigger:** SLA level selected in user input
**Inheritance:** Higher SLA includes lower.

---

## SLI/SLO/SLA Reference

### Error Budget by SLA Level

| SLA | Error Budget | Downtime/Month | Downtime/Year |
|-----|--------------|----------------|---------------|
| 99% | 1% | 7.3 hours | 3.65 days |
| 99.9% | 0.1% | 43.8 minutes | 8.76 hours |
| 99.99% | 0.01% | 4.38 minutes | 52.56 minutes |
| 99.999% | 0.001% | 26.3 seconds | 5.26 minutes |

### Error Budget Burn Response

| Budget Consumed | Action |
|-----------------|--------|
| 50% | Team notification, review incidents |
| 75% | Incident response, pause feature work |
| 90% | Feature freeze, focus on stability |
| 100% | All-hands, halt all non-critical changes |

### Common SLIs

| SLI Type | Calculation | Good Threshold |
|----------|-------------|----------------|
| Availability | Successful requests / Total requests | > 99.9% |
| Latency (p50) | 50th percentile response time | < 200ms |
| Latency (p99) | 99th percentile response time | < 1000ms |
| Error Rate | Failed requests / Total requests | < 0.1% |
| Throughput | Requests processed per second | > baseline |

---

## Basics (SLA:Any)
- **Error-Tracking**: Sentry or similar error tracking
- **Critical-Alerts**: Immediate notification for critical errors
- **Health-Endpoint**: `/health` returning 200 when healthy

## Standard (SLA:99%+)
- **Correlation-ID**: Request tracing across services
- **RED-Metrics**: Rate, Error, Duration dashboards
- **Distributed-Trace**: OpenTelemetry/Jaeger for multi-service
- **Error-Budget-Track**: Track error budget consumption weekly

## HA (SLA:99.9%+)
- **Redundancy**: No single point of failure
- **Auto-Failover**: Automatic recovery mechanisms
- **Runbooks**: Documented incident response
- **Error-Budget-Alert**: Alert at 50%, 75%, 90% consumption
- **Incident-Postmortem**: Blameless postmortem within 48 hours

## Critical (SLA:99.99%+)
- **Multi-Region**: Geographic redundancy
- **Chaos-Engineering**: Fault injection testing (GameDay)
- **DR-Tested**: Disaster recovery procedures tested quarterly
- **On-Call-Rotation**: 24/7 on-call with escalation path
- **SLO-Review**: Weekly SLO review meetings
