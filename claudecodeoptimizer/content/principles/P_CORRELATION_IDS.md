# P_CORRELATION_IDS: Correlation IDs for Request Tracing

**Severity**: High

 User request spans 5 services; logs scattered; impossible to trace "Find all logs for this request" requires manual correlation Cannot see which service is slow without tracing Cannot tell which serv.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```python
import uuid
import logging
from contextvars import ContextVar
from functools import wraps
from typing import Optional

# Context variable stores correlation ID per request
correlation_id_var: ContextVar[Optional[str]] = ContextVar(
    'correlation_id', default=None
)

class CorrelationIDFilter(logging.Filter):
    """Adds correlation ID to all log records."""

    def filter(self, record):
        correlation_id = correlation_id_var.get()
```
**Why right**: ---

### ❌ Bad
```python
# ❌ BAD: No correlation ID; logs scattered
# User service logs
logger.info("Fetching user 123")
logger.info("User loaded")
logger.info("Calling profile service")

# Profile service logs (from different process, different log file!)
logger.info("Loading profile 123")
logger.info("Profile loaded")

# Settings service logs (yet another process!)
```
**Why wrong**: ---

---

## Checklist

- [ ] Generate if missing - Create new correlation ID if not provided
- [ ] Use if provided - Accept and use provided correlation ID
- [ ] Propagate downstream - Pass to all downstream service calls
- [ ] Store in context - Use context variables to make available
- [ ] Include in all logs - Automatically add to every log from request
- [ ] In response headers - Return correlation ID to client
- [ ] Consistent naming - Always use `X-Correlation-ID` header
