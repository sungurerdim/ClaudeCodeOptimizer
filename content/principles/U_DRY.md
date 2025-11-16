---
id: U_DRY
title: DRY Enforcement & Single Source of Truth
category: universal
severity: high
weight: 10
applicability:
  project_types: ['all']
  languages: ['all']
---

# U_DRY: DRY Enforcement & Single Source of Truth 🔴

**Severity**: High

Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

**Applies to:**
- **Code/Logic**: No duplicate functions, extract reusable patterns
- **Data/State**: One authoritative source (DB = truth, cache = derived)
- **Configuration**: Constants, feature flags, env vars in one place

**Why**: Eliminates duplication to reduce bugs, prevent data inconsistency, and simplify maintenance

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: all
**Languages**: all

**Rules**:
- **No Duplicate Functions**: No duplicate function definitions
- **No Magic Numbers**: No magic numbers except 0, 1, -1
- **DB is Truth**: Database is authoritative, cache/aggregates are derived
- **Config Once**: Configuration defined once, referenced everywhere

**❌ Bad - Code Duplication**:
```python
MAX_RETRIES = 3  # file1
MAX_RETRIES = 3  # file2 - duplicate!
```

**✅ Good - Code**:
```python
# shared/constants.py
MAX_RETRIES = 3

# Other files
from shared.constants import MAX_RETRIES
```

**❌ Bad - Data Duplication**:
```python
# User email stored in both places - which is truth?
user.email = "old@example.com"  # DB
cache.set("user_email", "new@example.com")  # Cache
```

**✅ Good - Data**:
```python
# DB is source of truth
user.email = db.get_user(id).email  # Truth
cache.set("user_email", user.email)  # Derived from truth
```

**❌ Bad - Config Duplication**:
```python
if os.getenv("USE_NEW_API") == "true":  # File 1
    use_new_api()

if os.getenv("USE_NEW_API") == "true":  # File 2 - duplicate logic!
    use_new_api()
```

**✅ Good - Config**:
```python
# config.py - single source
USE_NEW_API = os.getenv("USE_NEW_API") == "true"

# Other files
from config import USE_NEW_API
if USE_NEW_API:
    use_new_api()
```

## Autofix Available
