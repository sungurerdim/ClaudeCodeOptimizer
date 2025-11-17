---
name: deployment-strategies
description: Zero-downtime blue-green/canary deployments with rollback and feature flags
---

# Deployment Strategies

## Core Strategies

**Blue-Green**: Two environments (blue=current, green=new). Switch traffic atomically. Instant rollback via traffic switch.

**Canary**: Progressive 1%→5%→25%→50%→100%. Auto-rollback if error rate spikes. 5-10min per stage.

**Feature Flags**: Runtime on/off. Kill switch for instant disable. Gradual rollout + A/B testing.

**Rollback**: Traffic switch (blue-green), feature flag disable, version pinning. Target: <5min.

## Pre-Deployment

- [ ] Migrations backward-compatible
- [ ] Health checks pass
- [ ] Smoke tests verified
- [ ] Metrics ready
- [ ] Rollback tested

## Examples

**K8s Blue-Green:**
```yaml
# Switch selector.version: blue → green
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  selector:
    app: myapp
    version: blue  # Change to "green"
```

**Feature Flags:**
```python
def is_enabled(flag, user_id):
    if not flag["enabled"]: return False
    pct = flag["rollout_percentage"]
    if pct == 100: return True
    return (hash(user_id) % 100) < pct

if flags.is_enabled("new_feature", user.id):
    return new_version()
```

**Migration:**
```python
# Add column with default (backward-compatible)
ALTER TABLE users ADD COLUMN verified BOOLEAN DEFAULT FALSE
# Rollback: DROP COLUMN verified
```

## Anti-Patterns

- No health checks before traffic
- Breaking DB changes
- Big-bang deploys
- Untested rollback
- Permanent feature flags
