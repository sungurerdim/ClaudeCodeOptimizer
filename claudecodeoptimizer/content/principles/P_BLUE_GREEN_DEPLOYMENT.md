---
name: blue_green_deployment
description: Deploy with zero downtime using blue-green and canary strategies
type: project
severity: high
keywords: [deployment, zero-downtime, blue-green, strategy]
category: [infrastructure]
related_skills: []
---
# P_BLUE_GREEN_DEPLOYMENT: Blue-Green Deployment Strategy

**Severity**: High

 Traditional rolling deployments can cause inconsistent state during transition Traffic switches gradually; old and new versions coexist in unpredictable ways New version untested under real traffic b.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```yaml
# blue-deployment.yaml - Current production version
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
```
**Why right**: **Advantages:**
---

## Checklist

- [ ] *No rules extracted*

