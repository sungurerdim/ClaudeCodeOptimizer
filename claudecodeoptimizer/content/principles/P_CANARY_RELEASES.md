---
name: canary_releases
description: Deploy to subset of users to validate changes before full rollout
type: project
severity: high
keywords: [deployment, canary, testing, risk-reduction]
category: [infrastructure]
related_skills: []
---
# P_CANARY_RELEASES: Canary Release Pattern

**Severity**: High

 All users get new version simultaneously; widespread incidents if broken Problems affect 100% of users instead of 5% Can't test with real traffic patterns until full rollout Rolling back production a.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```yaml
# istio-canary-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-canary
  namespace: production
spec:
  replicas: 1  # 1 canary pod (small percentage of traffic)
  selector:
    matchLabels:
      app: myapp
      version: canary
  template:
    metadata:
      labels:
        app: myapp
```
**Why right**: **Advantages:**
---

## Checklist

- [ ] *No rules extracted*

