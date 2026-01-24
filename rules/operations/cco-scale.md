# Scale Rules
*Performance and scaling rules based on user/request volume*

**Inheritance:** Higher tiers include all lower tier rules.

## Small (Scale:100+)
- **Caching**: TTL + invalidation strategy for data fetching
- **Lazy-Load**: Defer loading of non-critical resources
- **Query-Optimize**: Index frequently queried columns

## Medium (Scale:1K+)
- **Conn-Pool**: Connection pooling with appropriate sizing
- **Async-IO**: Non-blocking I/O operations
- **CDN-Static**: Serve static assets from CDN
- **Read-Replicas**: Database read replicas for read-heavy workloads

## Large (Scale:10K+ | Architecture:Microservices)
- **Idempotency**: Safe retries for write operations with idempotency keys
- **API-Version**: Version in URL or header for public APIs
- **Compression**: gzip/brotli for large responses
- **Bulkhead**: Isolate failures to prevent cascade
- **Queue-Async**: Use message queues for async processing

---

## Resilience Patterns

### Circuit Breaker Configuration

| Parameter | Value | Purpose |
|-----------|-------|---------|
| failureRateThreshold | 50% | Open breaker when failures exceed |
| slowCallRateThreshold | 80% | Open breaker when slow calls exceed |
| slowCallDurationThreshold | 3s | Define "slow" call |
| minimumNumberOfCalls | 20 | Minimum calls before calculating rate |
| permittedCallsInHalfOpen | 5 | Test calls when half-open |
| waitDurationInOpenState | 30s | Wait before testing recovery |
| slidingWindowSize | 100 | Calls in measurement window |

**States**: CLOSED → OPEN (failures exceed threshold) → HALF_OPEN (after wait) → CLOSED (recovery success)

**Implementation**:
- Separate breaker per external service
- Log state transitions
- Expose breaker state in health endpoint

### Retry with Exponential Backoff

**Formula**: `delay = min(cap, initialDelay × factor^attempt) + jitter`

**Jitter** (REQUIRED - prevents thundering herd):
- Full Jitter: `random(0, calculatedDelay)`
- Decorrelated: `min(cap, random(base, lastDelay × 3))`

| Operation | Initial | Max | Retries | Idempotent |
|-----------|---------|-----|---------|------------|
| GET/Read | 100ms | 30s | 5 | Yes |
| POST/Write | 500ms | 60s | 3 | Only with idempotency key |
| Connection | 100ms | 10s | 3 | Yes |
| Database | 250ms | 32s | 3 | Query-dependent |

**Non-retriable**: 4xx errors (except 429), auth failures, validation errors

### Rate Limiting

**Token Bucket Configuration**:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| tokenLimit | 100-1000 | Maximum burst capacity |
| tokensPerPeriod | 10-100 | Refill rate |
| replenishmentPeriod | 1-10s | Refill interval |
| queueLimit | 0-10 | Waiting requests |

**Thresholds by Endpoint**:

| Endpoint Type | Per Minute | Per Hour | Burst |
|---------------|------------|----------|-------|
| Public read | 100 | 1000 | +20% |
| Authenticated | 1000 | 10000 | +50% |
| Login/auth | 5/IP | 20/IP | None |
| Password reset | 3/email | 6/email | None |

**Response**: Return 429 with headers:
```
RateLimit-Limit: 1000
RateLimit-Remaining: 999
RateLimit-Reset: 1705335000
Retry-After: 60
```

### Timeout Configuration

| Timeout Type | Value | Purpose |
|--------------|-------|---------|
| Connection | 5-10s | TCP establishment |
| Read | 30-60s | Response receipt |
| Total | Connection + Read | End-to-end limit |
| Idle | 60-300s | Keep-alive timeout |

**By Operation**:

| Operation | Connect | Read | Rationale |
|-----------|---------|------|-----------|
| API GET | 5s | 10s | Fast response expected |
| API POST compute | 5s | 120s | Long processing allowed |
| Database query | 2s | 30s | Local network |
| Third-party API | 10s | 30s | Network variance |

### Cache-Aside Pattern

**TTL by Data Type**:

| Data Type | TTL | Rationale |
|-----------|-----|-----------|
| User profile | 5 min | Frequent changes |
| Product catalog | 1 hour | Moderate changes |
| Configuration | 1 day | Rare changes |
| Static content | 7 days | Immutable |
| Session data | 30 min | Security boundary |

**Invalidation Strategies**:
- TTL-only: Simple, acceptable staleness
- Event-driven: Real-time, complex setup
- Write-through: Always fresh, slower writes
- Delayed delete: Prevents race conditions

**Key Pattern**: `{entity}:{id}:{version}` e.g., `user:123:v2`

### Health Check Specification

**Endpoint**: `/health` or `/healthz`

**Timing**:

| Check Type | Interval | Timeout | Healthy After | Unhealthy After |
|------------|----------|---------|---------------|-----------------|
| HTTP probe | 10s | 5s | 2 consecutive | 3 consecutive |
| TCP probe | 10s | 3s | 2 consecutive | 3 consecutive |

**Response Format**:
```json
{
  "status": "healthy|degraded|unhealthy",
  "checks": {
    "database": "pass|fail",
    "cache": "pass|fail",
    "disk": "pass|warn|fail"
  },
  "timestamp": "ISO8601"
}
```

**Rules**:
- Return 200 for healthy/degraded, 503 for unhealthy
- Include dependency health in checks
- Set appropriate probe timeouts in orchestrator

---

## SLA-Based Observability
*Observability requirements based on SLA commitments*

**Trigger:** SLA level selected in user input

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

### Basics (SLA:Any)
- **Error-Tracking**: Sentry or similar error tracking
- **Critical-Alerts**: Immediate notification for critical errors
- **Health-Endpoint**: `/health` returning 200 when healthy

### Standard (SLA:99%+)
- **Correlation-ID**: Request tracing across services
- **RED-Metrics**: Rate, Error, Duration dashboards
- **Distributed-Trace**: OpenTelemetry/Jaeger for multi-service
- **Error-Budget-Track**: Track error budget consumption weekly

### HA (SLA:99.9%+)
- **Redundancy**: No single point of failure
- **Auto-Failover**: Automatic recovery mechanisms
- **Runbooks**: Documented incident response
- **Error-Budget-Alert**: Alert at 50%, 75%, 90% consumption
- **Incident-Postmortem**: Blameless postmortem within 48 hours

### Critical (SLA:99.99%+)
- **Multi-Region**: Geographic redundancy
- **Chaos-Engineering**: Fault injection testing (GameDay)
- **DR-Tested**: Disaster recovery procedures tested quarterly
- **On-Call-Rotation**: 24/7 on-call with escalation path
- **SLO-Review**: Weekly SLO review meetings
