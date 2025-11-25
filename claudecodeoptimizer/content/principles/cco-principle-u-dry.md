---
name: dry-enforcement
description: Every piece of knowledge must have a single, unambiguous, authoritative representation
type: universal
severity: high
keywords: [DRY principle, code duplication, single source of truth, refactoring]
category: [quality, maintainability]
---

# CCO_U_DRY: DRY Enforcement & Single Source of Truth

**Severity**: High

Every piece of knowledge must have a single, unambiguous, authoritative representation.

---

## Why

Eliminates duplication to reduce bugs, prevent data inconsistency, simplify maintenance.

---

## Scope

- **Code/Logic**: No duplicate functions, extract reusable patterns
- **Data/State**: DB = truth, cache = derived
- **Configuration**: Constants, flags, env vars in one place

---

## Rules

- **No Duplicate Functions**: No duplicate definitions
- **No Magic Numbers**: Except 0, 1, -1
- **DB is Truth**: Database authoritative, cache/aggregates derived
- **Config Once**: Define once, reference everywhere

---

## Examples

### ❌ Bad - Code Duplication
```python
MAX_RETRIES = 3  # file1
MAX_RETRIES = 3  # file2 - duplicate!
```

### ✅ Good - Code
```python
# shared/constants.py
MAX_RETRIES = 3

# Other files
from shared.constants import MAX_RETRIES
```

### ❌ Bad - Data Duplication
```python
user.email = "{OLD_EMAIL}"  # DB
cache.set("user_email", "{NEW_EMAIL}")  # Cache - which is truth?
```

### ✅ Good - Data
```python
user.email = db.<function_name>(id).email  # Truth from DB
cache.set("user_email", user.email)  # Derived
```

### ❌ Bad - Config Duplication
```python
if os.getenv("USE_NEW_API") == "true":  # File 1
    use_new_api()
if os.getenv("USE_NEW_API") == "true":  # File 2 - duplicate!
    use_new_api()
```

### ✅ Good - Config
```python
# config.py - single source
USE_NEW_API = os.getenv("USE_NEW_API") == "true"

# Other files
from config import USE_NEW_API
if USE_NEW_API:
    use_new_api()
```

---

## Checklist

Before committing code:
- [ ] No duplicate function definitions (search for similar function names)
- [ ] No magic numbers except 0, 1, -1 (extract to named constants)
- [ ] All constants defined once in a single location
- [ ] Database is single source of truth (cache/aggregates are derived)
- [ ] Configuration values read from one place (no repeated `os.getenv()` calls)
- [ ] No copy-paste code blocks (extract to reusable function)
- [ ] When found duplication: refactor to single source, then update all references
