---
name: resilience-circuitbreaker-retry-bulkhead
description: Prevent cascading failures in distributed systems via circuit breakers, retry patterns, and failure isolation. Includes exponential backoff with jitter, bulkhead isolation, graceful degradation chains, timeout configuration, and dead letter queues.
keywords: [resilience, circuit breaker, retry, bulkhead, timeout, cascading failure, fault tolerance, fallback, isolation, graceful degradation, dead letter queue]
category: architecture
related_commands:
  action_types: [audit, generate, fix]
  categories: [architecture, infrastructure]
pain_points: [5, 6, 10]
---

# Skill: Resilience - Circuit Breaker, Retry, Bulkhead

## Domain & Purpose

Prevent cascading failures in distributed systems via circuit breakers, retry patterns, and failure isolation.

**Problems**: Cascading failures (95% distributed outages), resource exhaustion (thundering herd), hanging requests, unpredictable recovery

**Includes**: @content/principles/P_CIRCUIT_BREAKER.md, @content/principles/P_RETRY_WITH_BACKOFF.md, @content/principles/P_BULKHEAD_PATTERN.md, @content/principles/P_GRACEFUL_DEGRADATION.md, @content/principles/P_TIMEOUT_CONFIGURATION.md, @content/principles/P_DEAD_LETTER_QUEUE.md, @content/principles/P_FAIL_FAST_STRATEGY.md, @content/principles/P_PRODUCTION_GRADE.md

---

## Core Techniques

**Circuit Breaker**: Stop after N failures
```python
@circuit(failure_threshold=5, recovery_timeout=60)
def call_external_api():
    return requests.get("https://api.example.com/data", timeout=5).json()
```

**Retry + Backoff**: Exponential + jitter
```python
@backoff.on_exception(backoff.expo, requests.RequestException, max_tries=5)
def fetch_data():
    return requests.get("https://api.example.com/data")
```

**Bulkhead**: Separate resource pools
```python
payment_pool = ThreadPoolExecutor(max_workers=20)      # Critical
notification_pool = ThreadPoolExecutor(max_workers=5)  # Non-critical
```

**Graceful Degradation**: Fallback chain
```python
def get_recs(user_id):
    try:
        return ml_service.get_recs(user_id)
    except ServiceUnavailableError:
        return redis.get(f"rec:{user_id}") or get_popular_items()
```

**Timeouts**: Always explicit
```python
response = requests.get("https://api.com/data", timeout=(3.0, 10.0))
```

**Dead Letter Queue**: Preserve failures
```python
try:
    handle_order(msg)
    msg.ack()
except Exception as e:
    dlq.publish(msg, error=str(e))
    msg.reject()
```

---

## Patterns

**Resilient Client**: Circuit + Retry + Timeout
```python
class ResilientAPIClient:
    @circuit(failure_threshold=5, recovery_timeout=60)
    @backoff.on_exception(backoff.expo, requests.RequestException, max_tries=3)
    def get(self, endpoint, timeout=(3, 10)):
        return requests.get(f"{self.base_url}{endpoint}", timeout=timeout).json()
```

**Multi-Level Fallback**: Service → Cache → DB → Default
```python
def get_price(id):
    try:
        return pricing_svc.get(id, timeout=2)
    except ServiceUnavailableError:
        return redis.get(f"p:{id}") or db.get_product(id).price or 0.0
```

---

## Checklist

- [ ] All external calls have timeouts
- [ ] Circuit breakers on critical deps
- [ ] Retry with exponential backoff + jitter
- [ ] Separate thread pools (critical vs non-critical)
- [ ] Fallback strategy per dependency
- [ ] Dead letter queue for failures
- [ ] Monitor: circuit state, retry rates, timeouts, fallback usage

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for this skill's domain
action_types: [audit, generate, fix]
keywords: [resilience, circuit breaker, retry, timeout, fallback, bulkhead]
category: architecture
pain_points: [5, 6, 10]
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*[pattern]` in frontmatter
2. Match `category: architecture`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.
