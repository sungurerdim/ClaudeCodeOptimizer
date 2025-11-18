---
name: dead-letter-queue
description: Capture and handle failed messages in dead letter queue for analysis and replay
type: project
severity: high
keywords: [messaging, error-handling, reliability, observability, queuing]
category: [quality, observability, architecture]
related_skills: []
---

# P_DEAD_LETTER_QUEUE: Dead Letter Queue Pattern

**Severity**: High

 Failed messages discarded; nobody notices Orders, payments, notifications disappear Problems discovered days later in metrics Can't replay failed messages; lost forever Why did message fail. No trace.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import json
import logging

@dataclass
class DeadLetterEntry:
    """Entry in Dead Letter Queue."""
    original_message: dict
    error_message: str
    error_type: str
    timestamp: datetime
    retry_count: int
    source_queue: str
    worker_id: str
```
**Why right**: **Usage:**

### ❌ Bad
```python
# ❌ BAD: Failures silently ignored
def process_message(message):
    try:
        # Process order
        save_order(message['order_id'])
    except Exception:
        pass  # SILENT FAILURE! Order lost!

# ❌ BAD: Failures logged but not moved to DLQ
def process_message(message):
    try:
```
**Why wrong**: ---

---

## Checklist

- [ ] DLQ configured - Main queue routes failures to DLQ
- [ ] Error context stored - Original message, error, traceback
- [ ] DLQ monitoring - Alert on any messages
- [ ] Retention policy - Messages kept for investigation period
- [ ] Replay mechanism - Easy way to replay messages
- [ ] Analytics tracking - Error patterns, frequency
- [ ] Runbook created - How to handle DLQ incidents
