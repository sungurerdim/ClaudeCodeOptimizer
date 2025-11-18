---
name: bulkhead_pattern
description: Isolate failures using thread pools and resource partitioning
type: project
severity: high
keywords: [pattern, resilience, isolation, fault-tolerance, architecture]
category: [architecture]
related_skills: []
---
# P_BULKHEAD_PATTERN: Bulkhead Pattern

**Severity**: High

 One slow dependency consumes all threads/connections Slow service blocks fast service, bringing down entire platform All clients retry same service, overload it further Error in one feature affects a.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```python
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Any
import logging

class BulkheadExecutor:
    """Executor with isolated thread pools per feature."""

    def __init__(self):
        self.executors = {}
        self.logger = logging.getLogger(__name__)

    def register_feature(self, feature_name: str, thread_count: int):
        """Register feature with dedicated thread pool."""
        executor = ThreadPoolExecutor(
            max_workers=thread_count,
            thread_name_prefix=feature_name
```
**Why right**: ---

### ❌ Bad
```python
# ❌ BAD: Shared thread pool
executor = ThreadPoolExecutor(max_workers=10)

# All features share same 10 threads
def get_recommendations(user_id):
    return executor.submit(recommendation_service.get, user_id)

def process_payment(data):
    return executor.submit(payment_service.process, data)

# If recommendations hangs, takes up to 10 threads
```
**Why wrong**: ---

---

## Checklist

- [ ] Identify features/services - What should be isolated?
- [ ] Choose bulkhead type - Thread pools, connection pools, semaphores?
- [ ] Size appropriately - Calculate expected concurrent load
- [ ] Implement isolation - Use separate resource pools
- [ ] Add monitoring - Track load, rejections, capacity
- [ ] Set up alerts - Alert on high load or rejections
- [ ] Document decisions - Why each bulkhead sized that way
