# P_TIMEOUT_CONFIGURATION: Timeout Configuration

**Severity**: High

 No timeout, requests wait forever Hung connections block new requests Hung threads accumulate, leak memory Upstream servers overload waiting for downstream Timeout issues appear as performance degrad.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```python
from typing import Optional
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import socket
import logging

class TimeoutConfig:
    """Centralized timeout configuration."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # HTTP Client Timeouts (all in seconds)
        self.http_connect_timeout = 5.0      # Establish connection
        self.http_read_timeout = 10.0        # Read response body
```
**Why right**: ---

### ❌ Bad
```python
# ❌ BAD: No timeout specified
import requests

response = requests.get('https://api.example.com/data')  # No timeout!
# If server hangs, request waits forever
# Connection hangs, thread blocked, resources exhausted

# ❌ BAD: Infinite timeout
socket.settimeout(None)  # Block forever!

# ✅ GOOD: Always specify timeout
```
**Why wrong**: ---

---

## Checklist

- [ ] HTTP client timeouts - Set connect, read, write timeouts
- [ ] Database timeouts - Set connection and query timeouts
- [ ] Cache timeouts - Set reasonable cache get/set timeouts
- [ ] Request timeouts - Parent timeout > all child timeouts
- [ ] Timeout hierarchy - Validate parent > child throughout stack
- [ ] Document timeouts - Record why each timeout value chosen
- [ ] Monitor timeouts - Track timeout frequency, adjust if needed
