# Observability
*Metrics, logging, and alerting standards*

## Core Metrics [CRITICAL]

### RED Metrics (Services)

| Metric | Alert Threshold |
|--------|-----------------|
| Rate | < 80% baseline |
| Errors | > 0.1% |
| Duration p50 | > 200ms |
| Duration p95 | > 500ms |
| Duration p99 | > 1000ms |

### USE Metrics (Infrastructure)

| Metric | Alert Threshold |
|--------|-----------------|
| Utilization | > 80% sustained |
| Saturation | > 0 (queue depth) |
| Errors | > 0 |

---

## Structured Logging [CRITICAL]

```json
{
  "timestamp": "2025-01-15T10:30:00.123Z",
  "level": "INFO",
  "message": "User login successful",
  "service": "auth-service",
  "trace_id": "abc123def456",
  "span_id": "span789",
  "duration_ms": 45
}
```

**Required Fields**: timestamp (ISO 8601 UTC), level, message, trace_id
**NEVER Log**: passwords, tokens, PII, credit cards

---

## Alert Configuration

### Fatigue Prevention

| Target | Value |
|--------|-------|
| Actionable rate | 30-50% |
| Consolidation window | 5 min |
| Sustained threshold | 5 min before alert |

### Alert Structure

```yaml
primary_condition: "> threshold for 5 minutes"
recovery_condition: "< threshold for 2 minutes"
notification_chain:
  - 0min: email
  - 15min: slack
  - 30min: page
```

---

## SLA-Based Requirements

### Error Budget

| SLA | Downtime/Month | Downtime/Year |
|-----|----------------|---------------|
| 99% | 7.3 hours | 3.65 days |
| 99.9% | 43.8 minutes | 8.76 hours |
| 99.99% | 4.38 minutes | 52.56 minutes |

### Budget Burn Response

| Consumed | Action |
|----------|--------|
| 50% | Team notification |
| 75% | Pause feature work |
| 90% | Feature freeze |
| 100% | All-hands stability |
