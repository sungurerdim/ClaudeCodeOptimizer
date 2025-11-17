# P_ERROR_BUDGETS: Error Budgets and SLOs

**Severity**: High

 Deploy risky changes without knowing impact on SLO Add features without understanding risk budget Some services 99%, others 99.9%, no consistency No tracking of error budget consumption Commit to 99.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```python
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

@dataclass
class SLO:
    """Service Level Objective."""
    name: str
    target: float  # e.g., 0.999 for 99.9%
    window: timedelta  # e.g., 1 month
    sli_metrics: list  # What to measure

class ErrorBudgetTracker:
    """Track error budget for SLO compliance."""

    def __init__(self, slo: SLO):
```
**Why right**: ---

### ❌ Bad
```python
# ❌ BAD: Deploy whenever, ignore SLO impact
def deploy_new_feature():
    deploy()  # Hope it doesn't break!

# ❌ BAD: Make SLO commitments but don't track
SLO = "99.99% uptime"  # But nobody tracks errors

# ❌ BAD: Ignore downtime until SLO violated
# Service has 1 minute downtime every week
# At 99.99% SLO, should have triggered alerts weeks ago
# But nobody noticed until SLO officially violated
```
**Why wrong**: ---

---

## Checklist

- [ ] Define SLOs - What are your uptime targets?
- [ ] Calculate error budget - Total downtime allowed
- [ ] Measure SLIs - Track actual performance
- [ ] Implement tracking - Monitor budget consumption
- [ ] Set alerts - Alert on high burn rate
- [ ] Gate deployments - Use budget for deployment decisions
- [ ] Review monthly - Analyze incidents and budget usage
