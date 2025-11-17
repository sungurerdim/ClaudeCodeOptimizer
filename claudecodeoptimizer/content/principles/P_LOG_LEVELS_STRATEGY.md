# P_LOG_LEVELS_STRATEGY: Log Levels Strategy

**Severity**: High

Log spam overwhelms operators Critical errors buried in INFO noise Cost explosion (DEBUG logging costs 10x more) Alert fatigue (false positives cause ignoring real alerts) **Evidence:** Typical produc.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```python
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # INFO+ in production; DEBUG only in dev

# 1. DEBUG - Fine-grained trace (development only)
logger.debug("Processing payment", amount=amount, account_id=account_id)
# Output only visible in development

# 2. INFO - Significant events (normal operation)
logger.info("User authenticated", user_id=user.id, ip_address=ip)
logger.info("Session created", session_id=session.id)
# Normal operational visibility

# 3. WARN - Unusual but recoverable
logger.warning("Expired orders found", expired_count=len(expired))
logger.warning("Low stock items", affected_count=len(low_stock))
```
**Why right**: ---

### ❌ Bad
```python
# ❌ BAD: Everything at INFO
logger.info("Payment received")                    # ✅ Correct
logger.info("SQL query executed")                  # ❌ Should be DEBUG
logger.info("Payment failed: timeout")             # ❌ Should be ERROR
logger.info("Database connection lost")            # ❌ Should be FATAL
# Result: Log spam; cannot find errors; alert on everything

# ❌ BAD: DEBUG in production
logger.setLevel(logging.DEBUG)  # 10x more logs!
for user in users:
    logger.debug(f"Processing user {user.id}")  # 1M logs/minute!
```
**Why wrong**: ---

---

## Checklist

- [ ] DEBUG disabled in production (only INFO+)
- [ ] INFO for significant events (user actions, state changes)
- [ ] WARN for unusual conditions (recoverable issues)
- [ ] ERROR for failures (operations failed; action required)
- [ ] FATAL for system failures (cannot continue)
- [ ] Error context complete (actionable details)
- [ ] No spam at high levels (INFO < 100 logs/second)
