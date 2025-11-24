---
name: cco-skill-logging-structured-correlation-tracing
description: Structured logging, correlation IDs, tracing, PII masking, audit trails
keywords: [logging, logs, structured logging, correlation, correlation ids, tracing, audit, pii, observability, metrics]
category: observability
related_commands:
  action_types: [audit, fix, generate]
  categories: [observability]
pain_points: [5]
---

# Skill: Structured Logging & Correlation Tracing

> **Standards:** Format defined in [STANDARDS_SKILLS.md](../STANDARDS_SKILLS.md)  
> **Discovery:** See [STANDARDS_COMMANDS.md](../STANDARDS_COMMANDS.md#18-command-discovery-protocol)


## Purpose

Enable production debugging via structured logs, correlation IDs, tracing, PII masking, audit trails.

**Solves**: Unstructured logs (80% debugging time wasted), lost context (60%+ incomplete traces), PII leaks (30% breaches), compliance failures (40%+ audits), slow MTTR (hours→minutes)
---

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
