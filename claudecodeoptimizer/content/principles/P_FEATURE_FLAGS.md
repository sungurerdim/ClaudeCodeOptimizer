# P_FEATURE_FLAGS: Feature Flags Strategy

**Severity**: High

 Must choose between code and feature; can't separate decisions All-or-nothing feature rollout to all users simultaneously Reverting features requires redeployment, not instant config change Can't tes.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```python
# features.py - Feature flag definitions
from dataclasses import dataclass
from enum import Enum

class FeatureFlagBackend:
    """Interface for feature flag providers."""
    def is_enabled(self, flag_name: str, user_id: str = None) -> bool:
        raise NotImplementedError

class LocalFeatureFlags(FeatureFlagBackend):
    """Simple in-memory feature flags for development."""
    def __init__(self):
        self.flags = {
            'new_payment_flow': False,
            'oauth_authentication': False,
            'advanced_analytics': False,
```
**Why right**: ---
