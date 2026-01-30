# Scale Rules
*Performance thresholds and resilience configurations*

**Trigger:** {scale_indicators}, {cache_deps}, {queue_deps}

## Scale Tiers

| Tier | Threshold | Key Patterns |
|------|-----------|--------------|
| Small | 100+ users | Caching, lazy load, query indexes |
| Medium | 1K+ users | Connection pool, async I/O, CDN, read replicas |
| Large | 10K+ users | Idempotency keys, API versioning, queues, bulkhead |

---

## Circuit Breaker Configuration

| Parameter | Value |
|-----------|-------|
| failureRateThreshold | 50% |
| slowCallRateThreshold | 80% |
| slowCallDurationThreshold | 3s |
| minimumNumberOfCalls | 20 |
| permittedCallsInHalfOpen | 5 |
| waitDurationInOpenState | 30s |
| slidingWindowSize | 100 |

**States**: CLOSED → OPEN → HALF_OPEN → CLOSED

---

## Retry Configuration

**Formula**: `delay = min(cap, initialDelay × factor^attempt) + jitter`

**Jitter REQUIRED** (prevents thundering herd):
- Full: `random(0, calculatedDelay)`
- Decorrelated: `min(cap, random(base, lastDelay × 3))`

| Operation | Initial | Max | Retries |
|-----------|---------|-----|---------|
| GET/Read | 100ms | 30s | 5 |
| POST/Write | 500ms | 60s | 3 |
| Connection | 100ms | 10s | 3 |
| Database | 250ms | 32s | 3 |

**Non-retriable**: 4xx (except 429), auth failures, validation errors

---

## Rate Limiting

### Token Bucket

| Parameter | Range |
|-----------|-------|
| tokenLimit | 100-1000 |
| tokensPerPeriod | 10-100 |
| replenishmentPeriod | 1-10s |

### Thresholds by Endpoint

| Endpoint | Per Minute | Per Hour |
|----------|------------|----------|
| Public read | 100 | 1000 |
| Authenticated | 1000 | 10000 |
| Login/auth | 5/IP | 20/IP |
| Password reset | 3/email | 6/email |

**Response**: 429 with `Retry-After` header

---

## Timeout Configuration

| Operation | Connect | Read |
|-----------|---------|------|
| API GET | 5s | 10s |
| API POST | 5s | 120s |
| Database | 2s | 30s |
| Third-party | 10s | 30s |

---

## Cache TTL

| Data Type | TTL |
|-----------|-----|
| User profile | 5 min |
| Product catalog | 1 hour |
| Configuration | 1 day |
| Static content | 7 days |
| Session | 30 min |

**Key Pattern**: `{entity}:{id}:{version}`

---

## Health Check

| Parameter | Value |
|-----------|-------|
| Interval | 10s |
| Timeout | 5s |
| Healthy after | 2 consecutive |
| Unhealthy after | 3 consecutive |

**Response**: 200 for healthy/degraded, 503 for unhealthy
