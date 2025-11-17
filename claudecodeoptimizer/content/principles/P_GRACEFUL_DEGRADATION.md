# P_GRACEFUL_DEGRADATION: Graceful Degradation

**Severity**: High



---

## Rules

- Use circuit breaker pattern
- Degrade to cached/default data when dependencies fail
- Queue non-critical operations for later
- Return partial results over complete failure

---

## Examples

### ✅ Good
\**Why right**: Serves stale data over complete failure

### ❌ Bad
\**Why wrong**: Complete outage instead of degraded service

---

## Checklist

- [ ] Identify core vs nice-to-have features
- [ ] Cache data for fallback
- [ ] Use circuit breaker pattern
- [ ] Return partial results
