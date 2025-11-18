---
name: adr_architecture_decisions
description: Document architectural decisions and tradeoffs using decision records
type: project
severity: high
keywords: [architecture, documentation, decisions, tradeoffs]
category: [architecture]
related_skills: []
---
# P_ADR_ARCHITECTURE_DECISIONS: Architecture Decision Records

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
