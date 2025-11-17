# U_COMPLETE_REPORTING: Complete Action Reporting

**Severity**: Critical

Every action must be explicitly reported with precise file references. No hidden operations, no vague locations.

---

## Why

Enables user verification and direct navigation to affected code via `file_path:line_number` format.

---

## Rules

- **Precise References**: Always `file_path:line_number` when referencing code
- **Report All Actions**: Every file read, edit, search explicitly stated
- **No Hidden Ops**: No silent fixes or background changes

---

## Examples

### ❌ Bad - Vague
```
"Fixed the authentication bug"
"Updated the API to handle errors"
"Improved the caching logic"
```

### ✅ Good - Precise
```
"Fixed authentication bug in src/auth.py:127"
"Updated API error handling in api/main.py:89-105"
"Improved caching in shared/storage.py:200-220"
```

---

## Reporting Pattern

**When reporting changes:**
```
✅ "Added JWT refresh token support to shared/auth.py:127-145"
✅ "Fixed SQL injection in services/api/main.py:89 (parameterized query)"
✅ "Refactored Redis connection in shared/storage.py:200-220"
```

**When answering questions:**
```
✅ "Authentication happens in shared/auth.py:50-80"
✅ "Rate limiting configured in shared/settings.py:120"
✅ "DB connection pool managed in shared/core.py:30"
```

---

## Integration

Works with:
- **U_EVIDENCE_BASED**: Requires verifiable proof
- **U_EXPLICIT_COMPLETION**: Together ensure verifiable, locatable results
