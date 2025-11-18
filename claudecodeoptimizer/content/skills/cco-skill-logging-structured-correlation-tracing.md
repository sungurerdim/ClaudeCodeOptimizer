---
name: cco-skill-logging-structured-correlation-tracing
description: |
  Structured logging, correlation IDs, tracing, PII masking, audit trails
  Triggers: logging, logs, correlation, tracing, audit, PII
  Files: *logger*.py, *logging*.js, *audit*.go, middleware.ts
---

# Skill: Structured Logging & Correlation Tracing

## Purpose

Enable production debugging via structured logs, correlation IDs, tracing, PII masking, audit trails.

**Solves**: Unstructured logs (80% debugging time wasted), lost context (60%+ incomplete traces), PII leaks (30% breaches), compliance failures (40%+ audits), slow MTTR (hours→minutes)

---

## Principles Included

**P_STRUCTURED_LOGGING**: JSON logs for machine-readable search/aggregation
**P_LOG_LEVELS_STRATEGY**: ERROR/WARN/INFO/DEBUG prevent noise, enable alerts
**P_PII_MASKING_IN_LOGS**: Prevent passwords/tokens/SSNs; GDPR compliance
**P_CORRELATION_IDS**: Trace requests across services
**P_CENTRALIZED_LOGGING**: Aggregate logs (ELK, Loki, CloudWatch)
**P_AUDIT_LOGGING**: Immutable security logs for forensics

---

## Activation

**Keywords**: logging, logs, correlation, tracing, audit, PII, structured logs
**Files**: `*logger*.py`, `*logging*.js`, `*audit*.go`, `middleware.ts`

---

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for this skill's domain
action_types: [audit, fix, generate]
keywords: [logging, structured logging, correlation ids, tracing, observability, metrics]
category: observability
pain_points: [5]
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*logging|observability|correlation` in frontmatter
2. Match `category: observability`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.

---

## Examples

### Structured Logging
```python
import structlog
logger = structlog.get_logger()

def process_payment(user_id, amount, cid):
    logger.info("payment_started", user_id=user_id, amount=amount, correlation_id=cid)
    try:
        result = gateway.charge(amount)
        logger.info("payment_success", transaction_id=result.id, correlation_id=cid)
    except PaymentError as e:
        logger.error("payment_failed", error=str(e), correlation_id=cid)
        raise
```

### Correlation Middleware
```javascript
const { v4: uuidv4 } = require('uuid');
function correlationMiddleware(req, res, next) {
  const cid = req.headers['x-correlation-id'] || uuidv4();
  req.correlationId = cid;
  res.setHeader('X-Correlation-ID', cid);
  req.log = logger.child({ correlationId: cid });
  next();
}
```

### PII Masking
```python
def mask_email(email):
    user, domain = email.split('@')
    return f"{user[0]}***@{domain}"
```

### Audit Logging
```python
def audit_log(action, user_id, resource, ip):
    audit_logger.info("security_event", action=action, user_id=user_id,
                      resource=resource, ip=ip, timestamp=datetime.utcnow().isoformat())
```
