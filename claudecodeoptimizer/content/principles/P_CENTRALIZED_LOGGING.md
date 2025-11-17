# P_CENTRALIZED_LOGGING: Centralized Logging

**Severity**: High

 Each service logs to disk; cannot search across system Cannot correlate logs from multiple services to single issue Logs rotated locally; no long-term historical analysis No centralized monitoring; m.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```python
import logging
import json
from pythonjsonlogger import jsonlogger
import requests
from datetime import datetime

# Configure Python logging to output JSON
class JSONFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(JSONFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['service'] = 'user-service'
        log_record['environment'] = 'production'
        log_record['version'] = '1.0.0'


```
**Why right**: ---

### ❌ Bad
```bash
# ❌ BAD: Each service logs locally
# Service 1: /var/log/user-service/app.log
2024-01-15 10:30:45 User login: john@example.com
2024-01-15 10:30:46 Calling profile service
2024-01-15 10:30:47 Request completed

# Service 2: /var/log/profile-service/app.log
2024-01-15 10:30:47 Loading profile for user 123
2024-01-15 10:30:48 Profile loaded

# Service 3: /var/log/settings-service/app.log
```
**Why wrong**: ---

---

## Checklist

- [ ] Centralized system selected - ELK, Splunk, Datadog, CloudWatch, etc
- [ ] All services log there - Every service configured to send logs
- [ ] JSON format - Structured logs for parsing/aggregation
- [ ] Correlation IDs - All related logs linked
- [ ] Retention policy - Appropriate retention by severity
- [ ] Search/query working - Can find logs by various fields
- [ ] Dashboards created - Key metrics visible at a glance
